"""
Clean Report Generator - 7 Data-Driven Insights
"""

from datetime import datetime

def generate_clean_report(categorized, analyses):
    """Generate clean, reliable insights"""
    
    total_videos = len(categorized['all'])
    
    # CSS with escaped braces
    css = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, sans-serif; background: #f8f9fa; padding: 40px 20px; }
.container { max-width: 850px; margin: 0 auto; }
.card { background: white; border-radius: 12px; padding: 50px 60px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.insight-num { font-size: 10px; color: #999; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 25px; font-weight: 600; }
.insight-title { font-size: 26px; line-height: 1.4; color: #1a1a1a; margin-bottom: 25px; }
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin: 30px 0; }
.stat-value { font-size: 48px; font-weight: 700; color: #d32f2f; }
.stat-label { font-size: 14px; color: #666; margin-top: 8px; }
.bar-chart { margin: 30px 0; }
.bar-item { margin-bottom: 15px; }
.bar-label { font-size: 14px; color: #666; margin-bottom: 8px; display: flex; justify-content: space-between; }
.bar-visual { background: #d32f2f; height: 40px; border-radius: 6px; display: flex; align-items: center; padding: 0 15px; color: white; font-weight: 600; }
.bar-visual.gray { background: #e0e0e0; color: #666; }
.highlight { color: #d32f2f; font-weight: 600; }
.keyword-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 25px 0; }
.keyword-item { padding: 12px; background: #f8f9fa; border-radius: 6px; }
"""
    
    html = f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>YouTube Analysis Report</title>
<style>{css}</style>
</head>
<body>
<div class="container">
<div class="card" style="text-align: center; padding: 30px;">
<h1 style="font-size: 32px; margin-bottom: 10px;">YouTube Channel Analysis</h1>
<p style="color: #666; margin-bottom: 15px;">{total_videos} videos analyzed</p>
<div style="display: flex; justify-content: center; gap: 40px; margin-top: 15px;">
    <div>
        <div style="font-size: 24px; font-weight: 700; color: #d32f2f;">{len(categorized["shorts"])}</div>
        <div style="font-size: 13px; color: #999;">Shorts (≤60s)</div>
    </div>
    <div>
        <div style="font-size: 24px; font-weight: 700; color: #d32f2f;">{len(categorized["videos"])}</div>
        <div style="font-size: 13px; color: #999;">Videos (>60s)</div>
    </div>
</div>
</div>
"""
    
    # INSIGHT 1: Performance Gap
    if 'performance' in analyses:
        perf = analyses['performance']
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT 1</div>
    <div class="insight-title">top performers significantly outperform the rest.</div>
    <div class="stat-grid">
        <div>
            <div class="stat-value">{int(perf['top_avg']):,}</div>
            <div class="stat-label">views/day (top 20%)</div>
        </div>
        <div>
            <div class="stat-value" style="color: #999;">{int(perf['bottom_avg']):,}</div>
            <div class="stat-label">views/day (bottom 20%)</div>
        </div>
    </div>
    <p style="font-size: 15px; color: #666; margin-top: 20px;">
        that's a <span class="highlight">{perf['multiplier']:.1f}x gap</span> between your best and worst performing content.
    </p>
</div>"""
    
    # INSIGHT 2: Title Length
    if 'title_length' in analyses:
        tl = analyses['title_length']
        direction = "shorter" if tl['char_diff'] < 0 else "longer"
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT 2</div>
    <div class="insight-title">{direction} titles perform better.</div>
    <div class="stat-grid">
        <div>
            <div class="stat-value">{int(tl['top_chars'])}</div>
            <div class="stat-label">characters (top 20%)</div>
        </div>
        <div>
            <div class="stat-value" style="color: #999;">{int(tl['bottom_chars'])}</div>
            <div class="stat-label">characters (bottom 20%)</div>
        </div>
    </div>
    <p style="font-size: 15px; color: #666; margin-top: 20px;">
        winning titles are <span class="highlight">{abs(tl['char_diff']):.0f} characters {direction}</span> on average.
    </p>
</div>"""
    
    # INSIGHT 3: Title Patterns
    if 'title_patterns' in analyses:
        tp = analyses['title_patterns']
        
        patterns = []
        if tp['top_question_pct'] > tp['bottom_question_pct'] + 10:
            patterns.append(f"questions ({tp['top_question_pct']:.0f}% top vs {tp['bottom_question_pct']:.0f}% bottom)")
        if tp['top_colon_pct'] > tp['bottom_colon_pct'] + 10:
            patterns.append(f"colons ({tp['top_colon_pct']:.0f}% top vs {tp['bottom_colon_pct']:.0f}% bottom)")
        if tp['top_number_pct'] > tp['bottom_number_pct'] + 10:
            patterns.append(f"numbers ({tp['top_number_pct']:.0f}% top vs {tp['bottom_number_pct']:.0f}% bottom)")
        
        if patterns:
            html += f"""
<div class="card">
    <div class="insight-num">INSIGHT 3</div>
    <div class="insight-title">winning titles use specific patterns.</div>
    <p style="font-size: 15px; color: #666; margin: 20px 0;">
        top performers are more likely to use: {', '.join(patterns)}.
    </p>
</div>"""
    
    # INSIGHT 4: Duration
    if 'duration' in analyses and analyses['duration']:
        dur = analyses['duration']
        sorted_buckets = sorted(dur['all_buckets'].items(), key=lambda x: x[1]['avg_vpd'], reverse=True)
        max_vpd = sorted_buckets[0][1]['avg_vpd']
        
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT 4</div>
    <div class="insight-title">the sweet spot is {dur['sweet_spot_name'].lower()}.</div>
    <div class="bar-chart">"""
        
        for i, (bucket_name, data) in enumerate(sorted_buckets[:5]):
            width_pct = (data['avg_vpd'] / max_vpd) * 100
            # Highlight the actual sweet spot (not just the first one)
            is_winner = (bucket_name == dur['sweet_spot_name'])
            
            html += f"""
        <div class="bar-item">
            <div class="bar-label">
                <span>{bucket_name}</span>
                <span>n={data['count']}</span>
            </div>
            <div class="bar-visual {'gray' if not is_winner else ''}" style="width: {width_pct}%;">
                {int(data['avg_vpd']):,}
            </div>
        </div>"""
        
        html += """
    </div>
</div>"""
    
    # INSIGHT 5: Engagement
    if 'engagement' in analyses:
        eng = analyses['engagement']
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT 5</div>
    <div class="insight-title">engagement metrics.</div>
    <div class="stat-grid">
        <div>
            <div class="stat-value">{eng['top_like_rate']:.2f}%</div>
            <div class="stat-label">like rate (top 20%)</div>
        </div>
        <div>
            <div class="stat-value">{eng['top_comment_rate']:.1f}</div>
            <div class="stat-label">comments per 1K views (top 20%)</div>
        </div>
    </div>
</div>"""
    
    # INSIGHT 6A & 6B: Publishing patterns
    if 'publishing' in analyses:
        pub = analyses['publishing']
        
        # Get day counts
        day_counts = {}
        for video in categorized['all']:
            day = video['publish_day']
            day_counts[day] = day_counts.get(day, 0) + 1
        
        # Find most common posting day
        most_common_day = max(day_counts.items(), key=lambda x: x[1])
        
        # INSIGHT 6A: Best performing day
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT 6A</div>
    <div class="insight-title">best performing day: {pub['best_day']} ({int(pub['best_day_vpd']):,} avg views/day, n={day_counts.get(pub['best_day'], 0)}).</div>
    <div class="bar-chart">"""
        
        for day, vpd in list(pub['day_breakdown'].items())[:7]:
            width_pct = (vpd / pub['best_day_vpd']) * 100
            is_best = (day == pub['best_day'])
            count = day_counts.get(day, 0)
            
            html += f"""
        <div class="bar-item">
            <div class="bar-label">
                <span>{day}</span>
                <span>n={count}</span>
            </div>
            <div class="bar-visual {'gray' if not is_best else ''}" style="width: {width_pct}%;">
                {int(vpd):,}
            </div>
        </div>"""
        
        html += """
    </div>
    <p style="font-size: 14px; color: #666; margin-top: 15px;">
        videos posted on this day get the highest average views per day.
    </p>
</div>"""
        
        # INSIGHT 6B: Most consistent posting day
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT 6B</div>
    <div class="insight-title">most common posting day: {most_common_day[0]} (n={most_common_day[1]}).</div>
    <div class="bar-chart">"""
        
        # Sort by count instead of views/day
        sorted_by_count = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)
        max_count = sorted_by_count[0][1]
        
        for day, count in sorted_by_count:
            width_pct = (count / max_count) * 100
            is_most_common = (day == most_common_day[0])
            avg_vpd = pub['day_breakdown'].get(day, 0)
            
            html += f"""
        <div class="bar-item">
            <div class="bar-label">
                <span>{day}</span>
                <span>{int(avg_vpd):,} views/day</span>
            </div>
            <div class="bar-visual {'gray' if not is_most_common else ''}" style="width: {width_pct}%;">
                n={count}
            </div>
        </div>"""
        
        html += """
    </div>
    <p style="font-size: 14px; color: #666; margin-top: 15px;">
        you post most frequently on this day. consistency matters for audience expectation.
    </p>
</div>"""
    
    # INSIGHT 7: Keywords
    if 'keywords' in analyses:
        kw = analyses['keywords']
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT 7</div>
    <div class="insight-title">top keywords in high-performing videos.</div>
    <div class="keyword-grid">"""
        
        for word, count in kw['keywords'][:8]:
            html += f"""
        <div class="keyword-item">
            <strong>{word}</strong> ({count} videos)
        </div>"""
        
        html += """
    </div>
</div>"""
    
    html += f"""
<div style="text-align: center; padding: 40px 20px; font-size: 12px; color: #999;">
    source: {total_videos} videos analyzed, {datetime.now().strftime('%Y')}
</div>
</div>
</body>
</html>"""
    
    filename = f"youtube_analysis_data/clean_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w') as f:
        f.write(html)
    
    return filename
