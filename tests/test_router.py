from app.services.router import ModelRouter

def test_fast_tasks_route_to_gemini():
    assert ModelRouter().choose("summarize this", "fast") == "gemini"

def test_code_tasks_route_to_groq():
    assert ModelRouter().choose("write code", "code") == "groq"

def test_long_prompts_route_to_gemini():
    assert ModelRouter().choose("x" * 7001, "auto") == "gemini"

def test_code_keyword_routes_to_groq():
    assert ModelRouter().choose("debug this stack trace", "auto") == "groq"
