"""
Advanced Report Generator
Creates professional HTML reports with data visualizations
"""

import os
from datetime import datetime

def generate_report(videos, insights, channel_name):
    """Generate professional HTML report"""
    
    # Create reports directory
    os.makedirs('reports', exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"reports/{channel_name.replace('@', '')}_{timestamp}.html"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{channel_name} - YouTube Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 48px;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 18px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 60px 40px;
        }}
        
        .section {{
            margin-bottom: 60px;
        }}
        
        .section-title {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 30px;
            color: #2d3748;
            border-bottom: 4px solid #667eea;
            padding-bottom: 15px;
        }}
        
        .insight-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}
        
        .insight-number {{
            font-size: 72px;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .insight-label {{
            font-size: 20px;
            opacity: 0.9;
        }}
        
        .insight-text {{
            font-size: 18px;
            margin-top: 20px;
            line-height: 1.8;
        }}
        
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}
        
        .stat-box {{
            background: #f7fafc;
            padding: 30px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }}
        
        .stat-value {{
            font-size: 36px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #718096;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .comparison-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: #f7fafc;
            border-radius: 10px;
            margin-bottom: 15px;
        }}
        
        .comparison-label {{
            font-weight: 600;
            color: #2d3748;
        }}
        
        .comparison-values {{
            display: flex;
            gap: 30px;
        }}
        
        .value-top {{
            color: #48bb78;
            font-weight: 700;
            font-size: 20px;
        }}
        
        .value-bottom {{
            color: #f56565;
            font-weight: 700;
            font-size: 20px;
        }}
        
        .bar-chart {{
            margin: 30px 0;
        }}
        
        .bar-item {{
            margin-bottom: 20px;
        }}
        
        .bar-label {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2d3748;
        }}
        
        .bar-bg {{
            background: #e2e8f0;
            height: 40px;
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }}
        
        .bar-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            border-radius: 10px;
            display: flex;
            align-items: center;
            padding-left: 15px;
            color: white;
            font-weight: 700;
            transition: width 0.3s ease;
        }}
        
        .top-videos {{
            background: #f7fafc;
            border-radius: 15px;
            overflow: hidden;
        }}
        
        .video-item {{
            padding: 20px;
            border-bottom: 1px solid #e2e8f0;
            transition: background 0.2s;
        }}
        
        .video-item:hover {{
            background: white;
        }}
        
        .video-item:last-child {{
            border-bottom: none;
        }}
        
        .video-rank {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            text-align: center;
            line-height: 35px;
            font-weight: 700;
            margin-right: 15px;
        }}
        
        .video-title {{
            font-size: 16px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
        }}
        
        .video-stats {{
            color: #718096;
            font-size: 14px;
        }}
        
        .stat-highlight {{
            color: #667eea;
            font-weight: 700;
        }}
        
        .footer {{
            background: #2d3748;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 32px;
            }}
            
            .section-title {{
                font-size: 24px;
            }}
            
            .stat-grid {{
                grid-template-columns: 1fr;
            }}
            
            .comparison-row {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 {channel_name}</h1>
            <div class="subtitle">Data-Driven YouTube Analysis Report</div>
            <div class="subtitle">Generated {datetime.now().strftime('%B %d, %Y')}</div>
        </div>
        
        <div class="content">
            <!-- OVERVIEW -->
            <div class="section">
                <h2 class="section-title">📈 Overview</h2>
                <div class="stat-grid">
                    <div class="stat-box">
                        <div class="stat-value">{insights['overview']['total_videos']}</div>
                        <div class="stat-label">Total Videos Analyzed</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{insights['overview']['total_views']:,}</div>
                        <div class="stat-label">Total Views</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{insights['overview']['avg_views']:,}</div>
                        <div class="stat-label">Average Views per Video</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{insights['overview']['avg_views_per_day']:,}</div>
                        <div class="stat-label">Avg Views per Day</div>
                    </div>
                </div>
            </div>
            
            <!-- KEY INSIGHT: PERFORMANCE GAP -->
            <div class="section">
                <h2 class="section-title">🎯 Insight #1: Performance Gap</h2>
                <div class="insight-card">
                    <div class="insight-number">{insights['performance_gap']['performance_gap']}x</div>
                    <div class="insight-label">Performance Gap Between Top 20% and Bottom 20%</div>
                    <div class="insight-text">{insights['performance_gap']['insight']}</div>
                </div>
                <div class="stat-grid">
                    <div class="stat-box">
                        <div class="stat-value" style="color: #48bb78;">{insights['performance_gap']['top_20_avg']:,}</div>
                        <div class="stat-label">Top 20% Avg Views/Day</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" style="color: #f56565;">{insights['performance_gap']['bottom_20_avg']:,}</div>
                        <div class="stat-label">Bottom 20% Avg Views/Day</div>
                    </div>
                </div>
            </div>
            
            <!-- TITLE ANALYSIS -->
            <div class="section">
                <h2 class="section-title">✍️ Insight #2: Title Intelligence</h2>
                <div class="insight-card">
                    <div class="insight-text">{insights['title_insights']['insight']}</div>
                </div>
                
                <div class="comparison-row">
                    <div class="comparison-label">Title Length (Characters)</div>
                    <div class="comparison-values">
                        <span class="value-top">Top: {insights['title_insights']['top_avg_chars']}</span>
                        <span class="value-bottom">Bottom: {insights['title_insights']['bottom_avg_chars']}</span>
                    </div>
                </div>
                
                <div class="comparison-row">
                    <div class="comparison-label">Title Length (Words)</div>
                    <div class="comparison-values">
                        <span class="value-top">Top: {insights['title_insights']['top_avg_words']}</span>
                        <span class="value-bottom">Bottom: {insights['title_insights']['bottom_avg_words']}</span>
                    </div>
                </div>
                
                <div class="stat-grid" style="margin-top: 30px;">
                    <div class="stat-box">
                        <div class="stat-value">{insights['title_insights']['top_colon_usage']}%</div>
                        <div class="stat-label">Top Videos Use Colons</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{insights['title_insights']['top_number_usage']}%</div>
                        <div class="stat-label">Top Videos Use Numbers</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{insights['title_insights']['top_question_usage']}%</div>
                        <div class="stat-label">Top Videos Use Questions</div>
                    </div>
                </div>
            </div>
            
            <!-- DURATION ANALYSIS -->
            <div class="section">
                <h2 class="section-title">⏱️ Insight #3: Duration Sweet Spot</h2>
                <div class="insight-card">
                    <div class="insight-number">{insights['duration_insights']['sweet_spot']}</div>
                    <div class="insight-label">Best Performing Duration</div>
                    <div class="insight-text">{insights['duration_insights']['insight']}</div>
                </div>
                
                <div class="bar-chart">
                    {generate_duration_bars(insights['duration_insights']['buckets'])}
                </div>
            </div>
            
            <!-- PUBLISHING PATTERNS -->
            <div class="section">
                <h2 class="section-title">📅 Insight #4: Publishing Strategy</h2>
                <div class="insight-card">
                    <div class="insight-text">{insights['publishing_insights']['insight']}</div>
                </div>
                
                <div class="stat-grid">
                    <div class="stat-box">
                        <div class="stat-value">{insights['publishing_insights']['best_day']}</div>
                        <div class="stat-label">Best Day to Publish</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{insights['publishing_insights']['best_hour']}</div>
                        <div class="stat-label">Best Time to Publish ({insights['publishing_insights']['timezone']})</div>
                    </div>
                </div>
            </div>
            
            <!-- ENGAGEMENT -->
            <div class="section">
                <h2 class="section-title">❤️ Insight #5: Engagement Metrics</h2>
                <div class="insight-card">
                    <div class="insight-text">{insights['engagement_insights']['insight']}</div>
                </div>
                
                <div class="comparison-row">
                    <div class="comparison-label">Likes per 1,000 Views</div>
                    <div class="comparison-values">
                        <span class="value-top">Top: {insights['engagement_insights']['top_like_ratio']}</span>
                        <span class="value-bottom">Bottom: {insights['engagement_insights']['bottom_like_ratio']}</span>
                    </div>
                </div>
                
                <div class="comparison-row">
                    <div class="comparison-label">Comments per 1,000 Views</div>
                    <div class="comparison-values">
                        <span class="value-top">Top: {insights['engagement_insights']['top_comment_ratio']}</span>
                        <span class="value-bottom">Bottom: {insights['engagement_insights']['bottom_comment_ratio']}</span>
                    </div>
                </div>
            </div>
            
            <!-- CONTENT PATTERNS -->
            <div class="section">
                <h2 class="section-title">🔍 Insight #6: Content Patterns</h2>
                <div class="insight-card">
                    <div class="insight-text">{insights['content_patterns']['insight']}</div>
                </div>
                
                <div class="stat-grid">
                    {generate_keyword_boxes(insights['content_patterns']['trending_keywords'])}
                </div>
            </div>
            
            <!-- TOP 10 VIDEOS -->
            <div class="section">
                <h2 class="section-title">🏆 Top 10 Performing Videos</h2>
                <div class="top-videos">
                    {generate_top_videos_html(insights['top_performers'])}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by YouTube Analyzer • {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    </div>
</body>
</html>"""
    
    # Write file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filename


def generate_duration_bars(buckets):
    """Generate HTML for duration bars"""
    if not buckets:
        return "<p>No duration data available</p>"
    
    # Find max for scaling
    max_views = max(b['avg_views_per_day'] for b in buckets.values())
    
    html = ""
    for name, stats in buckets.items():
        width = (stats['avg_views_per_day'] / max_views * 100) if max_views > 0 else 0
        html += f"""
        <div class="bar-item">
            <div class="bar-label">
                <span>{name}</span>
                <span>{stats['avg_views_per_day']:,} views/day • {stats['count']} videos</span>
            </div>
            <div class="bar-bg">
                <div class="bar-fill" style="width: {width}%;">
                    {stats['avg_views_per_day']:,}
                </div>
            </div>
        </div>
        """
    
    return html


def generate_keyword_boxes(keywords):
    """Generate keyword stat boxes"""
    html = ""
    for keyword in keywords:
        html += f"""
        <div class="stat-box">
            <div class="stat-value" style="font-size: 24px; text-transform: capitalize;">{keyword}</div>
            <div class="stat-label">Trending Keyword</div>
        </div>
        """
    return html


def generate_top_videos_html(top_performers):
    """Generate top videos list"""
    html = ""
    for video in top_performers:
        html += f"""
        <div class="video-item">
            <span class="video-rank">{video['rank']}</span>
            <div style="display: inline-block; vertical-align: top; width: calc(100% - 60px);">
                <div class="video-title">{video['title']}</div>
                <div class="video-stats">
                    <span class="stat-highlight">{video['views']:,}</span> views • 
                    <span class="stat-highlight">{video['views_per_day']:,}</span> views/day • 
                    {video['duration_min']} min • 
                    {video['age_days']} days old
                </div>
            </div>
        </div>
        """
    
    return html