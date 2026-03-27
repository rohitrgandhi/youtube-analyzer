"""
YouTube Analyzer Base Class with OpenAI Integration
Enhanced with better pagination for fetching more videos
"""

from googleapiclient.discovery import build
from openai import OpenAI

class YouTubeAnalyzer:
    def __init__(self, youtube_api_key, openai_api_key, model="gpt-4o"):
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.model = model
    
    def get_channel_id(self, channel_handle):
        """Get channel ID from handle or username"""
        # Remove @ if present
        handle = channel_handle.replace('@', '')
        
        try:
            # Try as handle first
            request = self.youtube.channels().list(
                part='id',
                forHandle=handle
            )
            response = request.execute()
            
            if response.get('items'):
                return response['items'][0]['id']
            
            # Try as username
            request = self.youtube.channels().list(
                part='id',
                forUsername=handle
            )
            response = request.execute()
            
            if response.get('items'):
                return response['items'][0]['id']
            
            # Try searching
            request = self.youtube.search().list(
                part='snippet',
                q=channel_handle,
                type='channel',
                maxResults=1
            )
            response = request.execute()
            
            if response.get('items'):
                return response['items'][0]['snippet']['channelId']
            
            return None
            
        except Exception as e:
            print(f"Error finding channel: {e}")
            return None
    
    def get_all_videos(self, channel_id, max_results=100):
        """
        Fetch videos from channel with proper pagination
        YouTube API returns max 50 per page, so we need to paginate
        """
        videos = []
        next_page_token = None
        
        # Calculate how many requests we need
        # YouTube max is 50 per request
        requests_needed = (max_results // 50) + (1 if max_results % 50 > 0 else 0)
        
        print(f"\nFetching up to {max_results} videos...")
        print(f"This will take {requests_needed} API request(s)...\n")
        
        for request_num in range(requests_needed):
            try:
                # Get videos from uploads playlist
                # First, get the uploads playlist ID
                if request_num == 0:
                    channel_request = self.youtube.channels().list(
                        part='contentDetails',
                        id=channel_id
                    )
                    channel_response = channel_request.execute()
                    
                    if not channel_response.get('items'):
                        print("Channel not found!")
                        return []
                    
                    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                
                # Fetch playlist items
                results_this_page = min(50, max_results - len(videos))
                
                playlist_request = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=uploads_playlist_id,
                    maxResults=results_this_page,
                    pageToken=next_page_token
                )
                playlist_response = playlist_request.execute()
                
                # Get video IDs
                video_ids = [item['contentDetails']['videoId'] for item in playlist_response.get('items', [])]
                
                if not video_ids:
                    print(f"No more videos found (page {request_num + 1})")
                    break
                
                # Get video details
                video_request = self.youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(video_ids)
                )
                video_response = video_request.execute()
                
                # Process videos
                for item in video_response.get('items', []):
                    video_data = {
                        'video_id': item['id'],
                        'title': item['snippet']['title'],
                        'published_at': item['snippet']['publishedAt'],
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'like_count': int(item['statistics'].get('likeCount', 0)),
                        'comment_count': int(item['statistics'].get('commentCount', 0)),
                        'duration': item['contentDetails']['duration']
                    }
                    videos.append(video_data)
                
                print(f"✓ Fetched {len(videos)} videos so far...")
                
                # Check if there's a next page
                next_page_token = playlist_response.get('nextPageToken')
                
                # Stop if we've got enough or no more pages
                if len(videos) >= max_results or not next_page_token:
                    break
                    
            except Exception as e:
                print(f"Error fetching videos (page {request_num + 1}): {e}")
                break
        
        print(f"\n✅ Total videos fetched: {len(videos)}\n")
        return videos
    
    def analyze_with_openai(self, prompt, temperature=0.7):
        """Use OpenAI to analyze data"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a YouTube analytics expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
