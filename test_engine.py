"""
Test Suite for Marketing Content Engine
========================================

Basic tests to verify the core functionality of all five pillars.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from models import ContentIdea, ContentType, Platform
from config import ConfigManager, EngineConfig, BrandConfig
from pillar_ingestion import ContentIngestionPillar
from pillar_creative import CreativeDirectionPillar
from pillar_synthesis import MediaSynthesisPillar
from pillar_state import StateManagementPillar
from pillar_distribution import MultiPlatformDistributionPillar
from engine import MarketingContentEngine


def test_content_ingestion():
    """Test content ingestion pillar."""
    print("\n[TEST] Content Ingestion Pillar")
    print("-" * 60)
    
    config = EngineConfig(
        brand=BrandConfig(name="Test Brand", tone="professional")
    )
    pillar = ContentIngestionPillar(config)
    
    # Valid content
    idea = ContentIdea(
        title="Test Content",
        description="This is a test content description for validation.",
        content_type=ContentType.EDUCATIONAL,
        target_audience="Test audience",
        duration_seconds=60
    )
    
    result = pillar.ingest_content(idea)
    assert result['success'], "Content ingestion should succeed"
    assert result['idea'].keywords, "Keywords should be auto-generated"
    print("  ✓ Content ingestion successful")
    print(f"  ✓ Keywords generated: {len(result['idea'].keywords)}")
    
    # Invalid content (too short title)
    invalid_idea = ContentIdea(
        title="X",
        description="Too short",
        content_type=ContentType.EDUCATIONAL,
        target_audience="Test",
        duration_seconds=60
    )
    
    invalid_result = pillar.ingest_content(invalid_idea)
    assert not invalid_result['success'], "Invalid content should fail"
    assert invalid_result['errors'], "Should have validation errors"
    print(f"  ✓ Validation correctly rejected invalid content")
    
    return True


def test_creative_direction():
    """Test creative direction pillar."""
    print("\n[TEST] Creative Direction Pillar")
    print("-" * 60)
    
    config = EngineConfig(
        brand=BrandConfig(name="Test Brand", tone="professional")
    )
    pillar = CreativeDirectionPillar(config)
    
    idea = ContentIdea(
        title="Marketing Strategy Guide",
        description="Learn effective marketing strategies for business growth.",
        content_type=ContentType.EDUCATIONAL,
        target_audience="Business owners",
        duration_seconds=90
    )
    
    result = pillar.create_direction(idea)
    assert result['success'], "Creative direction should succeed"
    assert result['direction'].scenes, "Should have scenes"
    assert result['direction'].voiceover_script, "Should have voiceover script"
    print(f"  ✓ Creative direction generated")
    print(f"  ✓ Scenes created: {len(result['direction'].scenes)}")
    print(f"  ✓ Brand compliant: {result['direction'].brand_compliant}")
    
    return True


def test_media_synthesis():
    """Test media synthesis pillar."""
    print("\n[TEST] Media Synthesis Pillar")
    print("-" * 60)
    
    config = EngineConfig(
        brand=BrandConfig(name="Test Brand"),
        output_dir="/tmp/test_output"
    )
    pillar = MediaSynthesisPillar(config)
    
    # Create test creative direction
    from models import CreativeDirection
    
    direction = CreativeDirection(
        content_id="test_content",
        visual_style="Modern and professional",
        narrative_arc=["Hook", "Content", "CTA"],
        scenes=[
            {"scene_number": 1, "duration": 30, "description": "Opening"},
            {"scene_number": 2, "duration": 30, "description": "Content"}
        ],
        voiceover_script="Test script",
        music_style="Upbeat"
    )
    
    result = pillar.synthesize_video(direction)
    assert result['success'], "Video synthesis should succeed"
    assert result['video'], "Should have video object"
    assert result['video'].duration_seconds > 0, "Should have duration"
    print(f"  ✓ Video synthesized")
    print(f"  ✓ Duration: {result['video'].duration_seconds}s")
    print(f"  ✓ Quality score: {result['quality_report']['quality_score']}/100")
    
    return True


def test_state_management():
    """Test state management pillar."""
    print("\n[TEST] State Management Pillar")
    print("-" * 60)
    
    config = EngineConfig(
        brand=BrandConfig(name="Test Brand"),
        state_db_path="/tmp/test_state.db"
    )
    pillar = StateManagementPillar(config)
    
    # Test tracking content
    idea = ContentIdea(
        title="Test Content",
        description="Test description for state management.",
        content_type=ContentType.EDUCATIONAL,
        target_audience="Test audience",
        duration_seconds=60
    )
    
    from models import ContentStatus
    pillar.track_content(idea, ContentStatus.INGESTED)
    
    status = pillar.get_content_status(idea.id)
    assert status == ContentStatus.INGESTED, "Status should be tracked"
    print(f"  ✓ Content tracked successfully")
    print(f"  ✓ Current status: {status}")
    
    # Test metrics
    metrics = pillar.get_metrics("overall")
    assert metrics['total_content_ideas'] > 0, "Should have content ideas"
    print(f"  ✓ Metrics collection working")
    print(f"  ✓ Total content ideas: {metrics['total_content_ideas']}")
    
    return True


def test_distribution():
    """Test distribution pillar."""
    print("\n[TEST] Multi-Platform Distribution Pillar")
    print("-" * 60)
    
    config = EngineConfig(
        brand=BrandConfig(name="Test Brand")
    )
    pillar = MultiPlatformDistributionPillar(config)
    
    # Create test video
    from models import VideoContent, CreativeDirection
    
    direction = CreativeDirection(
        content_id="test_content",
        visual_style="Modern",
        narrative_arc=["Hook", "Content", "CTA"],
        scenes=[{"duration": 60}],
        voiceover_script="Test script with engaging content and exciting opportunities",
        music_style="Upbeat"
    )
    
    video = VideoContent(
        content_id="test_content",
        creative_direction_id=direction.id,
        file_path="/tmp/test_video.mp4",
        duration_seconds=60,
        resolution="1920x1080",
        format="mp4"
    )
    
    # Test viral analysis
    viral_score = pillar.viral_analyzer.analyze_viral_potential(
        video, direction.model_dump()
    )
    assert viral_score.overall_score > 0, "Should have viral score"
    print(f"  ✓ Viral analysis completed")
    print(f"  ✓ Overall score: {viral_score.overall_score:.1f}/100")
    print(f"  ✓ Engagement: {viral_score.engagement_potential:.1f}/100")
    
    # Test platform recommendations
    recommendations = pillar.get_platform_recommendations(video, viral_score)
    assert recommendations, "Should have platform recommendations"
    print(f"  ✓ Platform recommendations: {[p.value for p in recommendations]}")
    
    return True


def test_full_pipeline():
    """Test complete end-to-end pipeline."""
    print("\n[TEST] Full Pipeline Integration")
    print("-" * 60)
    
    # Initialize engine with test config
    engine = MarketingContentEngine()
    
    # Create test content
    idea = ContentIdea(
        title="Complete Pipeline Test",
        description="This is a comprehensive test of the entire pipeline system.",
        content_type=ContentType.MARKETING,
        target_audience="Test users",
        duration_seconds=60
    )
    
    # Process through pipeline
    result = engine.process_content_idea(
        idea=idea,
        platforms=[Platform.YOUTUBE, Platform.INSTAGRAM],
        auto_distribute=False
    )
    
    assert result['success'], "Pipeline should complete successfully"
    assert 'ingestion' in result['stages'], "Should have ingestion stage"
    assert 'creative' in result['stages'], "Should have creative stage"
    assert 'synthesis' in result['stages'], "Should have synthesis stage"
    assert 'distribution_plan' in result['stages'], "Should have distribution plan"
    
    print(f"  ✓ Full pipeline completed successfully")
    print(f"  ✓ All 5 pillars executed")
    print(f"  ✓ Content ID: {result['content_id']}")
    
    # Test metrics
    metrics = engine.get_metrics("overall")
    print(f"  ✓ System metrics available")
    print(f"    - Total content: {metrics['total_content_ideas']}")
    print(f"    - Total videos: {metrics['total_videos']}")
    
    return True


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("Marketing Content Engine - Test Suite")
    print("="*60)
    
    tests = [
        ("Content Ingestion", test_content_ingestion),
        ("Creative Direction", test_creative_direction),
        ("Media Synthesis", test_media_synthesis),
        ("State Management", test_state_management),
        ("Distribution", test_distribution),
        ("Full Pipeline", test_full_pipeline),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✓ {name} test PASSED")
        except Exception as e:
            failed += 1
            print(f"\n✗ {name} test FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print(f"Test Results: {passed}/{len(tests)} passed, {failed}/{len(tests)} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
