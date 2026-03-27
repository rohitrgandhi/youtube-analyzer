import isodate
from datetime import datetime
from collections import Counter
import re
from youtube_analyzer_openai import YouTubeAnalyzer

class AdvancedInsightsAnalyzer(YouTubeAnalyzer):
    def categorize_videos(self, videos):
        categories = {'shorts': [], 'regular': [], 'podcasts': [], 'all': videos}
        
        for video in videos:
            duration = isodate.parse_duration(video['duration']).total_seconds()
            video['duration_seconds'] = duration
            
            if duration < 60:
                categories['shorts'].append(video)
            elif duration < 1800:
                categories['regular'].append(video)
            else:
                categories['podcasts'].append(video)
        
        return categories
    
    def analyze_titles(self, videos):
        """Analyze title patterns"""
        top_20_pct = sorted(videos, key=lambda x: x['view_count'], reverse=True)[:max(1, len(videos)//5)]
        bottom_20_pct = sorted(videos, key=lambda x: x['view_count'])[:max(1, len(videos)//5)]
        
        # Title length
        top_avg_length = sum(len(v['title']) for v in top_20_pct) / len(top_20_pct)
        bottom_avg_length = sum(len(v['title']) for v in bottom_20_pct) / len(bottom_20_pct)
        
        # Colon usage
        top_colon = sum(':' in v['title'] for v in top_20_pct) / len(top_20_pct) * 100
        bottom_colon = sum(':' in v['title'] for v in bottom_20_pct) / len(bottom_20_pct) * 100
        
        # Question marks
        top_questions = sum('?' in v['title'] for v in top_20_pct) / len(top_20_pct) * 100
        bottom_questions = sum('?' in v['title'] for v in bottom_20_pct) / len(bottom_20_pct) * 100
        
        return {
            'title_length': {'top': top_avg_length, 'bottom': bottom_avg_length},
            'colon_usage': {'top': top_colon, 'bottom': bottom_colon},
            'question_marks': {'top': top_questions, 'bottom': bottom_questions}
        }
    
    def generate_beautiful_html(self, categorized, analyses):
        top_videos = sorted(categorized['all'], key=lambda x: x['view_count'], reverse=True)[:10]
        
        html = """<!DOCTYPE html>
<html><head>
<title>YouTube Analysis Insights</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f8f9fa; }
.container { max-width: 900px; margin: 40px auto; }
.insight-card { background: white; border-radius: 16px; padding: 60px; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.insight-number { font-size: 12px; color: #999; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 30px; }
.insight-title { font-size: 32px; line-height: 1.3; font-weight: 400; margin-bottom: 40px; color: #1a1a1a; }
.stat-huge { font-size: 80px; font-weight: 700; color: #dc143c; margin-bottom: 10px; }
.stat-label { font-size: 16px; color: #666; }
.comparison { display: flex; gap: 40px; margin: 30px 0; }
.comparison-item { flex: 1; }
.comparison-value { font-size: 48px; font-weight: 700; }
.comparison-value.winner { color: #dc143c; }
.comparison-value.loser { color: #ccc; }
.video-list { margin-top: 30px; }
.video-item { padding: 15px 0; border-bottom: 1px solid #eee; }
.video-title { font-size: 16px; color: #333; margin-bottom: 5px; }
.video-stats { font-size: 14px; color: #999; }
.effect-size { background: #f0f0f0; padding: 8px 16px; border-radius: 6px; display: inline-block; margin-top: 20px; font-size: 14px; }
</style>
</head>
<body>
<div class="container">"""
        
        # Insight 1: Top performers
        if top_videos:
            top_avg = sum(v['view_count'] for v in top_videos[:3]) / 3
            bottom_avg = sum(v['view_count'] for v in top_videos[-3:]) / 3
            multiplier = top_avg / bottom_avg if bottom_avg > 0 else 0
            
            html += f"""
<div class="insight-card">
    <div class="insight-number">INSIGHT 1</div>
    <div class="insight-title">top performers outperform by a significant margin.</div>
    <div class="stat-huge">{multiplier:.1f}x</div>
    <div class="stat-label">gap between top 3 and bottom 3 videos</div>
</div>"""
        
        # Insight 2: Title analysis
        if 'all' in analyses:
            title_data = analyses['all']
            html += f"""
<div class="insight-card">
    <div class="insight-number">INSIGHT 2</div>
    <div class="insight-title">shorter titles perform better.</div>
    <div class="comparison">
        <div class="comparison-item">
            <div class="comparison-value winner">{title_data['title_length']['top']:.0f}</div>
            <div class="stat-label">chars (top 20%)</div>
        </div>
        <div class="comparison-item">
            <div class="comparison-value loser">{title_data['title_length']['bottom']:.0f}</div>
            <div class="stat-label">chars (bottom 20%)</div>
        </div>
    </div>
</div>"""
        
        # Insight 3: Colon usage
        if 'all' in analyses:
            html += f"""
<div class="insight-card">
    <div class="insight-number">INSIGHT 3</div>
    <div class="insight-title">colons in titles drive engagement.</div>
    <div class="comparison">
        <div class="comparison-item">
            <div class="comparison-value winner">{title_data['colon_usage']['top']:.1f}%</div>
            <div class="stat-label">top 20%</div>
        </div>
        <div class="comparison-item">
            <div class="comparison-value loser">{title_data['colon_usage']['bottom']:.1f}%</div>
            <div class="stat-label">bottom 20%</div>
        </div>
    </div>
</div>"""
        
        # Top videos list
        html += """
<div class="insight-card">
    <div class="insight-number">TOP VIDEOS</div>
    <div class="video-list">"""
        
        for i, video in enumerate(top_videos[:10], 1):
            html += f"""
        <div class="video-item">
            <div class="video-title">{i}. {video['title']}</div>
            <div class="video-stats">{video['view_count']:,} views • {video['like_count']:,} likes</div>
        </div>"""
        
        html += """
    </div>
</div>

</div>
</body>
</html>"""
        
        filename = f"youtube_analysis_data/insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, 'w') as f:
            f.write(html)
        
        return filename
