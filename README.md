<div align="center">

<h1>Atlas</h1>

Thème Blogger gratuit et open source pour le site vitrine d'une petite entreprise de services, en français et en arabe.

[Démo](https://atlas-muh.blogspot.com) · [Installation](#installation)

</div>

<p align="center">
  <img src="https://cdn.simpleicons.org/blogger/FF5722" height="36" alt="Blogger">
  <img src="https://cdn.simpleicons.org/html5/E34F26" height="36" alt="HTML5">
  <img src="https://cdn.simpleicons.org/css/663399" height="36" alt="CSS">
  <img src="https://cdn.simpleicons.org/javascript/F7DF1E" height="36" alt="JavaScript">
  <img src="https://cdn.simpleicons.org/googlefonts/4285F4" height="36" alt="Google Fonts">
  <img src="https://cdn.simpleicons.org/whatsapp/25D366" height="36" alt="WhatsApp">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/licence-MIT-750014" alt="licence-MIT">
  <img src="https://img.shields.io/badge/Blogger-layouts%20v3-FF5722" alt="Blogger-layouts v3">
  <img src="https://img.shields.io/badge/JavaScript-0%20d%C3%A9pendance-F7DF1E" alt="JavaScript-0 dépendance">
  <img src="https://img.shields.io/badge/PageSpeed%20mobile-97-0CCE6B" alt="PageSpeed mobile 97">
  <img src="https://img.shields.io/badge/langues-FR%20%7C%20AR-4285F4" alt="langues-FR | AR">
</p>

## Le projet

Au Maroc, les petites entreprises de services ont souvent besoin d’un site vitrine, dont le coût peut atteindre environ 12 000 à 28 000 MAD. Atlas fournit un thème Blogger gratuit et open source pour présenter l’entreprise en français et en arabe.

Le thème fournit l’hébergement gratuit, un domaine personnalisé gratuit et le HTTPS via Blogger. Le propriétaire modifie tout depuis Blogger : mise en page, contenus, images, projets et couleurs.

| Élément | Fonctionnement |
|---|---|
| Hébergement | Gratuit via Blogger |
| Domaine | Domaine personnalisé gratuit via Blogger |
| Mise à jour | Le propriétaire modifie le site depuis Blogger |

## Fonctionnalités

- Slider principal avec 3 images.
- Marquee des services.
- Services en bento.
- Slider avant/après.
- Carrousel de projets alimenté par les articles.
- Chiffres animés.
- Slider de témoignages.
- Présentation de l’équipe.
- Formulaire de contact WhatsApp qui ouvre WhatsApp avec le message.
- Bouton WhatsApp flottant.
- Sélecteur FR/AR avec prise en charge du RTL.
- Données structurées `LocalBusiness`.
- Aucun JavaScript externe.
- Respect de `prefers-reduced-motion`.

## Architecture

```text
theme.xml   Le thème, seul fichier livré
demo/       Contenu de démonstration
tools/      Vérificateur et tests JavaScript
mockup/     Maquettes approuvées
docs/       Conception et plan
```

## Installation

Dans Blogger :

1. **Thème → Personnaliser ▸ Restaurer** : importez `theme.xml`.
2. **Mise en page** : remplissez les widgets en suivant `demo/widgets.md` et conservez les identifiants qui y sont indiqués.
3. **Articles** : créez un article par projet, avec le titre `Titre FR | العنوان`, exactement **un label** correspondant à la catégorie, et un corps contenant `<div lang="fr">` et `<div lang="ar">`.
4. **LinkList de contact** : la cible définit le rôle : `wa.me` = WhatsApp, `tel:` = téléphone, `#hours` = horaires, Google Maps = adresse.
5. **Langue par défaut** : la langue du blog détermine la langue initiale ; arabe pour un blog en arabe, français sinon.
6. **Theme Designer** : les 4 couleurs peuvent être modifiées ; la police est fixe.

Les pages de labels ne sont pas indexées par le `robots.txt` par défaut de Blogger.

## Performance

Mesuré sur la démo avec PageSpeed Insights (5 novembre 2026) :

| Page | Appareil | Performance | Accessibilité | Bonnes pratiques | SEO |
|---|---|---|---|---|---|
| Accueil | Mobile | 97 | 100 | 100 | 100 |
| Accueil | Ordinateur | 99 | 100 | 100 | 100 |
| Projet | Mobile | 85 | 98 | 100 | 100 |

La page projet de la démo charge une photo Unsplash de 800 px non optimisée par Blogger ; avec des images importées dans Blogger, le poids baisse.

## Développement

```sh
python3 tools/check_theme.py theme.xml --also demo README.md
node --test tools/test_js.mjs
python3 -m unittest tools/test_checker.py
xmllint --noout theme.xml
```

Il n’y a pas d’étape de build.

## Besoin d'aide ?

Installation et personnalisation sur demande : [muhdroid.com](https://muhdroid.com).

## العربية

<div dir="rtl">

### المشروع

في المغرب، تحتاج الشركات الصغيرة للخدمات غالبا إلى موقع تعريفي، وقد تتراوح تكلفة هذا الموقع بين 12,000 و28,000 درهم مغربي تقريبا. يوفر Atlas قالب Blogger مجانيا ومفتوح المصدر لعرض الشركة بالفرنسية والعربية.

يوفر القالب استضافة مجانية، ونطاقا مخصصا مجانيا، وHTTPS عبر Blogger. يستطيع صاحب الشركة تعديل كل شيء من Blogger: التخطيط، والمحتوى، والصور، والمشاريع، والألوان.

| العنصر | طريقة العمل |
|---|---|
| الاستضافة | مجانية عبر Blogger |
| النطاق | نطاق مخصص مجاني عبر Blogger |
| التحديث | يعدل صاحب الشركة الموقع من Blogger |

### الوظائف

- شريط رئيسي للصور يتضمن 3 صور.
- شريط متحرك للخدمات.
- خدمات بتخطيط bento.
- شريط تمرير قبل/بعد.
- شريط دائري للمشاريع مصدره المقالات.
- أرقام متحركة.
- شريط تمرير لشهادات العملاء.
- عرض أعضاء الفريق.
- نموذج اتصال عبر WhatsApp يفتح WhatsApp مع الرسالة.
- زر WhatsApp عائم.
- مفتاح FR/AR مع دعم RTL.
- بيانات منظمة من نوع `LocalBusiness`.
- لا يوجد JavaScript خارجي.
- احترام `prefers-reduced-motion`.

### البنية

```text
theme.xml   القالب، الملف الوحيد الذي يتم تسليمه
demo/       محتوى العرض التجريبي
tools/      أداة التحقق واختبارات JavaScript
mockup/     النماذج المعتمدة
docs/       التصميم والخطة
```

### التثبيت

في Blogger:

1. **المظهر → تخصيص ▸ استعادة**: ارفع `theme.xml`.
2. **التخطيط**: املأ الأدوات باتباع `demo/widgets.md` وحافظ على المعرّفات المذكورة فيه.
3. **المقالات**: أنشئ مقالا واحدا لكل مشروع، بعنوان `Titre FR | العنوان`، مع **تصنيف واحد بالضبط** يمثل الفئة، ومحتوى يتضمن `<div lang="fr">` و`<div lang="ar">`.
4. **LinkList الخاص بالاتصال**: يحدد الرابط الدور: `wa.me` = WhatsApp، و`tel:` = الهاتف، و`#hours` = أوقات العمل، وGoogle Maps = العنوان.
5. **اللغة الافتراضية**: تحدد لغة المدونة اللغة الأولية؛ العربية للمدونة العربية، والفرنسية في غير ذلك.
6. **Theme Designer**: يمكن تغيير الألوان الأربعة؛ الخط ثابت.

صفحات التصنيفات غير مفهرسة بواسطة ملف `robots.txt` الافتراضي في Blogger.

### الأداء

تم القياس على النسخة التجريبية بـ PageSpeed Insights (5 نونبر 2026):

| الصفحة | الجهاز | الأداء | الوصولية | الممارسات | SEO |
|---|---|---|---|---|---|
| الرئيسية | موبايل | 97 | 100 | 100 | 100 |
| الرئيسية | حاسوب | 99 | 100 | 100 | 100 |
| مشروع | موبايل | 85 | 98 | 100 | 100 |

صفحة المشروع فالنسخة التجريبية كتحمّل تصويرة من Unsplash ما مرتش من Blogger؛ مع تصاور مرفوعة لـ Blogger كيخف الوزن.

### التطوير

```sh
python3 tools/check_theme.py theme.xml --also demo README.md
node --test tools/test_js.mjs
python3 -m unittest tools/test_checker.py
xmllint --noout theme.xml
```

لا توجد خطوة بناء.

### هل تحتاج إلى المساعدة؟

التثبيت والتخصيص عند الطلب: [muhdroid.com](https://muhdroid.com).

</div>

<div align="center">

Conçu et développé par [MuhDroid](https://muhdroid.com)

Licence MIT

</div>
