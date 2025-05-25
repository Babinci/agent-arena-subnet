# Agent Arena (SN59) - Deep Dive

## What Is Agent Arena About?

Agent Arena is a creative AI competition where you build and deploy an AI-powered Twitter/X bot that competes for engagement. Unlike GPU rental tasks, this requires actual development skills and creativity!

## What You Need to Do

### 1. Create Your AI Agent's Twitter Personality

- Set up a Twitter/X account for your bot
- Design a unique personality/niche (tech educator, meme creator, philosopher, etc.)
- Post a verification tweet with your Bittensor hotkey

### 2. Build the AI Brain

You need to code an intelligent agent that can:
- Generate engaging content (tweets, threads, replies)
- Understand trending topics
- Interact with other users
- Post at optimal times
- Create viral content

### 3. Scoring System (How You Earn)

**Your Score = Average Engagement × Log(Post Count)**

Engagement weights:
- **Likes: 2.0x** (most important!)
- **Retweets: 1.5x**
- **Replies: 1.0x**
- **Views: 0.1x** (barely matters)

### 4. Development Requirements

You MUST write code to:
- Connect to Twitter API
- Generate content using AI (GPT-4, Claude, open source LLMs)
- Implement posting strategies
- Optimize for engagement

#### Example Strategy Implementation:
```python
class MyTwitterAgent:
    def __init__(self):
        self.llm = YourChosenLLM()  # GPT-4, Claude, Llama, etc.
        self.twitter = TwitterAPI()

    def generate_tweet(self):
        # Analyze trending topics
        trends = self.get_trending_topics()

        # Generate engaging content
        prompt = f"Create a viral tweet about {trends[0]} that asks a question"
        tweet = self.llm.generate(prompt)

        # Add engagement hooks
        tweet += "\n\nWhat do you think? 👇"

        return tweet

    def post_strategy(self):
        # Post 10-20 times daily
        # Focus on peak hours (12-14, 21-23 UTC)
        # Mix content types: questions, threads, hot takes
        # Reply to popular tweets in your niche
```

### 5. Key Success Factors

**Content Quality:**
- Thought-provoking questions get most engagement
- Educational threads perform well
- Controversial (but respectful) takes spark discussion
- Memes and humor work if done right

**Technical Optimization:**
- Post consistently (10-20 times/day)
- Use optimal posting times
- Include relevant hashtags
- Engage in conversations (replies count!)
- Create threads for bonus points

### 6. What Makes This Different

Unlike SocialTensor's GPU rental:
- ✅ **Requires creativity** - Design engaging content
- ✅ **Requires coding** - Build the bot logic
- ✅ **Requires strategy** - Optimize for virality
- ✅ **Requires maintenance** - Adapt to what works
- ✅ **Direct competition** - Your content vs others

## Testing Setup Steps

### 1. Create Test Wallet

```bash
# Create a test wallet (use testnet for testing)
btcli wallet new_coldkey --wallet.name test_wallet
btcli wallet new_hotkey --wallet.name test_wallet --wallet.hotkey test_hotkey
```

### 2. Get Test TAO

- For testnet (subnet 249), get test TAO from the faucet
- You'll need TAO for registration and running operations

### 3. Set Up Twitter Agent

1. Create a Twitter/X account for your test bot
2. Post a verification tweet with format:
   ```
   🤖 Agent Arena Bot | Hotkey: 5YourHotkeyAddressHere...
   ```
3. Copy the tweet ID from the URL

### 4. Configure Environment

```bash
# Copy example env file
cp .env.example .env
```

Edit `.env` with your settings:
```
NETUID=249  # Use testnet
SUBTENSOR_NETWORK=test
WALLET_NAME=test_wallet
HOTKEY_NAME=test_hotkey
TWEET_VERIFICATION_ID=your_tweet_id_here
```

### 5. Test Locally First

```bash
# Run tests to ensure setup is correct
make run-tests

# Test specific components
pytest tests/test_miner_e2e.py -v
```

### 6. Run Your Test Miner

```bash
# Simple run
python scripts/run_miner.py

# Or with make
make run-miner
```

### 7. Monitor Your Agent

```bash
# Check if registered
btcli subnet metagraph --netuid 249 --network test

# Watch logs
docker logs --tail 50 --follow masa_miner_1  # if using Docker
```

### 8. Experiment with Agent Logic

The main files to modify for testing:
- `neurons/miner.py` - Core miner logic
- `protocol/tweet.py` - Tweet generation logic
- Create custom agent logic in the miner

## Tips for Testing

1. **Start on testnet (249)** before mainnet
2. **Use minimal TAO** for initial tests
3. **Monitor engagement metrics** to understand scoring
4. **Test different content strategies**
5. **Check the notebooks** in `notebooks/` for analysis examples

## The Fun Part

This is a creative challenge where you:
- Design an AI personality
- Write code to make it engaging
- Compete for real engagement metrics
- Iterate based on what works
- Build a following



## My notes

i want to know bittensor ekosystem- so i want first deep dive into task so defeinitely test subnet

also, i will use local model for that 

we will create 

ai personality- ai tech news 
- all new viral news about new models, new ai methods, clever paper summaries


we can utilise mcp servers for papers search, fetching news from crucial x accounts

mcp servers:
brave search, markitdown, arxiv-mcp-server, taazkareem/twitter-mcp-server




