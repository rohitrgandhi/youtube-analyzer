from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import threading
import time
import os

app = Flask(__name__)
CORS(app)

tasks = {}

class Task:
    def __init__(self, task_id):
        self.task_id = task_id
        self.status = "running"
        self.progress = 0
        self.message = "Starting..."
        self.result = None
        self.error = None

def run_analysis(task_id, channel):
    task = tasks[task_id]
    try:
        from clean_analyzer import CleanAnalyzer
        from clean_report import generate_clean_report
        
        # Get API keys
        youtube_key = os.environ.get("YOUTUBE_API_KEY")
        openai_key = os.environ.get("OPENAI_API_KEY")
        
        # Debug logging
        print(f"\n{'='*50}")
        print(f"DEBUG: Starting analysis for {channel}")
        print(f"YouTube API Key exists: {youtube_key is not None}")
        print(f"OpenAI API Key exists: {openai_key is not None}")
        print(f"{'='*50}\n")
        
        if not youtube_key:
            task.status = "error"
            task.error = "YouTube API key not configured on server"
            print("ERROR: YouTube API key missing!")
            return
            
        if not openai_key:
            task.status = "error"
            task.error = "OpenAI API key not configured on server"
            print("ERROR: OpenAI API key missing!")
            return
        
        task.progress = 10
        task.message = "Initializing analyzer..."
        
        analyzer = CleanAnalyzer(youtube_key, openai_key, "gpt-4o-mini")
        print(f"✓ Analyzer initialized successfully")
        
        task.progress = 20
        task.message = f"Finding channel {channel}..."
        channel_id = analyzer.get_channel_id(channel)
        
        if not channel_id:
            task.status = "error"
            task.error = "Channel not found. Please check the channel name."
            print(f"ERROR: Could not find channel: {channel}")
            return
        
        print(f"✓ Found channel ID: {channel_id}")
        
        task.progress = 30
        task.message = "Fetching videos..."
        videos = analyzer.get_all_videos(channel_id, 200)
        
        if len(videos) < 10:
            task.status = "error"
            task.error = f"Only {len(videos)} videos found. Need at least 10 for analysis."
            return
        
        print(f"✓ Fetched {len(videos)} videos")
        
        task.progress = 40
        task.message = "Processing videos..."
        categorized = analyzer.categorize_videos(videos)
        
        task.progress = 50
        task.message = "Analyzing performance..."
        performance = analyzer.insight_1_performance_gap(categorized['all'])
        
        task.progress = 60
        task.message = "Analyzing titles..."
        title_length = analyzer.insight_2_title_length(categorized['all'])
        
        task.progress = 65
        task.message = "Detecting patterns..."
        title_patterns = analyzer.insight_3_title_patterns(categorized['all'])
        
        task.progress = 70
        task.message = "Finding sweet spot..."
        duration = analyzer.insight_4_duration_buckets(categorized['all'])
        
        task.progress = 80
        task.message = "Analyzing engagement..."
        engagement = analyzer.insight_5_engagement(categorized['all'])
        
        task.progress = 85
        task.message = "Best publishing times..."
        publishing = analyzer.insight_6_publishing(categorized['all'])
        
        task.progress = 90
        task.message = "Extracting keywords..."
        keywords = analyzer.insight_7_keywords(categorized['all'])
        
        task.progress = 95
        task.message = "Generating report..."
        
        analyses = {
            'performance': performance,
            'title_length': title_length,
            'title_patterns': title_patterns,
            'duration': duration,
            'engagement': engagement,
            'publishing': publishing,
            'keywords': keywords
        }
        
        html_file = generate_clean_report(categorized, analyses)
        
        print(f"✓ Analysis complete! Report: {html_file}")
        
        task.status = "complete"
        task.progress = 100
        task.result = {
            'html_file': html_file,
            'stats': {
                'total': len(categorized['all']),
                'shorts': len(categorized['shorts']),
                'videos': len(categorized['videos'])
            }
        }
        
    except Exception as e:
        task.status = "error"
        task.error = str(e)
        print(f"\n{'!'*50}")
        print(f"ERROR in analysis:")
        print(f"{e}")
        print(f"{'!'*50}\n")
        import traceback
        traceback.print_exc()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    channel = data.get('channel', '').strip()
    task_id = f"{channel}_{int(time.time())}"
    tasks[task_id] = Task(task_id)
    thread = threading.Thread(target=run_analysis, args=(task_id, channel))
    thread.daemon = True
    thread.start()
    return jsonify({'task_id': task_id})

@app.route('/api/progress/<task_id>')
def get_progress(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({
        'status': task.status,
        'progress': task.progress,
        'message': task.message,
        'error': task.error,
        'result': task.result
    })

@app.route('/api/report/<path:filename>')
def serve_report(filename):
    return send_file(f'youtube_analysis_data/{filename}')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("📊 CLEAN YOUTUBE ANALYZER - 7 DATA-DRIVEN INSIGHTS")
    print("="*70)
    print("\nOpen: http://localhost:8080\n")
    app.run(host='0.0.0.0', port=8080, debug=False)

application = app