# Marketing Content Engine 🚀

An AI-powered engine that automates the transformation of educational or marketing content ideas into high-fidelity, brand-compliant video campaigns and lessons. The system orchestrates five operational pillars to enable effective creation and delivery of video content at scale.

## 🎯 Overview

The Marketing Content Engine is designed to maximize:
- ✅ **Accuracy** - Precise content generation aligned with your specifications
- 🛡️ **Brand Safety** - Automated compliance checks and validation
- 📈 **Commercial Impact** - Data-driven optimization for business results
- 🌟 **Viral Potential** - AI-powered analysis and scoring for maximum reach

## 🏗️ Architecture: Five Operational Pillars

### 1. Content Ingestion 📥
Processes and validates incoming content ideas, ensuring quality standards and brand safety.

**Features:**
- Content validation and quality checks
- Brand safety screening
- Automatic content enrichment (keywords, key messages)
- Batch processing capabilities

### 2. Creative Direction 🎨
Generates brand-compliant creative guidelines and direction for content production.

**Features:**
- AI-powered creative direction generation
- Brand compliance validation
- Narrative arc development
- Scene breakdown and planning
- Voiceover script generation
- Visual style recommendations

### 3. Media Synthesis 🎬
Creates high-fidelity video content from creative direction.

**Features:**
- Video content generation
- Quality assurance checks
- Resolution and format management
- Thumbnail generation
- Batch synthesis support

### 4. State Management 📊
Tracks content lifecycle, workflow states, and system metrics.

**Features:**
- Persistent state storage
- Workflow tracking through pipeline
- Real-time status updates
- Metrics collection and aggregation
- Campaign management
- Complete audit trail

### 5. Multi-Platform Distribution 🌐
Distributes content across multiple platforms with viral optimization.

**Features:**
- Viral potential analysis and scoring
- Platform-specific optimization
- Automated distribution execution
- Multi-platform support (YouTube, TikTok, Instagram, Facebook, LinkedIn, Twitter)
- Smart platform recommendations
- Scheduling and timing optimization

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/nishchith-m1015/Marketing-Content-Engine.git
cd Marketing-Content-Engine

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from engine import MarketingContentEngine
from models import ContentIdea, ContentType, Platform

# Initialize the engine
engine = MarketingContentEngine()

# Create a content idea
idea = ContentIdea(
    title="10 Tips for Digital Marketing Success",
    description="Learn proven strategies to boost your digital marketing efforts.",
    content_type=ContentType.EDUCATIONAL,
    target_audience="Small business owners",
    duration_seconds=90
)

# Process through the complete pipeline
result = engine.process_content_idea(
    idea=idea,
    platforms=[Platform.YOUTUBE, Platform.LINKEDIN],
    auto_distribute=False
)

# Check results
if result['success']:
    viral_score = result['stages']['distribution_plan']['viral_score']
    print(f"Viral Score: {viral_score.overall_score}/100")
```

### Creating a Campaign

```python
# Create multiple content ideas for a campaign
campaign_ideas = [
    ContentIdea(
        title="Product Overview",
        description="Comprehensive overview of our product features.",
        content_type=ContentType.MARKETING,
        target_audience="Potential customers",
        duration_seconds=60
    ),
    ContentIdea(
        title="Customer Testimonial",
        description="Real success story from a satisfied customer.",
        content_type=ContentType.PROMOTIONAL,
        target_audience="Prospective buyers",
        duration_seconds=45
    )
]

# Process as a campaign
campaign_result = engine.create_campaign(
    name="Q4 Product Launch",
    description="Multi-platform product launch campaign",
    ideas=campaign_ideas,
    platforms=[Platform.YOUTUBE, Platform.INSTAGRAM, Platform.FACEBOOK]
)
```

## 📋 Configuration

Create a `config.yaml` file to customize the engine:

```yaml
brand:
  name: "Your Brand Name"
  colors:
    - "#0066CC"
    - "#FFFFFF"
  fonts:
    - "Roboto"
    - "Open Sans"
  tone: "professional"
  voice: "engaging"
  guidelines: "Your brand guidelines here"

ai:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 2000

media:
  video_resolution: "1920x1080"
  video_fps: 30
  video_format: "mp4"
  audio_bitrate: "192k"

distribution:
  platforms:
    - "youtube"
    - "instagram"
    - "linkedin"
  auto_publish: false
  scheduling_enabled: true

output_dir: "./output"
state_db_path: "./state.db"
```

## 🎯 Use Cases

### Educational Content
- Online course videos
- Tutorial series
- Training materials
- Webinar recordings

### Marketing Content
- Product demos
- Brand stories
- Feature highlights
- Value propositions

### Promotional Content
- Campaign videos
- Event promotions
- Limited-time offers
- Product launches

### Advertisement Content
- Social media ads
- Video commercials
- Sponsored content
- Retargeting campaigns

## 📊 Viral Potential Scoring

The engine analyzes content for viral potential across multiple dimensions:

- **Engagement Potential** (30% weight) - Duration, pacing, scene dynamics
- **Shareability** (30% weight) - Brand trust, call-to-action, visual appeal
- **Emotional Impact** (20% weight) - Emotional keywords, narrative quality
- **Trend Alignment** (20% weight) - Modern styling, music, current trends

Each dimension is scored 0-100, providing actionable insights for optimization.

## 🔧 API Reference

### MarketingContentEngine

Main orchestration class that coordinates all five pillars.

**Methods:**
- `process_content_idea(idea, platforms, auto_distribute)` - Process single content idea
- `create_campaign(name, description, ideas, platforms)` - Create multi-content campaign
- `get_content_status(content_id)` - Get content workflow status
- `get_metrics(metric_type, entity_id)` - Retrieve system metrics
- `update_config(config)` - Update engine configuration

### ContentIdea

Input model for content ideas.

**Fields:**
- `title: str` - Content title
- `description: str` - Content description
- `content_type: ContentType` - Type of content (educational, marketing, etc.)
- `target_audience: str` - Target audience description
- `key_messages: List[str]` - Key messages to convey
- `keywords: List[str]` - Content keywords
- `duration_seconds: int` - Target duration

### Platform Enum

Supported distribution platforms:
- `YOUTUBE`
- `TIKTOK`
- `INSTAGRAM`
- `FACEBOOK`
- `LINKEDIN`
- `TWITTER`

## 📈 Metrics and Analytics

Get comprehensive metrics at multiple levels:

```python
# Overall system metrics
overall = engine.get_metrics("overall")

# Content-specific metrics
content_metrics = engine.get_metrics("content", content_id="...")

# Campaign metrics
campaign_metrics = engine.get_metrics("campaign", campaign_id="...")
```

## 🔐 Brand Safety

The engine includes built-in brand safety features:
- Automated content screening
- Inappropriate keyword detection
- Brand guideline compliance checking
- Tone and voice validation
- Manual review checkpoints

## 🎨 Customization

### Custom Content Validators

```python
from pillar_ingestion import ContentValidator

class CustomValidator(ContentValidator):
    def _check_brand_safety(self, idea):
        # Custom validation logic
        return {'safe': True, 'issues': []}
```

### Custom Creative Generators

```python
from pillar_creative import CreativeGenerator

class CustomCreativeGenerator(CreativeGenerator):
    def _generate_voiceover_script(self, idea, narrative_arc):
        # Custom script generation
        return "Custom script..."
```

## 🐛 Troubleshooting

**Issue: Content validation fails**
- Ensure title is at least 3 characters
- Description must be at least 10 characters
- Duration must be between 10-600 seconds
- Target audience must be specified

**Issue: Brand compliance warnings**
- Review brand configuration in config.yaml
- Check tone and voice settings
- Verify brand guidelines are properly defined

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Built with modern AI and media processing technologies:
- OpenAI GPT models for content generation
- Pydantic for data validation
- MoviePy for video processing (planned)
- FastAPI for API endpoints (planned)

## 📞 Support

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for marketers, educators, and content creators**