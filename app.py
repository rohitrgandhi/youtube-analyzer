from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import threading
import time
import os
import sys
import traceback

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
    
    print("\n" + "="*70, flush=True)
    print(f"🔍 ANALYSIS STARTED: {channel}", flush=True)
    print("="*70, flush=True)
    
    try:
        # Step 1: Check API keys
        youtube_key = os.environ.get("YOUTUBE_API_KEY")
        openai_key = os.environ.get("OPENAI_API_KEY")
        
        print(f"✓ YouTube Key: {'Found' if youtube_key else 'MISSING'}", flush=True)
        print(f"✓ OpenAI Key: {'Found' if openai_key else 'MISSING'}", flush=True)
        
        if not youtube_key or not openai_key:
            task.status = "error"
            task.error = "API keys not configured. Check Render environment variables."
            print("❌ Missing API keys!", flush=True)
            return
        
        # Step 2: Import modules
        print("📦 Importing modules...", flush=True)
        from youtube_analyzer import YouTubeAnalyzer
        from report_generator import generate_report
        print("✓ Modules imported", flush=True)
        
        # Step 3: Initialize analyzer
        task.progress = 10
        task.message = "Initializing..."
        print("🔧 Creating analyzer...", flush=True)
        analyzer = YouTubeAnalyzer(youtube_key, openai_key)
        print("✓ Analyzer ready", flush=True)
        
        # Step 4: Find channel
        task.progress = 20
        task.message = f"Finding {channel}..."
        print(f"🔎 Looking up channel: {channel}", flush=True)
        channel_id = analyzer.get_channel_id(channel)
        
        if not channel_id:
            task.status = "error"
            task.error = "Channel not found. Check the channel name and try again."
            print(f"❌ Channel not found: {channel}", flush=True)
            return
        
        print(f"✓ Found channel ID: {channel_id}", flush=True)
        
        # Step 5: Fetch videos
        task.progress = 30
        task.message = "Fetching videos..."
        print("📹 Fetching videos...", flush=True)
        videos = analyzer.get_videos(channel_id, max_results=100)
        print(f"✓ Fetched {len(videos)} videos", flush=True)
        
        if len(videos) < 10:
            task.status = "error"
            task.error = f"Only {len(videos)} videos found. Need at least 10."
            return
        
        # Step 6: Analyze
        task.progress = 50
        task.message = "Analyzing performance..."
        print("📊 Running analysis...", flush=True)
        analysis_data = analyzer.analyze_videos(videos)
        print("✓ Analysis complete", flush=True)
        
        # Step 7: Generate report
        task.progress = 90
        task.message = "Generating report..."
        print("📄 Creating report...", flush=True)
        report_file = generate_report(videos, analysis_data, channel)
        print(f"✓ Report created: {report_file}", flush=True)
        
        # Done!
        task.status = "complete"
        task.progress = 100
        task.result = {
            'html_file': report_file,
            'stats': {
                'total_videos': len(videos)
            }
        }
        
        print("🎉 SUCCESS!", flush=True)
        print("="*70 + "\n", flush=True)
        
    except Exception as e:
        task.status = "error"
        task.error = str(e)
        print("\n" + "!"*70, flush=True)
        print("❌ ERROR:", flush=True)
        print(f"   {type(e).__name__}: {str(e)}", flush=True)
        print("\nFull traceback:", flush=True)
        traceback.print_exc()
        print("!"*70 + "\n", flush=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    channel = data.get('channel', '').strip()
    
    if not channel:
        return jsonify({'error': 'Channel name required'}), 400
    
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
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({
        'status': task.status,
        'progress': task.progress,
        'message': task.message,
        'error': task.error,
        'result': task.result
    })

@app.route('/api/report/<path:filename>')
def serve_report(filename):
    return send_file(f'reports/{filename}')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("📊 YOUTUBE ANALYZER")
    print("="*70)
    print("\n🌐 Running on http://localhost:8080\n")
    app.run(host='0.0.0.0', port=8080, debug=False)

application = app