# 🚀 Docker Setup for Trading Agents

This guide provides instructions for running the Trading Agents application within a secure and reproducible Docker environment. Using Docker simplifies setup, manages dependencies, and ensures a consistent experience across different machines.

The recommended method is using `docker-compose`, which handles the entire stack, including the Ollama server and model downloads.

## Prerequisites

Before you begin, ensure you have the following installed:
*   [**Docker**](https://docs.docker.com/get-docker/)
*   [**Docker Compose**](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

## ⚡ Quickstart

For those familiar with Docker, here are the essential steps:

```bash
# 1. Clone the repository
git clone https://github.com/AppliedAIMuse/TradingAgents.git
cd TradingAgents

# 2. Create the environment file
cp .env.example .env

# 3. Edit .env and set your API Keys or pick local LLM settings to run locally

# 4. Build the app
docker-compose build

# 5. Run the comman-line app
docker-compose run -it app
```

## Step-by-Step Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

### Step 2: Configure Your Environment (`.env` file)

The application is configured using an environment file. Create your own `.env` file by copying the provided template.

```bash
cp .env.example .env
```

Next, open the `.env` file and customize the settings. The most important variables are `LLM_PROVIDER` and `OPENAI_API_KEY`.

*   **To use the local Ollama server:**
    ```env
    LLM_PROVIDER="ollama"
    ```
*   **To use external provider like OpenAI:**
    ```env
    LLM_PROVIDER="openai"
    OPENAI_API_KEY="your-api-key-here"
    ```
    > **Note:** If you use an external provider, the Ollama service will not start, saving system resources.

### Step 3: Run with `docker-compose` (Recommended)

This is the simplest way to run the entire application.

#### Build and Start the Containers

The following command will build the Docker image, download the required LLM models (if using Ollama), and start the application.

```bash
# Use --build the first time or when you change dependencies
docker-compose build

# On subsequent runs, you can run directily
docker-compose run -it app
```

The first time you run this, it may take several minutes to download the base image and the LLM models. Subsequent builds will be much faster thanks to Docker's caching.

#### View Logs

To view the application logs in real-time, you can run:
```bash
docker-compose logs -f
```

#### Stop the Containers

To stop and remove the containers, press `Ctrl + C` in the terminal where `docker-compose run` is running, or run the following command from another terminal:
```bash
docker-compose down
```


### Step 4: Verify the Ollama Setup (Optional)

If you are using `LLM_PROVIDER="ollama"`, you can verify that the Ollama server is running correctly and has the necessary models.

Run the verification script inside the running container:
```bash
docker-compose exec app python test_ollama_connection.py
```

### Step 5: Run Ollama server commands (Optional)

If you are using `LLM_PROVIDER="ollama"`, you can verify run any of the Ollama server commands like  list of all the models using: 
```bash
docker-compose exec app ollama list
```

✅ **Expected Output:**
```
Testing Ollama connection:
  Backend URL: http://localhost:11434/v1
  Model: qwen3:0.6b
  Embedding Model: nomic-embed-text
✅ Ollama API is responding
✅ Model 'qwen3:0.6b' is available
✅ OpenAI-compatible API is working
   Response: ...
```

---

## Alternative Method: Using `docker` Only

If you prefer not to use `docker-compose`, you can build and run the container manually.

**1. Build the Docker Image:**
```bash
docker build -t trading-agents .
```

**2. Test local ollama setup (Optional):**
Make sure you have a `.env` file configured as described in Step 2. If you are using `LLM_PROVIDER="ollama"`, you can verify that the Ollama server is running correctly and has the necessary models.
```bash
docker run -it --env-file .env trading-agents python test_ollama_connection.py
```
for picking environment settings from .env file. You can pass values directly using: 
```bash
docker run -it \
  -e LLM_PROVIDER="ollama" \
  -e LLM_BACKEND_URL="http://localhost:11434/v1" \
  -e LLM_DEEP_THINK_MODEL="qwen3:0.6b" \
  -e LLM_EMBEDDING_MODEL="nomic-embed-text"\ 
  trading-agents \
  python test_ollama_connection.py
```
To prevent re-downloading of Ollama models, mount folder from your host and run as
```bash
docker run -it \
  -e LLM_PROVIDER="ollama" \
  -e LLM_BACKEND_URL="http://localhost:11434/v1" \
  -e LLM_DEEP_THINK_MODEL="qwen3:0.6b" \
  -e LLM_EMBEDDING_MODEL="nomic-embed-text"\ 
  -v ./ollama_cache:/app/.ollma \
  trading-agents \
  python test_ollama_connection.py
```


**3. Run the Docker Container:**
Make sure you have a `.env` file configured as described in Step 2.
```bash
docker run --rm -it \
  --env-file .env \
  -p 11434:11434 \
  -v ./data:/app/data \
  --name tradingagents-app \
  trading-agents
```


## Configuration Details

### Live Reloading
The `app` directory is mounted as a volume into the container. This means any changes you make to the source code on your local machine will be reflected instantly in the running container without needing to rebuild the image.

### Persistent Data
The following volumes are used to persist data between container runs:
*   `./data`: Stores any data generated by or used by the application.
*   `ollama-cache`: A named volume that caches the Ollama models, so they don't need to be re-downloaded every time you restart the container.