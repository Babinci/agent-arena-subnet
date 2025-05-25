# Technical Decisions & Rationale

## Architecture Decisions

### 1. Modular Design
**Decision**: Separate concerns into distinct modules
- `agent.py` - Orchestration only
- `content_generator.py` - LLM logic only
- `twitter_client.py` - API interactions only

**Rationale**: Easy to test, maintain, and swap components

### 2. Local LLM vs Cloud
**Decision**: Use local model instead of OpenAI
**Rationale**: 
- Cost efficiency for high volume
- No API rate limits
- Full control over prompts
- Privacy for strategy

### 3. MCP Server Integration
**Decision**: Use MCP servers for content sources
**Rationale**:
- Real-time data access
- Standardized interfaces
- Easy to add new sources
- Battle-tested implementations

### 4. Async Architecture
**Decision**: Full async/await pattern
**Rationale**:
- Non-blocking operations
- Efficient resource usage
- Better concurrency
- Scales with load

## Content Strategy Decisions

### 1. Content Mix (40/30/20/10)
- 40% Paper summaries - High authority
- 30% Breaking news - Timeliness
- 20% Educational threads - Engagement
- 10% Questions - Community building

### 2. Posting Frequency
**Decision**: 15-20 posts/day
**Rationale**: 
- Balances visibility with quality
- Avoids spam classification
- Maintains consistent presence
- Allows content variety

### 3. Peak Hour Focus
**Decision**: 80% posts during peak hours
**Rationale**:
- Maximum initial engagement
- Better algorithmic boost
- Higher audience availability
- Proven engagement windows

## Implementation Priorities

### 1. MVP First
Start with:
- Basic posting functionality
- Single content type (papers)
- Manual monitoring
- Simple scheduling

### 2. Iterate Based on Data
Add features based on performance:
- More content types if engagement good
- Advanced scheduling if timing matters
- Caching if API limits hit
- Analytics if strategy unclear

### 3. Testnet Before Mainnet
**Decision**: Minimum 7 days on testnet
**Rationale**:
- Catch edge cases
- Refine prompts
- Optimize timing
- Build confidence

## Risk Mitigation

### 1. Twitter API Limits
- Implement exponential backoff
- Queue failed posts
- Monitor rate limits
- Have backup content ready

### 2. Content Quality
- Review first 100 posts manually
- Set engagement thresholds
- Emergency stop mechanism
- Sentiment monitoring

### 3. Scoring Algorithm Changes
- Flexible content strategy
- Monitor validator updates
- Quick pivot capability
- Diverse content types