"""
Environment variable loader for TradingAgents.
Automatically loads environment variables from .env file if it exists.
"""

import os
from pathlib import Path

def load_environment():
    """Load environment variables from .env file if it exists."""
    try:
        from dotenv import load_dotenv
        
        # Find the project root (where .env should be located)
        current_dir = Path(__file__).parent
        project_root = current_dir.parent  # Go up one level from tradingagents/
        env_file = project_root / ".env"
        
        if env_file.exists():
            load_dotenv(env_file)
            print(f"✅ Environment variables loaded from {env_file}")
            
            # Verify required API keys are loaded
            required_keys = ["FINNHUB_API_KEY", "OPENAI_API_KEY"]
            missing_keys = []
            
            for key in required_keys:
                if not os.getenv(key) or os.getenv(key) == f"your_{key.lower()}_here":
                    missing_keys.append(key)
            
            if missing_keys:
                print(f"⚠️  Warning: The following API keys need to be set in your .env file:")
                for key in missing_keys:
                    print(f"   - {key}")
                print(f"   Please edit {env_file} and replace the placeholder values with your actual API keys.")
            else:
                print("✅ All required API keys are configured!")
                
        else:
            print(f"ℹ️  No .env file found at {env_file}")
            print("   You can create one with your API keys or use environment variables directly.")
            
    except ImportError:
        print("⚠️  python-dotenv not installed. Install it with: pip install python-dotenv")
    except Exception as e:
        print(f"❌ Error loading .env file: {e}")

# Call load_environment when this module is imported
load_environment() 