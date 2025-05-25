# Next Steps - Agent Arena Bot Development

## Phase 1: Environment Setup (Current)

### 1. Create Test Wallet
```bash
btcli wallet new_coldkey --wallet.name arena_test_wallet
btcli wallet new_hotkey --wallet.name arena_test_wallet --wallet.hotkey arena_test_hotkey
```

### 2. Get Test TAO
- Visit testnet faucet for subnet 249
- Need TAO for registration and operations

### 3. Create Twitter Account
- Username: @AITechNewsBot or similar
- Bio: "🤖 AI Tech News & Research | Powered by Bittensor | Breaking papers & insights daily"
- Profile pic: AI-themed avatar

### 4. Post Verification Tweet
```
🤖 Agent Arena Bot | Hotkey: 5YourHotkeyAddressHere...
```
- Copy tweet ID from URL for registration

---

## Phase 2: Local LLM Setup

### 1. Choose Local Model
Options:
- Ollama with Llama 3/Mistral
- LocalAI with various models
- Text-generation-webui
- vLLM for production speed

### 2. Modify content_generator.py
- Replace OpenAI calls with local model API
- Adjust prompts for chosen model
- Test generation quality

### 3. Configure Model Endpoint
```python
# In .env
LOCAL_LLM_ENDPOINT=http://localhost:8000
LOCAL_LLM_MODEL=mistral:7b-instruct
```

---

## Phase 3: MCP Server Setup

### 1. Install MCP Servers
```bash
# ArXiv MCP
npm install -g arxiv-mcp-server

# Brave Search MCP  
npm install -g brave-search-mcp

# Twitter MCP
npm install -g twitter-mcp-server
```

### 2. Configure MCP Endpoints
- Set up each server with API keys
- Test connections
- Configure in mcp_integrations.py

---

## Phase 4: Integration & Testing

### 1. Wire Agent into Miner
```python
# In neurons/miner.py
from ai_agent import AITechNewsAgent

# Add to AgentMiner.__init__
self.ai_agent = AITechNewsAgent(config)

# Start in background
asyncio.create_task(self.ai_agent.start())
```

### 2. Configure Environment
```bash
# .env file
NETUID=249  # testnet
SUBTENSOR_NETWORK=test
WALLET_NAME=arena_test_wallet
HOTKEY_NAME=arena_test_hotkey
TWEET_VERIFICATION_ID=your_tweet_id

# Twitter API
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
TWITTER_ACCESS_TOKEN=xxx
TWITTER_ACCESS_TOKEN_SECRET=xxx

# Local LLM
LOCAL_LLM_ENDPOINT=http://localhost:8000
LOCAL_LLM_MODEL=your_model

# MCP Servers
ARXIV_MCP_URL=http://localhost:3000
BRAVE_MCP_URL=http://localhost:3001
TWITTER_MCP_URL=http://localhost:3002
```

### 3. Test Components
```bash
# Test miner registration
python scripts/run_miner.py

# Check metagraph
btcli subnet metagraph --netuid 249 --network test

# Monitor logs
docker logs --tail 50 --follow masa_miner_1
```

---

## Phase 5: Content Strategy Testing

### 1. Test Content Types
- Paper summaries from ArXiv
- Breaking news from Brave Search
- Educational threads
- Engagement questions

### 2. Analyze Performance
- Track engagement metrics
- A/B test posting times
- Optimize content mix
- Refine prompts

### 3. Iterate Strategy
- What gets most likes?
- Which topics trend?
- Best posting frequency?
- Optimal thread length?

---

## Phase 6: Production Deployment

### 1. Mainnet Preparation
- Create production wallet
- Get real TAO
- Create professional Twitter account
- Thorough testing

### 2. Deploy to Subnet 59
```bash
NETUID=59
SUBTENSOR_NETWORK=finney
```

### 3. Monitor & Optimize
- Daily performance tracking
- Content strategy updates
- Engagement analysis
- Continuous improvement

---

## Quick Command Reference

```bash
# Run tests
make run-tests

# Start miner
python scripts/run_miner.py

# Check registration
btcli subnet metagraph --netuid 249 --network test

# View logs
tail -f logs/miner.log
```