"""
Marketing Content Engine
=========================

Core configuration and settings management for the content engine.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from pathlib import Path
import yaml
import os


class BrandConfig(BaseModel):
    """Brand configuration for content generation."""
    name: str
    colors: List[str] = Field(default_factory=list)
    fonts: List[str] = Field(default_factory=list)
    tone: str = "professional"
    voice: str = "engaging"
    guidelines: str = ""


class AIConfig(BaseModel):
    """AI model configuration."""
    provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000


class MediaConfig(BaseModel):
    """Media synthesis configuration."""
    video_resolution: str = "1920x1080"
    video_fps: int = 30
    video_format: str = "mp4"
    audio_bitrate: str = "192k"


class DistributionConfig(BaseModel):
    """Multi-platform distribution configuration."""
    platforms: List[str] = Field(default_factory=list)
    auto_publish: bool = False
    scheduling_enabled: bool = True


class EngineConfig(BaseModel):
    """Main engine configuration."""
    brand: BrandConfig
    ai: AIConfig = Field(default_factory=AIConfig)
    media: MediaConfig = Field(default_factory=MediaConfig)
    distribution: DistributionConfig = Field(default_factory=DistributionConfig)
    output_dir: str = "./output"
    state_db_path: str = "./state.db"


class ConfigManager:
    """Manages configuration loading and access."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.getenv("ENGINE_CONFIG_PATH", "./config.yaml")
        self.config: Optional[EngineConfig] = None
        
    def load_config(self) -> EngineConfig:
        """Load configuration from file."""
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f)
                self.config = EngineConfig(**data)
        else:
            # Use default configuration
            self.config = EngineConfig(
                brand=BrandConfig(
                    name="Default Brand",
                    colors=["#0066CC", "#FFFFFF"],
                    tone="professional",
                    voice="engaging"
                )
            )
        return self.config
    
    def save_config(self, config: EngineConfig):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            yaml.dump(config.model_dump(), f, default_flow_style=False)
        self.config = config
    
    def get_config(self) -> EngineConfig:
        """Get current configuration, loading if necessary."""
        if self.config is None:
            return self.load_config()
        return self.config
