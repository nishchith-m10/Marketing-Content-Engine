"""
Data Models
===========

Core data models for the Marketing Content Engine.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class ContentType(str, Enum):
    """Types of content that can be processed."""
    EDUCATIONAL = "educational"
    MARKETING = "marketing"
    PROMOTIONAL = "promotional"
    TUTORIAL = "tutorial"
    ADVERTISEMENT = "advertisement"


class ContentStatus(str, Enum):
    """Status of content in the pipeline."""
    DRAFT = "draft"
    INGESTED = "ingested"
    CREATIVE_REVIEW = "creative_review"
    SYNTHESIZING = "synthesizing"
    REVIEW = "review"
    APPROVED = "approved"
    DISTRIBUTED = "distributed"
    PUBLISHED = "published"
    FAILED = "failed"


class Platform(str, Enum):
    """Supported distribution platforms."""
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"


class ContentIdea(BaseModel):
    """Input content idea from user."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    content_type: ContentType
    target_audience: str = ""
    key_messages: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    duration_seconds: int = 60
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CreativeDirection(BaseModel):
    """Creative direction generated for content."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_id: str
    visual_style: str
    narrative_arc: List[str] = Field(default_factory=list)
    scenes: List[Dict[str, Any]] = Field(default_factory=list)
    music_style: str = ""
    voiceover_script: str = ""
    brand_compliant: bool = True
    compliance_notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VideoContent(BaseModel):
    """Synthesized video content."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_id: str
    creative_direction_id: str
    file_path: str
    duration_seconds: float
    resolution: str
    format: str
    file_size_mb: float = 0.0
    thumbnail_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ViralScore(BaseModel):
    """Viral potential score for content."""
    overall_score: float = Field(ge=0.0, le=100.0)
    engagement_potential: float = Field(ge=0.0, le=100.0)
    shareability: float = Field(ge=0.0, le=100.0)
    emotional_impact: float = Field(ge=0.0, le=100.0)
    trend_alignment: float = Field(ge=0.0, le=100.0)
    reasoning: str = ""


class DistributionPlan(BaseModel):
    """Distribution plan for content across platforms."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_id: str
    video_id: str
    platforms: List[Platform]
    scheduled_time: Optional[datetime] = None
    captions: Dict[Platform, str] = Field(default_factory=dict)
    hashtags: List[str] = Field(default_factory=list)
    viral_score: Optional[ViralScore] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DistributionResult(BaseModel):
    """Result of distributing content to a platform."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    distribution_plan_id: str
    platform: Platform
    status: str  # "success", "failed", "pending"
    platform_url: Optional[str] = None
    platform_id: Optional[str] = None
    error_message: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Campaign(BaseModel):
    """A marketing campaign containing multiple content pieces."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    content_ids: List[str] = Field(default_factory=list)
    status: ContentStatus = ContentStatus.DRAFT
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
