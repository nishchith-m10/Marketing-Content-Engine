"""
Example: Basic Content Processing
==================================

This example demonstrates how to process a single content idea
through the Marketing Content Engine pipeline.
"""

from engine import MarketingContentEngine
from models import ContentIdea, ContentType, Platform


def main():
    # Initialize the engine
    print("Initializing Marketing Content Engine...")
    engine = MarketingContentEngine()
    
    # Create a content idea
    idea = ContentIdea(
        title="5 Proven Strategies for Social Media Growth",
        description="""
        Unlock the secrets to growing your social media presence with these 
        five proven strategies. Learn how to create engaging content, optimize 
        posting times, leverage hashtags effectively, build community, and 
        measure your success with analytics.
        """,
        content_type=ContentType.EDUCATIONAL,
        target_audience="Social media managers and small business owners",
        key_messages=[
            "Create content that resonates with your audience",
            "Consistency is key to building a loyal following",
            "Data-driven decisions lead to better results"
        ],
        keywords=["social media", "growth", "engagement", "marketing", "strategy"],
        duration_seconds=120
    )
    
    print(f"\nProcessing content: {idea.title}")
    print("="*70)
    
    # Process through the complete pipeline
    result = engine.process_content_idea(
        idea=idea,
        platforms=[Platform.YOUTUBE, Platform.LINKEDIN, Platform.INSTAGRAM],
        auto_distribute=False  # Set to True to automatically publish
    )
    
    # Display results
    if result['success']:
        print("\n✓ Content processed successfully!")
        print("\nResults Summary:")
        print("="*70)
        
        # Ingestion results
        ingestion = result['stages']['ingestion']
        print(f"\n1. Content Ingestion:")
        print(f"   - Status: ✓ Success")
        print(f"   - Keywords added: {len(ingestion['idea'].keywords)}")
        
        # Creative direction results
        creative = result['stages']['creative']
        direction = creative['direction']
        print(f"\n2. Creative Direction:")
        print(f"   - Visual Style: {direction.visual_style}")
        print(f"   - Scenes: {len(direction.scenes)}")
        print(f"   - Brand Compliant: {'✓' if direction.brand_compliant else '✗'}")
        if creative['compliance_issues']:
            print(f"   - Compliance Issues: {len(creative['compliance_issues'])}")
        
        # Synthesis results
        synthesis = result['stages']['synthesis']
        video = synthesis['video']
        print(f"\n3. Media Synthesis:")
        print(f"   - Duration: {video.duration_seconds}s")
        print(f"   - Resolution: {video.resolution}")
        print(f"   - Estimated Size: {video.file_size_mb:.2f} MB")
        print(f"   - Quality Score: {synthesis['quality_report']['quality_score']}/100")
        
        # Distribution plan results
        dist_plan = result['stages']['distribution_plan']
        plan = dist_plan['plan']
        viral_score = dist_plan['viral_score']
        print(f"\n4. Distribution Plan:")
        print(f"   - Platforms: {[p.value for p in plan.platforms]}")
        print(f"   - Hashtags: {', '.join(plan.hashtags)}")
        print(f"\n5. Viral Potential Analysis:")
        print(f"   - Overall Score: {viral_score.overall_score:.1f}/100")
        print(f"   - Engagement: {viral_score.engagement_potential:.1f}/100")
        print(f"   - Shareability: {viral_score.shareability:.1f}/100")
        print(f"   - Emotional Impact: {viral_score.emotional_impact:.1f}/100")
        print(f"   - Trend Alignment: {viral_score.trend_alignment:.1f}/100")
        print(f"   - Analysis: {viral_score.reasoning}")
        
        # Distribution execution results
        dist_exec = result['stages']['distribution_execution']
        if not dist_exec.get('skipped'):
            print(f"\n6. Distribution Execution:")
            print(f"   - Published: {dist_exec['successful_count']} platforms")
            print(f"   - Platforms Reached: {[p.value for p in dist_exec['platforms_reached']]}")
        
        # Get current status
        status = engine.get_content_status(idea.id)
        print(f"\nCurrent Status: {status['current_status']}")
        
    else:
        print(f"\n✗ Content processing failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
