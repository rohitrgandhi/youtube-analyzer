"""
Clean YouTube Analyzer - API Data Only
7 Reliable Insights Based on Available Data
"""

import isodate
import re
from datetime import datetime
from collections import Counter, defaultdict
from youtube_analyzer_openai import YouTubeAnalyzer

class CleanAnalyzer(YouTubeAnalyzer):
    
    def categorize_videos(self, videos):
        """Calculate metrics and separate shorts from videos"""
        shorts = []
        regular_videos = []
        
        for video in videos:
            duration = isodate.parse_duration(video['duration']).total_seconds()
            video['duration_seconds'] = duration
            video['duration_minutes'] = duration / 60
            
            # Views per day
            pub_date = datetime.strptime(video['published_at'][:10], '%Y-%m-%d')
            days_old = max(1, (datetime.now() - pub_date).days)
            video['views_per_day'] = video['view_count'] / days_old
            video['days_old'] = days_old
            
            # Engagement metrics
            if video['view_count'] > 0:
                video['like_rate'] = (video['like_count'] / video['view_count']) * 100
                video['comment_rate'] = (video['comment_count'] / video['view_count']) * 1000
                video['engagement_score'] = (video['like_count'] + video['comment_count']) / video['view_count'] * 100
            else:
                video['like_rate'] = 0
                video['comment_rate'] = 0
                video['engagement_score'] = 0
            
            # Publishing data
            video['publish_day'] = pub_date.strftime('%A')
            video['publish_hour'] = pub_date.hour
            
            # Categorize: Shorts vs Regular Videos
            # Shorts are typically under 60 seconds
            if duration <= 60:
                video['type'] = 'short'
                shorts.append(video)
            else:
                video['type'] = 'video'
                regular_videos.append(video)
        
        print(f"\n�� Content Breakdown:")
        print(f"   🎬 Shorts (≤60s): {len(shorts)}")
        print(f"   📹 Videos (>60s): {len(regular_videos)}")
        print(f"   📦 Total: {len(videos)}\n")
        
        return {
            'all': videos,
            'shorts': shorts,
            'videos': regular_videos
        }
    
    def insight_1_performance_gap(self, videos):
        """Top 20% vs bottom 20% performance"""
        top_20_pct = max(1, len(videos) // 5)
        
        top = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:top_20_pct]
        bottom = sorted(videos, key=lambda x: x['views_per_day'])[:top_20_pct]
        
        top_avg = sum(v['views_per_day'] for v in top) / len(top)
        bottom_avg = sum(v['views_per_day'] for v in bottom) / len(bottom)
        
        return {
            'top_avg': top_avg,
            'bottom_avg': bottom_avg,
            'multiplier': top_avg / bottom_avg if bottom_avg > 0 else 0,
            'top_count': len(top),
            'bottom_count': len(bottom)
        }
    
    def insight_2_title_length(self, videos):
        """Title length analysis"""
        top_20_pct = max(1, len(videos) // 5)
        
        top = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:top_20_pct]
        bottom = sorted(videos, key=lambda x: x['views_per_day'])[:top_20_pct]
        
        top_chars = sum(len(v['title']) for v in top) / len(top)
        bottom_chars = sum(len(v['title']) for v in bottom) / len(bottom)
        
        top_words = sum(len(v['title'].split()) for v in top) / len(top)
        bottom_words = sum(len(v['title'].split()) for v in bottom) / len(bottom)
        
        return {
            'top_chars': top_chars,
            'bottom_chars': bottom_chars,
            'top_words': top_words,
            'bottom_words': bottom_words,
            'char_diff': top_chars - bottom_chars
        }
    
    def insight_3_title_patterns(self, videos):
        """Title pattern detection"""
        top_20_pct = max(1, len(videos) // 5)
        
        top = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:top_20_pct]
        bottom = sorted(videos, key=lambda x: x['views_per_day'])[:top_20_pct]
        
        def analyze_title(title):
            return {
                'has_question': '?' in title,
                'has_colon': ':' in title,
                'has_pipe': '|' in title,
                'has_number': bool(re.search(r'\d', title)),
                'has_caps': bool(re.search(r'[A-Z]{3,}', title))
            }
        
        top_patterns = [analyze_title(v['title']) for v in top]
        bottom_patterns = [analyze_title(v['title']) for v in bottom]
        
        return {
            'top_question_pct': sum(p['has_question'] for p in top_patterns) / len(top_patterns) * 100,
            'bottom_question_pct': sum(p['has_question'] for p in bottom_patterns) / len(bottom_patterns) * 100,
            'top_colon_pct': sum(p['has_colon'] for p in top_patterns) / len(top_patterns) * 100,
            'bottom_colon_pct': sum(p['has_colon'] for p in bottom_patterns) / len(bottom_patterns) * 100,
            'top_number_pct': sum(p['has_number'] for p in top_patterns) / len(top_patterns) * 100,
            'bottom_number_pct': sum(p['has_number'] for p in bottom_patterns) / len(bottom_patterns) * 100
        }
    
    def insight_4_duration_buckets(self, videos):
        """Duration sweet spot"""
        buckets = {
            '0-5 min': (0, 5),
            '5-15 min': (5, 15),
            '15-30 min': (15, 30),
            '30-60 min': (30, 60),
            '60-90 min': (60, 90),
            '90+ min': (90, 999999)
        }
        
        bucket_data = {name: [] for name in buckets.keys()}
        
        for video in videos:
            duration_min = video['duration_minutes']
            for bucket_name, (min_dur, max_dur) in buckets.items():
                if min_dur <= duration_min < max_dur:
                    bucket_data[bucket_name].append(video)
                    break
        
        bucket_stats = {}
        for bucket_name, vids in bucket_data.items():
            if vids:
                avg_vpd = sum(v['views_per_day'] for v in vids) / len(vids)
                bucket_stats[bucket_name] = {
                    'count': len(vids),
                    'avg_vpd': avg_vpd
                }
        
        # Find sweet spot: bucket with highest count (minimum 5 videos)
        valid_buckets = {k: v for k, v in bucket_stats.items() if v['count'] >= 5}
        
        if valid_buckets:
            # Pick the bucket with the MOST videos (highest count)
            sweet_spot = max(valid_buckets.items(), key=lambda x: x[1]['count'])
            return {
                'sweet_spot_name': sweet_spot[0],
                'sweet_spot_vpd': sweet_spot[1]['avg_vpd'],
                'sweet_spot_count': sweet_spot[1]['count'],
                'all_buckets': bucket_stats
            }
        
        return None
    
    def insight_5_engagement(self, videos):
        """Engagement analysis"""
        top_20_pct = max(1, len(videos) // 5)
        
        top = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:top_20_pct]
        bottom = sorted(videos, key=lambda x: x['views_per_day'])[:top_20_pct]
        
        top_like_rate = sum(v['like_rate'] for v in top) / len(top)
        bottom_like_rate = sum(v['like_rate'] for v in bottom) / len(bottom)
        
        top_comment_rate = sum(v['comment_rate'] for v in top) / len(top)
        bottom_comment_rate = sum(v['comment_rate'] for v in bottom) / len(bottom)
        
        return {
            'top_like_rate': top_like_rate,
            'bottom_like_rate': bottom_like_rate,
            'top_comment_rate': top_comment_rate,
            'bottom_comment_rate': bottom_comment_rate
        }
    
    def insight_6_publishing(self, videos):
        """Best day/time to publish"""
        day_performance = defaultdict(list)
        hour_performance = defaultdict(list)
        
        for video in videos:
            day_performance[video['publish_day']].append(video['views_per_day'])
            hour_performance[video['publish_hour']].append(video['views_per_day'])
        
        day_avg = {day: sum(vpds)/len(vpds) for day, vpds in day_performance.items()}
        hour_avg = {hour: sum(vpds)/len(vpds) for hour, vpds in hour_performance.items()}
        
        best_day = max(day_avg.items(), key=lambda x: x[1]) if day_avg else ('Unknown', 0)
        best_hour = max(hour_avg.items(), key=lambda x: x[1]) if hour_avg else (0, 0)
        
        return {
            'best_day': best_day[0],
            'best_day_vpd': best_day[1],
            'day_breakdown': dict(sorted(day_avg.items(), key=lambda x: x[1], reverse=True)),
            'best_hour': best_hour[0],
            'best_hour_vpd': best_hour[1]
        }
    
    def insight_7_keywords(self, videos):
        """Top performing keywords"""
        top_20_pct = max(1, len(videos) // 5)
        top = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:top_20_pct]
        
        # Extract keywords from top videos
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'my', 'your', 'this', 'that', 'i', 'you', 'we'}
        
        keyword_counts = Counter()
        for video in top:
            words = re.findall(r'\w+', video['title'].lower())
            for word in words:
                if len(word) > 3 and word not in stop_words:
                    keyword_counts[word] += 1
        
        top_keywords = keyword_counts.most_common(10)
        
        return {
            'keywords': top_keywords
        }
