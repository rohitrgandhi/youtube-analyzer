# YouTube Analyzer - Fixed Version

## 📋 Files You Need

Replace these files in your GitHub repository:

1. **app.py** - Main application
2. **requirements.txt** - Python dependencies  
3. **templates/index.html** - Web interface

## 🔑 Environment Variables on Render

Make sure you have BOTH of these set in Render → Environment:

1. `YOUTUBE_API_KEY` = Your YouTube Data API v3 key
2. `OPENAI_API_KEY` = Your OpenAI API key (starts with sk-)

## 🚀 Deployment Steps

### Step 1: Replace Files in Your Project

Copy these files from this fixed version to your local youtube-analyzer folder:
- Replace `app.py`
- Replace `requirements.txt`
- Replace `templates/index.html`

### Step 2: Make Sure You Have These Files

Your project should have:
- app.py ✅
- requirements.txt ✅
- templates/index.html ✅
- clean_analyzer.py ✅ (keep your existing one)
- clean_report.py ✅ (keep your existing one)
- youtube_analyzer_openai.py ✅ (keep your existing one)

### Step 3: Push to GitHub

```bash
git add .
git commit -m "Fix all deployment issues"
git push
```

### Step 4: Check Render Logs

After deployment, the logs should show:
```
==================================================
DEBUG: Starting analysis for @channelname
YouTube API Key exists: True
OpenAI API Key exists: True
==================================================
```

If you see `False` for either key, that key is missing on Render!

## 🐛 Troubleshooting

**Error: "Channel not found"**
- Check that BOTH API keys are set in Render environment variables
- Look at Render logs for the DEBUG output
- Make sure you're using the correct channel handle (with or without @)

**Error: "YouTube API key not configured"**
- Add YOUTUBE_API_KEY to Render environment variables

**Error: "OpenAI API key not configured"**  
- Add OPENAI_API_KEY to Render environment variables

## 📞 Support

If you still have issues, check the Render logs and look for:
1. The DEBUG output showing which keys exist
2. Any Python errors or stack traces
3. The specific error message

The debug logging will tell you EXACTLY what's wrong!