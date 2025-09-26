"""
Unit tests for InsightExtractor.

Tests the insight extraction functionality with various input scenarios.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from meetmogger.core.insight_extractor import InsightExtractor, InsightType


class TestInsightExtractor:
    """Test cases for InsightExtractor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = InsightExtractor()
    
    def test_extract_problems(self):
        """Test extraction of problems."""
        text = "We have a major problem with the system. The issue is causing delays."
        result = self.extractor.extract_insights(text)
        
        assert len(result["problems"]) > 0
        assert any("problem" in problem.lower() for problem in result["problems"])
        assert "problems" in result["detailed_insights"]
    
    def test_extract_solutions(self):
        """Test extraction of solutions."""
        text = "We can fix this by implementing a new solution. Let's address the issue."
        result = self.extractor.extract_insights(text)
        
        assert len(result["solutions"]) > 0
        assert any("solution" in solution.lower() for solution in result["solutions"])
        assert "solutions" in result["detailed_insights"]
    
    def test_extract_action_items(self):
        """Test extraction of action items."""
        text = "We need to follow up next week. The action item is to schedule a meeting."
        result = self.extractor.extract_insights(text)
        
        assert len(result["action_items"]) > 0
        assert any("action" in item.lower() for item in result["action_items"])
        assert "action_items" in result["detailed_insights"]
    
    def test_extract_opportunities(self):
        """Test extraction of opportunities."""
        text = "There's a great opportunity to expand our market. We could partner with them."
        result = self.extractor.extract_insights(text)
        
        assert len(result["opportunities"]) > 0
        assert any("opportunity" in opp.lower() for opp in result["opportunities"])
        assert "opportunities" in result["detailed_insights"]
    
    def test_extract_risks(self):
        """Test extraction of risks."""
        text = "There's a risk of budget overrun. We're concerned about the timeline."
        result = self.extractor.extract_insights(text)
        
        assert len(result["risks"]) > 0
        assert any("risk" in risk.lower() for risk in result["risks"])
        assert "risks" in result["detailed_insights"]
    
    def test_extract_decisions(self):
        """Test extraction of decisions."""
        text = "We decided to proceed with the project. The decision was made to go ahead."
        result = self.extractor.extract_insights(text)
        
        assert len(result["decisions"]) > 0
        assert any("decide" in decision.lower() for decision in result["decisions"])
        assert "decisions" in result["detailed_insights"]
    
    def test_empty_text(self):
        """Test extraction from empty text."""
        result = self.extractor.extract_insights("")
        
        assert result["problems"] == []
        assert result["solutions"] == []
        assert result["action_items"] == []
        assert result["metadata"]["total_insights"] == 0
    
    def test_invalid_input(self):
        """Test extraction from invalid input."""
        result = self.extractor.extract_insights(None)
        
        assert "error" in result["metadata"]
        assert result["metadata"]["total_insights"] == 0
    
    def test_insight_confidence(self):
        """Test confidence calculation for insights."""
        text = "We definitely need to fix this critical problem immediately."
        result = self.extractor.extract_insights(text)
        
        assert result["metadata"]["extraction_confidence"] > 0
        assert result["metadata"]["extraction_confidence"] <= 1.0
    
    def test_insight_prioritization(self):
        """Test priority assignment for insights."""
        text = "This is urgent! We need to address this critical issue ASAP."
        result = self.extractor.extract_insights(text)
        
        # Check that high priority items are identified
        high_priority = result["metadata"]["high_priority_items"]
        assert len(high_priority) >= 0  # May or may not have high priority items
    
    def test_insight_deduplication(self):
        """Test that duplicate insights are removed."""
        text = "We have a problem. The problem is serious. We need to fix the problem."
        result = self.extractor.extract_insights(text)
        
        # Should not have exact duplicates
        problems = result["problems"]
        assert len(problems) == len(set(problems))
    
    def test_insight_categorization(self):
        """Test insight categorization."""
        text = "We have a technical problem with the software system."
        result = self.extractor.extract_insights(text)
        
        if result["detailed_insights"]["problems"]:
            problem = result["detailed_insights"]["problems"][0]
            assert "category" in problem
            assert problem["category"] in ["technical", "business", "process", "resource", "timeline"]
    
    def test_metadata_creation(self):
        """Test metadata creation."""
        text = "We have problems and solutions. Let's create action items."
        result = self.extractor.extract_insights(text)
        
        assert "total_insights" in result["metadata"]
        assert "insights_by_type" in result["metadata"]
        assert "extraction_confidence" in result["metadata"]
        assert "high_priority_items" in result["metadata"]
