"""
Example: Campaign Creation
===========================

This example demonstrates how to create a multi-content campaign
with the Marketing Content Engine.
"""

from engine import MarketingContentEngine
from models import ContentIdea, ContentType, Platform


def main():
    # Initialize the engine
    print("Initializing Marketing Content Engine...")
    engine = MarketingContentEngine()
    
    # Create multiple content ideas for a product launch campaign
    campaign_ideas = [
        ContentIdea(
            title="Introducing Our Revolutionary Product",
            description="""
            Get ready to experience the future. Our new product combines 
            cutting-edge technology with intuitive design to solve your 
            biggest challenges. This is more than just a product—it's a 
            game-changer.
            """,
            content_type=ContentType.MARKETING,
            target_audience="Tech-savvy consumers and early adopters",
            key_messages=[
                "Revolutionary technology meets elegant design",
                "Solves real problems with innovative solutions",
                "Join thousands of satisfied customers"
            ],
            duration_seconds=60
        ),
        
        ContentIdea(
            title="How It Works: Product Demo",
            description="""
            See our product in action! This step-by-step demonstration 
            shows you exactly how easy it is to get started and achieve 
            amazing results in minutes.
            """,
            content_type=ContentType.TUTORIAL,
            target_audience="Potential customers researching solutions",
            key_messages=[
                "Easy setup in under 5 minutes",
                "Intuitive interface anyone can use",
                "Powerful features at your fingertips"
            ],
            duration_seconds=90
        ),
        
        ContentIdea(
            title="Customer Success Story: Sarah's Journey",
            description="""
            Meet Sarah, a small business owner who transformed her operations 
            using our product. Hear her story of challenges, discovery, and 
            ultimate success. Real results from a real customer.
            """,
            content_type=ContentType.PROMOTIONAL,
            target_audience="Small business owners and entrepreneurs",
            key_messages=[
                "Real customer, real results",
                "Increased efficiency by 300%",
                "ROI achieved in first month"
            ],
            duration_seconds=75
        ),
        
        ContentIdea(
            title="Limited Time Offer: Launch Special",
            description="""
            Don't miss out! For a limited time, get our revolutionary product 
            at an exclusive launch price. Plus, receive bonus training materials 
            and priority support. This offer won't last long!
            """,
            content_type=ContentType.ADVERTISEMENT,
            target_audience="Ready-to-buy customers",
            key_messages=[
                "Exclusive launch pricing - save 40%",
                "Bonus training materials included",
                "Limited time offer - act now"
            ],
            duration_seconds=30
        )
    ]
    
    print("\nCreating Q1 Product Launch Campaign")
    print("="*70)
    print(f"Campaign includes {len(campaign_ideas)} content pieces:")
    for i, idea in enumerate(campaign_ideas, 1):
        print(f"  {i}. {idea.title} ({idea.content_type.value})")
    
    # Create and process the campaign
    campaign_result = engine.create_campaign(
        name="Q1 2025 Product Launch Campaign",
        description="""
        Comprehensive multi-platform campaign for our new product launch.
        Includes introduction, demonstration, testimonial, and promotional content.
        """,
        ideas=campaign_ideas,
        platforms=[Platform.YOUTUBE, Platform.INSTAGRAM, Platform.FACEBOOK, Platform.LINKEDIN]
    )
    
    # Display campaign results
    print("\n\nCampaign Results:")
    print("="*70)
    
    if campaign_result['success']:
        print("✓ Campaign created successfully!")
    else:
        print("⚠ Campaign completed with some failures")
    
    campaign = campaign_result['campaign']
    print(f"\nCampaign ID: {campaign.id}")
    print(f"Name: {campaign.name}")
    print(f"Status: {campaign.status}")
    print(f"Content Pieces: {len(campaign.content_ids)}")
    
    print(f"\nSuccess Rate:")
    successful = len(campaign_result['successful_content'])
    total = len(campaign_ideas)
    print(f"  Successful: {successful}/{total} ({successful/total*100:.1f}%)")
    
    if campaign_result['failed_content']:
        print(f"  Failed: {len(campaign_result['failed_content'])}")
        for failed in campaign_result['failed_content']:
            print(f"    - {failed['title']}: {failed['error']}")
    
    # Display campaign metrics
    print("\n\nCampaign Metrics:")
    print("="*70)
    metrics = campaign_result['metrics']
    print(f"Total Content: {metrics['total_content']}")
    
    total_videos = sum(cm['video_count'] for cm in metrics['content_metrics'])
    print(f"Total Videos Generated: {total_videos}")
    
    all_platforms = set()
    for cm in metrics['content_metrics']:
        all_platforms.update(cm['platforms'])
    print(f"Distribution Platforms: {', '.join(all_platforms)}")
    
    total_duration = sum(cm['total_duration'] for cm in metrics['content_metrics'])
    print(f"Total Content Duration: {total_duration:.0f} seconds ({total_duration/60:.1f} minutes)")
    
    # Display individual content metrics
    print("\n\nIndividual Content Breakdown:")
    print("="*70)
    for i, cm in enumerate(metrics['content_metrics'], 1):
        print(f"\n{i}. {cm['title']}")
        print(f"   - Videos: {cm['video_count']}")
        print(f"   - Duration: {cm['total_duration']:.0f}s")
        print(f"   - Distributions: {cm['distribution_count']}")
    
    # Overall system metrics
    print("\n\nSystem-Wide Metrics:")
    print("="*70)
    overall = engine.get_metrics("overall")
    print(f"Total Content Ideas: {overall['total_content_ideas']}")
    print(f"Total Creative Directions: {overall['total_creative_directions']}")
    print(f"Total Videos: {overall['total_videos']}")
    print(f"Total Distribution Plans: {overall['total_distribution_plans']}")
    print(f"Total Campaigns: {overall['total_campaigns']}")


if __name__ == "__main__":
    main()
