import os

# Get the project root directory (TradingAgents folder)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DEFAULT_CONFIG = {
    "project_dir": PROJECT_ROOT,
    "data_dir": os.path.join(PROJECT_ROOT, "data"),  # Use local data directory
    "data_cache_dir": os.path.join(PROJECT_ROOT, "tradingagents", "dataflows", "data_cache"),
    # LLM settings
    "deep_think_llm": "gpt-4o-mini",  # Fixed model name
    "quick_think_llm": "gpt-4o-mini",
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": False,  # Start with offline for testing
}
