#!/usr/bin/env python3
"""Small, dependency-free checks for the Blogger theme."""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

B = "http://www.google.com/2005/gml/b"
NAMESPACES = {
    "b": B, "data": "http://www.google.com/2005/gml/data", "expr": "http://www.google.com/2005/gml/expr",
}
OPTIONAL_JSONLD_KEYS = ["telephone", "address", "openingHours"]
REQUIRED_SECTIONS = [
    "header", "hero", "marquee", "services", "beforeafter", "main", "numbers",
    "reviews", "team", "contact",
]
ALLOWED_HOSTS = {
    "fonts.googleapis.com", "fonts.gstatic.com", "blogger.googleusercontent.com",
    "muhdroid.com", "wa.me",
}


def local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def rule_well_formed(text: str, root) -> list[str]:
    try:
        ET.fromstring(text)
    except ET.ParseError as error:
        return [str(error)]
    return []


def rule_html_attrs(text: str, root) -> list[str]:
    expected = {"css": "false", "js": "false", "layoutsVersion": "3", "defaultwidgetversion": "2"}
    errors = [] if local_name(root.tag) == "html" else ["root element must be html"]
    errors.extend(f"html b:{key} must be {value!r}" for key, value in expected.items()
                  if root.get(f"{{{B}}}{key}") != value)
    start = re.search(r"<html\b[^>]*>", text)
    tag = start.group(0) if start else ""
    errors.extend(f"html must declare xmlns:{prefix}={uri!r}" for prefix, uri in NAMESPACES.items()
                  if not re.search(rf"""xmlns:{prefix}=(['"]){re.escape(uri)}\1""", tag))
    return errors


def rule_no_emoji(text: str, root) -> list[str]:
    errors = []
    for number, line in enumerate(text.splitlines(), 1):
        if any(0x1F000 <= ord(char) <= 0x1FAFF or 0x2600 <= ord(char) <= 0x27BF for char in line):
            errors.append(f"emoji on line {number}")
    return errors


def allowed_external(value: str) -> bool:
    parsed = urlparse(value if not value.startswith("//") else f"https:{value}")
    host = parsed.hostname or ""
    return (
        host in ALLOWED_HOSTS
        or host.endswith(".bp.blogspot.com")
        or (host == "www.google.com" and parsed.path == "/maps")
    )


def rule_external_refs(text: str, root) -> list[str]:
    errors = []
    for element in root.iter():
        if local_name(element.tag) == "script" and any(local_name(key) == "src" for key in element.attrib):
            errors.append("script src is not allowed")
        for key, value in element.attrib.items():
            if local_name(key) in {"src", "href"} and (value.startswith("http") or value.startswith("//")):
                if not allowed_external(value):
                    errors.append(f"external reference not allowed: {value}")
    return errors


def rule_symbol_ids_unique(text: str, root) -> list[str]:
    ids = [element.get("id") for element in root.iter() if local_name(element.tag) == "symbol" and element.get("id")]
    return [f"duplicate symbol id: {value}" for value in dict.fromkeys(ids) if ids.count(value) > 1]


def rule_js_budget(text: str, root) -> list[str]:
    scripts = {element.get("id"): element for element in root.iter() if local_name(element.tag) == "script"}
    if "atlas-js" not in scripts:
        return ["script #atlas-js is missing"]
    errors = []
    for name, limit in (("atlas-js", 9216), ("atlas-head", 400)):
        if name in scripts:
            size = len("".join(scripts[name].itertext()).encode())
            if size > limit:
                errors.append(f"script #{name} is {size} bytes (maximum {limit})")
    return errors


def rule_sections_present(text: str, root) -> list[str]:
    ids = [element.get("id") for element in root.iter() if element.tag == f"{{{B}}}section"]
    position = 0
    for required in REQUIRED_SECTIONS:
        try:
            position = ids.index(required, position) + 1
        except ValueError:
            return [f"sections must include ordered ids: {', '.join(REQUIRED_SECTIONS)}"]
    return []


def rule_bi_rule(text: str, root) -> list[str]:
    expected = "html[lang=fr] [lang=ar], html[lang=ar] [lang=fr]{display:none}"
    return [] if expected in text else ["missing bilingual visibility rule"]


def rule_contact_everywhere(text: str, root) -> list[str]:
    parents = {child: parent for parent in root.iter() for child in parent}
    section = next((element for element in root.iter()
                    if element.tag == f"{{{B}}}section" and element.get("id") == "contact"), None)
    element, errors = section, []
    while element is not None:
        if "data:view" in (element.get("cond") or ""):
            errors.append("section contact must not sit inside a data:view condition")
        element = parents.get(element)
    return errors


def rule_wa_buttons(text: str, root) -> list[str]:
    return [f"data-wa must be on <a href='#contact'>, found <{local_name(element.tag)} href={element.get('href')!r}>"
            for element in root.iter() if "data-wa" in element.attrib
            and (local_name(element.tag) != "a" or element.get("href") != "#contact")]


def unguarded_text(element) -> str:
    out = element.text or ""
    for child in element:
        if child.tag != f"{{{B}}}if":
            out += unguarded_text(child)
        out += child.tail or ""
    return out


def rule_jsonld_guarded(text: str, root) -> list[str]:
    scripts = [element for element in root.iter()
               if local_name(element.tag) == "script" and element.get("type") == "application/ld+json"]
    return [f"JSON-LD key {key!r} must sit inside a b:if" for script in scripts
            for key in OPTIONAL_JSONLD_KEYS if f'"{key}"' in unguarded_text(script)]


def rule_nav_absolute(text: str, root) -> list[str]:
    nav = next((element for element in root.iter()
                if local_name(element.tag) == "widget" and element.get("id") == "LinkList2"), None)
    if nav is None:
        return ["widget LinkList2 (navigation) is missing"]
    hrefs = [value for element in nav.iter() for key, value in element.attrib.items() if local_name(key) == "href"]
    return [] if any("data:blog.homepageUrl" in value for value in hrefs) else \
        ["LinkList2 hrefs must be built with data:blog.homepageUrl"]


def rule_hero_lcp(text: str, root) -> list[str]:
    found = [element for element in root.iter() if any(local_name(key) == "fetchpriority" for key in element.attrib)]
    if len(found) != 1:
        return [f"exactly one fetchpriority expected, found {len(found)}"]
    parents = {child: parent for parent in root.iter() for child in parent}
    element = found[0]
    while element is not None:
        if element.tag == f"{{{B}}}section" and element.get("id") == "hero":
            return []
        element = parents.get(element)
    return ["fetchpriority must sit inside section hero"]


def rule_ba_ltr(text: str, root) -> list[str]:
    rule = re.search(r"(?:^|[}\s])\.ba\{([^}]*)\}", text)
    return [] if rule and "direction:ltr" in rule.group(1) else [".ba rule must contain direction:ltr"]


RULES = [
    ("well_formed", rule_well_formed),
    ("html_attrs", rule_html_attrs),
    ("no_emoji", rule_no_emoji),
    ("external_refs", rule_external_refs),
    ("symbol_ids_unique", rule_symbol_ids_unique),
    ("js_budget", rule_js_budget),
    ("sections_present", rule_sections_present),
    ("bi_rule", rule_bi_rule),
    ("contact_everywhere", rule_contact_everywhere),
    ("wa_buttons", rule_wa_buttons),
    ("jsonld_guarded", rule_jsonld_guarded),
    ("nav_absolute", rule_nav_absolute),
    ("hero_lcp", rule_hero_lcp),
    ("ba_ltr", rule_ba_ltr),
]


def check_text(text: str) -> list[str]:
    errors = [("well_formed", error) for error in rule_well_formed(text, None)]
    if errors:
        return [f"{rule}: {message}" for rule, message in errors]
    root = ET.fromstring(text)
    for name, rule in RULES[1:]:
        errors.extend((name, error) for error in rule(text, root))
    return [f"{rule}: {message}" for rule, message in errors]


def extra_paths(paths: list[str]) -> list[Path]:
    files = []
    for value in paths:
        path = Path(value)
        if not path.exists():
            raise FileNotFoundError(value)
        files.extend(candidate for candidate in (path.rglob("*") if path.is_dir() else [path])
                     if candidate.is_file() and candidate.suffix in {".md", ".html"})
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("theme", nargs="?", default="theme.xml")
    parser.add_argument("--also", nargs="+", default=[])
    args = parser.parse_args(argv)
    theme = Path(args.theme)
    if not theme.is_file():
        print(f"{args.theme} not found")
        return 1
    errors = check_text(theme.read_text(encoding="utf-8"))
    try:
        also = extra_paths(args.also)
    except FileNotFoundError as missing:
        print(f"{missing} not found")
        return 1
    for path in also:
        errors.extend(f"no_emoji: {path}: {message}" for message in rule_no_emoji(path.read_text(encoding="utf-8"), None))
    if errors:
        print("\n".join(errors))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
