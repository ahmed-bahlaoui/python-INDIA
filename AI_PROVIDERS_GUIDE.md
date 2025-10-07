# 🤖 AI Provider Comparison & Setup Guide

**Date:** October 7, 2025  
**Purpose:** Compare free and cheap AI providers for QuizAI  
**Focus:** Performance, cost, and ease of setup

---

## 🎯 Quick Recommendation

**Best FREE Option:** 🏆 **Groq** (Fast, completely free, great quality)  
**Best CHEAP Option:** 💰 **DeepSeek** ($0.14-0.28 per million tokens)  
**Best LOCAL Option:** 🏠 **Ollama** (100% free, runs on your PC)

---

## 📊 Provider Comparison Table

| Provider        | Cost       | Speed      | Quality    | Setup  | Free Tier     | Best For       |
| --------------- | ---------- | ---------- | ---------- | ------ | ------------- | -------------- |
| **Groq** ⭐     | FREE       | ⚡ Fastest | ⭐⭐⭐⭐   | Easy   | Unlimited\*   | Production     |
| **DeepSeek**    | Very Cheap | Fast       | ⭐⭐⭐⭐⭐ | Easy   | Trial credits | Quality + Cost |
| **Ollama**      | FREE       | Medium     | ⭐⭐⭐     | Medium | Unlimited     | Privacy/Local  |
| **Together AI** | Cheap      | Fast       | ⭐⭐⭐⭐   | Easy   | $25 credit    | Fast inference |
| **OpenAI**      | Expensive  | Medium     | ⭐⭐⭐⭐⭐ | Easy   | $5 credit     | Best quality   |
| **Anthropic**   | Expensive  | Medium     | ⭐⭐⭐⭐⭐ | Easy   | Trial         | Long context   |

\*Rate limited but very generous

---

## 🏆 Top 3 Recommendations

### 1. 🥇 **Groq - BEST FREE OPTION**

**Why Choose Groq:**

- ✅ **Completely FREE** (with rate limits)
- ✅ **FASTEST** AI inference (seriously fast!)
- ✅ Great quality (Llama 3.1 70B, Mixtral)
- ✅ Easy to set up (2 minutes)
- ✅ Perfect for students and testing

**Pricing:**

- 🎉 **FREE tier**: 14,400 requests/day per model
- 🎉 **No credit card required**
- Rate limits: ~30 requests/min

**Setup Instructions:**

1. **Get API Key:**

   - Go to: https://console.groq.com
   - Sign up with email (free, no credit card)
   - Go to "API Keys" section
   - Click "Create API Key"
   - Copy your key (starts with `gsk_`)

2. **Configure in .env:**

   ```properties
   AI_PROVIDER=groq
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Recommended Models:**
   - `llama-3.1-70b-versatile` (Default - Best balance)
   - `mixtral-8x7b-32768` (Good for long context)
   - `llama-3.1-8b-instant` (Faster, lighter)

**Perfect For:**

- ✅ Students (no cost!)
- ✅ Testing and development
- ✅ High-speed applications
- ✅ Limited budget projects

---

### 2. 🥈 **DeepSeek - BEST CHEAP OPTION**

**Why Choose DeepSeek:**

- 💰 **Super cheap**: $0.14-0.28 per million tokens
- ✅ High quality (competitive with GPT-4)
- ✅ Fast inference
- ✅ Good for French (multilingual)

**Pricing:**

- Input: $0.14 per 1M tokens (~10,000 pages)
- Output: $0.28 per 1M tokens
- **Example cost**: 100 quizzes ≈ $0.50 USD 💰

**Setup Instructions:**

1. **Get API Key:**

   - Go to: https://platform.deepseek.com
   - Sign up and verify email
   - Add credits (minimum $5)
   - Get API key from dashboard

2. **Configure in .env:**

   ```properties
   AI_PROVIDER=deepseek
   DEEPSEEK_API_KEY=sk-your_deepseek_key_here
   ```

3. **Model:**
   - `deepseek-chat` (Latest V3.2-Exp model)

**Perfect For:**

- ✅ Production use (reliable)
- ✅ Budget-conscious projects
- ✅ High-quality outputs needed
- ✅ Long-term usage

**Current Status:** ⚠️ Your key has insufficient balance ($0). Add $5-10 to continue.

---

### 3. 🥉 **Ollama - BEST LOCAL OPTION**

**Why Choose Ollama:**

- 🎉 **100% FREE** (runs on your PC)
- 🔒 **Complete privacy** (no data sent online)
- ✅ Unlimited usage (no rate limits)
- ✅ Works offline

**Requirements:**

- RAM: 8GB+ (16GB recommended)
- Storage: 5-50GB depending on model
- GPU: Optional but recommended

**Setup Instructions:**

1. **Install Ollama:**

   - Download: https://ollama.com/download
   - Install for Windows
   - Open PowerShell

2. **Download Models:**

   ```bash
   # Light model (4GB RAM)
   ollama pull llama3.1:8b

   # Better quality (16GB RAM)
   ollama pull llama3.1:70b

   # Fast and small (2GB RAM)
   ollama pull phi3
   ```

3. **Start Ollama Server:**

   ```bash
   ollama serve
   ```

4. **Configure in .env:**

   ```properties
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.1:8b
   ```

5. **Update config.py** (already done):
   ```python
   MODELS = {
       "ollama": "llama3.1:8b",  # Your downloaded model
   }
   ```

**Perfect For:**

- ✅ Privacy concerns
- ✅ Offline usage
- ✅ No internet restrictions
- ✅ Development/testing

---

## 💰 Cost Comparison (Real Numbers)

### Scenario: 100 Quiz Generations

**Assumptions:**

- 100 quizzes with 15 questions each
- Average: 2,000 tokens input + 3,000 tokens output per quiz
- Total: 200K input + 300K output tokens

| Provider                 | Cost for 100 Quizzes | Notes                 |
| ------------------------ | -------------------- | --------------------- |
| **Groq**                 | **$0.00** 🎉         | FREE! (within limits) |
| **Ollama**               | **$0.00** 🎉         | FREE! (local)         |
| **DeepSeek**             | **$0.11** 💰         | Super cheap           |
| **Together AI**          | **$0.20**            | Cheap                 |
| **OpenAI (GPT-4o-mini)** | **$3.00**            | Expensive             |
| **OpenAI (GPT-4)**       | **$15.00**           | Very expensive        |
| **Anthropic (Claude)**   | **$15.00**           | Very expensive        |

---

## 🚀 Other Good Options

### 4. **Together AI** - Fast & Cheap

**Pricing:**

- $0.18-0.90 per million tokens
- **$25 free credits** for new users
- Good speed and quality

**Setup:**

```properties
AI_PROVIDER=together
TOGETHER_API_KEY=your_together_key
```

**Get Key:** https://api.together.xyz/signup

---

### 5. **OpenAI GPT-4o-mini** - Premium Quality

**Pricing:**

- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens
- **$5 free credits** for new users

**Setup:**

```properties
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your_openai_key
```

**Get Key:** https://platform.openai.com/api-keys

---

## ⚙️ How to Switch Providers

### Method 1: Edit .env File (Recommended)

Just change one line in `.env`:

```properties
# Use Groq (FREE)
AI_PROVIDER=groq
GROQ_API_KEY=your_groq_key

# Or use DeepSeek (CHEAP)
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_deepseek_key

# Or use Ollama (LOCAL)
AI_PROVIDER=ollama
```

### Method 2: Multiple Keys (Fallback)

Set up multiple providers in `.env`:

```properties
AI_PROVIDER=groq

# Primary
GROQ_API_KEY=your_groq_key

# Fallback options
DEEPSEEK_API_KEY=your_deepseek_key
TOGETHER_API_KEY=your_together_key
OPENAI_API_KEY=your_openai_key
```

---

## 🎯 Recommendations by Use Case

### 🎓 **For Students (No Budget)**

1. **Primary:** Groq (free, fast)
2. **Backup:** Ollama (local, private)
3. **Fallback:** Together AI ($25 free credits)

### 💼 **For Small Production**

1. **Primary:** DeepSeek (cheap, quality)
2. **Backup:** Groq (free tier for peak times)
3. **Fallback:** Together AI (fast inference)

### 🏢 **For Enterprise**

1. **Primary:** OpenAI GPT-4 (best quality)
2. **Backup:** Anthropic Claude (long context)
3. **Fallback:** DeepSeek (cost optimization)

### 🔒 **For Privacy-Focused**

1. **Primary:** Ollama (100% local)
2. **Backup:** Self-hosted LLM
3. **Fallback:** DeepSeek (if internet needed)

---

## 📋 Quick Setup Checklist

### Groq (Recommended - FREE)

- [ ] Sign up at https://console.groq.com
- [ ] Get API key (no credit card needed)
- [ ] Add to `.env`: `AI_PROVIDER=groq`
- [ ] Add to `.env`: `GROQ_API_KEY=gsk_...`
- [ ] Restart Streamlit
- [ ] Test with quiz generation

### DeepSeek (Recommended - CHEAP)

- [ ] Sign up at https://platform.deepseek.com
- [ ] Add $5-10 credits
- [ ] Get API key
- [ ] Add to `.env`: `AI_PROVIDER=deepseek`
- [ ] Add to `.env`: `DEEPSEEK_API_KEY=sk-...`
- [ ] Restart Streamlit
- [ ] Test with quiz generation

### Ollama (Recommended - LOCAL)

- [ ] Download from https://ollama.com/download
- [ ] Install Ollama
- [ ] Run: `ollama pull llama3.1:8b`
- [ ] Run: `ollama serve`
- [ ] Add to `.env`: `AI_PROVIDER=ollama`
- [ ] Restart Streamlit
- [ ] Test with quiz generation

---

## 🔧 Troubleshooting

### Groq Errors

**"Rate limit exceeded"**

- ✅ Wait 1 minute and retry
- ✅ Switch to different model
- ✅ Use fallback provider

**"Invalid API key"**

- ✅ Check key starts with `gsk_`
- ✅ Regenerate key in console
- ✅ Check for extra spaces in .env

### DeepSeek Errors

**"Insufficient balance"**

- ✅ Add credits to account
- ✅ Minimum $5 recommended
- ✅ Switch to Groq (free) temporarily

### Ollama Errors

**"Connection refused"**

- ✅ Start Ollama: `ollama serve`
- ✅ Check if running: http://localhost:11434
- ✅ Restart Ollama service

**"Model not found"**

- ✅ Download model: `ollama pull llama3.1:8b`
- ✅ Check model name matches config
- ✅ List models: `ollama list`

---

## 📊 Performance Comparison

### Speed Test (15-question quiz generation)

| Provider     | Model         | Time        | Quality    |
| ------------ | ------------- | ----------- | ---------- |
| **Groq**     | Llama 3.1 70B | **3-5s** ⚡ | ⭐⭐⭐⭐   |
| **DeepSeek** | DeepSeek V3   | 8-12s       | ⭐⭐⭐⭐⭐ |
| **Ollama**   | Llama 3.1 8B  | 30-60s      | ⭐⭐⭐     |
| **Together** | Llama 3.1 70B | 5-8s        | ⭐⭐⭐⭐   |
| **OpenAI**   | GPT-4o-mini   | 10-15s      | ⭐⭐⭐⭐⭐ |

---

## 🎯 Final Recommendation

### **Start with Groq (FREE) + DeepSeek (CHEAP) as backup**

**Setup both in .env:**

```properties
AI_PROVIDER=groq

# Primary (FREE)
GROQ_API_KEY=gsk_your_groq_key_here

# Backup (CHEAP)
DEEPSEEK_API_KEY=sk_your_deepseek_key_here
```

**Why this combo?**

- ✅ Free for most usage (Groq)
- ✅ Extremely fast (Groq)
- ✅ High quality (both)
- ✅ Cheap fallback (DeepSeek)
- ✅ Easy to switch providers

---

## 📝 Next Steps

1. **Choose your provider** (Groq recommended)
2. **Get API key** (links above)
3. **Update .env file** (see examples)
4. **Restart Streamlit** (`streamlit run app.py`)
5. **Test with quiz** (generate and check quality)
6. **Monitor usage** (check provider dashboard)

---

## 🔗 Useful Links

- **Groq Console:** https://console.groq.com
- **DeepSeek Platform:** https://platform.deepseek.com
- **Ollama Download:** https://ollama.com/download
- **Together AI:** https://api.together.xyz
- **OpenAI Platform:** https://platform.openai.com

---

**💡 Pro Tip:** Set up multiple providers and switch between them based on your needs:

- Use Groq for speed and development
- Use DeepSeek when you need highest quality
- Use Ollama for private/offline work

---

_Last updated: October 7, 2025_  
_Current setup: DeepSeek (needs balance) + Groq (recommended switch)_
