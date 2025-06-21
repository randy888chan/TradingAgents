#!/usr/bin/env python3
"""
Simple test script to verify Ollama connection is working.
"""

import os
import requests
import time
from openai import OpenAI

def test_ollama_connection():
    """Test if Ollama is accessible and responding."""
    
    # Get configuration from environment
    backend_url = os.environ.get("LLM_BACKEND_URL", "http://localhost:11434/v1")
    model = os.environ.get("LLM_DEEP_THINK_MODEL", "qwen2.5")
    
    print(f"Testing Ollama connection:")
    print(f"  Backend URL: {backend_url}")
    print(f"  Model: {model}")
    
    # Test 1: Check if Ollama API is responding
    try:
        response = requests.get(f"{backend_url.replace('/v1', '')}/api/tags", timeout=10)
        if response.status_code == 200:
            print("✅ Ollama API is responding")
        else:
            print(f"❌ Ollama API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to Ollama API: {e}")
        return False
    
    # Test 2: Check if the model is available
    try:
        response = requests.get(f"{backend_url.replace('/v1', '')}/api/tags", timeout=10)
        models = response.json().get("models", [])
        model_names = [m.get("name", "") for m in models]
        
        if model in model_names:
            print(f"✅ Model '{model}' is available")
        else:
            print(f"❌ Model '{model}' not found. Available models: {model_names}")
            return False
    except Exception as e:
        print(f"❌ Failed to check model availability: {e}")
        return False
    
    # Test 3: Test OpenAI-compatible API
    try:
        client = OpenAI(base_url=backend_url, api_key="dummy")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello, say 'test successful'"}],
            max_tokens=50
        )
        print("✅ OpenAI-compatible API is working")
        print(f"   Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ OpenAI-compatible API test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ollama_connection()
    if success:
        print("\n🎉 All tests passed! Ollama is ready.")
        exit(0)
    else:
        print("\n💥 Tests failed! Check Ollama configuration.")
        exit(1) 