"""
Media Synthesis Module
=======================

Third operational pillar: Creates video content from creative direction.
"""

from typing import Dict, List, Optional
from pathlib import Path
import json
from datetime import datetime
from models import CreativeDirection, VideoContent
from config import EngineConfig


class VideoGenerator:
    """Generates video content from creative direction."""
    
    def __init__(self, config: EngineConfig):
        self.config = config
        self.media_config = config.media
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_video(self, direction: CreativeDirection) -> VideoContent:
        """
        Generate video from creative direction.
        
        Args:
            direction: CreativeDirection to generate video from
            
        Returns:
            VideoContent object with video metadata
        """
        # Create video metadata
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        video_filename = f"video_{direction.content_id}_{timestamp}.{self.media_config.video_format}"
        video_path = self.output_dir / video_filename
        
        # Create thumbnail
        thumbnail_filename = f"thumb_{direction.content_id}_{timestamp}.jpg"
        thumbnail_path = self.output_dir / thumbnail_filename
        
        # Calculate total duration from scenes
        total_duration = sum(scene.get('duration', 0) for scene in direction.scenes)
        
        # Generate placeholder video metadata (actual video generation would use moviepy)
        # For this implementation, we create a metadata file representing the video
        video_metadata = {
            'content_id': direction.content_id,
            'creative_direction_id': direction.id,
            'scenes': direction.scenes,
            'voiceover_script': direction.voiceover_script,
            'visual_style': direction.visual_style,
            'music_style': direction.music_style,
            'resolution': self.media_config.video_resolution,
            'fps': self.media_config.video_fps,
            'format': self.media_config.video_format,
            'duration': total_duration,
            'generated_at': timestamp
        }
        
        # Write metadata file
        metadata_path = self.output_dir / f"metadata_{direction.content_id}_{timestamp}.json"
        with open(metadata_path, 'w') as f:
            json.dump(video_metadata, f, indent=2)
        
        # Create VideoContent object
        video = VideoContent(
            content_id=direction.content_id,
            creative_direction_id=direction.id,
            file_path=str(video_path),
            duration_seconds=total_duration,
            resolution=self.media_config.video_resolution,
            format=self.media_config.video_format,
            file_size_mb=self._estimate_file_size(total_duration),
            thumbnail_path=str(thumbnail_path)
        )
        
        return video
    
    def _estimate_file_size(self, duration_seconds: float) -> float:
        """Estimate file size based on duration and quality settings."""
        # Rough estimation: 1080p @ 30fps ≈ 8-12 MB per minute
        mb_per_minute = 10.0
        return (duration_seconds / 60.0) * mb_per_minute


class VideoQualityChecker:
    """Checks video quality and compliance."""
    
    def __init__(self, config: EngineConfig):
        self.config = config
    
    def check_quality(self, video: VideoContent) -> Dict[str, any]:
        """
        Check video quality metrics.
        
        Returns:
            Dict with quality assessment
        """
        issues = []
        warnings = []
        
        # Check duration
        if video.duration_seconds < 10:
            issues.append("Video duration is too short (< 10 seconds)")
        elif video.duration_seconds > 600:
            warnings.append("Video duration is very long (> 10 minutes)")
        
        # Check file size
        if video.file_size_mb > 500:
            warnings.append("Video file size is very large (> 500 MB)")
        
        # Check resolution
        if video.resolution not in ["1920x1080", "1280x720", "3840x2160"]:
            warnings.append(f"Non-standard resolution: {video.resolution}")
        
        quality_score = 100.0
        if issues:
            quality_score -= len(issues) * 20
        if warnings:
            quality_score -= len(warnings) * 5
        
        return {
            'quality_score': max(0, quality_score),
            'issues': issues,
            'warnings': warnings,
            'passed': len(issues) == 0
        }


class MediaSynthesisPillar:
    """
    Third Operational Pillar: Media Synthesis
    
    Creates high-fidelity video content from creative direction,
    ensuring quality and technical specifications are met.
    """
    
    def __init__(self, config: EngineConfig):
        self.config = config
        self.video_generator = VideoGenerator(config)
        self.quality_checker = VideoQualityChecker(config)
    
    def synthesize_video(self, direction: CreativeDirection) -> Dict[str, any]:
        """
        Synthesize video content from creative direction.
        
        Args:
            direction: CreativeDirection to synthesize
            
        Returns:
            Dict containing:
                - success: bool
                - video: VideoContent object
                - quality_report: Quality assessment
        """
        # Generate video
        video = self.video_generator.generate_video(direction)
        
        # Check quality
        quality_report = self.quality_checker.check_quality(video)
        
        success = quality_report['passed']
        
        return {
            'success': success,
            'video': video,
            'quality_report': quality_report
        }
    
    def batch_synthesize(self, directions: List[CreativeDirection]) -> Dict[str, any]:
        """
        Synthesize multiple videos in batch.
        
        Returns:
            Dict with synthesis results
        """
        successful = []
        failed = []
        
        for direction in directions:
            result = self.synthesize_video(direction)
            if result['success']:
                successful.append(result['video'])
            else:
                failed.append({
                    'direction': direction,
                    'issues': result['quality_report']['issues']
                })
        
        return {
            'successful': successful,
            'failed': failed,
            'total': len(directions),
            'success_rate': len(successful) / len(directions) if directions else 0
        }
