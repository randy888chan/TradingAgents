.PHONY: setup

setup:
	@if [ ! -d .venv ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv .venv; \
		echo "Downloading uv binary..."; \
		curl -sL https://github.com/astral-sh/uv/releases/download/0.7.12/uv-aarch64-apple-darwin.tar.gz -o .venv/bin/uv.tar.gz; \
		tar -xzf .venv/bin/uv.tar.gz -C .venv/bin; \
		mv .venv/bin/uv-aarch64-apple-darwin/uv .venv/bin/uv; \
		chmod +x .venv/bin/uv; \
		rm .venv/bin/uv.tar.gz; \
		rm -rf /.venv/bin/uv-aarch64-apple-darwin; \
	fi

	@echo "Installing dependencies with uv..."
	@.venv/bin/uv pip install -r requirements.txt
	@echo "Please enter your API keys:"
	@bash -c 'read -s -p "FINNHUB_API_KEY: " FINNHUB_KEY; echo; \
	          read -s -p "OPENAI_API_KEY: " OPENAI_KEY; echo; \
	          echo "export FINNHUB_API_KEY=$$FINNHUB_KEY" > .env; \
	          echo "export OPENAI_API_KEY=$$OPENAI_KEY" >> .env; \
	          echo "API keys saved to .env file. Run '\''source .env'\'' to load them."'
