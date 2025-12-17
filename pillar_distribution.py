"""
Multi-Platform Distribution Module
===================================

Fifth operational pillar: Distributes content to various platforms.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from models import (
    VideoContent, DistributionPlan, DistributionResult,
    Platform, ViralScore
)
from config import EngineConfig


class ViralPotentialAnalyzer:
    """Analyzes and scores viral potential of content."""
    
    def __init__(self, config: EngineConfig):
        self.config = config
    
    def analyze_viral_potential(self, video: VideoContent, direction_data: Dict) -> ViralScore:
        """
        Analyze viral potential of video content.
        
        Args:
            video: VideoContent to analyze
            direction_data: Creative direction data
            
        Returns:
            ViralScore with detailed scoring
        """
        # Engagement potential (based on duration and pacing)
        engagement = self._calculate_engagement(video, direction_data)
        
        # Shareability (based on content type and appeal)
        shareability = self._calculate_shareability(video, direction_data)
        
        # Emotional impact (based on narrative and messaging)
        emotional_impact = self._calculate_emotional_impact(direction_data)
        
        # Trend alignment (based on keywords and themes)
        trend_alignment = self._calculate_trend_alignment(direction_data)
        
        # Overall score (weighted average)
        overall = (
            engagement * 0.3 +
            shareability * 0.3 +
            emotional_impact * 0.2 +
            trend_alignment * 0.2
        )
        
        reasoning = self._generate_reasoning(
            engagement, shareability, emotional_impact, trend_alignment
        )
        
        return ViralScore(
            overall_score=overall,
            engagement_potential=engagement,
            shareability=shareability,
            emotional_impact=emotional_impact,
            trend_alignment=trend_alignment,
            reasoning=reasoning
        )
    
    def _calculate_engagement(self, video: VideoContent, direction_data: Dict) -> float:
        """Calculate engagement potential."""
        score = 70.0  # Base score
        
        # Optimal duration (30-90 seconds)
        duration = video.duration_seconds
        if 30 <= duration <= 90:
            score += 20
        elif 15 <= duration < 30 or 90 < duration <= 120:
            score += 10
        elif duration < 15:
            score -= 10
        
        # Scene count (more scenes = more dynamic)
        scene_count = len(direction_data.get('scenes', []))
        if scene_count >= 4:
            score += 10
        
        return min(100.0, score)
    
    def _calculate_shareability(self, video: VideoContent, direction_data: Dict) -> float:
        """Calculate shareability score."""
        score = 65.0  # Base score
        
        # Brand compliance increases trust
        if direction_data.get('brand_compliant'):
            score += 15
        
        # Clear call to action
        voiceover = direction_data.get('voiceover_script', '').lower()
        if any(cta in voiceover for cta in ['share', 'subscribe', 'follow', 'like']):
            score += 10
        
        # Visual appeal
        if direction_data.get('visual_style'):
            score += 10
        
        return min(100.0, score)
    
    def _calculate_emotional_impact(self, direction_data: Dict) -> float:
        """Calculate emotional impact score."""
        score = 60.0  # Base score
        
        voiceover = direction_data.get('voiceover_script', '').lower()
        
        # Emotional keywords
        emotional_keywords = [
            'amazing', 'incredible', 'powerful', 'inspiring', 'exciting',
            'discover', 'transform', 'achieve', 'success', 'breakthrough'
        ]
        
        emotion_count = sum(1 for keyword in emotional_keywords if keyword in voiceover)
        score += min(emotion_count * 5, 25)
        
        # Narrative arc quality
        arc_length = len(direction_data.get('narrative_arc', []))
        if arc_length >= 3:
            score += 15
        
        return min(100.0, score)
    
    def _calculate_trend_alignment(self, direction_data: Dict) -> float:
        """Calculate trend alignment score."""
        score = 70.0  # Base score
        
        # Modern visual styles
        visual_style = direction_data.get('visual_style', '').lower()
        if any(trend in visual_style for trend in ['dynamic', 'bold', 'vibrant', 'modern']):
            score += 15
        
        # Music presence
        if direction_data.get('music_style'):
            score += 15
        
        return min(100.0, score)
    
    def _generate_reasoning(self, engagement: float, shareability: float, 
                          emotional: float, trend: float) -> str:
        """Generate reasoning for viral score."""
        parts = []
        
        if engagement >= 80:
            parts.append("High engagement potential due to optimal duration and pacing")
        elif engagement >= 60:
            parts.append("Moderate engagement potential")
        else:
            parts.append("Could improve engagement with better pacing")
        
        if shareability >= 80:
            parts.append("highly shareable content")
        elif shareability >= 60:
            parts.append("decent shareability")
        
        if emotional >= 75:
            parts.append("strong emotional impact")
        
        if trend >= 75:
            parts.append("well-aligned with current trends")
        
        return "; ".join(parts) + "."


class PlatformOptimizer:
    """Optimizes content for different platforms."""
    
    def __init__(self, config: EngineConfig):
        self.config = config
        self.distribution_config = config.distribution
    
    def optimize_for_platform(self, video: VideoContent, platform: Platform) -> Dict[str, Any]:
        """
        Optimize video metadata for specific platform.
        
        Returns:
            Dict with platform-specific optimizations
        """
        optimizations = {
            'platform': platform,
            'video_id': video.id,
            'recommended_caption_length': self._get_caption_length(platform),
            'recommended_hashtags_count': self._get_hashtag_count(platform),
            'optimal_posting_times': self._get_optimal_times(platform),
            'platform_specific_requirements': self._get_requirements(platform)
        }
        
        return optimizations
    
    def _get_caption_length(self, platform: Platform) -> int:
        """Get recommended caption length for platform."""
        lengths = {
            Platform.YOUTUBE: 5000,
            Platform.TIKTOK: 150,
            Platform.INSTAGRAM: 2200,
            Platform.FACEBOOK: 500,
            Platform.LINKEDIN: 1300,
            Platform.TWITTER: 280
        }
        return lengths.get(platform, 500)
    
    def _get_hashtag_count(self, platform: Platform) -> int:
        """Get recommended hashtag count for platform."""
        counts = {
            Platform.YOUTUBE: 15,
            Platform.TIKTOK: 5,
            Platform.INSTAGRAM: 11,
            Platform.FACEBOOK: 3,
            Platform.LINKEDIN: 5,
            Platform.TWITTER: 3
        }
        return counts.get(platform, 5)
    
    def _get_optimal_times(self, platform: Platform) -> List[str]:
        """Get optimal posting times for platform."""
        # General best practices
        times = {
            Platform.YOUTUBE: ["14:00-16:00 weekdays", "09:00-11:00 weekends"],
            Platform.TIKTOK: ["07:00-09:00", "19:00-23:00"],
            Platform.INSTAGRAM: ["11:00-13:00", "19:00-21:00"],
            Platform.FACEBOOK: ["13:00-15:00 weekdays"],
            Platform.LINKEDIN: ["07:00-09:00", "12:00-13:00 weekdays"],
            Platform.TWITTER: ["08:00-10:00", "18:00-21:00"]
        }
        return times.get(platform, ["09:00-17:00"])
    
    def _get_requirements(self, platform: Platform) -> Dict[str, Any]:
        """Get platform-specific requirements."""
        requirements = {
            Platform.YOUTUBE: {
                "min_duration": 1,
                "max_duration": 720,
                "formats": ["mp4", "mov", "avi"],
                "max_file_size_mb": 128000
            },
            Platform.TIKTOK: {
                "min_duration": 3,
                "max_duration": 180,
                "formats": ["mp4", "mov"],
                "max_file_size_mb": 287
            },
            Platform.INSTAGRAM: {
                "min_duration": 3,
                "max_duration": 90,
                "formats": ["mp4", "mov"],
                "max_file_size_mb": 100
            }
        }
        return requirements.get(platform, {})


class DistributionExecutor:
    """Executes content distribution to platforms."""
    
    def __init__(self, config: EngineConfig):
        self.config = config
    
    def distribute(self, plan: DistributionPlan, video: VideoContent) -> List[DistributionResult]:
        """
        Distribute video according to plan.
        
        Args:
            plan: DistributionPlan to execute
            video: VideoContent to distribute
            
        Returns:
            List of DistributionResult objects
        """
        results = []
        
        for platform in plan.platforms:
            result = self._distribute_to_platform(plan, video, platform)
            results.append(result)
        
        return results
    
    def _distribute_to_platform(self, plan: DistributionPlan, 
                                video: VideoContent, platform: Platform) -> DistributionResult:
        """
        Distribute to a specific platform.
        
        Note: In production, this would integrate with platform APIs.
        """
        # Simulate distribution
        caption = plan.captions.get(platform, f"Check out this content! {' '.join(f'#{tag}' for tag in plan.hashtags)}")
        
        # Create result (simulated success)
        result = DistributionResult(
            distribution_plan_id=plan.id,
            platform=platform,
            status="success",
            platform_url=f"https://{platform}.com/video/{video.id}",
            platform_id=f"{platform}_id_{video.id}",
            published_at=datetime.utcnow()
        )
        
        return result


class MultiPlatformDistributionPillar:
    """
    Fifth Operational Pillar: Multi-Platform Distribution
    
    Distributes content across multiple platforms with optimization
    for viral potential and platform-specific requirements.
    """
    
    def __init__(self, config: EngineConfig):
        self.config = config
        self.viral_analyzer = ViralPotentialAnalyzer(config)
        self.platform_optimizer = PlatformOptimizer(config)
        self.distribution_executor = DistributionExecutor(config)
    
    def create_distribution_plan(self, video: VideoContent, 
                                 direction_data: Dict,
                                 platforms: List[Platform],
                                 hashtags: Optional[List[str]] = None) -> DistributionPlan:
        """
        Create a distribution plan for video content.
        
        Args:
            video: VideoContent to distribute
            direction_data: Creative direction data
            platforms: List of platforms to distribute to
            hashtags: Optional list of hashtags
            
        Returns:
            DistributionPlan object
        """
        # Analyze viral potential
        viral_score = self.viral_analyzer.analyze_viral_potential(video, direction_data)
        
        # Generate platform-specific captions
        captions = {}
        for platform in platforms:
            optimization = self.platform_optimizer.optimize_for_platform(video, platform)
            max_length = optimization['recommended_caption_length']
            
            base_caption = direction_data.get('voiceover_script', '')[:max_length]
            captions[platform] = base_caption
        
        # Create distribution plan
        plan = DistributionPlan(
            content_id=video.content_id,
            video_id=video.id,
            platforms=platforms,
            captions=captions,
            hashtags=hashtags or [],
            viral_score=viral_score
        )
        
        return plan
    
    def execute_distribution(self, plan: DistributionPlan, 
                           video: VideoContent) -> Dict[str, Any]:
        """
        Execute distribution plan.
        
        Returns:
            Dict with distribution results
        """
        results = self.distribution_executor.distribute(plan, video)
        
        successful = [r for r in results if r.status == "success"]
        failed = [r for r in results if r.status == "failed"]
        
        return {
            'success': len(failed) == 0,
            'results': results,
            'successful_count': len(successful),
            'failed_count': len(failed),
            'platforms_reached': [r.platform for r in successful]
        }
    
    def get_platform_recommendations(self, video: VideoContent, 
                                    viral_score: ViralScore) -> List[Platform]:
        """
        Get recommended platforms based on content and viral score.
        
        Returns:
            List of recommended platforms
        """
        recommendations = []
        
        # Always recommend YouTube for longer content
        if video.duration_seconds > 60:
            recommendations.append(Platform.YOUTUBE)
        
        # Recommend TikTok and Instagram for short, high-engagement content
        if video.duration_seconds <= 90 and viral_score.engagement_potential >= 70:
            recommendations.extend([Platform.TIKTOK, Platform.INSTAGRAM])
        
        # Recommend LinkedIn for professional content
        if viral_score.overall_score >= 75:
            recommendations.append(Platform.LINKEDIN)
        
        # Always include Facebook for broad reach
        recommendations.append(Platform.FACEBOOK)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for platform in recommendations:
            if platform not in seen:
                seen.add(platform)
                unique_recommendations.append(platform)
        
        return unique_recommendations
