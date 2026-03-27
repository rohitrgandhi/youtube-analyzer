from datetime import datetime

def generate_insights_html(categorized, analyses):
    """Generate beautiful insights report"""
    
    all_videos = categorized['all']
    
    html = """<!DOCTYPE html>
<html><head>
<title>YouTube Insights Report</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f8f9fa; padding: 20px; }
.container { max-width: 900px; margin: 0 auto; }
.insight { background: white; border-radius: 16px; padding: 50px; margin-bottom: 25px; box-shadow: 0 2px 15px rgba(0,0,0,0.06); }
.insight-num { font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 25px; }
.insight-title { font-size: 28px; line-height: 1.4; color: #1a1a1a; margin-bottom: 35px; font-weight: 400; }
.stat-big { font-size: 72px; font-weight: 700; color: #dc143c; line-height: 1; }
.stat-label { font-size: 15px; color: #666; margin-top: 8px; }
.stat-small { font-size: 14px; color: #999; }
.comparison { display: flex; gap: 50px; margin: 25px 0; }
.comp-item { flex: 1; }
.comp-value { font-size: 52px; font-weight: 700; }
.comp-value.win { color: #dc143c; }
.comp-value.lose { color: #ddd; }
.comp-label { font-size: 14px; color: #666; margin-top: 5px; }
.list-item { padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
.list-item:last-child { border: none; }
.topic-bar { background: #dc143c; height: 40px; display: flex; align-items: center; padding: 0 15px; color: white; font-weight: 600; border-radius: 6px; margin-bottom: 8px; }
.topic-stats { font-size: 13px; color: #666; margin-left: auto; }
</style>
</head>
<body>
<div class="container">"""
    
    # INSIGHT 1: Performance gap
    top_3 = sorted(all_videos, key=lambda x: x['views_per_day'], reverse=True)[:3]
    bottom_3 = sorted(all_videos, key=lambda x: x['views_per_day'])[:3]
    top_avg = sum(v['views_per_day'] for v in top_3) / 3
    bottom_avg = sum(v['views_per_day'] for v in bottom_3) / 3
    gap = top_avg / bottom_avg if bottom_avg > 0 else 0
    
    html += f"""
<div class="insight">
    <div class="insight-num">INSIGHT 1</div>
    <div class="insight-title">top performers significantly outperform the rest.</div>
    <div class="stat-big">{gap:.1f}x</div>
    <div class="stat-label">gap between top 3 and bottom 3 videos</div>
    <div class="stat-small" style="margin-top: 20px;">top 3 avg: {top_avg:,.0f} views/day • bottom 3 avg: {bottom_avg:,.0f} views/day</div>
</div>"""
    
    # INSIGHT 2: Title length
    if 'title_analysis' in analyses:
        ta = analyses['title_analysis']
        top_chars = ta['top']['avg_length_chars']
        bottom_chars = ta['bottom']['avg_length_chars']
        
        html += f"""
<div class="insight">
    <div class="insight-num">INSIGHT 2</div>
    <div class="insight-title">{"shorter" if top_chars < bottom_chars else "longer"} titles perform better.</div>
    <div class="comparison">
        <div class="comp-item">
            <div class="comp-value {'win' if top_chars < bottom_chars else 'lose'}">{top_chars:.0f}</div>
            <div class="comp-label">chars (top 20%)</div>
        </div>
        <div class="comp-item">
            <div class="comp-value {'win' if top_chars >= bottom_chars else 'lose'}">{bottom_chars:.0f}</div>
            <div class="comp-label">chars (bottom 20%)</div>
        </div>
    </div>
</div>"""
        
        # INSIGHT 3: Colon usage
        top_colon = ta['top']['colon_pct']
        bottom_colon = ta['bottom']['colon_pct']
        
        html += f"""
<div class="insight">
    <div class="insight-num">INSIGHT 3</div>
    <div class="insight-title">colons in titles {'boost' if top_colon > bottom_colon else 'hurt'} performance.</div>
    <div class="comparison">
        <div class="comp-item">
            <div class="comp-value {'win' if top_colon > bottom_colon else 'lose'}">{top_colon:.1f}%</div>
            <div class="comp-label">top 20%</div>
        </div>
        <div class="comp-item">
            <div class="comp-value {'win' if top_colon <= bottom_colon else 'lose'}">{bottom_colon:.1f}%</div>
            <div class="comp-label">bottom 20%</div>
        </div>
    </div>
</div>"""
    
    # INSIGHT 4: Duration sweet spot
    if 'duration_analysis' in analyses and 'sweet_spot' in analyses['duration_analysis']:
        da = analyses['duration_analysis']
        
        html += f"""
<div class="insight">
    <div class="insight-num">INSIGHT 4</div>
    <div class="insight-title">the sweet spot is {da['sweet_spot']}.</div>
    <div class="stat-big">{da['sweet_spot_vpd']:,.0f}</div>
    <div class="stat-label">avg views/day for {da['sweet_spot']} videos</div>
</div>"""
    
    # INSIGHT 5: Best topics
    if 'topic_analysis' in analyses:
        topics = list(analyses['topic_analysis'].items())[:5]
        
        html += """
<div class="insight">
    <div class="insight-num">INSIGHT 5</div>
    <div class="insight-title">top performing topics.</div>"""
        
        for topic, data in topics:
            html += f"""
    <div class="topic-bar">
        <span>{topic.title()}</span>
        <span class="topic-stats">{data['avg_views_per_day']:,.0f} views/day • {data['count']} videos</span>
    </div>"""
        
        html += "</div>"
    
    # INSIGHT 6: Best publishing day
    if 'publishing' in analyses:
        best_day, best_vpd = analyses['publishing']['best_day']
        
        html += f"""
<div class="insight">
    <div class="insight-num">INSIGHT 6</div>
    <div class="insight-title">publish on {best_day} for best results.</div>
    <div class="stat-big">{best_vpd:,.0f}</div>
    <div class="stat-label">avg views/day on {best_day}</div>
</div>"""
    
    # INSIGHT 7: Title formulas
    if 'title_formulas' in analyses:
        formulas = analyses['title_formulas'][:5]
        
        html += """
<div class="insight">
    <div class="insight-num">INSIGHT 7</div>
    <div class="insight-title">winning title formulas.</div>"""
        
        for i, formula in enumerate(formulas, 1):
            html += f"""
    <div class="list-item">
        <div style="font-weight: 600; margin-bottom: 4px;">{i}. {formula['pattern']}</div>
        <div style="font-size: 14px; color: #666; margin-bottom: 4px;">"{formula['title']}"</div>
        <div style="font-size: 13px; color: #999;">{formula['views_per_day']:,.0f} views/day</div>
    </div>"""
        
        html += "</div>"
    
    html += """
</div>
</body>
</html>"""
    
    filename = f"youtube_analysis_data/insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w') as f:
        f.write(html)
    
    return filename
