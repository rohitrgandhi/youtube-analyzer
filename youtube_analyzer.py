from googleapiclient.discovery import build
from openai import OpenAI
import isodate
from datetime import datetime
from collections import Counter
import re

class YouTubeAnalyzer:
    def __init__(self, youtube_api_key, openai_api_key):
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        self.openai = OpenAI(api_key=openai_api_key)
    
    def get_channel_id(self, channel_handle):
        """Get channel ID from handle or username"""
        handle = channel_handle.replace('@', '')
        
        try:
            # Try search first - this is the most reliable method
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
        
        try:
            # Get uploads playlist
            channel_request = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            )
            channel_response = channel_request.execute()
            
            if not channel_response.get('items'):
                return []
            
            uploads_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Fetch videos
            next_token = None
            while len(videos) < max_results:
                playlist_request = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=uploads_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_token
                )
                playlist_response = playlist_request.execute()
                
                video_ids = [item['contentDetails']['videoId'] for item in playlist_response.get('items', [])]
                
                if not video_ids:
                    break
                
                # Get video details
                video_request = self.youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(video_ids)
                )
                video_response = video_request.execute()
                
                for item in video_response.get('items', []):
                    duration = isodate.parse_duration(item['contentDetails']['duration']).total_seconds()
                    pub_date = datetime.strptime(item['snippet']['publishedAt'][:10], '%Y-%m-%d')
                    days_old = max(1, (datetime.now() - pub_date).days)
                    
                    video_data = {
                        'id': item['id'],
                        'title': item['snippet']['title'],
                        'published_at': item['snippet']['publishedAt'],
                        'views': int(item['statistics'].get('viewCount', 0)),
                        'likes': int(item['statistics'].get('likeCount', 0)),
                        'comments': int(item['statistics'].get('commentCount', 0)),
                        'duration_seconds': duration,
                        'duration_minutes': duration / 60,
                        'days_old': days_old,
                        'views_per_day': int(item['statistics'].get('viewCount', 0)) / days_old
                    }
                    videos.append(video_data)
                
                next_token = playlist_response.get('nextPageToken')
                if not next_token:
                    break
            
            return videos
        
        except Exception as e:
            print(f"Error fetching videos: {e}")
            return []
    
    def analyze_videos(self, videos):
        """Analyze video performance"""
        if not videos:
            return {}
        
        # Sort by performance
        sorted_videos = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)
        top_20_pct = max(1, len(videos) // 5)
        
        top_videos = sorted_videos[:top_20_pct]
        bottom_videos = sorted_videos[-top_20_pct:]
        
        # Calculate metrics
        top_avg_vpd = sum(v['views_per_day'] for v in top_videos) / len(top_videos)
        bottom_avg_vpd = sum(v['views_per_day'] for v in bottom_videos) / len(bottom_videos)
        
        # Title analysis
        top_title_len = sum(len(v['title']) for v in top_videos) / len(top_videos)
        bottom_title_len = sum(len(v['title']) for v in bottom_videos) / len(bottom_videos)
        
        # Duration buckets
        duration_buckets = {}
        for v in videos:
            if v['duration_minutes'] < 1:
                bucket = "Shorts (<1min)"
            elif v['duration_minutes'] < 10:
                bucket = "Short (1-10min)"
            elif v['duration_minutes'] < 30:
                bucket = "Medium (10-30min)"
            else:
                bucket = "Long (30min+)"
            
            if bucket not in duration_buckets:
                duration_buckets[bucket] = []
            duration_buckets[bucket].append(v['views_per_day'])
        
        duration_stats = {
            k: sum(v) / len(v) for k, v in duration_buckets.items() if v
        }
        
        return {
            'performance_gap': top_avg_vpd / bottom_avg_vpd if bottom_avg_vpd > 0 else 0,
            'top_avg_vpd': top_avg_vpd,
            'bottom_avg_vpd': bottom_avg_vpd,
            'top_title_length': top_title_len,
            'bottom_title_length': bottom_title_len,
            'duration_stats': duration_stats,
            'top_videos': top_videos[:10],
            'total_videos': len(videos)
        }