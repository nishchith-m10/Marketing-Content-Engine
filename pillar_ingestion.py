"""
Content Ingestion Module
=========================

First operational pillar: Processes and validates content ideas.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import validators
from models import ContentIdea, ContentType, ContentStatus
from config import EngineConfig


class ContentValidator:
    """Validates content ideas for quality and completeness."""
    
    def __init__(self, config: EngineConfig):
        self.config = config
    
    def validate_idea(self, idea: ContentIdea) -> Dict[str, Any]:
        """
        Validate a content idea.
        
        Returns:
            Dict with 'valid' bool and 'errors' list
        """
        errors = []
        
        # Check required fields
        if not idea.title or len(idea.title.strip()) < 3:
            errors.append("Title must be at least 3 characters long")
        
        if not idea.description or len(idea.description.strip()) < 10:
            errors.append("Description must be at least 10 characters long")
        
        # Check duration constraints
        if idea.duration_seconds < 10:
            errors.append("Duration must be at least 10 seconds")
        elif idea.duration_seconds > 600:
            errors.append("Duration cannot exceed 600 seconds (10 minutes)")
        
        # Validate target audience
        if not idea.target_audience:
            errors.append("Target audience must be specified")
        
        # Check for brand safety
        brand_safety_result = self._check_brand_safety(idea)
        if not brand_safety_result['safe']:
            errors.extend(brand_safety_result['issues'])
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _check_brand_safety(self, idea: ContentIdea) -> Dict[str, Any]:
        """
        Check content for brand safety concerns.
        
        Returns:
            Dict with 'safe' bool and 'issues' list
        """
        issues = []
        
        # Check for inappropriate keywords
        inappropriate_keywords = [
            'violence', 'explicit', 'offensive', 'controversial',
            'illegal', 'harmful'
        ]
        
        text_to_check = (idea.title + " " + idea.description).lower()
        
        for keyword in inappropriate_keywords:
            if keyword in text_to_check:
                issues.append(f"Content may contain inappropriate theme: {keyword}")
        
        return {
            'safe': len(issues) == 0,
            'issues': issues
        }


class ContentEnricher:
    """Enriches content ideas with additional metadata and context."""
    
    def __init__(self, config: EngineConfig):
        self.config = config
    
    def enrich_idea(self, idea: ContentIdea) -> ContentIdea:
        """
        Enrich a content idea with additional metadata.
        """
        # Auto-generate keywords if not provided
        if not idea.keywords:
            idea.keywords = self._extract_keywords(idea)
        
        # Ensure key messages are present
        if not idea.key_messages:
            idea.key_messages = self._extract_key_messages(idea)
        
        return idea
    
    def _extract_keywords(self, idea: ContentIdea) -> List[str]:
        """Extract keywords from content idea."""
        # Simple keyword extraction based on common words
        words = (idea.title + " " + idea.description).split()
        keywords = []
        
        # Filter out common words and keep meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        for word in words:
            clean_word = word.strip('.,!?;:').lower()
            if len(clean_word) > 3 and clean_word not in stop_words:
                if clean_word not in keywords:
                    keywords.append(clean_word)
        
        return keywords[:10]  # Return top 10 keywords
    
    def _extract_key_messages(self, idea: ContentIdea) -> List[str]:
        """Extract key messages from content description."""
        # Split description into sentences as key messages
        sentences = idea.description.replace('!', '.').replace('?', '.').split('.')
        messages = [s.strip() for s in sentences if len(s.strip()) > 10]
        return messages[:3]  # Return top 3 messages


class ContentIngestionPillar:
    """
    First Operational Pillar: Content Ingestion
    
    Processes and validates incoming content ideas, ensuring they meet
    quality standards and brand safety requirements.
    """
    
    def __init__(self, config: EngineConfig):
        self.config = config
        self.validator = ContentValidator(config)
        self.enricher = ContentEnricher(config)
    
    def ingest_content(self, idea: ContentIdea) -> Dict[str, Any]:
        """
        Ingest and process a content idea.
        
        Args:
            idea: ContentIdea to process
            
        Returns:
            Dict containing:
                - success: bool
                - idea: Enriched ContentIdea (if successful)
                - errors: List of validation errors (if failed)
        """
        # Validate the content idea
        validation_result = self.validator.validate_idea(idea)
        
        if not validation_result['valid']:
            return {
                'success': False,
                'errors': validation_result['errors'],
                'idea': None
            }
        
        # Enrich the content idea
        enriched_idea = self.enricher.enrich_idea(idea)
        
        return {
            'success': True,
            'errors': [],
            'idea': enriched_idea
        }
    
    def batch_ingest(self, ideas: List[ContentIdea]) -> Dict[str, Any]:
        """
        Ingest multiple content ideas in batch.
        
        Returns:
            Dict with successful and failed ingestions
        """
        successful = []
        failed = []
        
        for idea in ideas:
            result = self.ingest_content(idea)
            if result['success']:
                successful.append(result['idea'])
            else:
                failed.append({
                    'idea': idea,
                    'errors': result['errors']
                })
        
        return {
            'successful': successful,
            'failed': failed,
            'total': len(ideas),
            'success_rate': len(successful) / len(ideas) if ideas else 0
        }
