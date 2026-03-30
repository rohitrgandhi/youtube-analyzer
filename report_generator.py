import os
from datetime import datetime

def generate_report(videos, analysis, channel_name):
    """Generate HTML report"""
    
    os.makedirs('reports', exist_ok=True)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{channel_name} - YouTube Analysis</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .card {{ background: white; border-radius: 12px; padding: 40px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ font-size: 32px; margin-bottom: 10px; color: #1a1a1a; }}
        .subtitle {{ color: #666; font-size: 16px; margin-bottom: 30px; }}
        .stat-big {{ font-size: 64px; font-weight: bold; color: #dc143c; line-height: 1; }}
        .stat-label {{ font-size: 14px; color: #666; margin-top: 8px; }}
        .comparison {{ display: flex; gap: 40px; margin: 30px 0; }}
        .comp-item {{ flex: 1; }}
        .comp-value {{ font-size: 48px; font-weight: bold; }}
        .comp-value.win {{ color: #dc143c; }}
        .comp-value.lose {{ color: #ddd; }}
        .video-list {{ margin-top: 20px; }}
        .video-item {{ padding: 15px 0; border-bottom: 1px solid #f0f0f0; }}
        .video-title {{ font-weight: 600; margin-bottom: 5px; }}
        .video-stats {{ font-size: 14px; color: #999; }}
        .insight-num {{ font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 20px; }}
        .insight-title {{ font-size: 24px; margin-bottom: 30px; line-height: 1.4; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>📊 {channel_name}</h1>
            <div class="subtitle">Analysis of {analysis['total_videos']} videos</div>
        </div>
        
        <div class="card">
            <div class="insight-num">INSIGHT 1</div>
            <div class="insight-title">Top performers significantly outperform the rest</div>
            <div class="stat-big">{analysis['performance_gap']:.1f}x</div>
            <div class="stat-label">Performance gap between top 20% and bottom 20%</div>
            <div style="margin-top: 20px; font-size: 14px; color: #666;">
                Top 20% avg: {analysis['top_avg_vpd']:,.0f} views/day<br>
                Bottom 20% avg: {analysis['bottom_avg_vpd']:,.0f} views/day
            </div>
        </div>
        
        <div class="card">
            <div class="insight-num">INSIGHT 2</div>
            <div class="insight-title">{'Shorter' if analysis['top_title_length'] < analysis['bottom_title_length'] else 'Longer'} titles perform better</div>
            <div class="comparison">
                <div class="comp-item">
                    <div class="comp-value {'win' if analysis['top_title_length'] < analysis['bottom_title_length'] else 'lose'}">{analysis['top_title_length']:.0f}</div>
                    <div class="stat-label">chars (top 20%)</div>
                </div>
                <div class="comp-item">
                    <div class="comp-value {'win' if analysis['top_title_length'] >= analysis['bottom_title_length'] else 'lose'}">{analysis['bottom_title_length']:.0f}</div>
                    <div class="stat-label">chars (bottom 20%)</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="insight-num">INSIGHT 3</div>
            <div class="insight-title">Duration performance breakdown</div>
"""
    
    for bucket, vpd in sorted(analysis['duration_stats'].items(), key=lambda x: x[1], reverse=True):
        html += f"""
            <div style="margin-bottom: 15px;">
                <div style="font-weight: 600;">{bucket}</div>
                <div style="color: #666; font-size: 14px;">{vpd:,.0f} views/day average</div>
            </div>
"""
    
    html += """
        </div>
        
        <div class="card">
            <div class="insight-num">TOP 10 VIDEOS</div>
            <div class="video-list">
"""
    
    for i, video in enumerate(analysis['top_videos'][:10], 1):
        html += f"""
                <div class="video-item">
                    <div class="video-title">{i}. {video['title']}</div>
                    <div class="video-stats">{video['views']:,} views • {video['views_per_day']:,.0f} views/day • {video['duration_minutes']:.1f} min</div>
                </div>
"""
    
    html += """
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    filename = f"reports/{channel_name.replace('@', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filename