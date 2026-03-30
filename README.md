# 📊 YouTube Channel Analyzer

Clean, simple YouTube analytics tool built with Flask.

## 🚀 Quick Setup

### 1. Get API Keys

**YouTube Data API v3:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create credentials → API Key
5. Copy your API key

**OpenAI API:**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create new secret key
3. Copy your API key (starts with `sk-`)

### 2. Deploy to Render

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Create Render Service:**
   - Go to [Render.com](https://render.com/)
   - New → Web Service
   - Connect your GitHub repository
   - Settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:application`

3. **Add Environment Variables:**
   - Go to Environment tab
   - Add:
     - `YOUTUBE_API_KEY` = your YouTube API key
     - `OPENAI_API_KEY` = your OpenAI API key

### 3. Test It!

Visit your Render URL and analyze any YouTube channel!

## 📁 Project Structure

```
youtube-analyzer/
├── app.py                    # Main Flask application
├── youtube_analyzer.py       # YouTube API & analysis logic
├── report_generator.py       # HTML report generation
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Web interface
└── reports/                 # Generated reports (auto-created)
```

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export YOUTUBE_API_KEY="your_key"
export OPENAI_API_KEY="your_key"

# Run
python app.py
```

Visit http://localhost:8080

## 📝 Features

- ✅ Clean, simple codebase
- ✅ Detailed debug logging
- ✅ Performance gap analysis
- ✅ Title length analysis
- ✅ Duration analysis
- ✅ Top 10 videos
- ✅ Beautiful HTML reports

## 🐛 Troubleshooting

Check Render logs for detailed output. Every step is logged with emojis for easy reading:

- 🔍 = Starting analysis
- ✓ = Success
- ❌ = Error
- 📦 = Importing
- 🔧 = Initializing
- 📹 = Fetching videos
- 📊 = Analyzing
- 📄 = Generating report

If you see an error, the logs will show exactly which step failed!