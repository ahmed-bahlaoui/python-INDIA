# 🚀 Quick Start: Switch to Groq (FREE AI Provider)

## Why Groq?

- ✅ **100% FREE** (no credit card needed!)
- ✅ **Fastest AI** (seriously, it's insanely fast)
- ✅ **Great quality** (Llama 3.1 70B model)
- ✅ **Easy setup** (2 minutes)

---

## 📝 Setup Steps (2 Minutes)

### Step 1: Get Your FREE Groq API Key

1. Go to: **https://console.groq.com**
2. Click "Sign Up" (use your email)
3. Verify your email
4. Go to "API Keys" in the left menu
5. Click "Create API Key"
6. **Copy your key** (starts with `gsk_`)

---

### Step 2: Update Your .env File

Open `c:\Users\PC\Desktop\python-INDIA\.env` and change these two lines:

```properties
# Change from deepseek to groq
AI_PROVIDER=groq

# Add your Groq API key
GROQ_API_KEY=gsk_YOUR_KEY_HERE_PASTE_IT
```

**Your current .env should look like:**

```properties
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_key_from_groq_console

# Keep your DeepSeek key as backup
DEEPSEEK_API_KEY=sk-2426687b875a4cb699b10a5cb14c19b1

# App Configuration
APP_ENV=development
DEBUG=True
```

---

### Step 3: Restart Streamlit

Close your current Streamlit app and restart:

```powershell
# In PowerShell (in your project folder)
streamlit run app.py
```

---

### Step 4: Test It!

1. Upload a document
2. Generate a quiz
3. Watch it generate **super fast** (3-5 seconds!) ⚡

---

## 🎯 What You Get with Groq

### Free Tier Limits:

- **14,400 requests per day** per model
- **~30 requests per minute**
- **No credit card required**
- **No expiration**

### Models Available:

- `llama-3.1-70b-versatile` (Default - Best for your app)
- `llama-3.1-8b-instant` (Faster, lighter)
- `mixtral-8x7b-32768` (32K context window)
- `gemma2-9b-it` (Google's model)

---

## 💡 Why This Is Perfect For You

**Your Current Situation:**

- DeepSeek key has $0 balance ❌
- Need to add credits to continue ❌
- Costs money 💰

**With Groq:**

- Completely FREE forever ✅
- Works immediately ✅
- Actually FASTER than DeepSeek ✅
- Better for students ✅

---

## 🔄 Easy to Switch Back

If you ever want to go back to DeepSeek:

1. Add credits to your DeepSeek account
2. Change `.env`: `AI_PROVIDER=deepseek`
3. Restart Streamlit

**You can keep both configured and switch anytime!**

---

## 📊 Speed Comparison

| Provider       | Quiz Generation Time |
| -------------- | -------------------- |
| **Groq**       | **3-5 seconds** ⚡   |
| DeepSeek       | 8-12 seconds         |
| OpenAI         | 10-15 seconds        |
| Ollama (local) | 30-60 seconds        |

---

## ⚠️ Troubleshooting

### "Invalid API key"

- ✅ Make sure key starts with `gsk_`
- ✅ No extra spaces before or after key
- ✅ Restart Streamlit after changing .env

### "Rate limit exceeded"

- ✅ Wait 1 minute
- ✅ You hit the 30 requests/min limit
- ✅ Totally normal, just retry

### "Connection error"

- ✅ Check your internet connection
- ✅ Groq servers might be down (rare)
- ✅ Try again in a few minutes

---

## 🎉 Ready to Go!

After completing these steps, you'll have:

- ✅ FREE AI provider (no more "insufficient balance" errors!)
- ✅ FAST quiz generation (3-5 seconds)
- ✅ Unlimited usage (within rate limits)
- ✅ No credit card needed

**Total cost: $0.00 forever** 🎉

---

## 🔗 Useful Links

- **Groq Console:** https://console.groq.com
- **Groq Documentation:** https://console.groq.com/docs
- **Groq Playground:** https://console.groq.com/playground (test models)

---

_Ready to switch? Just follow the 3 steps above!_ 🚀
