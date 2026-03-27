import isodate
import re
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from youtube_analyzer_openai import YouTubeAnalyzer

class ComprehensiveAnalyzer(YouTubeAnalyzer):
    
    def categorize_videos(self, videos):
        """Categorize videos by duration"""
        categories = {'shorts': [], 'regular': [], 'podcasts': [], 'all': videos}
        
        for video in videos:
            duration = isodate.parse_duration(video['duration']).total_seconds()
            video['duration_seconds'] = duration
            video['duration_minutes'] = duration / 60
            
            # Calculate views per day
            pub_date = datetime.strptime(video['published_at'][:10], '%Y-%m-%d')
            days_old = max(1, (datetime.now() - pub_date).days)
            video['views_per_day'] = video['view_count'] / days_old
            video['days_old'] = days_old
            
            if duration < 60:
                categories['shorts'].append(video)
            elif duration < 1800:
                categories['regular'].append(video)
            else:
                categories['podcasts'].append(video)
        
        return categories
    
    def analyze_titles(self, videos):
        """Deep title analysis"""
        top_20 = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:max(1, len(videos)//5)]
        bottom_20 = sorted(videos, key=lambda x: x['views_per_day'])[:max(1, len(videos)//5)]
        
        def analyze_group(vids):
            return {
                'avg_length_chars': sum(len(v['title']) for v in vids) / len(vids),
                'avg_length_words': sum(len(v['title'].split()) for v in vids) / len(vids),
                'colon_pct': sum(':' in v['title'] for v in vids) / len(vids) * 100,
                'question_pct': sum('?' in v['title'] for v in vids) / len(vids) * 100,
                'exclamation_pct': sum('!' in v['title'] for v in vids) / len(vids) * 100,
                'number_pct': sum(bool(re.search(r'\d', v['title'])) for v in vids) / len(vids) * 100,
                'all_caps_words': sum(sum(1 for word in v['title'].split() if word.isupper() and len(word) > 1) for v in vids) / len(vids),
            }
        
        top_stats = analyze_group(top_20)
        bottom_stats = analyze_group(bottom_20)
        
        # Find common words in top performers
        top_words = ' '.join(v['title'].lower() for v in top_20).split()
        word_freq = Counter(top_words)
        common_words = [w for w, c in word_freq.most_common(20) if len(w) > 3]
        
        return {
            'top': top_stats,
            'bottom': bottom_stats,
            'common_words': common_words[:10]
        }
    
    def extract_topics_simple(self, videos):
        """Extract topics from titles (simple keyword extraction)"""
        # Common topic keywords
        topic_keywords = {
            'money': ['money', 'wealth', 'rich', 'millionaire', 'billionaire', 'financial', 'invest', 'business'],
            'health': ['health', 'fitness', 'workout', 'diet', 'sleep', 'doctor', 'medical'],
            'relationships': ['love', 'relationship', 'dating', 'marriage', 'breakup', 'toxic'],
            'success': ['success', 'motivation', 'mindset', 'productivity', 'habit', 'goal'],
            'tech': ['ai', 'tech', 'technology', 'software', 'coding', 'startup'],
            'life': ['life', 'advice', 'tips', 'lesson', 'mistake', 'change'],
            'psychology': ['psychology', 'mind', 'brain', 'mental', 'think', 'behavior'],
        }
        
        topic_videos = defaultdict(list)
        
        for video in videos:
            title_lower = video['title'].lower()
            matched = False
            
            for topic, keywords in topic_keywords.items():
                if any(kw in title_lower for kw in keywords):
                    topic_videos[topic].append(video)
                    matched = True
                    break
            
            if not matched:
                topic_videos['other'].append(video)
        
        # Calculate avg views/day per topic
        topic_stats = {}
        for topic, vids in topic_videos.items():
            if vids:
                avg_vpd = sum(v['views_per_day'] for v in vids) / len(vids)
                topic_stats[topic] = {
                    'count': len(vids),
                    'avg_views_per_day': avg_vpd,
                    'videos': vids
                }
        
        # Sort by performance
        sorted_topics = sorted(topic_stats.items(), key=lambda x: x[1]['avg_views_per_day'], reverse=True)
        
        return dict(sorted_topics)
    
    def analyze_duration_sweet_spot(self, videos):
        """Find optimal video duration"""
        if not videos:
            return {}
        
        # Create duration buckets
        buckets = {
            '0-30s': [],
            '30-60s': [],
            '1-5min': [],
            '5-15min': [],
            '15-30min': [],
            '30-60min': [],
            '60-90min': [],
            '90-120min': [],
            '120min+': []
        }
        
        for v in videos:
            duration_min = v['duration_minutes']
            if duration_min < 0.5:
                buckets['0-30s'].append(v)
            elif duration_min < 1:
                buckets['30-60s'].append(v)
            elif duration_min < 5:
                buckets['1-5min'].append(v)
            elif duration_min < 15:
                buckets['5-15min'].append(v)
            elif duration_min < 30:
                buckets['15-30min'].append(v)
            elif duration_min < 60:
                buckets['30-60min'].append(v)
            elif duration_min < 90:
                buckets['60-90min'].append(v)
            elif duration_min < 120:
                buckets['90-120min'].append(v)
            else:
                buckets['120min+'].append(v)
        
        bucket_stats = {}
        for bucket_name, vids in buckets.items():
            if vids:
                bucket_stats[bucket_name] = {
                    'count': len(vids),
                    'avg_views_per_day': sum(v['views_per_day'] for v in vids) / len(vids)
                }
        
        # Find sweet spot
        if bucket_stats:
            sweet_spot = max(bucket_stats.items(), key=lambda x: x[1]['avg_views_per_day'])
            return {
                'buckets': bucket_stats,
                'sweet_spot': sweet_spot[0],
                'sweet_spot_vpd': sweet_spot[1]['avg_views_per_day']
            }
        
        return {}
    
    def analyze_publishing_patterns(self, videos):
        """Analyze best day/time to publish"""
        day_stats = defaultdict(list)
        
        for v in videos:
            pub_date = datetime.strptime(v['published_at'], '%Y-%m-%dT%H:%M:%SZ')
            day_name = pub_date.strftime('%A')
            day_stats[day_name].append(v['views_per_day'])
        
        day_averages = {day: sum(vpds)/len(vpds) for day, vpds in day_stats.items()}
        sorted_days = sorted(day_averages.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'best_day': sorted_days[0] if sorted_days else ('Unknown', 0),
            'all_days': sorted_days
        }
    
    def find_title_formulas(self, videos):
        """Identify winning title patterns"""
        top_10 = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:10]
        
        patterns = []
        for v in top_10:
            title = v['title']
            pattern = ""
            
            # Check for colon structure
            if ':' in title:
                pattern = "X: Y format"
            elif '|' in title:
                pattern = "X | Y format"
            elif '?' in title:
                pattern = "Question format"
            elif any(word.isupper() for word in title.split() if len(word) > 2):
                pattern = "CAPS emphasis"
            elif re.search(r'\d+', title):
                pattern = "Number-driven"
            else:
                pattern = "Direct statement"
            
            patterns.append({
                'title': title,
                'views_per_day': v['views_per_day'],
                'pattern': pattern
            })
        
        return patterns
