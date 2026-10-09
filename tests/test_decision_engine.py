import pytest
import json
import os
import joblib
from decision_engine import normalize_text, DecisionEngine, VALID_ACTIONS
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def test_normalize_text_english():
    assert normalize_text("  Hello  World  ") == "hello world"

def test_normalize_text_persian_arabic():
    # 'ي' should become 'ی', 'ك' should become 'ک'
    assert normalize_text("يک كلاس") == "یک کلاس"

def test_normalize_text_empty_or_invalid():
    assert normalize_text(None) == ""
    assert normalize_text("") == ""

def test_decision_engine_no_model():
    engine = DecisionEngine(model_pipeline=None)
    with pytest.raises(ValueError, match="Model pipeline is not loaded."):
        engine.predict("some context")

def test_decision_engine_empty_input():
    # Should handle empty input even if a model exists (mocking model to avoid error)
    engine = DecisionEngine(model_pipeline=True)
    res = engine.predict("")
    assert res['action'] == "ask_user"
    assert res['status'] == "needs_review"
    assert res['error'] == "Empty context"

@pytest.fixture
def dummy_pipeline():
    # Create a small dummy pipeline to test the engine's predict method
    texts = [
        "error error",
        "search code",
        "read file",
        "run tests",
        "propose patch",
        "ask user user"
    ]
    labels = [
        "inspect_error",
        "search_code",
        "read_file",
        "run_tests",
        "propose_patch",
        "ask_user"
    ]
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))),
        ('clf', LogisticRegression())
    ])
    pipeline.fit(texts, labels)
    return pipeline

def test_decision_engine_with_model(dummy_pipeline):
    engine = DecisionEngine(model_pipeline=dummy_pipeline, threshold=0.1) # low threshold for test
    res = engine.predict("search the code")

    assert 'action' in res
    assert res['action'] in VALID_ACTIONS
    assert 'score' in res
    assert isinstance(res['score'], float)
    assert 'status' in res

    # Test JSON output
    json_out = engine.to_json(res)
    assert isinstance(json_out, str)
    parsed = json.loads(json_out)
    assert parsed['action'] == res['action']

def test_invalid_label_handling(dummy_pipeline):
    import numpy as np
    # Modify pipeline classes to simulate an invalid prediction
    dummy_pipeline.steps[-1][1].classes_ = np.array(["invalid_action"] * len(dummy_pipeline.steps[-1][1].classes_))
    engine = DecisionEngine(model_pipeline=dummy_pipeline)
    res = engine.predict("some text")
    assert res['action'] == "ask_user"
    assert res['error'] == "Invalid action predicted"
