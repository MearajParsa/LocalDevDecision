import json
import re

# Fixed list of valid actions
VALID_ACTIONS = [
    "inspect_error",
    "search_code",
    "read_file",
    "run_tests",
    "propose_patch",
    "ask_user",
]

def normalize_text(text: str) -> str:
    """
    Normalizes Persian/Arabic and English text.
    Replaces Arabic 'ي' with Persian 'ی' and Arabic 'ك' with Persian 'ک'.
    """
    if not isinstance(text, str):
        return ""

    text = text.replace('ي', 'ی').replace('ك', 'ک')
    # Simple lowercasing for English consistency
    text = text.lower()
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class DecisionEngine:
    def __init__(self, model_pipeline=None, threshold=0.6):
        self.model_pipeline = model_pipeline
        self.threshold = threshold

    def predict(self, context: str) -> dict:
        """
        Takes a context string, normalizes it, and returns a JSON-compatible dict.
        """
        if not context or not context.strip():
            return self._format_response("ask_user", 0.0, "needs_review", True, "Empty context")

        if self.model_pipeline is None:
            raise ValueError("Model pipeline is not loaded.")

        normalized_context = normalize_text(context)

        try:
            # Get probabilities for all classes
            proba = self.model_pipeline.predict_proba([normalized_context])[0]

            # Access classes_ correctly whether it's a pipeline or a direct estimator
            if hasattr(self.model_pipeline, 'classes_'):
                classes = self.model_pipeline.classes_
            elif hasattr(self.model_pipeline, 'steps'):
                classes = self.model_pipeline.steps[-1][1].classes_
            else:
                classes = VALID_ACTIONS # Fallback

            # Find the max probability and corresponding class
            max_index = proba.argmax()
            max_score = float(proba[max_index])
            best_action = classes[max_index]

            if best_action not in VALID_ACTIONS:
                 return self._format_response("ask_user", max_score, "needs_review", True, "Invalid action predicted")

            # Determine confidence status
            if max_score >= self.threshold:
                status = "confident"
                review_required = False
            else:
                status = "needs_review"
                review_required = True

            return self._format_response(best_action, max_score, status, review_required)

        except Exception as e:
             return self._format_response("ask_user", 0.0, "needs_review", True, f"Prediction error: {str(e)}")


    def _format_response(self, action: str, score: float, status: str, review_required: bool, error_msg: str = None) -> dict:
        response = {
            "action": action,
            "score": round(score, 4),
            "status": status,
            "review_required": review_required
        }
        if error_msg:
            response["error"] = error_msg
        return response

    def to_json(self, response_dict: dict) -> str:
        """
        Converts the response dictionary to a JSON string.
        """
        return json.dumps(response_dict, ensure_ascii=False, indent=2)
