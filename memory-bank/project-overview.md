# Agent Arena AI Tech News Bot - Project Overview

## Mission
Build an AI-powered Twitter bot that posts engaging tech news content and competes for engagement on Bittensor's Agent Arena (SN59).

## Bot Personality
- **Niche**: AI Tech News Expert
- **Focus**: Breaking AI news, paper summaries, industry insights
- **Style**: Educational yet engaging, thought-provoking
- **Target**: AI researchers, developers, enthusiasts

## Technical Architecture

### Core Components (neurons/ai_agent/)
1. **agent.py** - Main orchestrator, posting loop
2. **content_generator.py** - LLM integration (using local model)
3. **twitter_client.py** - Twitter API wrapper
4. **mcp_integrations.py** - Content sources (ArXiv, Brave, Twitter)
5. **strategies/** - Content formatting strategies

### Key Features
- Automated content generation using local LLM
- Multiple content types (papers, news, threads, questions)
- Engagement optimization strategies
- MCP server integration for real-time content
- Smart posting schedule (peak hours focus)

## Scoring Formula
**Score = Average Engagement × Log(Post Count)**
- Likes: 2.0x weight (most important!)
- Retweets: 1.5x weight
- Replies: 1.0x weight  
- Views: 0.1x weight (barely matters)

## Development Environment
- **Test Subnet**: 249 (testnet)
- **Main Subnet**: 59 (mainnet)
- **Local Model**: To be configured (instead of OpenAI)
- **MCP Servers**: arxiv-mcp-server, brave-search, twitter-mcp-server

## Project Status
- ✅ Code structure created
- ✅ Core modules implemented
- ⏳ Wallet setup pending
- ⏳ Twitter account creation pending
- ⏳ Local LLM integration pending
- ⏳ MCP server setup pending
- ⏳ Testing on subnet 249 pending