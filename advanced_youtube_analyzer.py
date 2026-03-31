"""
Advanced YouTube Channel Analyzer
Generates deep insights from YouTube API data only
"""

from googleapiclient.discovery import build
from datetime import datetime
import statistics
from collections import Counter
import re

class AdvancedYouTubeAnalyzer:
    def __init__(self, youtube_api_key, openai_api_key):
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        self.openai_api_key = openai_api_key
    
    def get_channel_id(self, channel_handle):
        """Get channel ID from handle or username"""
        handle = channel_handle.replace('@', '')
        
        try:
            # Try search first - most reliable
            request = self.youtube.search().list(
                part='snippet',
                q=channel_handle,
                type='channel',
                maxResults=1
            )
            response = request.execute()
            
            if response.get('items'):
                return response['items'][0]['snippet']['channelId']
            
            # Try without @ symbol
            request = self.youtube.search().list(
                part='snippet',
                q=handle,
                type='channel',
                maxResults=1
            )
            response = request.execute()
            
            if response.get('items'):
                return response['items'][0]['snippet']['channelId']
            
            # Try as username (old method)
            request = self.youtube.channels().list(
                part='id',
                forUsername=handle
            )
            response = request.execute()
            
            if response.get('items'):
                return response['items'][0]['id']
            
            return None
        except Exception as e:
            print(f"Error finding channel: {e}")
            return None
    
    def get_videos(self, channel_id, max_results=100):
        """Fetch videos from channel"""
        videos = []
        
        # Get uploads playlist ID
        channel_response = self.youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()
        
        playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Fetch videos
        next_page_token = None
        
        while len(videos) < max_results:
            playlist_request = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=min(50, max_results - len(videos)),
                pageToken=next_page_token
            )
            playlist_response = playlist_request.execute()
            
            video_ids = [item['snippet']['resourceId']['videoId'] 
                        for item in playlist_response['items']]
            
            # Get video details
            video_request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            )
            video_response = video_request.execute()
            
            for video in video_response['items']:
                videos.append({
                    'id': video['id'],
                    'title': video['snippet']['title'],
                    'description': video['snippet'].get('description', ''),
                    'published_at': video['snippet']['publishedAt'],
                    'duration': video['contentDetails']['duration'],
                    'views': int(video['statistics'].get('viewCount', 0)),
                    'likes': int(video['statistics'].get('likeCount', 0)),
                    'comments': int(video['statistics'].get('commentCount', 0)),
                    'tags': video['snippet'].get('tags', [])
                })
            
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
        
        return videos
    
    def parse_duration(self, duration_str):
        """Convert ISO 8601 duration to minutes"""
        # PT1H2M10S -> 62.17 minutes
        hours = re.search(r'(\d+)H', duration_str)
        minutes = re.search(r'(\d+)M', duration_str)
        seconds = re.search(r'(\d+)S', duration_str)
        
        total_minutes = 0
        if hours:
            total_minutes += int(hours.group(1)) * 60
        if minutes:
            total_minutes += int(minutes.group(1))
        if seconds:
            total_minutes += int(seconds.group(1)) / 60
        
        return round(total_minutes, 2)
    
    def analyze_videos(self, videos):
        """Deep analysis of video data"""
        
        # Enrich video data
        for video in videos:
            # Parse duration
            video['duration_minutes'] = self.parse_duration(video['duration'])
            
            # Calculate age in days
            published = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
            age_days = (datetime.now(published.tzinfo) - published).days + 1
            video['age_days'] = age_days
            
            # Views per day
            video['views_per_day'] = video['views'] / age_days if age_days > 0 else 0
            
            # Engagement metrics
            video['like_ratio'] = (video['likes'] / video['views'] * 1000) if video['views'] > 0 else 0
            video['comment_ratio'] = (video['comments'] / video['views'] * 1000) if video['views'] > 0 else 0
            
            # Title analysis
            video['title_length'] = len(video['title'])
            video['title_words'] = len(video['title'].split())
            video['has_colon'] = ':' in video['title']
            video['has_question'] = '?' in video['title']
            video['has_number'] = bool(re.search(r'\d', video['title']))
            video['has_caps'] = any(word.isupper() and len(word) > 1 for word in video['title'].split())
            
            # Day of week
            video['day_of_week'] = published.strftime('%A')
            video['hour_of_day'] = published.hour
        
        # Sort by views per day
        videos_sorted = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)
        
        # Separate Shorts vs Videos
        shorts = [v for v in videos if v['duration_minutes'] < 1]
        long_videos = [v for v in videos if v['duration_minutes'] >= 1]
        
        # Get top and bottom 20%
        total = len(videos_sorted)
        top_20_idx = max(1, int(total * 0.2))
        bottom_20_idx = max(1, int(total * 0.2))
        
        top_20 = videos_sorted[:top_20_idx]
        bottom_20 = videos_sorted[-bottom_20_idx:]
        
        # Generate insights
        insights = {
            'overview': self._analyze_overview(videos, shorts, long_videos),
            'performance_gap': self._analyze_performance_gap(top_20, bottom_20),
            'title_insights': self._analyze_titles(top_20, bottom_20),
            'duration_insights': self._analyze_duration(videos),
            'publishing_insights': self._analyze_publishing(top_20, bottom_20, videos),
            'engagement_insights': self._analyze_engagement(top_20, bottom_20),
            'top_performers': self._get_top_performers(videos_sorted[:10]),
            'content_patterns': self._analyze_content_patterns(top_20, videos)
        }
        
        return insights
    
    def _analyze_overview(self, videos, shorts, long_videos):
        """Overall statistics"""
        total_views = sum(v['views'] for v in videos)
        avg_views = statistics.mean([v['views'] for v in videos])
        
        return {
            'total_videos': len(videos),
            'total_shorts': len(shorts),
            'total_long_videos': len(long_videos),
            'total_views': total_views,
            'avg_views': int(avg_views),
            'avg_views_per_day': int(statistics.mean([v['views_per_day'] for v in videos]))
        }
    
    def _analyze_performance_gap(self, top_20, bottom_20):
        """Performance gap analysis"""
        top_avg = statistics.mean([v['views_per_day'] for v in top_20])
        bottom_avg = statistics.mean([v['views_per_day'] for v in bottom_20])
        gap = top_avg / bottom_avg if bottom_avg > 0 else 0
        
        return {
            'top_20_avg': int(top_avg),
            'bottom_20_avg': int(bottom_avg),
            'performance_gap': round(gap, 1),
            'insight': f"Top 20% videos get {gap:.1f}x more views per day than bottom 20%"
        }
    
    def _analyze_titles(self, top_20, bottom_20):
        """Title structure analysis"""
        top_chars = statistics.mean([v['title_length'] for v in top_20])
        bottom_chars = statistics.mean([v['title_length'] for v in bottom_20])
        
        top_words = statistics.mean([v['title_words'] for v in top_20])
        bottom_words = statistics.mean([v['title_words'] for v in bottom_20])
        
        top_colon_pct = sum(1 for v in top_20 if v['has_colon']) / len(top_20) * 100
        bottom_colon_pct = sum(1 for v in bottom_20 if v['has_colon']) / len(bottom_20) * 100
        
        top_question_pct = sum(1 for v in top_20 if v['has_question']) / len(top_20) * 100
        top_number_pct = sum(1 for v in top_20 if v['has_number']) / len(top_20) * 100
        top_caps_pct = sum(1 for v in top_20 if v['has_caps']) / len(top_20) * 100
        
        return {
            'top_avg_chars': round(top_chars, 1),
            'bottom_avg_chars': round(bottom_chars, 1),
            'char_difference': round(top_chars - bottom_chars, 1),
            'top_avg_words': round(top_words, 1),
            'bottom_avg_words': round(bottom_words, 1),
            'word_difference': round(top_words - bottom_words, 1),
            'top_colon_usage': round(top_colon_pct, 1),
            'bottom_colon_usage': round(bottom_colon_pct, 1),
            'top_question_usage': round(top_question_pct, 1),
            'top_number_usage': round(top_number_pct, 1),
            'top_caps_usage': round(top_caps_pct, 1),
            'insight': self._generate_title_insight(top_chars, bottom_chars, top_colon_pct)
        }
    
    def _generate_title_insight(self, top_chars, bottom_chars, top_colon_pct):
        """Generate title insight"""
        if top_chars < bottom_chars:
            length_insight = f"Shorter titles perform better ({top_chars:.0f} vs {bottom_chars:.0f} chars)"
        else:
            length_insight = f"Longer titles perform better ({top_chars:.0f} vs {bottom_chars:.0f} chars)"
        
        if top_colon_pct > 60:
            structure_insight = f"{top_colon_pct:.0f}% of top videos use colons (two-part structure)"
        else:
            structure_insight = "Simple titles without colons perform better"
        
        return f"{length_insight}. {structure_insight}."
    
    def _analyze_duration(self, videos):
        """Duration bucket analysis"""
        buckets = {
            'Shorts (<1min)': [],
            'Short (1-5min)': [],
            'Medium (5-15min)': [],
            'Standard (15-30min)': [],
            'Long (30-60min)': [],
            'Extended (60+ min)': []
        }
        
        for v in videos:
            dur = v['duration_minutes']
            vpd = v['views_per_day']
            
            if dur < 1:
                buckets['Shorts (<1min)'].append(vpd)
            elif dur < 5:
                buckets['Short (1-5min)'].append(vpd)
            elif dur < 15:
                buckets['Medium (5-15min)'].append(vpd)
            elif dur < 30:
                buckets['Standard (15-30min)'].append(vpd)
            elif dur < 60:
                buckets['Long (30-60min)'].append(vpd)
            else:
                buckets['Extended (60+ min)'].append(vpd)
        
        bucket_stats = {}
        for name, vpd_list in buckets.items():
            if vpd_list:
                bucket_stats[name] = {
                    'avg_views_per_day': int(statistics.mean(vpd_list)),
                    'count': len(vpd_list)
                }
        
        # Find sweet spot (requires at least 5 videos for statistical significance)
        significant_buckets = {k: v for k, v in bucket_stats.items() if v['count'] >= 5}
        
        if significant_buckets:
            sweet_spot = max(significant_buckets.items(), key=lambda x: x[1]['avg_views_per_day'])
        else:
            # Fallback to any bucket if none have 5+ videos
            sweet_spot = max(bucket_stats.items(), key=lambda x: x[1]['avg_views_per_day'])
        
        return {
            'buckets': bucket_stats,
            'sweet_spot': sweet_spot[0],
            'sweet_spot_avg': sweet_spot[1]['avg_views_per_day'],
            'insight': f"{sweet_spot[0]} is the sweet spot with {sweet_spot[1]['avg_views_per_day']:,} views/day avg"
        }
    
    def _analyze_publishing(self, top_20, bottom_20, all_videos):
        """Publishing pattern analysis"""
        # Day of week analysis
        top_days = Counter([v['day_of_week'] for v in top_20])
        all_days = Counter([v['day_of_week'] for v in all_videos])
        
        # Normalize by how many videos published on each day
        day_performance = {}
        for day in top_days:
            if all_days[day] > 0:
                day_performance[day] = top_days[day] / all_days[day]
        
        best_day = max(day_performance.items(), key=lambda x: x[1])[0] if day_performance else "N/A"
        
        # Hour of day (top performers)
        top_hours = Counter([v['hour_of_day'] for v in top_20])
        best_hour = top_hours.most_common(1)[0][0] if top_hours else 0
        
        return {
            'best_day': best_day,
            'best_hour': f"{best_hour:02d}:00",
            'day_distribution': dict(top_days.most_common(3)),
            'insight': f"Best publishing: {best_day}s around {best_hour:02d}:00"
        }
    
    def _analyze_engagement(self, top_20, bottom_20):
        """Engagement metrics analysis"""
        top_like_ratio = statistics.mean([v['like_ratio'] for v in top_20])
        bottom_like_ratio = statistics.mean([v['like_ratio'] for v in bottom_20])
        
        top_comment_ratio = statistics.mean([v['comment_ratio'] for v in top_20])
        bottom_comment_ratio = statistics.mean([v['comment_ratio'] for v in bottom_20])
        
        return {
            'top_like_ratio': round(top_like_ratio, 1),
            'bottom_like_ratio': round(bottom_like_ratio, 1),
            'top_comment_ratio': round(top_comment_ratio, 1),
            'bottom_comment_ratio': round(bottom_comment_ratio, 1),
            'insight': f"Top videos get {top_like_ratio:.1f} likes per 1K views vs {bottom_like_ratio:.1f} for bottom"
        }
    
    def _get_top_performers(self, top_10):
        """Format top 10 videos"""
        return [{
            'rank': i + 1,
            'title': v['title'],
            'views': v['views'],
            'views_per_day': int(v['views_per_day']),
            'duration_min': v['duration_minutes'],
            'age_days': v['age_days']
        } for i, v in enumerate(top_10)]
    
    def _analyze_content_patterns(self, top_20, all_videos):
        """Analyze content patterns from titles"""
        # Extract common words from top performers
        top_words = []
        for v in top_20:
            # Remove common stop words
            words = re.findall(r'\b[A-Za-z]{4,}\b', v['title'].lower())
            top_words.extend(words)
        
        # Get most common meaningful words
        common_words = Counter(top_words).most_common(10)
        
        return {
            'trending_keywords': [word for word, count in common_words[:5]],
            'insight': f"Top performing videos often mention: {', '.join([w for w, c in common_words[:3]])}"
        }