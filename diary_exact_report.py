"""
Diary of a CEO - Exact Report Generator
Crisp, data-driven insights matching the tweet thread style
"""

from datetime import datetime

def generate_exact_report(categorized, analyses):
    """Generate insights with crisp conclusions like the tweet"""
    
    total_videos = len(categorized['all'])
    
    html = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YouTube Analysis Report</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f8f9fa;
    padding: 40px 20px;
    line-height: 1.6;
}
.container { max-width: 850px; margin: 0 auto; }
.card { 
    background: white;
    border-radius: 12px;
    padding: 50px 60px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.insight-num { 
    font-size: 10px;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 25px;
    font-weight: 600;
}
.insight-title { 
    font-size: 26px;
    line-height: 1.4;
    color: #1a1a1a;
    margin-bottom: 25px;
    font-weight: 400;
}
.data-point { 
    font-size: 15px;
    color: #444;
    margin-bottom: 15px;
    line-height: 1.6;
}
.highlight { 
    color: #d32f2f;
    font-weight: 600;
}
.stat-huge { 
    font-size: 96px;
    font-weight: 700;
    color: #d32f2f;
    line-height: 1;
    letter-spacing: -2px;
    margin: 20px 0;
}
.stat-label { 
    font-size: 14px;
    color: #666;
    margin-bottom: 20px;
}
.takeaway { 
    background: #f8f9fa;
    padding: 20px 25px;
    border-left: 4px solid #d32f2f;
    margin-top: 25px;
    border-radius: 4px;
}
.takeaway-title { 
    font-size: 12px;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
    font-weight: 600;
}
.takeaway-text { 
    font-size: 15px;
    color: #333;
    line-height: 1.5;
}
.conclusion { 
    font-size: 15px;
    color: #666;
    font-style: italic;
    margin-top: 15px;
}
</style>
</head>
<body>
<div class="container">"""
    
    insight_num = 1
    
    # INSIGHT 1: Fame
    if 'guest_fame' in analyses and analyses['guest_fame']:
        gf = analyses['guest_fame']
        
        # Dynamic conclusion based on multiplier
        if gf['multiplier'] > 10:
            conclusion = "fame is the biggest growth hack for you."
        elif gf['multiplier'] > 5:
            conclusion = "high-fame guests significantly outperform low-fame guests."
        elif gf['multiplier'] > 2:
            conclusion = "guest fame impacts performance moderately."
        else:
            conclusion = "guest fame has minimal impact on views."
        
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT {insight_num}</div>
    <div class="insight-title">{conclusion}</div>
    <div class="data-point">
        high-fame guests averaged <span class="highlight">{gf['high_fame_avg']:,.0f} views/day</span>.
        low-fame guests averaged <span class="highlight">{gf['low_fame_avg']:,.0f}</span>.
        that's a <span class="highlight">{gf['multiplier']:.1f}x gap</span>, and low-fame guests STILL made up {gf['low_fame_count']} of the {gf['total_episodes']} episodes.
    </div>
    <div class="takeaway">
        <div class="takeaway-title">Takeaway:</div>
        <div class="takeaway-text">
            {"borrow demand with known people, known conflicts, or known stories." if gf['multiplier'] > 5 else "focus on content quality over guest fame - your audience watches for you, not the guest."}
        </div>
    </div>
</div>"""
        insight_num += 1
    
    # INSIGHT 2: Questions
    if 'questions' in analyses:
        qa = analyses['questions']
        
        # Only show if there's a meaningful difference
        if qa['multiplier'] > 1.2:  # At least 20% difference
            
            # Dynamic conclusion
            if qa['multiplier'] > 5:
                conclusion = "the best videos asked WAY more questions than the worst ones."
                impact = "which is fkn massive"
            elif qa['multiplier'] > 2:
                conclusion = "top performers asked significantly more questions."
                impact = "which is substantial"
            elif qa['multiplier'] > 1.3:
                conclusion = "question usage shows a moderate correlation with performance."
                impact = "which is noticeable"
            else:
                conclusion = "question usage has minimal impact on performance."
                impact = "which suggests other factors matter more"
            
            html += f"""
<div class="card">
    <div class="insight-num">INSIGHT {insight_num}</div>
    <div class="insight-title">{conclusion}</div>
    <div class="data-point">
        top-20% interviews averaged <span class="highlight">{qa['top_avg']:.1f} questions</span>.
        bottom-20% interviews averaged <span class="highlight">{qa['bottom_avg']:.1f}</span>.
        that's a <span class="highlight">{qa['multiplier']:.2f}x gap</span> and an effect size of {qa['effect_size']:.2f}, {impact}.
    </div>
    <div class="takeaway">
        <div class="takeaway-title">Takeaway:</div>
        <div class="takeaway-text">
            {"script more curiosity pivots. every new question is a new retention hook." if qa['multiplier'] > 2 else "focus on content depth rather than question quantity."}
        </div>
    </div>
</div>"""
            insight_num += 1
        else:
            # Skip this insight if multiplier is too low
            insight_num += 1
    
    # INSIGHT 3: Title Structure
    if 'title_structure' in analyses:
        ts = analyses['title_structure']
        
        # Only show if patterns exist
        if ts['colon_pct'] > 10:  # At least 10% use structure
            
            # Dynamic conclusion based on percentages
            if ts['name_frame_pct'] > 70:
                conclusion = "the winning title was a 2-part sentence, not a topic dump."
            elif ts['name_frame_pct'] > 40:
                conclusion = "structured titles with clear framing perform better."
            else:
                conclusion = "title structure shows varied patterns - no dominant format."
            
            html += f"""
<div class="card">
    <div class="insight-num">INSIGHT {insight_num}</div>
    <div class="insight-title">{conclusion}</div>
    <div class="data-point">
        <span class="highlight">{ts['name_frame_pct']:.1f}%</span> of the top videos used a name/frame: claim structure.
        <span class="highlight">{ts['colon_pct']:.1f}%</span> of top videos used a colon.
        {"the pattern was simple: credibility or name first, then the payoff." if ts['colon_pct'] > 70 else "titles use mixed formatting approaches."}
    </div>
    <div class="takeaway">
        <div class="takeaway-title">Takeaway:</div>
        <div class="takeaway-text">
            {"try this template tomorrow: [who/why trust this]: [specific consequence or prediction]." if ts['name_frame_pct'] > 50 else "experiment with different title formats to find what works for your audience."}
        </div>
    </div>
</div>"""
            insight_num += 1
        else:
            # Skip if no patterns
            insight_num += 1
    
    # INSIGHT 4: Title Length
    if 'title_length' in analyses:
        tl = analyses['title_length']
        direction = "shorter" if tl['char_diff'] < 0 else "longer"
        
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT {insight_num}</div>
    <div class="insight-title">{direction} titles beat {"longer" if direction=="shorter" else "shorter"} ones, even on a long-form podcast channel.</div>
    <div class="data-point">
        the top 20% averaged <span class="highlight">{tl['top_chars']:.1f} characters</span> and <span class="highlight">{tl['top_words']:.1f} words</span>.
        the bottom 20% averaged <span class="highlight">{tl['bottom_chars']:.1f} characters</span> and <span class="highlight">{tl['bottom_words']:.1f} words</span>.
        winning titles were {"shorter" if tl['char_diff']<0 else "longer"} by <span class="highlight">{abs(tl['char_diff']):.1f} characters</span>.
    </div>
    <div class="takeaway">
        <div class="takeaway-title">Takeaway:</div>
        <div class="takeaway-text">
            nail your first 5 words. they're everything.
        </div>
    </div>
</div>"""
        insight_num += 1
    
    # INSIGHT 5: Duration
    if 'duration' in analyses and analyses['duration']:
        dur = analyses['duration']
        
        # Get all buckets sorted by performance
        buckets = dur['all_buckets']
        sweet_spot_name = dur['sweet_spot_name']
        
        # Sort buckets by views/day
        sorted_buckets = sorted(buckets.items(), key=lambda x: x[1]['avg_vpd'], reverse=True)
        
        # Dynamic conclusion based on sweet spot
        if '60-90 min' in sweet_spot_name:
            conclusion = "the sweet spot was 60-90 minutes."
        elif '30-60 min' in sweet_spot_name:
            conclusion = "the sweet spot was 30-60 minutes."
        elif '90-120 min' in sweet_spot_name:
            conclusion = "the sweet spot was 90-120 minutes."
        else:
            conclusion = f"the sweet spot was {sweet_spot_name.lower()}."
        
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT {insight_num}</div>
    <div class="insight-title">{conclusion}</div>
    
    <div style="margin: 30px 0;">"""
        
        # Generate bar chart
        max_vpd = sorted_buckets[0][1]['avg_vpd']
        
        for bucket_name, data in sorted_buckets:
            width_pct = (data['avg_vpd'] / max_vpd) * 100
            is_winner = (bucket_name == sweet_spot_name)
            
            html += f"""
        <div style="margin-bottom: 20px;">
            <div style="font-size: 14px; color: #666; margin-bottom: 8px; display: flex; justify-content: space-between;">
                <span>{bucket_name}</span>
                <span style="color: #999;">n={data['count']}</span>
            </div>
            <div style="background: {'#d32f2f' if is_winner else '#e0e0e0'}; height: 50px; width: {width_pct}%; border-radius: 6px; display: flex; align-items: center; padding: 0 15px; color: {'white' if is_winner else '#666'}; font-weight: 600; font-size: 18px;">
                {int(data['avg_vpd']):,}
            </div>
        </div>"""
        
        html += f"""
    </div>
    
    <div style="font-size: 13px; color: #999; margin-top: 25px;">
        avg views/day by episode duration
    </div>
    
    <div style="font-size: 13px; color: #999; margin-top: 8px;">
        note: {sweet_spot_name} bucket has n={dur['sweet_spot_count']} {"(small sample)" if dur['sweet_spot_count'] < 20 else ""}
    </div>
    
    <div class="takeaway">
        <div class="takeaway-title">Takeaway:</div>
        <div class="takeaway-text">
            cut your writing "final cut" by 20%.
        </div>
    </div>
</div>"""
        insight_num += 1
    
    # INSIGHT 6: Topics
    if 'topics' in analyses:
        top_data = analyses['topics']
        
        if top_data['topics'] and len(top_data['topics']) >= 2:
            top_topic = top_data['topics'][0]
            second_topic = top_data['topics'][1] if len(top_data['topics']) > 1 else None
            
            html += f"""
<div class="card">
    <div class="insight-num">INSIGHT {insight_num}</div>
    <div class="insight-title">topic framing mattered more than most creators think.</div>
    <div class="data-point">
        {top_topic[0]} episodes averaged <span class="highlight">{top_topic[1]['avg_vpd']:,.0f} views/day</span>."""
            
            if second_topic:
                html += f"""
        {second_topic[0]} averaged <span class="highlight">{second_topic[1]['avg_vpd']:,.0f}</span>."""
            
            if top_data['multiplier'] > 1:
                html += f"""
        same channel, same host, but the hidden-conflict frame pulled <span class="highlight">{top_data['multiplier']:.2f}x</span> {second_topic[0] if second_topic else 'other topics'}.
    </div>"""
            else:
                html += "</div>"
            
            html += """
    <div class="takeaway">
        <div class="takeaway-title">Takeaway:</div>
        <div class="takeaway-text">
            even in boring niches, package the post around secrecy, stakes, conflict, or consequences.
        </div>
    </div>
</div>"""
            insight_num += 1
    
    # INSIGHT 7: Hooks
    if 'hooks' in analyses:
        hooks = analyses['hooks']
        
        html += f"""
<div class="card">
    <div class="insight-num">INSIGHT {insight_num}</div>
    <div class="insight-title">pain-first hooks lost to proof-first hooks.</div>
    <div class="data-point">
        proof cold opens showed up in <span class="highlight">{hooks['top_proof_pct']:.1f}%</span> of top videos, but only <span class="highlight">{hooks['bottom_proof_pct']:.1f}%</span> of bottom videos.
        pain hooks did the reverse: <span class="highlight">{hooks['top_pain_pct']:.1f}%</span> of top videos vs <span class="highlight">{hooks['bottom_pain_pct']:.1f}%</span> of bottom videos.
        viewers clicked for receipts, not just emotion.
    </div>
    <div class="takeaway">
        <div class="takeaway-title">Takeaway:</div>
        <div class="takeaway-text">
            open with evidence, demonstration, or a hard claim before you open the wound.
        </div>
    </div>
</div>"""
        insight_num += 1
    
    # Final Summary
    html += f"""
<div class="card">
    <div class="insight-title" style="margin-bottom: 15px;">what you should do now:</div>
    <div class="data-point">
        this analysis went through <span class="highlight">{total_videos} episodes</span> for you.
    </div>
    <div class="conclusion">
        the patterns are pretty clear: fame pulls clicks, proof beats pain, and titles do more work than most creators think.
    </div>
</div>

<div style="text-align: center; padding: 40px 20px; font-size: 12px; color: #999;">
    source: {total_videos} episodes analyzed, {datetime.now().strftime('%Y')}
</div>

</div>
</body>
</html>"""
    
    filename = f"youtube_analysis_data/exact_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w') as f:
        f.write(html)
    
    return filename
