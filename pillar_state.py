"""
State Management Module
========================

Fourth operational pillar: Tracks workflow and content lifecycle.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import json
from models import (
    ContentIdea, CreativeDirection, VideoContent, 
    DistributionPlan, Campaign, ContentStatus
)
from config import EngineConfig


class StateStore:
    """Manages persistent state storage."""
    
    def __init__(self, config: EngineConfig):
        self.config = config
        self.db_path = Path(config.state_db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize in-memory state (in production, use SQLAlchemy/Redis)
        self.state = {
            'content_ideas': {},
            'creative_directions': {},
            'videos': {},
            'distribution_plans': {},
            'campaigns': {},
            'workflow_states': {}
        }
        
        # Load existing state
        self._load_state()
    
    def _load_state(self):
        """Load state from disk."""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r') as f:
                    self.state = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load state: {e}")
    
    def _save_state(self):
        """Save state to disk."""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.state, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save state: {e}")
    
    def save_content_idea(self, idea: ContentIdea):
        """Save a content idea."""
        self.state['content_ideas'][idea.id] = idea.model_dump()
        self._save_state()
    
    def get_content_idea(self, content_id: str) -> Optional[Dict]:
        """Retrieve a content idea."""
        return self.state['content_ideas'].get(content_id)
    
    def save_creative_direction(self, direction: CreativeDirection):
        """Save creative direction."""
        self.state['creative_directions'][direction.id] = direction.model_dump()
        self._save_state()
    
    def get_creative_direction(self, direction_id: str) -> Optional[Dict]:
        """Retrieve creative direction."""
        return self.state['creative_directions'].get(direction_id)
    
    def save_video(self, video: VideoContent):
        """Save video content."""
        self.state['videos'][video.id] = video.model_dump()
        self._save_state()
    
    def get_video(self, video_id: str) -> Optional[Dict]:
        """Retrieve video content."""
        return self.state['videos'].get(video_id)
    
    def save_distribution_plan(self, plan: DistributionPlan):
        """Save distribution plan."""
        self.state['distribution_plans'][plan.id] = plan.model_dump()
        self._save_state()
    
    def get_distribution_plan(self, plan_id: str) -> Optional[Dict]:
        """Retrieve distribution plan."""
        return self.state['distribution_plans'].get(plan_id)
    
    def save_campaign(self, campaign: Campaign):
        """Save campaign."""
        self.state['campaigns'][campaign.id] = campaign.model_dump()
        self._save_state()
    
    def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """Retrieve campaign."""
        return self.state['campaigns'].get(campaign_id)
    
    def list_all(self, entity_type: str) -> List[Dict]:
        """List all entities of a type."""
        return list(self.state.get(entity_type, {}).values())


class WorkflowTracker:
    """Tracks content through the workflow pipeline."""
    
    def __init__(self, state_store: StateStore):
        self.state_store = state_store
    
    def update_status(self, content_id: str, status: ContentStatus):
        """Update content status in workflow."""
        workflow_key = f"workflow_{content_id}"
        
        workflow_state = self.state_store.state['workflow_states'].get(workflow_key, {
            'content_id': content_id,
            'current_status': ContentStatus.DRAFT,
            'status_history': [],
            'created_at': datetime.utcnow().isoformat()
        })
        
        # Add to history
        workflow_state['status_history'].append({
            'status': status,
            'timestamp': datetime.utcnow().isoformat()
        })
        workflow_state['current_status'] = status
        workflow_state['updated_at'] = datetime.utcnow().isoformat()
        
        self.state_store.state['workflow_states'][workflow_key] = workflow_state
        self.state_store._save_state()
    
    def get_status(self, content_id: str) -> Optional[str]:
        """Get current status of content."""
        workflow_key = f"workflow_{content_id}"
        workflow_state = self.state_store.state['workflow_states'].get(workflow_key)
        return workflow_state['current_status'] if workflow_state else None
    
    def get_workflow_history(self, content_id: str) -> List[Dict]:
        """Get complete workflow history for content."""
        workflow_key = f"workflow_{content_id}"
        workflow_state = self.state_store.state['workflow_states'].get(workflow_key, {})
        return workflow_state.get('status_history', [])


class MetricsCollector:
    """Collects and aggregates metrics."""
    
    def __init__(self, state_store: StateStore):
        self.state_store = state_store
    
    def get_content_metrics(self, content_id: str) -> Dict[str, Any]:
        """Get metrics for specific content."""
        # Gather all related data
        idea = self.state_store.get_content_idea(content_id)
        videos = [v for v in self.state_store.list_all('videos') 
                 if v.get('content_id') == content_id]
        distributions = [d for d in self.state_store.list_all('distribution_plans')
                        if d.get('content_id') == content_id]
        
        return {
            'content_id': content_id,
            'title': idea.get('title') if idea else 'Unknown',
            'video_count': len(videos),
            'distribution_count': len(distributions),
            'platforms': [p for d in distributions for p in d.get('platforms', [])],
            'total_duration': sum(v.get('duration_seconds', 0) for v in videos)
        }
    
    def get_campaign_metrics(self, campaign_id: str) -> Dict[str, Any]:
        """Get metrics for a campaign."""
        campaign = self.state_store.get_campaign(campaign_id)
        if not campaign:
            return {}
        
        content_ids = campaign.get('content_ids', [])
        
        metrics = {
            'campaign_id': campaign_id,
            'name': campaign.get('name'),
            'total_content': len(content_ids),
            'content_metrics': []
        }
        
        for content_id in content_ids:
            content_metric = self.get_content_metrics(content_id)
            metrics['content_metrics'].append(content_metric)
        
        return metrics
    
    def get_overall_metrics(self) -> Dict[str, Any]:
        """Get overall system metrics."""
        return {
            'total_content_ideas': len(self.state_store.list_all('content_ideas')),
            'total_creative_directions': len(self.state_store.list_all('creative_directions')),
            'total_videos': len(self.state_store.list_all('videos')),
            'total_distribution_plans': len(self.state_store.list_all('distribution_plans')),
            'total_campaigns': len(self.state_store.list_all('campaigns')),
            'timestamp': datetime.utcnow().isoformat()
        }


class StateManagementPillar:
    """
    Fourth Operational Pillar: State Management
    
    Tracks content lifecycle, workflow states, and system metrics
    throughout the entire content creation and distribution process.
    """
    
    def __init__(self, config: EngineConfig):
        self.config = config
        self.state_store = StateStore(config)
        self.workflow_tracker = WorkflowTracker(self.state_store)
        self.metrics_collector = MetricsCollector(self.state_store)
    
    def track_content(self, idea: ContentIdea, status: ContentStatus = ContentStatus.INGESTED):
        """Start tracking a content idea."""
        self.state_store.save_content_idea(idea)
        self.workflow_tracker.update_status(idea.id, status)
    
    def track_creative_direction(self, direction: CreativeDirection):
        """Track creative direction."""
        self.state_store.save_creative_direction(direction)
        self.workflow_tracker.update_status(direction.content_id, ContentStatus.CREATIVE_REVIEW)
    
    def track_video(self, video: VideoContent):
        """Track synthesized video."""
        self.state_store.save_video(video)
        self.workflow_tracker.update_status(video.content_id, ContentStatus.REVIEW)
    
    def track_distribution(self, plan: DistributionPlan):
        """Track distribution plan."""
        self.state_store.save_distribution_plan(plan)
        self.workflow_tracker.update_status(plan.content_id, ContentStatus.DISTRIBUTED)
    
    def get_content_status(self, content_id: str) -> Optional[str]:
        """Get current status of content."""
        return self.workflow_tracker.get_status(content_id)
    
    def get_workflow_history(self, content_id: str) -> List[Dict]:
        """Get workflow history for content."""
        return self.workflow_tracker.get_workflow_history(content_id)
    
    def get_metrics(self, metric_type: str = "overall", entity_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get metrics.
        
        Args:
            metric_type: "overall", "content", or "campaign"
            entity_id: ID for content or campaign metrics
        """
        if metric_type == "content" and entity_id:
            return self.metrics_collector.get_content_metrics(entity_id)
        elif metric_type == "campaign" and entity_id:
            return self.metrics_collector.get_campaign_metrics(entity_id)
        else:
            return self.metrics_collector.get_overall_metrics()
