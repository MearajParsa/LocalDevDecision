import os
import argparse
import joblib
from decision_engine import DecisionEngine

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'artifacts', 'decision_model.joblib')

def load_engine():
    """Loads the model and initializes the DecisionEngine."""
    if not os.path.exists(MODEL_PATH):
        # We handle this gracefully by instantiating without a model,
        # which will trigger standard error messages in the engine.
        return DecisionEngine(model_pipeline=None)

    try:
        model = joblib.load(MODEL_PATH)
        return DecisionEngine(model_pipeline=model)
    except Exception as e:
        print(f"Error loading model: {e}")
        return DecisionEngine(model_pipeline=None)

def main():
    parser = argparse.ArgumentParser(description="LocalDevDecision Predictor")
    parser.add_argument("--context", type=str, help="Context string to predict action for")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")

    args = parser.parse_args()

    engine = load_engine()

    if args.interactive:
        print("حالت تعاملی فعال شد. برای خروج 'exit' یا 'quit' را تایپ کنید.")
        while True:
            try:
                user_input = input("Context: ")
                if user_input.lower() in ['exit', 'quit']:
                    break

                try:
                     result = engine.predict(user_input)
                     print(engine.to_json(result))
                except ValueError as ve:
                     # e.g., model not loaded
                     error_res = engine._format_response("ask_user", 0.0, "needs_review", True, str(ve))
                     print(engine.to_json(error_res))

            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                 error_res = engine._format_response("ask_user", 0.0, "needs_review", True, f"Unexpected error: {str(e)}")
                 print(engine.to_json(error_res))
    elif args.context:
         try:
              result = engine.predict(args.context)
              print(engine.to_json(result))
         except ValueError as ve:
              error_res = engine._format_response("ask_user", 0.0, "needs_review", True, str(ve))
              print(engine.to_json(error_res))
         except Exception as e:
              error_res = engine._format_response("ask_user", 0.0, "needs_review", True, f"Unexpected error: {str(e)}")
              print(engine.to_json(error_res))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
