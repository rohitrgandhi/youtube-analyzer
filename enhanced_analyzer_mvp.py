import isodate
from datetime import datetime
from youtube_analyzer_openai import YouTubeAnalyzer

class EnhancedYouTubeAnalyzer(YouTubeAnalyzer):
    def categorize_videos(self, videos):
        categories = {'shorts': [], 'regular': [], 'podcasts': [], 'all': videos}
        
        for video in videos:
            duration = isodate.parse_duration(video['duration']).total_seconds()
            if duration < 60:
                categories['shorts'].append(video)
            elif duration < 1800:
                categories['regular'].append(video)
            else:
                categories['podcasts'].append(video)
        
        return categories
    
    def calculate_metrics_by_type(self, categorized):
        metrics = {}
        for cat, vids in categorized.items():
            if vids and cat != 'all':
                avg_views = sum(v['view_count'] for v in vids) / len(vids)
                metrics[cat] = {'avg_views': avg_views, 'count': len(vids)}
        return metrics
    
    def analyze_category_with_openai(self, category, videos, metrics):
        prompt = f"Analyze these {category} videos and find patterns:\n"
        for v in videos[:10]:
            prompt += f"- {v['title']} ({v['view_count']} views)\n"
        
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def generate_html_report(self, categorized, metrics, analyses):
        html = f"""<!DOCTYPE html>
<html><head><title>Analysis Report</title>
<style>
body {{font-family: Arial; padding: 20px; background: #f5f5f5;}}
.container {{max-width: 1200px; background: white; padding: 40px; border-radius: 10px;}}
h1 {{color: #333;}}
.section {{margin: 30px 0; padding: 20px; background: #fafafa; border-radius: 8px;}}
</style></head><body><div class="container">
<h1>YouTube Analysis Report</h1>
<p>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
"""
        
        for cat in ['shorts', 'regular', 'podcasts']:
            if cat in analyses:
                html += f"""<div class="section">
<h2>{cat.title()} Analysis</h2>
<p><strong>Videos:</strong> {metrics[cat]['count']}</p>
<p><strong>Avg Views:</strong> {metrics[cat]['avg_views']:,.0f}</p>
<div>{analyses[cat]}</div>
</div>"""
        
        html += "</div></body></html>"
        
        filename = f"youtube_analysis_data/analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, 'w') as f:
            f.write(html)
        
        return filename
