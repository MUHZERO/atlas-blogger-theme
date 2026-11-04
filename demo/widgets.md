# Atlas Blogger demo widgets
Importez d’abord les images dans Blogger et remplacez leurs sources par les URLs Blogger.
Créez un widget par section et conservez les identifiants indiqués.
Collez les champs ci-dessous tels quels dans les widgets correspondants.
Utilisez un seul label par article.
Pour les titres, légendes et noms, gardez le format `FR | AR`.

## Header1 (header)
Type: Header
Title: `Atlas | أطلس`
Description: `Rénovation | للترميم`

## LinkList2 (navigation)
Type: LinkList
- `Services | الخدمات` → `#services`
- `Réalisations | أعمالنا` → `#projets`
- `Équipe | الفريق` → `#equipe`
- `Contact | اتصل بنا` → `#contact`

## Image2 (hero 1)
Type: Image
Title: `Rénovation clé en main. | ترميم شقتك من البداية للتسليم.`
Caption: `Devis gratuit sous 48 h. | عرض سعر مجاني خلال 48 ساعة.`
Link: `#contact`
Image source: `https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1800&fit=crop`

## Image3 (hero 2)
Type: Image
Image source: `https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=1800&fit=crop`

## Image4 (hero 3)
Type: Image
Image source: `https://images.unsplash.com/photo-1556911220-bff31c812dba?w=1800&fit=crop`

## LinkList3 (marquee)
Type: LinkList
- `Peinture | الصباغة` → `#services`
- `Carrelage | الزليج` → `#services`
- `Plomberie | الترصيص` → `#services`
- `Électricité | الكهرباء` → `#services`
- `Cuisines | المطابخ` → `#services`
- `Salles de bain | الحمامات` → `#services`

## Image5 (service main)
Type: Image
Title: `Rénovation complète | ترميم شامل`
Caption: `Du gros œuvre à la finition | من الأساس حتى التشطيب`
Image source: `https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1000&fit=crop`

## HTML1 (services)
Type: HTML
```html
<div class="tile" data-icon="paint"><h3><span lang="fr">Peinture</span><span lang="ar">الصباغة</span></h3><p><span lang="fr">Intérieur et façade</span><span lang="ar">داخلية وواجهات</span></p></div>
<div class="tile" data-icon="tile"><h3><span lang="fr">Carrelage</span><span lang="ar">الزليج والبلاط</span></h3><p><span lang="fr">Sols et murs</span><span lang="ar">الأرضيات والجدران</span></p></div>
<div class="tile" data-icon="drop"><h3><span lang="fr">Plomberie</span><span lang="ar">الترصيص</span></h3><p><span lang="fr">Cuisine et salle de bain</span><span lang="ar">المطبخ والحمام</span></p></div>
<div class="tile" data-icon="bolt"><h3><span lang="fr">Électricité</span><span lang="ar">الكهرباء</span></h3><p><span lang="fr">Mise aux normes</span><span lang="ar">مطابقة المعايير</span></p></div>
<div class="tile wide" data-icon="shield"><h3><span lang="fr">Garantie 2 ans</span><span lang="ar">ضمان سنتين</span></h3><p><span lang="fr">Sur tous nos travaux</span><span lang="ar">على جميع الأشغال</span></p></div>
<div class="tile" data-icon="clock"><h3><span lang="fr">Délais tenus</span><span lang="ar">احترام الآجال</span></h3><p><span lang="fr">Planning écrit</span><span lang="ar">جدول مكتوب</span></p></div>
<div class="tile" data-icon="chat"><h3><span lang="fr">Suivi WhatsApp</span><span lang="ar">متابعة بواتساب</span></h3><p><span lang="fr">Photos chaque semaine</span><span lang="ar">صور كل أسبوع</span></p></div>
```

## Image6 (before)
Type: Image
Title: `Avant | قبل`
Image source: `TODO: a real unrenovated-room photo (Unsplash, free licence) — must differ from the after photo`

## Image7 (after)
Type: Image
Title: `Après | بعد`
Image source: `https://images.unsplash.com/photo-1556911220-bff31c812dba?w=1200&fit=crop`

## LinkList4 (steps)
Type: LinkList
- `Visite gratuite | زيارة مجانية` → `#contact`
- `Devis détaillé | عرض سعر مفصل` → `#contact`
- `Travaux | الأشغال` → `#contact`
- `Livraison | التسليم` → `#contact`

## HTML2 (numbers)
Type: HTML
```html
<div><b data-count="12" data-suffix="">12</b><span lang="fr">ans d'expérience</span><span lang="ar">سنة خبرة</span></div>
<div><b data-count="340" data-suffix="+">340+</b><span lang="fr">chantiers livrés</span><span lang="ar">مشروع منجز</span></div>
<div><b data-count="18" data-suffix="">18</b><span lang="fr">artisans</span><span lang="ar">حرفي</span></div>
<div><b data-count="98" data-suffix="%">98%</b><span lang="fr">clients satisfaits</span><span lang="ar">عملاء راضون</span></div>
```

## HTML3 (reviews)
Type: HTML
```html
<div class="review"><div class="stars"><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg></div><blockquote><span lang="fr">« Travail propre, délais tenus. Je recommande. »</span><span lang="ar">«عمل نظيف واحترام للمواعيد. أنصح بهم.»</span></blockquote><div class="who"><div><b><span lang="fr">Samira B.</span><span lang="ar">سميرة ب.</span></b><small><span lang="fr">Maârif</span><span lang="ar">المعاريف</span></small></div></div></div>
<div class="review"><div class="stars"><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg></div><blockquote><span lang="fr">« Photos chaque semaine, zéro surprise sur le prix. »</span><span lang="ar">«صور كل أسبوع، وبلا مفاجآت فالثمن.»</span></blockquote><div class="who"><div><b><span lang="fr">Karim T.</span><span lang="ar">كريم ت.</span></b><small><span lang="fr">Californie</span><span lang="ar">كاليفورنيا</span></small></div></div></div>
<div class="review"><div class="stars"><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg></div><blockquote><span lang="fr">« Notre salle de bain est méconnaissable. »</span><span lang="ar">«الحمام ديالنا تبدل كامل.»</span></blockquote><div class="who"><div><b><span lang="fr">Leila M.</span><span lang="ar">ليلى م.</span></b><small><span lang="fr">Gauthier</span><span lang="ar">غوتييه</span></small></div></div></div>
```

## Image8 (team 1)
Type: Image
Title: `Youssef A. | يوسف أ.`
Caption: `Fondateur | المؤسس`
Image source: `https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=660&fit=crop`

## Image9 (team 2)
Type: Image
Title: `Nadia K. | نادية ك.`
Caption: `Architecte | مهندسة معمارية`
Image source: `https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=500&h=660&fit=crop`

## Image10 (team 3)
Type: Image
Title: `Hamid R. | حامد ر.`
Caption: `Chef de chantier | رئيس الورش`
Image source: `https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=500&h=660&fit=crop`

## Image11 (team 4)
Type: Image
Title: `Omar L. | عمر ل.`
Caption: `Électricien | كهربائي`
Image source: `https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=500&h=660&fit=crop`

## LinkList1 (contact)
The target decides the role: `wa.me` = WhatsApp, `tel:` = phone, `#hours` = hours, Google Maps = address.
Type: LinkList
- `WhatsApp` → `https://wa.me/212600000000`
- `+212 5 22 00 00 00` → `tel:+212522000000`
- `Lun–Sam 9h–18h | الإثنين–السبت 9–18` → `#hours`
- `Maârif, Casablanca | المعاريف، الدار البيضاء` → `https://www.google.com/maps/search/?api=1&query=Maarif+Casablanca`

## Image1 (contact background)
Type: Image
Image source: `https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1600&fit=crop`
