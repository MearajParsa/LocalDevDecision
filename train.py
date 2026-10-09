import os
import json
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, precision_recall_fscore_support
from decision_engine import normalize_text, VALID_ACTIONS

DATASET_PATH = 'data/decisions.csv'
MODEL_DIR = 'artifacts'
MODEL_PATH = os.path.join(MODEL_DIR, 'decision_model.joblib')
REPORT_PATH = os.path.join(MODEL_DIR, 'evaluation_report.json')

def load_and_validate_data():
    if not os.path.exists(DATASET_PATH):
        print(f"خطا: فایل دیتاست در مسیر '{DATASET_PATH}' یافت نشد.")
        print("لطفاً فایل نمونه را کپی کنید یا داده‌های واقعی خود را در این مسیر قرار دهید.")
        return None

    try:
        df = pd.read_csv(DATASET_PATH)
    except Exception as e:
        print(f"خطا در خواندن فایل CSV: {e}")
        return None

    if 'context' not in df.columns or 'label' not in df.columns:
        print("خطا: دیتاست باید حتماً شامل ستون‌های 'context' و 'label' باشد.")
        return None

    df = df.dropna(subset=['context', 'label'])
    if df.empty:
        print("خطا: دیتاست خالی است یا داده معتبری ندارد.")
        return None

    # Filter invalid actions
    invalid_labels = df[~df['label'].isin(VALID_ACTIONS)]
    if not invalid_labels.empty:
        print(f"هشدار: {len(invalid_labels)} سطر با برچسب‌های نامعتبر یافت و حذف شدند.")
        df = df[df['label'].isin(VALID_ACTIONS)]

    if len(df) < 20: # Minimum required for a meaningful (even if basic) split and stratify
        print(f"خطا: تعداد نمونه‌ها بسیار کم است ({len(df)} نمونه). برای آموزش حداقل به 20 نمونه نیاز دارید.")
        return None

    class_counts = df['label'].value_counts()
    print("توزیع کلاس‌ها:")
    print(class_counts)

    # Need at least 2 samples per class to perform stratified split
    classes_with_one_sample = class_counts[class_counts < 2]
    if not classes_with_one_sample.empty:
        print("\nهشدار: کلاس‌های زیر کمتر از ۲ نمونه دارند و نمی‌توانند در Stratified Split استفاده شوند:")
        print(classes_with_one_sample)
        print("آموزش متوقف شد. لطفاً داده‌های بیشتری برای این کلاس‌ها اضافه کنید.")
        return None

    df['context'] = df['context'].apply(normalize_text)
    return df

def train():
    print("شروع فرآیند آموزش...\n")
    df = load_and_validate_data()

    if df is None:
         print("\nآموزش به دلیل خطاهای دیتاست لغو شد.")
         return

    X = df['context']
    y = df['label']

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    except ValueError as e:
         print(f"\nخطا در تقسیم داده‌ها (احتمالاً به دلیل کمبود نمونه برای برخی کلاس‌ها): {e}")
         return

    # Pipeline setup
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))),
        ('clf', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000))
    ])

    print("در حال آموزش مدل...")
    pipeline.fit(X_train, y_train)

    print("در حال ارزیابی مدل...")
    y_pred = pipeline.predict(X_test)

    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='macro', zero_division=0)

    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    print("\nگزارش ارزیابی (Macro Average):")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    try:
        joblib.dump(pipeline, MODEL_PATH)
        print(f"\nمدل با موفقیت در مسیر '{MODEL_PATH}' ذخیره شد.")

        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
             json.dump(report_dict, f, ensure_ascii=False, indent=4)
        print(f"گزارش ارزیابی در مسیر '{REPORT_PATH}' ذخیره شد.")

    except Exception as e:
         print(f"\nخطا در ذخیره مدل یا گزارش: {e}")


if __name__ == "__main__":
    train()
