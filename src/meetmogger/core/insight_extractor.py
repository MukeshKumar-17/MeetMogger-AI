"""
Advanced insight extraction from call transcripts.

Provides modular and extendable insight extraction with classification,
tagging, and structured output capabilities.
"""

import re
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum

from ..utils.logger import get_logger
from ..utils.validators import validate_transcript, validate_insight_data

logger = get_logger(__name__)


class InsightType(Enum):
    """Types of insights that can be extracted."""
    PROBLEM = "problem"
    SOLUTION = "solution"
    ACTION_ITEM = "action_item"
    OPPORTUNITY = "opportunity"
    RISK = "risk"
    DECISION = "decision"


@dataclass
class Insight:
    """Data class for individual insights."""
    text: str
    type: InsightType
    confidence: float
    category: str
    keywords: List[str]
    context: str
    priority: str = "medium"


class InsightExtractor:
    """
    Advanced insight extractor with modular pattern matching.
    
    Provides comprehensive insight extraction with classification,
    confidence scoring, and structured output.
    """
    
    def __init__(self):
        """Initialize insight extractor with pattern definitions."""
        self.patterns = self._initialize_patterns()
        self.stop_words = self._initialize_stop_words()
        
    def _initialize_patterns(self) -> Dict[InsightType, Dict[str, List[str]]]:
        """Initialize extraction patterns for different insight types."""
        return {
            InsightType.PROBLEM: {
                "patterns": [
                    r"(?:problem|issue|challenge|concern|difficult|trouble|obstacle|barrier|pain point)[\s\w\',-]*[.!?]",
                    r"(?:struggling|facing|dealing with|having trouble with)[\s\w\',-]*[.!?]",
                    r"(?:not working|broken|failed|unsuccessful)[\s\w\',-]*[.!?]",
                    r"(?:need to fix|need to resolve|need to address)[\s\w\',-]*[.!?]",
                    r"(?:concerned about|worried about|anxious about)[\s\w\',-]*[.!?]"
                ],
                "keywords": ["problem", "issue", "challenge", "concern", "difficult", "trouble", "struggling", "broken", "failed"],
                "categories": ["technical", "business", "process", "resource", "timeline"]
            },
            
            InsightType.SOLUTION: {
                "patterns": [
                    r"(?:solution|resolve|fix|address|recommend|suggest|propose|implement)[\s\w\',-]*[.!?]",
                    r"(?:we can|we should|we need to|let's|how about)[\s\w\',-]*[.!?]",
                    r"(?:best practice|approach|method|strategy)[\s\w\',-]*[.!?]",
                    r"(?:workaround|alternative|option)[\s\w\',-]*[.!?]",
                    r"(?:upgrade|improve|enhance|optimize)[\s\w\',-]*[.!?]"
                ],
                "keywords": ["solution", "resolve", "fix", "address", "recommend", "suggest", "implement", "approach", "strategy"],
                "categories": ["technical", "process", "training", "resource", "timeline"]
            },
            
            InsightType.ACTION_ITEM: {
                "patterns": [
                    r"(?:action item|next step|todo|task|follow up|follow-up)[\s\w\',-]*[.!?]",
                    r"(?:we need to|we should|we will|we'll|let's)[\s\w\',-]*[.!?]",
                    r"(?:schedule|plan|arrange|coordinate)[\s\w\',-]*[.!?]",
                    r"(?:deadline|due date|timeline|schedule)[\s\w\',-]*[.!?]",
                    r"(?:assign|delegate|responsible|owner)[\s\w\',-]*[.!?]"
                ],
                "keywords": ["action", "next", "step", "todo", "task", "follow", "schedule", "deadline", "assign", "responsible"],
                "categories": ["immediate", "short_term", "long_term", "ongoing"]
            },
            
            InsightType.OPPORTUNITY: {
                "patterns": [
                    r"(?:opportunity|potential|possibility|chance|prospect)[\s\w\',-]*[.!?]",
                    r"(?:could|might|may|if we)[\s\w\',-]*[.!?]",
                    r"(?:upsell|cross-sell|expand|grow|scale)[\s\w\',-]*[.!?]",
                    r"(?:partnership|collaboration|joint|together)[\s\w\',-]*[.!?]",
                    r"(?:market|customer|client|account)[\s\w\',-]*[.!?]"
                ],
                "keywords": ["opportunity", "potential", "possibility", "chance", "upsell", "expand", "partnership", "market"],
                "categories": ["sales", "partnership", "expansion", "market", "product"]
            },
            
            InsightType.RISK: {
                "patterns": [
                    r"(?:risk|threat|danger|concern|worry)[\s\w\',-]*[.!?]",
                    r"(?:if not|unless|otherwise|or else)[\s\w\',-]*[.!?]",
                    r"(?:budget|cost|expense|financial)[\s\w\',-]*[.!?]",
                    r"(?:timeline|schedule|deadline|delay)[\s\w\',-]*[.!?]",
                    r"(?:competition|competitor|market)[\s\w\',-]*[.!?]"
                ],
                "keywords": ["risk", "threat", "danger", "concern", "worry", "budget", "cost", "timeline", "competition"],
                "categories": ["financial", "timeline", "competitive", "technical", "operational"]
            },
            
            InsightType.DECISION: {
                "patterns": [
                    r"(?:decide|decision|choose|select|pick)[\s\w\',-]*[.!?]",
                    r"(?:agree|disagree|approve|reject)[\s\w\',-]*[.!?]",
                    r"(?:final|conclude|determine|resolve)[\s\w\',-]*[.!?]",
                    r"(?:yes|no|maybe|perhaps|possibly)[\s\w\',-]*[.!?]",
                    r"(?:go with|proceed with|move forward)[\s\w\',-]*[.!?]"
                ],
                "keywords": ["decide", "decision", "choose", "select", "agree", "approve", "final", "conclude", "yes", "no"],
                "categories": ["approval", "selection", "direction", "commitment", "rejection"]
            }
        }
    
    def _initialize_stop_words(self) -> Set[str]:
        """Initialize common stop words for filtering."""
        return {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
            "will", "would", "could", "should", "may", "might", "must", "can", "this", "that", "these", "those"
        }
    
    def extract_insights(self, text: str) -> Dict[str, Any]:
        """
        Extract comprehensive insights from transcript.
        
        Args:
            text: Input transcript text
            
        Returns:
            Dictionary with extracted insights and metadata
        """
        # Validate input
        validation = validate_transcript(text)
        if not validation["is_valid"]:
            logger.warning(f"Invalid transcript: {validation['error']}")
            return self._create_empty_result(validation["error"])
        
        cleaned_text = validation["transcript"]
        
        try:
            # Extract insights by type
            insights_by_type = {}
            all_insights = []
            
            for insight_type in InsightType:
                insights = self._extract_insights_by_type(cleaned_text, insight_type)
                insights_by_type[insight_type.value] = insights
                all_insights.extend(insights)
            
            # Create structured output
            result = {
                "problems": [i.text for i in insights_by_type[InsightType.PROBLEM.value]],
                "solutions": [i.text for i in insights_by_type[InsightType.SOLUTION.value]],
                "action_items": [i.text for i in insights_by_type[InsightType.ACTION_ITEM.value]],
                "opportunities": [i.text for i in insights_by_type[InsightType.OPPORTUNITY.value]],
                "risks": [i.text for i in insights_by_type[InsightType.RISK.value]],
                "decisions": [i.text for i in insights_by_type[InsightType.DECISION.value]],
                "metadata": {
                    "total_insights": len(all_insights),
                    "insights_by_type": {k: len(v) for k, v in insights_by_type.items()},
                    "extraction_confidence": self._calculate_extraction_confidence(all_insights),
                    "high_priority_items": [i.text for i in all_insights if i.priority == "high"]
                },
                "detailed_insights": {
                    insight_type.value: [
                        {
                            "text": insight.text,
                            "confidence": insight.confidence,
                            "category": insight.category,
                            "keywords": insight.keywords,
                            "priority": insight.priority
                        }
                        for insight in insights
                    ]
                    for insight_type, insights in insights_by_type.items()
                }
            }
            
            # Validate result
            validation_result = validate_insight_data(result)
            if not validation_result["is_valid"]:
                logger.warning(f"Insight validation failed: {validation_result['errors']}")
            
            logger.info(f"Extracted {len(all_insights)} insights from transcript")
            return result
            
        except Exception as e:
            logger.error(f"Insight extraction error: {e}")
            return self._create_empty_result(f"Extraction error: {str(e)}")
    
    def _extract_insights_by_type(self, text: str, insight_type: InsightType) -> List[Insight]:
        """Extract insights of a specific type."""
        insights = []
        patterns_config = self.patterns[insight_type]
        
        # Extract using patterns
        for pattern in patterns_config["patterns"]:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    match = " ".join(match)
                
                # Clean and validate match
                cleaned_match = self._clean_insight_text(match)
                if self._is_valid_insight(cleaned_match):
                    insight = self._create_insight(
                        cleaned_match, 
                        insight_type, 
                        patterns_config,
                        text
                    )
                    if insight:
                        insights.append(insight)
        
        # Remove duplicates and sort by confidence
        unique_insights = self._deduplicate_insights(insights)
        return sorted(unique_insights, key=lambda x: x.confidence, reverse=True)
    
    def _clean_insight_text(self, text: str) -> str:
        """Clean and normalize insight text."""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common prefixes
        prefixes_to_remove = [
            r'^(?:so|well|okay|ok|alright|right|yes|no|sure|absolutely|definitely)\s*',
            r'^(?:i think|i believe|i feel|i guess|i suppose)\s*',
            r'^(?:we need to|we should|we can|we will|we\'ll)\s*'
        ]
        
        for prefix in prefixes_to_remove:
            cleaned = re.sub(prefix, '', cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip()
    
    def _is_valid_insight(self, text: str) -> bool:
        """Check if insight text is valid and meaningful."""
        if not text or len(text) < 10:
            return False
        
        # Check for minimum word count
        words = text.split()
        if len(words) < 3:
            return False
        
        # Check for too many stop words
        stop_word_count = sum(1 for word in words if word.lower() in self.stop_words)
        if stop_word_count / len(words) > 0.7:
            return False
        
        return True
    
    def _create_insight(
        self, 
        text: str, 
        insight_type: InsightType, 
        patterns_config: Dict[str, Any],
        context: str
    ) -> Optional[Insight]:
        """Create Insight object from extracted text."""
        try:
            # Calculate confidence based on pattern matching and text quality
            confidence = self._calculate_insight_confidence(text, patterns_config)
            
            # Extract keywords
            keywords = self._extract_keywords(text, patterns_config["keywords"])
            
            # Determine category
            category = self._categorize_insight(text, patterns_config["categories"])
            
            # Determine priority
            priority = self._determine_priority(text, insight_type, confidence)
            
            # Extract context (surrounding sentences)
            context_sentences = self._extract_context(text, context)
            
            return Insight(
                text=text,
                type=insight_type,
                confidence=confidence,
                category=category,
                keywords=keywords,
                context=context_sentences,
                priority=priority
            )
            
        except Exception as e:
            logger.error(f"Error creating insight: {e}")
            return None
    
    def _calculate_insight_confidence(self, text: str, patterns_config: Dict[str, Any]) -> float:
        """Calculate confidence score for insight."""
        confidence = 0.0
        
        # Base confidence from keyword presence
        keywords = patterns_config["keywords"]
        text_lower = text.lower()
        keyword_matches = sum(1 for keyword in keywords if keyword in text_lower)
        confidence += min(keyword_matches * 0.2, 0.6)
        
        # Boost confidence for longer, more detailed insights
        word_count = len(text.split())
        if word_count > 10:
            confidence += 0.2
        elif word_count > 5:
            confidence += 0.1
        
        # Boost confidence for specific action words
        action_words = ["will", "should", "need", "must", "can", "could"]
        action_matches = sum(1 for word in action_words if word in text_lower)
        confidence += min(action_matches * 0.1, 0.2)
        
        return min(confidence, 1.0)
    
    def _extract_keywords(self, text: str, pattern_keywords: List[str]) -> List[str]:
        """Extract relevant keywords from text."""
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in pattern_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _categorize_insight(self, text: str, categories: List[str]) -> str:
        """Categorize insight based on content."""
        text_lower = text.lower()
        
        # Simple keyword-based categorization
        category_keywords = {
            "technical": ["technical", "system", "software", "hardware", "bug", "error", "code"],
            "business": ["business", "revenue", "profit", "customer", "market", "sales"],
            "process": ["process", "workflow", "procedure", "method", "approach"],
            "resource": ["resource", "budget", "cost", "money", "funding", "staff", "team"],
            "timeline": ["timeline", "schedule", "deadline", "date", "time", "urgent", "priority"]
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return categories[0] if categories else "general"
    
    def _determine_priority(self, text: str, insight_type: InsightType, confidence: float) -> str:
        """Determine priority level for insight."""
        text_lower = text.lower()
        
        # High priority indicators
        high_priority_words = ["urgent", "critical", "important", "asap", "immediately", "deadline"]
        if any(word in text_lower for word in high_priority_words):
            return "high"
        
        # Medium priority for action items and problems
        if insight_type in [InsightType.ACTION_ITEM, InsightType.PROBLEM] and confidence > 0.5:
            return "medium"
        
        # Low priority for opportunities and general insights
        if insight_type in [InsightType.OPPORTUNITY, InsightType.DECISION]:
            return "low"
        
        return "medium"
    
    def _extract_context(self, text: str, full_context: str) -> str:
        """Extract surrounding context for insight."""
        # Find the insight in the full context
        text_lower = text.lower()
        context_lower = full_context.lower()
        
        start_pos = context_lower.find(text_lower)
        if start_pos == -1:
            return text
        
        # Extract surrounding sentences
        sentences = re.split(r'[.!?]+', full_context)
        context_sentences = []
        
        for i, sentence in enumerate(sentences):
            if text_lower in sentence.lower():
                # Add current sentence and surrounding ones
                start_idx = max(0, i - 1)
                end_idx = min(len(sentences), i + 2)
                context_sentences = sentences[start_idx:end_idx]
                break
        
        return " ".join(context_sentences).strip()
    
    def _deduplicate_insights(self, insights: List[Insight]) -> List[Insight]:
        """Remove duplicate insights based on text similarity."""
        if not insights:
            return []
        
        unique_insights = []
        seen_texts = set()
        
        for insight in insights:
            # Simple deduplication based on text similarity
            text_lower = insight.text.lower()
            if text_lower not in seen_texts:
                unique_insights.append(insight)
                seen_texts.add(text_lower)
        
        return unique_insights
    
    def _calculate_extraction_confidence(self, insights: List[Insight]) -> float:
        """Calculate overall extraction confidence."""
        if not insights:
            return 0.0
        
        avg_confidence = sum(insight.confidence for insight in insights) / len(insights)
        return round(avg_confidence, 3)
    
    def _create_empty_result(self, error: str) -> Dict[str, Any]:
        """Create empty result for error cases."""
        return {
            "problems": [],
            "solutions": [],
            "action_items": [],
            "opportunities": [],
            "risks": [],
            "decisions": [],
            "metadata": {
                "total_insights": 0,
                "insights_by_type": {},
                "extraction_confidence": 0.0,
                "high_priority_items": [],
                "error": error
            },
            "detailed_insights": {}
        }
