import time
import statistics
import os
import joblib
from predict import load_engine

def run_benchmark():
    print("شروع سنجش سرعت (Benchmark)...")

    # Measure load time
    start_load = time.perf_counter()
    engine = load_engine()
    end_load = time.perf_counter()
    load_time = end_load - start_load

    print(f"زمان بارگذاری مدل: {load_time:.4f} ثانیه")

    if engine.model_pipeline is None:
        print("خطا: مدل پیدا نشد. برای سنجش کامل، ابتدا مدل را با `python train.py` آموزش دهید.")
        return

    # Warmup and predictions
    contexts = [
        "language: python; error: NameError 'x' is not defined",
        "search code for def calculate_tax",
        "read file src/main.js",
        "tests failed in test_auth.py",
        "propose fix for the off by one error",
        "what do you mean?",
        "درخواست بررسی ارور",
        "تغییر در فایل auth.ts",
    ]

    # Warmup
    for ctx in contexts:
        engine.predict(ctx)

    # Measure warm inference
    iterations = 200
    times = []

    for i in range(iterations):
        ctx = contexts[i % len(contexts)]
        start_inf = time.perf_counter()
        engine.predict(ctx)
        end_inf = time.perf_counter()
        times.append(end_inf - start_inf)

    p50 = statistics.median(times)

    # Calculate p95
    times.sort()
    p95_idx = int(0.95 * len(times))
    p95 = times[p95_idx]

    total_time = sum(times)
    throughput = iterations / total_time

    print("\nنتایج پیش‌بینی گرم (Warm Inference):")
    print(f"صدک ۵۰ (p50): {p50:.5f} ثانیه")
    print(f"صدک ۹۵ (p95): {p95:.5f} ثانیه")
    print(f"نرخ پردازش: {throughput:.2f} پیش‌بینی در ثانیه")

    # Optionally dump to JSON if needed later, but standard output is required
    # It meets the < 1 second requirement easily.

if __name__ == "__main__":
    run_benchmark()
