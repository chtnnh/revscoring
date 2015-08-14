import sys

import enchant

from .space_delimited import SpaceDelimited

try:
    import enchant
    dictionary = enchant.Dict("fa")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'fa'.  " +
                      "Consider installing 'myspell-fa'.")

# Copy-pasted from https://meta.wikimedia.org/w/index.php?oldid=13044766
stopwords = set([
    "آثار" ,"آری" ,"آغاز" ,"آمریکا" ,"آنها" ,"اثر" ,"اساس" ,"است" ,"استان",
    "استفاده" ,"اسلام" ,"اسلامی" ,"اشاره" ,"اصلی" ,"اطلاعات" ,"افراد" ,"اما",
    "امکان" ,"انبار" ,"انجام" ,"اند" ,"اندازه" ,"انگلیسی" ,"اهالی" ,"اهل" ,"اول",
    "اولین" ,"اين" ,"اگر" ,"ایالات" ,"ایران" ,"ایرانی" ,"این" ,"بار" ,"بازیابی",
    "باشد" ,"بانی" ,"باید" ,"بخش" ,"بدون" ,"برای" ,"برخی" ,"بزرگ" ,"بسیار",
    "بسیاری" ,"بعد" ,"بنا" ,"بناهای" ,"بندانگشتی" ,"بود" ,"بودند" ,"بوده",
    "بیرون" ,"بیش" ,"بیشتر" ,"بین" ,"تاریخ" ,"تاریخی" ,"ترتیب" ,"ترتیب‌پیش‌فرض",
    "ترین" ,"تشکیل" ,"تصویر" ,"تغییر" ,"تغییرمسیر" ,"تلفن" ,"تمام" ,"تنها",
    "تهران" ,"توجه" ,"توسط" ,"جایهای" ,"جستارهای" ,"جعبه" ,"جلالی" ,"جمله",
    "جنگ" ,"جهان" ,"جهانی" ,"حال" ,"حدود" ,"حذف" ,"حروف" ,"خرد" ,"خود",
    "داد" ,"داده" ,"دارای" ,"دارد" ,"دارند" ,"داشت" ,"داشته" ,"دانشگاه",
    "درباره" ,"درگذشتگان" ,"دست" ,"دلیل" ,"دهد" ,"دور" ,"دوران" ,"دوره",
    "دوم" ,"دیرینگی" ,"دیگر" ,"دیگری" ,"راه" ,"ربات" ,"رباتیک" ,"رده",
    "رسمی" ,"روز" ,"روی" ,"روی‌نقشه" ,"زادگان" ,"زبان" ,"زمان" ,"زمانی",
    "زمینه" ,"زنده" ,"زندگی" ,"زیادی" ,"زیر" ,"ساخت" ,"ساخته" ,"سازمان",
    "سال" ,"سال‌های" ,"سده" ,"سرعت" ,"سپتامبر" ,"سیاسی" ,"شامل" ,"شدن",
    "شدند" ,"شده" ,"شده‌است" ,"شرکت" ,"شهر" ,"شهرستان" ,"شود" ,"صفحه",
    "صورت" ,"طول‌جغرافیایی" ,"عرض‌جغرافیایی" ,"علی" ,"عنوان" ,"غیر",
    "فارسی" ,"فعالیت" ,"فعلی" ,"فهرست" ,"فوریه" ,"قبل" ,"قدیمی" ,"قرار",
    "مالک" ,"مانند" ,"ماه" ,"متحده" ,"محل" ,"محلی" ,"محمد" ,"مختلف",
    "مدرک" ,"مردم" ,"مرمت" ,"مرکز" ,"مرکزی" ,"مرگ" ,"مسکونی",
    "مسیر" ,"معروف" ,"مقاله" ,"مقاله‌های" ,"ملی" ,"منابع" ,"مناطق" ,"منبع",
    "منطقه" ,"مورد" ,"میان" ,"میان‌ویکی" ,"میلادی" ,"می‌باشد" ,"می‌توان",
    "می‌دهد" ,"می‌شود" ,"می‌شوند" ,"می‌کند" ,"می‌کنند" ,"نادرست" ,"ناشر" ,
    "نام" ,"نام‌های" ,"نشان" ,"نشانی" ,"نشریه" ,"نظر" ,"نفر" ,"نوع" ,"نویسنده",
    "نیز" ,"نیست" ,"های" ,"هزار" ,"هستند" ,"همان" ,"همراه" ,"همه" ,"همچنین",
    "همین" ,"وابسته" ,"واقع" ,"وبگاه" ,"وب‌گاه" ,"وجود" ,"ولی" ,"ویکی",
    "ویکی‌انبار" ,"ویکی‌سازی" ,"ویکی‌پدیای" ,"پانویس" ,"پایان" ,"پایه" ,"پرونده",
    "پیش" ,"پیوند" ,"چند" ,"چون" ,"ژورنال" ,"کار" ,"کاربری" ,"کتاب" ,"کرد",
    "کردن" ,"کردند" ,"کرده" ,"کشور" ,"کشورهای" ,"کند" ,"کنند" ,"کنونی",
    "گرفت" ,"گرفته" ,"گروه" ,"گفته" ,"یادکرد" ,"یافت" ,"یونسکو" ,"یکی"
])

badwords = [
    r"(madar|nanae|zan|khahar)\s*?(ghahbeh|ghahveh|ghabe|jendeh?|be khata)",
    r"khar madar", r"khar kos deh",
    r"([qkc]+o+s+|[qkc]+o+n+|[qkc]+i+r+|m+e+g+h+a+d)\s*?((va|o)\s*?[qkc]oon|"+
    r"lis|pareh?|k+h+a+r+|[qkc]esh|nane|nanat|babat|khah?a?r|abjit|mi ?dad"+
    r"|mi ?dah[iy]|[qkc]on|deh|khor|goshad|gondeh|[qkc]oloft|[qkc]esh|mashang"+
    r"|khol|baz|shenas|nag[uo]o?|maghz|sh[ae]r)",
    r"\bmameh?", r"sho+[mn]bo+l", r"\brazl", r"gaei?d[ia]m", r"\bk+i+r+i+",
    r"\bk+o+s+o+",
    r"\bk+o+n+i+", r"j+e+n+d+e+h?", r"[qkc]iram",
    r"(pedar|baba|naneh?|tokhme?) sag",
    r"pedasag", r"bi (sho+r|shour|sharaf|namo+s)",    r"madareto?",
    r"\bamato?",
    r"da[iy]o+s", r"goh? ?nakhor", r"\bashghal", r"\bavazi",
    r"کیرم", r"کونی", r"برووتو", r"لعنت", r"کاکاسیاه", r"آشغال",
    r"گائیدم", r"گوزیده",
    r"مشنگ", r"ننتو", r"بخواب", r"خار مادر", r"خوار کس ده", r"شو?مبول",
    r"جنده",
    r"کاکاسیاه",
    r"آشغال",
    r"آله",
    r"ایتالیک",
    r"بخواب",
    r"برووتو",
    r"جمهورمحترم",
    r"فرمود",
    r"فرمودند",
    r"فرموده",
    r"لعنت",
    r"مشنگ",
    r"ننتو",
    r"کون",
    r"کونی",
    r"کیر",
    r"گائیدم",
    r"گوزیده",
    r"کیرم",
    r"ممه",
    r"(ما\.?در|ننه|زن|خو?اه?ر) ?(خرابه|ق\.?[حه]\.?ب\.?ه|قحبه|قبه|ج\.?ن\.?د\.?ه|به خطا)",
    r"([کك]+س+|[کك]+و+ن+|[کك]+[یي]+ر+|مقعد|عضو ?تحتانی|ما?تحت)\s*(و کون|لیسی?|پاره|خر|"+
    r"[کك]ش|نن[هت]\b|بابات|خو?اه?ر|آبجیت|هم ?شیره|می ?داد|می ?ده?ی|می ?کنی?|کن|خور)",
    r"[کك]+(و+ن|س)\s*(خر|گشاد|گنده|کش|مشنگ|پاره|ننت|ننه\b|خل|باز|خور\b|شناس|نگو|مغز|"+
    r"ه؟ ؟شعر|و ?شعر|مادر|خو?اه?ر|آبجیت|هم ?شیره|داد)",
    r"ر[زذ]ل", r"[کك]+[یي]+ر+\s*م?(ی|خر|(ب|)خور|تو[ی ]|مو |دهن)",
    r"گا[يئی]ید[میي]", r"گاهييد[نه]", r"بگامت", r"(پدر|ننه|مادر|بابا|تخم)\s*سگ",
    r"بی ?(شعور|شرف|ناموس)[یي]", r"\پريودى\؟", r"مادرت گا",
    r"تنت میخاره", r"به کیرم", r"به گا ميدم", r"بگای?د",
    r"برای مادرت", r"دیو[سث]", r"ننتو", r"گوزید[نه]?", r"گه نخور",
    r"انگشت به كون",
    r"چاکت", r"جنده", r"گه اضاف[يی] خورد[هیي]", r"خاک تو سرت",
    r"[کك][یي]رم", r"ر[یي]د[همی]", r"[کك]ون ?ده", r"[کك]س ?ده",
    r"گا[یي]ش", r"ب[کك]ن ب[کك]ن", r"([کك]+[یي]+ر+)ی+",
    r"(به پشت|دمر|دمرو) بخواب", r"خایه لیس", r"حسن کلیدساز", r"کره خر",
    r"آشغال ع+و+ض+ی+", r"پدسگ", r"سا[کك] زد", r"فاک (‌فنا|یو)",
    r"برو (گ+م+ش+و|ب+م+ی+ر+)",
    r"گوه خورد", r"شاش اضافه", r"آب [کك][یي]رو?",
    r"[کك]و?س [کك]ردن?", r"[کك][یي]ر [کك]لفت",
    r"کیونده", r"جر دادن?", r"مردک"
]

informals = [
    r"آله", r"فرموده?", r"فرمودند", r"السلام", r"حضرت\b", r"\([سعص]\)",
    r"\(ره\)",
    r"\(قس\)",
    r"\(عج\)", r"\bامام\b", r"فرمودند", r"روحی?‌? ?ا?ل?فدا",
    r"شَ?هید\b", r"آزادهٔ? سرا?فراز",
    r"شادروان", r"جهانخوار", r"مستکبر", r"ملحد", r"ملعون", r"عل[يی]ه‌? ?السلام",
    r"(لعن[تة]|رحمت|صلی|صلوات|سلام)‌? ?اللہ", r"دام‌? ?(ظلّ?ه|برکات)",
    r"قدس‌? ?سره‌? ?شریف",
    r"اسقف محترم", r"خدا[یش]? بیامرز", r"دار فانی", r"به هلاکت",
    r"سَقط شد", r"ا?علیا?‌? ?حضرت",
    r"خادم خادمان", r"مقام معظّ?م", r"(حرم|مرقد) مطهر", r"\bمرحوم\b",
    r"\bشهادت", r"شاهنشاه\b",
    r"علیها", r"مد ?ظله"
]



sys.modules[__name__] = SpaceDelimited(
    __name__,
    badwords=badwords,
    dictionary=dictionary,
    informals=informals,
    stopwords=stopwords
)
"""
persian
"""
