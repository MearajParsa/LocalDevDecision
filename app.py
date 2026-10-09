import os
import json
import joblib
from decision_engine import DecisionEngine
import sys

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'artifacts', 'decision_model.joblib')

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_engine():
    if not os.path.exists(MODEL_PATH):
        print(f"{Colors.FAIL}خطا: مدل یافت نشد! لطفاً ابتدا فایل train.py را اجرا کنید تا مدل ساخته شود.{Colors.ENDC}")
        sys.exit(1)

    try:
        model = joblib.load(MODEL_PATH)
        return DecisionEngine(model_pipeline=model)
    except Exception as e:
        print(f"{Colors.FAIL}خطا در بارگذاری مدل: {e}{Colors.ENDC}")
        sys.exit(1)

def main():
    print(f"{Colors.HEADER}{Colors.BOLD}======================================================{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}    به دستیار هوشمند LocalDevDecision خوش آمدید!    {Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}======================================================{Colors.ENDC}")
    print(f"شما می‌توانید مسئله یا درخواست خود را به زبان ساده (فارسی یا انگلیسی) بنویسید.")
    print(f"برنامه تصمیم می‌گیرد که قدم بعدی چه باید باشد.")
    print(f"{Colors.WARNING}برای خروج کلمه 'exit' یا 'quit' را تایپ کنید.{Colors.ENDC}")
    print(f"------------------------------------------------------")

    engine = load_engine()

    while True:
        try:
            user_input = input(f"\n{Colors.OKBLUE}{Colors.BOLD}مسئله شما: {Colors.ENDC}")
            if user_input.lower().strip() in ['exit', 'quit']:
                print(f"{Colors.OKGREEN}خداحافظ! به امید دیدار.{Colors.ENDC}")
                break

            if not user_input.strip():
                print(f"{Colors.WARNING}لطفا یک متن معتبر وارد کنید.{Colors.ENDC}")
                continue

            result = engine.predict(user_input)

            # Formatting the output nicely
            action = result.get('action')
            score = result.get('score', 0) * 100
            status = result.get('status')

            print(f"\n{Colors.BOLD}تصمیم سیستم:{Colors.ENDC}")
            print(f"  {Colors.BOLD}اقدام پیشنهادی:{Colors.ENDC} {Colors.OKGREEN}{action}{Colors.ENDC}")
            print(f"  {Colors.BOLD}میزان اطمینان:{Colors.ENDC} {score:.1f}%")

            if status == "needs_review":
                print(f"  {Colors.BOLD}وضعیت:{Colors.ENDC} {Colors.WARNING}نیاز به بررسی توسط شما (اطمینان پایین){Colors.ENDC}")
            else:
                print(f"  {Colors.BOLD}وضعیت:{Colors.ENDC} {Colors.OKCYAN}مطمئن{Colors.ENDC}")

        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.OKGREEN}خداحافظ!{Colors.ENDC}")
            break
        except Exception as e:
            print(f"{Colors.FAIL}خطای پیش‌بینی نشده: {str(e)}{Colors.ENDC}")

if __name__ == "__main__":
    main()
