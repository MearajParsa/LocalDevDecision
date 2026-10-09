import csv

data = [
    ("The code threw a NameError on line 45", "inspect_error"),
    ("I got a NullPointerException when running the Java app", "inspect_error"),
    ("TypeError: undefined is not a function in app.js", "inspect_error"),
    ("Tests failed with a syntax error in the backend", "inspect_error"),
    ("I encountered a strange error: index out of bounds", "inspect_error"),
    ("Can you show me where the error traceback points to?", "inspect_error"),
    ("خطای سینتکس توی خط ۴۰ فایل main.py میده", "inspect_error"),
    ("یه ارور ناشناخته موقع اجرای سرور دارم", "inspect_error"),
    ("برنامه کرش کرد و خطای out of memory داد", "inspect_error"),
    ("چرا ارور NameError: name 'x' is not defined میگیرم؟", "inspect_error"),

    ("Where is the user authentication logic located?", "search_code"),
    ("Find the function that calculates the total price", "search_code"),
    ("Search for 'TODO' comments in the project", "search_code"),
    ("How is the database connection initialized?", "search_code"),
    ("Look for all instances where process_data is called", "search_code"),
    ("Find the definition of class User", "search_code"),
    ("تابع محاسبه مالیات کجای پروژه تعریف شده؟", "search_code"),
    ("همه جاهایی که از تابع send_email استفاده شده رو پیدا کن", "search_code"),
    ("کلاس مربوط به مدیریت کاربران رو سرچ کن", "search_code"),
    ("فایل تنظیمات اتصال به دیتابیس کجاست؟", "search_code"),

    ("Open the file src/utils.py and show its contents", "read_file"),
    ("Can you read the README.md file?", "read_file"),
    ("Read the contents of package.json", "read_file"),
    ("Display the first 50 lines of main.py", "read_file"),
    ("I need to see what is written in config.yml", "read_file"),
    ("Read the test_app.py file to understand the tests", "read_file"),
    ("فایل models.py رو بخون و به من نشون بده", "read_file"),
    ("محتویات فایل متنی requirements.txt چیه؟", "read_file"),
    ("لطفا فایل settings.py رو باز کن", "read_file"),
    ("میشه محتوای فایل لاگ رو بخونی؟", "read_file"),

    ("Run all the unit tests in the project", "run_tests"),
    ("Execute the test suite for the payment module", "run_tests"),
    ("Run pytest on tests/test_math.py", "run_tests"),
    ("Trigger the automated tests for the frontend", "run_tests"),
    ("Check if the tests pass after the recent changes", "run_tests"),
    ("Run npm test to see if everything is green", "run_tests"),
    ("همه تست‌های برنامه رو اجرا کن", "run_tests"),
    ("تست‌های مربوط به لاگین رو ران کن", "run_tests"),
    ("با کامند pytest تست‌های این ماژول رو چک کن", "run_tests"),
    ("ببین بعد از تغییراتم تست‌ها پاس میشن یا نه؟", "run_tests"),

    ("Write a fix for the off-by-one error", "propose_patch"),
    ("Update the function to handle null inputs correctly", "propose_patch"),
    ("Refactor this code to use list comprehensions instead", "propose_patch"),
    ("Add a check for empty strings in the validator", "propose_patch"),
    ("Propose a patch to improve the performance of this loop", "propose_patch"),
    ("Implement the missing error handling here", "propose_patch"),
    ("برای باگی که پیدا کردیم یه پچ بنویس", "propose_patch"),
    ("تابع رو اصلاح کن که بتونه ورودی‌های خالی رو هم مدیریت کنه", "propose_patch"),
    ("این بخش از کد رو بهینه‌تر کن", "propose_patch"),
    ("یه تغییر پیشنهاد بده که این ارور دیگه تکرار نشه", "propose_patch"),

    ("I'm not sure what you mean, can you clarify?", "ask_user"),
    ("Do you want me to delete the file or just empty it?", "ask_user"),
    ("Should I commit these changes now?", "ask_user"),
    ("Which branch should I merge this into?", "ask_user"),
    ("Are there any specific coding guidelines I should follow?", "ask_user"),
    ("Please provide the credentials so I can log in.", "ask_user"),
    ("منظورت رو دقیق متوجه نشدم، میشه بیشتر توضیح بدی؟", "ask_user"),
    ("میخوای این فایل رو کلا پاک کنم یا فقط ویرایشش کنم؟", "ask_user"),
    ("اسم برنچی که باید کدها رو توش پوش کنم چیه؟", "ask_user"),
    ("آیا نیاز هست که تست‌های جدیدی هم اضافه کنم؟", "ask_user"),
]

with open('data/decisions.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['context', 'label'])
    writer.writerows(data)
