# 📊 YouTube Channel Analyzer

A data-driven YouTube analytics tool that provides 7 actionable insights based on real YouTube API data.

![YouTube Analyzer](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

Analyzes any YouTube channel and generates a beautiful report with:

1. **Performance Gap** - Top 20% vs bottom 20% comparison
2. **Title Length Analysis** - Optimal character/word count
3. **Title Patterns** - What works (questions, colons, numbers)
4. **Duration Sweet Spot** - Best video length (with min sample size)
5. **Engagement Metrics** - Like rate, comment rate analysis
6. **Best Performing Day** - When to post for maximum views
7. **Most Consistent Day** - Your posting patterns
8. **Top Keywords** - Words that drive performance

## 🎯 Why This Tool?

- ✅ **Data-driven** - Based on actual YouTube API data
- ✅ **Statistically valid** - Minimum sample size requirements
- ✅ **Beautiful reports** - Clean, professional HTML output
- ✅ **Fast** - Analyzes 200 videos in ~15 seconds
- ✅ **No BS** - No transcript analysis, no AI guessing

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- YouTube Data API v3 key ([get one here](https://console.cloud.google.com/apis/credentials))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/youtube-analyzer.git
cd youtube-analyzer

# Install dependencies
pip install -r requirements.txt

# Copy config example and add your API key
cp config.example.py config.py
# Edit config.py and add your YouTube API key
```

### 3. Run
```bash
python3 app.py
```

Then open `http://localhost:8080` in your browser!

## 📸 Screenshots

[Add screenshots here]

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **YouTube API**: Google API Client
- **Frontend**: Pure HTML/CSS/JavaScript
- **Analysis**: Pure Python (no ML/AI required)

## 📊 Sample Analysis

The tool analyzes:
- Up to 200 most recent videos
- Separates Shorts (≤60s) from Videos (>60s)
- Calculates views per day, engagement rates
- Identifies patterns in titles, publishing, duration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use for personal or commercial projects!

## ⚠️ API Quota

YouTube Data API has a quota of 10,000 units/day:
- Analyzing 200 videos uses ~203 units
- You can analyze ~50 channels per day

## 🙏 Credits

Created by [Your Name]

Inspired by data-driven YouTube analysis methodologies.

---

**⭐ Star this repo if you found it useful!**
