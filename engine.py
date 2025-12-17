"""
Marketing Content Engine
=========================

Main orchestration engine that coordinates all five operational pillars.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from models import (
    ContentIdea, ContentType, ContentStatus, Platform,
    CreativeDirection, VideoContent, DistributionPlan, Campaign
)
from config import ConfigManager, EngineConfig
from pillar_ingestion import ContentIngestionPillar
from pillar_creative import CreativeDirectionPillar
from pillar_synthesis import MediaSynthesisPillar
from pillar_state import StateManagementPillar
from pillar_distribution import MultiPlatformDistributionPillar


class MarketingContentEngine:
    """
    AI-Powered Marketing Content Engine
    
    Orchestrates five operational pillars to transform content ideas
    into high-fidelity, brand-compliant video campaigns with
    multi-platform distribution.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Marketing Content Engine.
        
        Args:
            config_path: Optional path to configuration file
        """
        # Load configuration
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()
        
        # Initialize five operational pillars
        self.ingestion = ContentIngestionPillar(self.config)
        self.creative = CreativeDirectionPillar(self.config)
        self.synthesis = MediaSynthesisPillar(self.config)
        self.state = StateManagementPillar(self.config)
        self.distribution = MultiPlatformDistributionPillar(self.config)
    
    def process_content_idea(self, idea: ContentIdea, 
                            platforms: Optional[List[Platform]] = None,
                            auto_distribute: bool = False) -> Dict[str, Any]:
        """
        Process a content idea through the complete pipeline.
        
        This is the main method that orchestrates all five pillars:
        1. Content Ingestion - Validate and enrich the idea
        2. Creative Direction - Generate brand-compliant creative guidelines
        3. Media Synthesis - Create video content
        4. State Management - Track throughout pipeline
        5. Multi-Platform Distribution - Distribute to platforms
        
        Args:
            idea: ContentIdea to process
            platforms: Optional list of platforms to distribute to
            auto_distribute: Whether to automatically distribute content
            
        Returns:
            Dict containing results from each pillar
        """
        result = {
            'success': False,
            'content_id': idea.id,
            'stages': {}
        }
        
        # Stage 1: Content Ingestion
        print(f"[Stage 1/5] Content Ingestion - Processing: {idea.title}")
        ingestion_result = self.ingestion.ingest_content(idea)
        result['stages']['ingestion'] = ingestion_result
        
        if not ingestion_result['success']:
            result['error'] = f"Ingestion failed: {ingestion_result['errors']}"
            return result
        
        enriched_idea = ingestion_result['idea']
        self.state.track_content(enriched_idea, ContentStatus.INGESTED)
        
        # Stage 2: Creative Direction
        print(f"[Stage 2/5] Creative Direction - Generating guidelines")
        creative_result = self.creative.create_direction(enriched_idea)
        result['stages']['creative'] = creative_result
        
        direction = creative_result['direction']
        self.state.track_creative_direction(direction)
        
        if creative_result['compliance_issues']:
            print(f"  ⚠ Compliance issues: {creative_result['compliance_issues']}")
        
        # Stage 3: Media Synthesis
        print(f"[Stage 3/5] Media Synthesis - Creating video content")
        synthesis_result = self.synthesis.synthesize_video(direction)
        result['stages']['synthesis'] = synthesis_result
        
        if not synthesis_result['success']:
            result['error'] = f"Synthesis failed: {synthesis_result['quality_report']['issues']}"
            return result
        
        video = synthesis_result['video']
        self.state.track_video(video)
        
        # Stage 4: Distribution Planning
        print(f"[Stage 4/5] Distribution Planning - Creating distribution plan")
        
        if platforms is None:
            # Get platform recommendations based on viral potential
            direction_data = direction.model_dump()
            viral_score = self.distribution.viral_analyzer.analyze_viral_potential(video, direction_data)
            platforms = self.distribution.get_platform_recommendations(video, viral_score)
            print(f"  ℹ Recommended platforms: {[p.value for p in platforms]}")
        
        distribution_plan = self.distribution.create_distribution_plan(
            video=video,
            direction_data=direction.model_dump(),
            platforms=platforms,
            hashtags=enriched_idea.keywords[:5]
        )
        
        self.state.track_distribution(distribution_plan)
        result['stages']['distribution_plan'] = {
            'plan': distribution_plan,
            'viral_score': distribution_plan.viral_score
        }
        
        # Stage 5: Distribution Execution (if auto_distribute is True)
        if auto_distribute:
            print(f"[Stage 5/5] Distribution Execution - Publishing to platforms")
            distribution_result = self.distribution.execute_distribution(distribution_plan, video)
            result['stages']['distribution_execution'] = distribution_result
            
            if distribution_result['success']:
                self.state.workflow_tracker.update_status(enriched_idea.id, ContentStatus.PUBLISHED)
                print(f"  ✓ Published to {distribution_result['successful_count']} platforms")
            else:
                print(f"  ✗ Failed to publish to {distribution_result['failed_count']} platforms")
        else:
            print(f"[Stage 5/5] Distribution Execution - Skipped (auto_distribute=False)")
            result['stages']['distribution_execution'] = {
                'skipped': True,
                'message': 'Set auto_distribute=True to publish automatically'
            }
        
        result['success'] = True
        print(f"\n✓ Pipeline completed successfully for: {idea.title}")
        
        return result
    
    def create_campaign(self, name: str, description: str, 
                       ideas: List[ContentIdea],
                       platforms: Optional[List[Platform]] = None) -> Dict[str, Any]:
        """
        Create and process a complete campaign with multiple content pieces.
        
        Args:
            name: Campaign name
            description: Campaign description
            ideas: List of ContentIdea objects
            platforms: Optional list of platforms for all content
            
        Returns:
            Dict with campaign results
        """
        print(f"\n{'='*60}")
        print(f"Creating Campaign: {name}")
        print(f"{'='*60}\n")
        
        campaign = Campaign(
            name=name,
            description=description,
            status=ContentStatus.DRAFT
        )
        
        successful_content = []
        failed_content = []
        
        for i, idea in enumerate(ideas, 1):
            print(f"\n--- Content {i}/{len(ideas)} ---")
            result = self.process_content_idea(idea, platforms=platforms)
            
            if result['success']:
                successful_content.append(idea.id)
                campaign.content_ids.append(idea.id)
            else:
                failed_content.append({
                    'id': idea.id,
                    'title': idea.title,
                    'error': result.get('error', 'Unknown error')
                })
        
        # Update campaign status
        if len(successful_content) == len(ideas):
            campaign.status = ContentStatus.APPROVED
        elif len(successful_content) > 0:
            campaign.status = ContentStatus.REVIEW
        else:
            campaign.status = ContentStatus.FAILED
        
        # Save campaign
        self.state.state_store.save_campaign(campaign)
        
        print(f"\n{'='*60}")
        print(f"Campaign Summary: {name}")
        print(f"{'='*60}")
        print(f"Successful: {len(successful_content)}/{len(ideas)}")
        print(f"Failed: {len(failed_content)}/{len(ideas)}")
        print(f"Campaign Status: {campaign.status}")
        
        return {
            'success': len(failed_content) == 0,
            'campaign': campaign,
            'successful_content': successful_content,
            'failed_content': failed_content,
            'metrics': self.state.metrics_collector.get_campaign_metrics(campaign.id)
        }
    
    def get_content_status(self, content_id: str) -> Dict[str, Any]:
        """Get current status and history of content."""
        status = self.state.get_content_status(content_id)
        history = self.state.get_workflow_history(content_id)
        
        return {
            'content_id': content_id,
            'current_status': status,
            'history': history
        }
    
    def get_metrics(self, metric_type: str = "overall", 
                   entity_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get system metrics.
        
        Args:
            metric_type: "overall", "content", or "campaign"
            entity_id: ID for content or campaign (required for non-overall)
        """
        return self.state.get_metrics(metric_type, entity_id)
    
    def update_config(self, config: EngineConfig):
        """Update engine configuration."""
        self.config_manager.save_config(config)
        self.config = config
        
        # Reinitialize pillars with new config
        self.ingestion = ContentIngestionPillar(self.config)
        self.creative = CreativeDirectionPillar(self.config)
        self.synthesis = MediaSynthesisPillar(self.config)
        self.state = StateManagementPillar(self.config)
        self.distribution = MultiPlatformDistributionPillar(self.config)


def main():
    """Example usage of the Marketing Content Engine."""
    print("Marketing Content Engine - AI-Powered Video Campaign Generator")
    print("="*70)
    
    # Initialize engine
    engine = MarketingContentEngine()
    
    # Example 1: Single content piece
    print("\n\nExample 1: Processing a single content idea")
    print("-"*70)
    
    idea = ContentIdea(
        title="10 Tips for Effective Digital Marketing",
        description="Learn the top 10 strategies that will transform your digital marketing efforts. From SEO to social media, we cover everything you need to know to succeed in today's competitive landscape.",
        content_type=ContentType.EDUCATIONAL,
        target_audience="Small business owners and marketing professionals",
        key_messages=[
            "SEO is the foundation of digital visibility",
            "Social media engagement drives brand loyalty",
            "Content quality matters more than quantity"
        ],
        keywords=["digital marketing", "SEO", "social media", "business growth"],
        duration_seconds=90
    )
    
    result = engine.process_content_idea(
        idea=idea,
        platforms=[Platform.YOUTUBE, Platform.LINKEDIN],
        auto_distribute=False
    )
    
    if result['success']:
        print("\n✓ Content processed successfully!")
        print(f"  Viral Score: {result['stages']['distribution_plan']['viral_score'].overall_score:.1f}/100")
    
    # Example 2: Campaign with multiple content pieces
    print("\n\nExample 2: Creating a marketing campaign")
    print("-"*70)
    
    campaign_ideas = [
        ContentIdea(
            title="Why Choose Our Product",
            description="Discover the unique features that set our product apart from the competition.",
            content_type=ContentType.MARKETING,
            target_audience="Potential customers",
            duration_seconds=60
        ),
        ContentIdea(
            title="Customer Success Story",
            description="See how our product helped a customer achieve their goals and transform their business.",
            content_type=ContentType.PROMOTIONAL,
            target_audience="Prospective buyers",
            duration_seconds=45
        )
    ]
    
    campaign_result = engine.create_campaign(
        name="Q4 Product Launch",
        description="Multi-platform campaign for Q4 product launch",
        ideas=campaign_ideas,
        platforms=[Platform.YOUTUBE, Platform.INSTAGRAM, Platform.FACEBOOK]
    )
    
    # Show metrics
    print("\n\nSystem Metrics")
    print("-"*70)
    metrics = engine.get_metrics("overall")
    print(f"Total Content Ideas: {metrics['total_content_ideas']}")
    print(f"Total Videos: {metrics['total_videos']}")
    print(f"Total Campaigns: {metrics['total_campaigns']}")


if __name__ == "__main__":
    main()
