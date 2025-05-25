# Local LLM Setup Guide

## Option 1: Ollama (Recommended for Simplicity)

### Installation
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull mistral:7b-instruct-q4_K_M  # Good balance of speed/quality
# or
ollama pull llama3:8b-instruct-q4_K_M   # Better quality, slower
```

### Running
```bash
# Start Ollama server (runs on http://localhost:11434)
ollama serve

# Test the model
curl http://localhost:11434/api/generate -d '{
  "model": "mistral:7b-instruct-q4_K_M",
  "prompt": "Create a viral tweet about AI"
}'
```

### Integration Code
```python
# Modified content_generator.py for Ollama
import aiohttp
import json

async def _generate_with_llm(self, prompt: str) -> Optional[str]:
    """Generate content using Ollama."""
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": self.config.get('model', 'mistral:7b-instruct-q4_K_M'),
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "max_tokens": 100
                }
            }
            
            async with session.post(
                f"{self.config.get('endpoint', 'http://localhost:11434')}/api/generate",
                json=payload
            ) as response:
                result = await response.json()
                return result.get('response', '').strip()
                
    except Exception as e:
        logger.error(f"LLM generation error: {e}")
        return None
```

---

## Option 2: LocalAI (OpenAI Compatible)

### Installation
```bash
# Download LocalAI
wget https://github.com/mudler/LocalAI/releases/latest/download/local-ai-Linux-x86_64
chmod +x local-ai-Linux-x86_64

# Download a model
mkdir models
cd models
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

### Running
```bash
# Start LocalAI (OpenAI compatible API on :8080)
./local-ai-Linux-x86_64 --models-path ./models --address :8080
```

### Integration Code
```python
# Can use existing OpenAI code, just change endpoint
openai.api_base = "http://localhost:8080/v1"
openai.api_key = "not-needed"  # LocalAI doesn't need key
```

---

## Option 3: Text Generation WebUI

### Installation
```bash
# Clone the repository
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui

# Install
bash start_linux.sh
```

### API Setup
```bash
# Start with API
python server.py --api --model mistral-7b-instruct
```

### Integration Code
```python
# WebUI API integration
async def _generate_with_llm(self, prompt: str) -> Optional[str]:
    url = "http://localhost:5000/api/v1/generate"
    payload = {
        "prompt": prompt,
        "max_new_tokens": 100,
        "temperature": self.temperature,
        "do_sample": True
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            result = await response.json()
            return result['results'][0]['text'].strip()
```

---

## Model Recommendations

### For Speed (Posts/minute matters)
1. **mistral:7b-instruct-q4_K_M** - Fast, good quality
2. **phi-2** - Very fast, decent for short content
3. **llama3:8b-instruct-q4_0** - Good balance

### For Quality (Engagement matters more)
1. **llama3:8b-instruct-q5_K_M** - Best overall
2. **mixtral:8x7b-instruct** - Excellent but slow
3. **mistral:7b-instruct-v0.2-q6_K** - High quality

### Prompt Optimization Tips
```python
# Optimized system prompt for local models
SYSTEM_PROMPT = """You are a viral Twitter content creator specializing in AI.
Your tweets get massive engagement. Be concise, punchy, and insightful.
Use emojis strategically. Ask questions. Create urgency."""

# Better prompt structure for local models
prompt = f"{SYSTEM_PROMPT}\n\nTask: {specific_instruction}\n\nTweet:"
```

---

## Performance Tuning

### 1. GPU Acceleration
```bash
# Check CUDA availability
nvidia-smi

# Ollama will auto-detect GPU
# For other tools, may need to set:
export CUDA_VISIBLE_DEVICES=0
```

### 2. Quantization Levels
- **Q4_K_M**: Best balance (4-bit)
- **Q5_K_M**: Higher quality (5-bit)
- **Q8_0**: Near full quality (8-bit)
- **F16**: Full quality (16-bit)

### 3. Context Window
- Keep prompts under 1000 tokens
- Most tweets need < 500 token context
- Batch similar requests

### 4. Caching Strategy
```python
# Simple cache for common patterns
class ContentCache:
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl
        
    async def get_or_generate(self, key, generator_func):
        if key in self.cache:
            content, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return content
        
        content = await generator_func()
        self.cache[key] = (content, time.time())
        return content
```