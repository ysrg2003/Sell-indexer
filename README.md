فهمت قصدك تماماً. أنت تريد "كتيب المصنع" الذي يخبرك ليس فقط ماذا تفعل، بل من أين تأتي بكل قطعة غيار وبأي زر تضغط بالتفصيل الممل.
إليك الدليل التشغيلي الشامل (نسخة التنفيذ الدقيق):
الجزء الأول: الحصول على "المواد الخام" (الروابط والأدوات)
| الأداة | من أين تحصل عليها؟ | ملاحظة هامة |
|---|---|---|
| حسابات Gmail | accounts.google.com | استخدم رقم هاتفك الحالي لإنشاء حسابين (واحد مشترك وواحد VIP). |
| بيئة Google Cloud | console.cloud.google.com | المكان الذي ستفعل منه الـ API وتستخرج منه ملف الـ JSON. |
| حساب GitHub العمل | github.com/signup | أنشئ حساباً جديداً باسم علامة تجارية (مثل Smart-Indexer-Ops). |
| كود Python | (الذي ناقشناه سابقاً) | ستحفظه في ملف باسم indexer.py. |
| ملف الـ Action | (مسار الأتمتة) | سيوضع في مسار .github/workflows/main.yml. |
الجزء الثاني: الخطوات "الذرية" للتنفيذ (Step-by-Step)
1. تجهيز محرك جوجل (Google Cloud)
 * ادخل للمنصة، اضغط على Select a Project ثم New Project.
 * ابحث في شريط البحث العلوي عن "Indexing API" واضغط Enable.
 * من القائمة الجانبية: IAM & Admin > Service Accounts.
 * اضغط Create Service Account، سمّه "Bot"، ثم Create and Continue.
 * في خانة الأدوار (Role)، اختر Owner (اختياري لكنه الأسهل لضمان العمل).
 * بعد الانتهاء، ستجد البريد الإلكتروني ظهر أمامك (انسخه للجدول).
 * اضغط على البريد، اذهب لتبويب Keys، اختر Add Key > Create New Key > JSON.
 * سيتحمل ملف على جهازك. هذا هو "قلب النظام"، حافظ عليه.
2. تجهيز مستودع العميل (GitHub)
 * في حساب GitHub العمل، اضغط New Repository.
 * Repository Name: سمه باسم العميل (مثلاً index-client-ali). واجعله Public.
 * رفع الملفات: ارفع ملف indexer.py و ملف urls.txt (فارغ).
 * إنشاء ملف الـ Action:
   * اضغط Add file > Create new file.
   * في اسم الملف اكتب: .github/workflows/main.yml.
   * الصق كود الأتمتة (الذي يخبر GitHub أن يشغل البايثون).
 * وضع السر (The Secret):
   * اذهب لـ Settings > Secrets and variables > Actions.
   * اضغط New repository secret.
   * الاسم: GOOGLE_INDEXING_JSON.
   * القيمة: افتح ملف الـ JSON الذي حملته من جوجل ببرنامج "Notepad"، انسخ كل ما بداخله والصقه هنا.
   * أضف سراً جديداً باسم DAILY_LIMIT.
   * القيمة التي دفع العميل ثمنها (مثلاً: 30 أو 100 أو 200).
3. استخراج "مفتاح الوصول" (The Fine-grained Token)
 * من صورة حسابك في GitHub (أعلى اليمين) > Settings.
 * انزل لآخر القائمة جهة اليسار: Developer settings.
 * Personal access tokens > Fine-grained tokens > Generate new token.
 * Token Name: اسم العميل.
 * Repository access: اختر Only select repositories وحدد مستودع العميل فقط.
 * Permissions: اضغط على Repository permissions وابحث عن Contents واجعلها Read and Write.
 * اضغط Generate وانسخ الكود الناتج (لن تراه مرة أخرى!).

 * إذن التشغيل: في المستودعات الخاصة، اذهب لـ Settings > Actions > General وتأكد أن الخيار هو Allow all actions and reusable workflows.
   
الجزء الثالث: لوحة التحكم (The UI) - من أين نأتي بها؟
ستقوم بإنشاء ملف index.html في نفس مستودع العميل. إليك أهم الأسطر التي ستقوم بتغييرها في كل مرة:
 * السطر الخاص بالتوكن: ابحث عن المتغير الذي يحمل التوكن وضعه بداخله.
 * السطر الخاص بالمسار: ابحث عن const REPO_PATH = 'اسم-حسابك/اسم-مستودع-العميل';.

الجزء الرابع: كيف تربط العميل بالنظام؟ (The Final Link)
هذه هي الخطوة التي يفعلها العميل:
 * يفتح Google Search Console الخاص بموقعه.
 * يذهب لـ Settings > Users and Permissions.
 * يضغط Add User.
 * يضع "بريد الـ Service Account" الذي نسخته أنت من جوجل كلاود (في الجزء الثاني - خطوة 6).
 * يختار الصلاحية Owner.
الجزء الخامس: جدول الإدارة (المصدر: Google Sheets)
افتح sheets.new وأنشئ الأعمدة التالية:
 * اسم العميل.
 * رابط الموقع.
 * بريد الـ Service Account (لكي تعرف من يتبع لمن).
 * ملف الـ JSON (ضع رابطاً للمجلد الذي تحفظ فيه الملفات).
 * تاريخ الاشتراك + تاريخ الانتهاء.
 * رابط لوحة التحكم (رابط GitHub Pages).
ملخص "أين أجد ماذا؟"
 * ملف الـ JSON: من Google Cloud Console.
 * بريد الـ Service Account: من Google Cloud Console.
 * التوكن (Token): من إعدادات GitHub الشخصية.
 * لوحة التحكم: هي رابط GitHub Pages للمستودع.
 * متابعة التنفيذ: من تبويب Actions داخل مستودع GitHub.
بهذا التفصيل، أصبح لديك "كتالوج" كامل. هل نبدأ الآن بصياغة أول إعلان لك لجذب العملاء، أم تريد مني شرح أي أداة من هذه الأدوات بعمق أكبر؟
