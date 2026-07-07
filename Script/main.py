import requests
import json
import os

# تنظيف الشاشة عند بدء التشغيل ليصبح المظهر أرتب
os.system('cls' if os.name == 'nt' else 'clear')

# محاولة استيراد مكتبة PrettyTable لتنسيق الجداول بشكل احترافي ومحاذاته بشكل صحيح مع العربي
try:
    from prettytable import PrettyTable
    HAS_PRETTYTABLE = True
except ImportError:
    HAS_PRETTYTABLE = False

# رموز الألوان (تم الإبقاء عليها للنصوص الفرعية فقط لتجنب تخريب المحاذاة)
BLUE = "\033[1;36m"
GREEN = "\033[1;32m"
ORANGE = "\033[1;33m"
RED = "\033[1;31m"
RESET = "\033[0m"
GRAY = "\033[90m"

print(f"{BLUE}========================================={RESET}")
print(f"{GREEN}    سكريبت البحث عن الأرقام بالاسم 💫    {RESET}")
print(f"{BLUE}========================================={RESET}\n")

search_name = input('♡ NAME :: ')  
print(f"\n{GRAY}[+] جاري البحث والترتيب، يرجى الانتظار...{RESET}\n")

seen_numbers = set()

# إعداد الجدول إذا كانت المكتبة متوفرة
if HAS_PRETTYTABLE:
    table = PrettyTable()
    table.field_names = ["الاسم المطابق (العدد)", "الرقم الكامل", "الألقاب البديلة المكتشفة"]
    table.align["الاسم المطابق (العدد)"] = "l"
    table.align["الرقم الكامل"] = "c"
    table.align["الألقاب البديلة المكتشفة"] = "l"

try:
    # تم إبقاء البريفكس على 964 الخاص بالعراق بناءً على موقعك الحالي لتجلب النتائج بدقة
    url = f"https://acr2.y0.com/search?prefix=964&q={search_name}"
    
    try:
        response = requests.get(url, timeout=10)
        raw_data = response.json()
    except Exception:
        print(f"{RED}[!] تعذر الاتصال بالخادم المفرغ.{RESET}")
        raw_data = []

    if type(raw_data) is not list:
        raw_data = [raw_data]

    results_found = False

    for element in raw_data:
        if type(element) is bytes:
            try:
                element = json.loads(element.decode('utf-8'))
            except Exception:
                continue
            
        if type(element) is list:
            items = element
        else:
            items = [element]
            
        for item in items:
            if type(item) is not dict:
                continue
                
            prefix = item.get("prefix", "")
            number = item.get("number", "")
            
            if str(number).startswith(str(prefix)):
                full_number = str(number)
            else:
                full_number = f"+{prefix}{number}"
            
            if full_number in seen_numbers:
                continue
            seen_numbers.add(full_number)
            results_found = True
                
            matched_name = item.get("matchedName", "بدون اسم")
            names_count = item.get("namesCount", 0)
            
            # صياغة حقل الاسم مع العدد بدون وضع رموز ألوان تخرب الجدول الداخلي
            name_with_count = f"{matched_name} ({names_count})"
            
            other_names = []
            seen_aliases = set()
            
            for n in item.get("names", []):
                alias = n.get('name', '')
                if alias and alias not in seen_aliases:
                    seen_aliases.add(alias)
                    other_names.append(f"{alias} ({n.get('occurrences', 0)})")
                
            names_list = " ، ".join(other_names) if other_names else "لا توجد ألقاب أخرى"
            
            if HAS_PRETTYTABLE:
                # إضافة السطر للجدول الاحترافي
                table.add_row([name_with_count, full_number, names_list])
            else:
                # طريقة طباعة بديلة منسقة يدوياً بدون ألوان مبعثرة إذا لم تتوفر المكتبة
                print(f"👤 {BLUE}{name_with_count}{RESET}")
                print(f"📞 {GREEN}{full_number}{RESET}")
                print(f"🏷️  {GRAY}الألقاب: {names_list}{RESET}")
                print(f"{GRAY}" + "-"*50 + f"{RESET}")

    if HAS_PRETTYTABLE and results_found:
        print(table)
    elif not results_found:
        print(f"{RED}[!] لم يتم العثور على نتائج لهذا الاسم.{RESET}")

except Exception as e:
    print(f"\n{RED}[!] حدث خطأ أثناء تشغيل البرنامج: {e}{RESET}")
