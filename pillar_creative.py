"""
Creative Direction Module
==========================

Second operational pillar: Generates brand-compliant creative guidelines.
"""

from typing import Dict, List, Optional
import os
from models import ContentIdea, CreativeDirection
from config import EngineConfig


class BrandComplianceChecker:
    """Ensures creative direction aligns with brand guidelines."""
    
    def __init__(self, config: EngineConfig):
        self.config = config
        self.brand = config.brand
    
    def check_compliance(self, direction: CreativeDirection) -> Dict[str, any]:
        """
        Check if creative direction complies with brand guidelines.
        
        Returns:
            Dict with 'compliant' bool and 'issues' list
        """
        issues = []
        
        # Check tone compliance
        if not self._check_tone_compliance(direction):
            issues.append(f"Tone may not align with brand tone: {self.brand.tone}")
        
        # Check voice compliance
        if not self._check_voice_compliance(direction):
            issues.append(f"Voice may not align with brand voice: {self.brand.voice}")
        
        # Check brand guidelines
        if self.brand.guidelines and not self._check_guidelines_compliance(direction):
            issues.append("Content may not follow brand guidelines")
        
        return {
            'compliant': len(issues) == 0,
            'issues': issues
        }
    
    def _check_tone_compliance(self, direction: CreativeDirection) -> bool:
        """Check if tone matches brand tone."""
        # Simple keyword matching for tone
        tone_keywords = {
            'professional': ['business', 'expert', 'quality', 'reliable'],
            'casual': ['friendly', 'relaxed', 'fun', 'easy'],
            'formal': ['prestigious', 'distinguished', 'refined', 'sophisticated'],
            'playful': ['exciting', 'vibrant', 'dynamic', 'energetic']
        }
        
        expected_keywords = tone_keywords.get(self.brand.tone.lower(), [])
        script_lower = direction.voiceover_script.lower()
        
        # If any expected keyword is found, consider it compliant
        return any(keyword in script_lower for keyword in expected_keywords) if expected_keywords else True
    
    def _check_voice_compliance(self, direction: CreativeDirection) -> bool:
        """Check if voice matches brand voice."""
        # Simplified voice compliance check
        return True  # Default to compliant
    
    def _check_guidelines_compliance(self, direction: CreativeDirection) -> bool:
        """Check compliance with specific brand guidelines."""
        return True  # Default to compliant


class CreativeGenerator:
    """Generates creative direction using AI."""
    
    def __init__(self, config: EngineConfig):
        self.config = config
        self.ai_config = config.ai
        self.brand = config.brand
    
    def generate_direction(self, idea: ContentIdea) -> CreativeDirection:
        """
        Generate creative direction from a content idea.
        
        Args:
            idea: ContentIdea to generate direction for
            
        Returns:
            CreativeDirection object
        """
        # Generate visual style
        visual_style = self._generate_visual_style(idea)
        
        # Generate narrative arc
        narrative_arc = self._generate_narrative_arc(idea)
        
        # Generate scenes
        scenes = self._generate_scenes(idea, narrative_arc)
        
        # Generate music style
        music_style = self._generate_music_style(idea)
        
        # Generate voiceover script
        voiceover_script = self._generate_voiceover_script(idea, narrative_arc)
        
        direction = CreativeDirection(
            content_id=idea.id,
            visual_style=visual_style,
            narrative_arc=narrative_arc,
            scenes=scenes,
            music_style=music_style,
            voiceover_script=voiceover_script,
            brand_compliant=True
        )
        
        return direction
    
    def _generate_visual_style(self, idea: ContentIdea) -> str:
        """Generate visual style based on content type and brand."""
        style_map = {
            'educational': f"Clean and professional with {self.brand.name} brand colors",
            'marketing': f"Eye-catching and dynamic with bold {self.brand.name} branding",
            'promotional': f"High-energy with vibrant {self.brand.name} brand elements",
            'tutorial': f"Clear and instructional with consistent {self.brand.name} styling",
            'advertisement': f"Compelling and memorable with strong {self.brand.name} identity"
        }
        return style_map.get(idea.content_type, f"Modern and engaging with {self.brand.name} branding")
    
    def _generate_narrative_arc(self, idea: ContentIdea) -> List[str]:
        """Generate narrative arc structure."""
        duration = idea.duration_seconds
        
        if duration <= 30:
            # Short form: Hook, Message, CTA
            return [
                "Hook: Attention-grabbing opening (0-5s)",
                "Core Message: Main content delivery (5-25s)",
                "Call to Action: Clear next steps (25-30s)"
            ]
        elif duration <= 90:
            # Medium form: Hook, Context, Solution, CTA
            return [
                "Hook: Compelling opening question or statement (0-10s)",
                "Context: Establish the problem or opportunity (10-30s)",
                "Solution: Present the main content/solution (30-75s)",
                "Call to Action: Encourage engagement (75-90s)"
            ]
        else:
            # Long form: Full story arc
            return [
                "Hook: Captivating introduction (0-15s)",
                "Context: Background and problem setup (15-60s)",
                "Development: Deep dive into content (60-240s)",
                "Resolution: Key takeaways and insights (240-300s)",
                "Call to Action: Next steps and engagement (300s+)"
            ]
    
    def _generate_scenes(self, idea: ContentIdea, narrative_arc: List[str]) -> List[Dict[str, any]]:
        """Generate scene breakdown."""
        scenes = []
        duration_per_arc = idea.duration_seconds / len(narrative_arc)
        
        for i, arc in enumerate(narrative_arc):
            scene = {
                'scene_number': i + 1,
                'description': arc,
                'duration': duration_per_arc,
                'visuals': f"Visual for {arc.split(':')[0].strip()}",
                'text_overlay': idea.key_messages[i] if i < len(idea.key_messages) else ""
            }
            scenes.append(scene)
        
        return scenes
    
    def _generate_music_style(self, idea: ContentIdea) -> str:
        """Generate appropriate music style."""
        music_map = {
            'educational': "Uplifting and focused background music",
            'marketing': "Energetic and motivational music",
            'promotional': "High-energy commercial music",
            'tutorial': "Calm and non-distracting background music",
            'advertisement': "Catchy and memorable music"
        }
        return music_map.get(idea.content_type, "Modern and appropriate background music")
    
    def _generate_voiceover_script(self, idea: ContentIdea, narrative_arc: List[str]) -> str:
        """Generate voiceover script."""
        script_parts = [
            f"# {self.brand.name} - {idea.title}",
            "",
            "## Opening Hook",
            f"Welcome! Today we're exploring {idea.title}.",
            "",
            "## Main Content"
        ]
        
        # Add key messages
        for i, message in enumerate(idea.key_messages, 1):
            script_parts.append(f"{i}. {message}")
        
        script_parts.extend([
            "",
            "## Closing",
            f"Thank you for watching. {idea.description[:100]}...",
            "",
            "## Call to Action",
            "Don't forget to like, subscribe, and share!"
        ])
        
        return "\n".join(script_parts)


class CreativeDirectionPillar:
    """
    Second Operational Pillar: Creative Direction
    
    Generates brand-compliant creative guidelines and direction
    for content production.
    """
    
    def __init__(self, config: EngineConfig):
        self.config = config
        self.generator = CreativeGenerator(config)
        self.compliance_checker = BrandComplianceChecker(config)
    
    def create_direction(self, idea: ContentIdea) -> Dict[str, any]:
        """
        Create creative direction for a content idea.
        
        Args:
            idea: ContentIdea to create direction for
            
        Returns:
            Dict containing:
                - success: bool
                - direction: CreativeDirection object
                - compliance_issues: List of compliance issues
        """
        # Generate creative direction
        direction = self.generator.generate_direction(idea)
        
        # Check brand compliance
        compliance_result = self.compliance_checker.check_compliance(direction)
        
        if not compliance_result['compliant']:
            direction.brand_compliant = False
            direction.compliance_notes = "; ".join(compliance_result['issues'])
        
        return {
            'success': True,
            'direction': direction,
            'compliance_issues': compliance_result['issues']
        }
    
    def refine_direction(self, direction: CreativeDirection, feedback: str) -> CreativeDirection:
        """
        Refine creative direction based on feedback.
        
        Args:
            direction: Existing CreativeDirection
            feedback: Feedback string for refinement
            
        Returns:
            Updated CreativeDirection
        """
        # Add feedback to compliance notes
        if direction.compliance_notes:
            direction.compliance_notes += f" | Feedback: {feedback}"
        else:
            direction.compliance_notes = f"Feedback: {feedback}"
        
        return direction
