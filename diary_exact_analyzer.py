"""
Diary of a CEO - Exact Methodology Analyzer
Matches the 205-episode analysis with crisp, data-driven insights
"""

import isodate
import re
from datetime import datetime
from collections import Counter, defaultdict
from youtube_analyzer_openai import YouTubeAnalyzer

class DiaryExactAnalyzer(YouTubeAnalyzer):
    
    def categorize_videos(self, videos):
        """Categorize videos and calculate views/day - PODCASTS ONLY"""
        categories = {'shorts': [], 'regular': [], 'podcasts': [], 'all': []}
        
        for video in videos:
            duration = isodate.parse_duration(video['duration']).total_seconds()
            video['duration_seconds'] = duration
            video['duration_minutes'] = duration / 60
            
            # Calculate views per day (CRITICAL METRIC)
            pub_date = datetime.strptime(video['published_at'][:10], '%Y-%m-%d')
            days_old = max(1, (datetime.now() - pub_date).days)
            video['views_per_day'] = video['view_count'] / days_old
            video['days_old'] = days_old
            
            # Categorize
            if duration < 60:
                categories['shorts'].append(video)
            elif duration < 900:  # Less than 15 minutes (changed from 30)
                categories['regular'].append(video)
            else:  # 15+ minutes = podcast/interview content
                categories['podcasts'].append(video)
        
        # CRITICAL: Only analyze podcasts (15+ min videos)
        # This filters out comedy sketches, shorts, and regular videos
        categories['all'] = categories['podcasts']
        
        print(f"\n📊 Video Breakdown:")
        print(f"   Shorts (<1 min): {len(categories['shorts'])}")
        print(f"   Regular (1-15 min): {len(categories['regular'])}")
        print(f"   🎙️ Podcasts/Interviews (15+ min): {len(categories['podcasts'])}")
        print(f"\n✅ Analyzing {len(categories['all'])} podcast/interview episodes only\n")
        
        return categories
    
    def analyze_guest_fame(self, videos):
        """
        INSIGHT 1: Fame analysis
        Extract guests and calculate fame multiplier
        """
        guests = {}
        
        # Extract guest names from titles
        for video in videos:
            guest = self._extract_guest_name(video['title'])
            if guest:
                if guest not in guests:
                    guests[guest] = []
                guests[guest].append(video)
        
        # Calculate performance per guest
        guest_performance = {}
        for guest, vids in guests.items():
            avg_vpd = sum(v['views_per_day'] for v in vids) / len(vids)
            guest_performance[guest] = {
                'videos': vids,
                'count': len(vids),
                'avg_vpd': avg_vpd
            }
        
        # Sort by performance
        sorted_guests = sorted(guest_performance.items(), key=lambda x: x[1]['avg_vpd'], reverse=True)
        
        if len(sorted_guests) >= 6:
            # Split into fame tiers
            total_guests = len(sorted_guests)
            high_fame_cutoff = total_guests // 3
            low_fame_start = total_guests - (total_guests // 3)
            
            high_fame = sorted_guests[:high_fame_cutoff]
            low_fame = sorted_guests[low_fame_start:]
            
            high_avg = sum(g[1]['avg_vpd'] for g in high_fame) / len(high_fame)
            low_avg = sum(g[1]['avg_vpd'] for g in low_fame) / len(low_fame)
            
            high_count = sum(g[1]['count'] for g in high_fame)
            low_count = sum(g[1]['count'] for g in low_fame)
            
            return {
                'high_fame_avg': high_avg,
                'low_fame_avg': low_avg,
                'high_fame_count': high_count,
                'low_fame_count': low_count,
                'multiplier': high_avg / low_avg if low_avg > 0 else 0,
                'total_episodes': len(videos)
            }
        
        return None
    
    def _extract_guest_name(self, title):
        """Extract guest name from title"""
        patterns = [
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)(?:\s*[:|])',
            r'with\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'\|\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title)
            if match:
                return match.group(1).strip()
        return None
    
    def analyze_questions(self, videos):
        """
        INSIGHT 2: Question analysis
        Top vs bottom 20% question count with effect size
        """
        top_20_pct = int(len(videos) * 0.2)
        
        top_videos = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:top_20_pct]
        bottom_videos = sorted(videos, key=lambda x: x['views_per_day'])[:top_20_pct]
        
        # Count questions in titles (proxy for interview questions)
        top_questions = sum(self._count_questions(v['title']) for v in top_videos) / len(top_videos)
        bottom_questions = sum(self._count_questions(v['title']) for v in bottom_videos) / len(bottom_videos)
        
        # Calculate effect size (Cohen's d)
        multiplier = top_questions / bottom_questions if bottom_questions > 0 else 0
        
        # Use actual question marks count (no scaling)
        effect_size = abs(top_questions - bottom_questions) / max(bottom_questions, 0.1)
        
        return {
            'top_avg': top_questions,
            'bottom_avg': bottom_questions,
            'multiplier': multiplier,
            'effect_size': effect_size
        }
    
    def _count_questions(self, title):
        """Count actual questions in title"""
        return title.count('?')
    
    def analyze_title_structure(self, videos):
        """
        INSIGHT 3: Title structure
        Name/frame: claim pattern analysis
        """
        top_20_pct = int(len(videos) * 0.2)
        top_videos = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:top_20_pct]
        
        # Check for colons and structured titles
        name_frame_count = 0
        colon_count = 0
        
        for video in top_videos:
            title = video['title']
            
            # Check if title has a colon
            if ':' in title or '|' in title or ' - ' in title:
                colon_count += 1
                # If it has structure, likely name/frame pattern
                name_frame_count += 1
        
        name_frame_pct = (name_frame_count / len(top_videos)) * 100
        colon_pct = (colon_count / len(top_videos)) * 100
        
        return {
            'name_frame_pct': name_frame_pct,
            'colon_pct': colon_pct,
            'sample_size': len(top_videos)
        }
    
    def analyze_title_length(self, videos):
        """
        INSIGHT 4: Title length
        Character and word count analysis
        """
        top_20_pct = int(len(videos) * 0.2)
        
        top_videos = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:top_20_pct]
        bottom_videos = sorted(videos, key=lambda x: x['views_per_day'])[:top_20_pct]
        
        top_chars = sum(len(v['title']) for v in top_videos) / len(top_videos)
        bottom_chars = sum(len(v['title']) for v in bottom_videos) / len(bottom_videos)
        
        top_words = sum(len(v['title'].split()) for v in top_videos) / len(top_videos)
        bottom_words = sum(len(v['title'].split()) for v in bottom_videos) / len(bottom_videos)
        
        char_diff = top_chars - bottom_chars
        
        return {
            'top_chars': top_chars,
            'bottom_chars': bottom_chars,
            'top_words': top_words,
            'bottom_words': bottom_words,
            'char_diff': char_diff
        }
    
    def analyze_duration_buckets(self, videos):
        """
        INSIGHT 5: Duration sweet spot
        Bucket videos by duration and find sweet spot
        """
        buckets = {
            '30-60 min': (30, 60),
            '60-90 min': (60, 90),
            '90-120 min': (90, 120),
            '120-150 min': (120, 150),
            '150+ min': (150, 999999)
        }
        
        bucket_data = {name: [] for name in buckets.keys()}
        
        for video in videos:
            duration_min = video['duration_minutes']
            for bucket_name, (min_dur, max_dur) in buckets.items():
                if min_dur <= duration_min < max_dur:
                    bucket_data[bucket_name].append(video)
                    break
        
        # Calculate stats
        bucket_stats = {}
        for bucket_name, vids in bucket_data.items():
            if vids:
                avg_vpd = sum(v['views_per_day'] for v in vids) / len(vids)
                bucket_stats[bucket_name] = {
                    'count': len(vids),
                    'avg_vpd': avg_vpd
                }
        
        # Find sweet spot with MINIMUM SAMPLE SIZE requirement
        # Only consider buckets with at least 5 videos
        MIN_SAMPLE_SIZE = 5
        
        valid_buckets = {k: v for k, v in bucket_stats.items() if v['count'] >= MIN_SAMPLE_SIZE}
        
        if valid_buckets:
            # Sweet spot = highest performing bucket with enough sample size
            sweet_spot = max(valid_buckets.items(), key=lambda x: x[1]['avg_vpd'])
            
            # Calculate multiplier vs longest bucket (if it exists)
            longest = bucket_stats.get('150+ min', {'avg_vpd': 1})
            multiplier = sweet_spot[1]['avg_vpd'] / longest['avg_vpd'] if longest['avg_vpd'] > 0 else 0
            
            return {
                'sweet_spot_name': sweet_spot[0],
                'sweet_spot_vpd': sweet_spot[1]['avg_vpd'],
                'sweet_spot_count': sweet_spot[1]['count'],
                'all_buckets': bucket_stats,
                'multiplier_vs_longest': multiplier,
                'min_sample_size': MIN_SAMPLE_SIZE
            }
        else:
            # No bucket has enough samples - return the one with most videos
            if bucket_stats:
                sweet_spot = max(bucket_stats.items(), key=lambda x: x[1]['count'])
                return {
                    'sweet_spot_name': sweet_spot[0],
                    'sweet_spot_vpd': sweet_spot[1]['avg_vpd'],
                    'sweet_spot_count': sweet_spot[1]['count'],
                    'all_buckets': bucket_stats,
                    'multiplier_vs_longest': 1,
                    'min_sample_size': MIN_SAMPLE_SIZE,
                    'insufficient_data': True
                }
            
        return None
    
    def analyze_topics(self, videos):
        """
        INSIGHT 6: Topic framing
        Crime/espionage vs health vs wealth
        """
        topic_keywords = {
            'crime/espionage': ['crime', 'spy', 'espionage', 'detective', 'murder', 'fbi', 'cia', 'secret', 'undercover', 'police', 'investigation'],
            'health': ['health', 'fitness', 'doctor', 'medical', 'sleep', 'diet', 'nutrition', 'workout', 'brain', 'body'],
            'wealth': ['wealth', 'rich', 'millionaire', 'billionaire', 'money', 'business', 'entrepreneur', 'ceo', 'invest', 'finance'],
            'science': ['science', 'physics', 'biology', 'space', 'universe', 'research', 'study', 'ai', 'tech'],
            'mindset': ['mindset', 'psychology', 'mental', 'motivation', 'success', 'habit', 'productivity']
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
        
        # Calculate stats
        topic_stats = {}
        for topic, vids in topic_videos.items():
            if vids:
                avg_vpd = sum(v['views_per_day'] for v in vids) / len(vids)
                topic_stats[topic] = {
                    'count': len(vids),
                    'avg_vpd': avg_vpd
                }
        
        # Calculate multipliers
        if 'crime/espionage' in topic_stats and 'health' in topic_stats:
            crime_vpd = topic_stats['crime/espionage']['avg_vpd']
            health_vpd = topic_stats['health']['avg_vpd']
            multiplier = crime_vpd / health_vpd if health_vpd > 0 else 0
            
            topic_stats['crime_vs_health_multiplier'] = multiplier
        
        # Sort by performance
        sorted_topics = sorted(
            [(k, v) for k, v in topic_stats.items() if k != 'crime_vs_health_multiplier'],
            key=lambda x: x[1]['avg_vpd'],
            reverse=True
        )
        
        return {
            'topics': sorted_topics,
            'multiplier': topic_stats.get('crime_vs_health_multiplier', 0)
        }
    
    def analyze_hook_types(self, videos):
        """
        INSIGHT 7: Hook types
        Proof-first vs pain-first
        """
        top_20_pct = int(len(videos) * 0.2)
        
        top_videos = sorted(videos, key=lambda x: x['views_per_day'], reverse=True)[:top_20_pct]
        bottom_videos = sorted(videos, key=lambda x: x['views_per_day'])[:top_20_pct]
        
        proof_keywords = ['expert', 'doctor', 'professor', 'ceo', 'billionaire', 'scientist', 'olympian', 'champion', 'founder', 'author']
        pain_keywords = ['struggle', 'problem', 'fix', 'solve', 'help', 'mistake', 'wrong', 'failed', 'losing', 'broken']
        
        def has_proof_hook(title):
            return any(kw in title.lower() for kw in proof_keywords)
        
        def has_pain_hook(title):
            return any(kw in title.lower() for kw in pain_keywords)
        
        top_proof = sum(has_proof_hook(v['title']) for v in top_videos) / len(top_videos) * 100
        top_pain = sum(has_pain_hook(v['title']) for v in top_videos) / len(top_videos) * 100
        
        bottom_proof = sum(has_proof_hook(v['title']) for v in bottom_videos) / len(bottom_videos) * 100
        bottom_pain = sum(has_pain_hook(v['title']) for v in bottom_videos) / len(bottom_videos) * 100
        
        return {
            'top_proof_pct': top_proof,
            'top_pain_pct': top_pain,
            'bottom_proof_pct': bottom_proof,
            'bottom_pain_pct': bottom_pain
        }
