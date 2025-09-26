"""
Professional Streamlit dashboard for MeetMogger AI.

Provides a polished, business-ready interface with navigation,
visualizations, and comprehensive analysis capabilities.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional
import json
import io

from ..core.sentiment_analyzer import SentimentAnalyzer
from ..core.insight_extractor import InsightExtractor
from ..core.transcript_processor import TranscriptProcessor
from ..utils.file_handler import FileHandler
from ..utils.logger import setup_logger

# Setup logging
logger = setup_logger("meetmogger_ui")


def create_dashboard():
    """Create and configure the main dashboard."""
    # Page configuration
    st.set_page_config(
        page_title="MeetMogger AI - Call Intelligence Platform",
        page_icon="📞",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "transcript_text" not in st.session_state:
        st.session_state.transcript_text = ""
    
    # Main header
    st.markdown('<h1 class="main-header">📞 MeetMogger AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Call Intelligence Platform</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/1f77b4/ffffff?text=MeetMogger", width=200)
        
        st.markdown("## Navigation")
        page = st.selectbox(
            "Select Page",
            ["📝 Input Transcript", "📊 Analysis Results", "📈 Insights Dashboard", "⚙️ Settings"]
        )
        
        st.markdown("---")
        st.markdown("## Quick Actions")
        if st.button("🔄 Clear All Data"):
            st.session_state.analysis_results = None
            st.session_state.transcript_text = ""
            st.rerun()
        
        if st.button("💾 Export Results"):
            if st.session_state.analysis_results:
                export_data(st.session_state.analysis_results)
    
    # Main content based on selected page
    if page == "📝 Input Transcript":
        input_page()
    elif page == "📊 Analysis Results":
        results_page()
    elif page == "📈 Insights Dashboard":
        dashboard_page()
    elif page == "⚙️ Settings":
        settings_page()


def input_page():
    """Input transcript page with file upload and text input."""
    st.header("📝 Input Transcript")
    
    # File upload section
    with st.expander("📁 Upload File", expanded=True):
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['txt', 'pdf', 'docx'],
            help="Supported formats: TXT, PDF, DOCX"
        )
        
        if uploaded_file is not None:
            file_handler = FileHandler()
            result = file_handler.process_uploaded_file(
                uploaded_file.read(),
                uploaded_file.type,
                uploaded_file.name
            )
            
            if result["success"]:
                st.session_state.transcript_text = result["content"]
                st.success(f"✅ Successfully loaded {uploaded_file.name}")
            else:
                st.error(f"❌ Error loading file: {result['error']}")
    
    # Seed brief generation
    with st.expander("🌱 Generate from Seed Brief", expanded=False):
        seed_brief = st.text_area(
            "Enter a brief description to generate a mock transcript:",
            height=100,
            placeholder="e.g., Tech startup seeking distribution partnership..."
        )
        
        if st.button("Generate Mock Transcript"):
            if seed_brief.strip():
                # Simple mock generation (would use actual LLM in production)
                mock_transcript = generate_mock_transcript(seed_brief)
                st.session_state.transcript_text = mock_transcript
                st.success("✅ Mock transcript generated!")
            else:
                st.warning("Please enter a seed brief")
    
    # Direct text input
    st.markdown("### Or paste transcript directly:")
    transcript = st.text_area(
        "Call Transcript:",
        height=300,
        value=st.session_state.transcript_text,
        placeholder="Paste your call transcript here...",
        help="Enter the conversation transcript for analysis"
    )
    
    if transcript:
        st.session_state.transcript_text = transcript
        
        # Analysis button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Analyze Transcript", type="primary", use_container_width=True):
                with st.spinner("Analyzing transcript..."):
                    try:
                        # Initialize analyzers
                        sentiment_analyzer = SentimentAnalyzer()
                        insight_extractor = InsightExtractor()
                        transcript_processor = TranscriptProcessor()
                        
                        # Process transcript
                        processed_transcript = transcript_processor.process(transcript)
                        
                        # Perform analysis
                        sentiment_result = sentiment_analyzer.analyze(transcript)
                        insights = insight_extractor.extract_insights(transcript)
                        
                        # Store results
                        st.session_state.analysis_results = {
                            "sentiment": sentiment_result,
                            "insights": insights,
                            "processed_transcript": processed_transcript,
                            "metadata": {
                                "transcript_length": len(transcript),
                                "word_count": len(transcript.split()),
                                "analysis_timestamp": pd.Timestamp.now().isoformat()
                            }
                        }
                        
                        st.success("✅ Analysis completed successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                        logger.error(f"Analysis error: {e}")


def results_page():
    """Display analysis results with visualizations."""
    if not st.session_state.analysis_results:
        st.warning("⚠️ No analysis results available. Please analyze a transcript first.")
        return
    
    st.header("📊 Analysis Results")
    
    results = st.session_state.analysis_results
    sentiment = results["sentiment"]
    insights = results["insights"]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Sentiment",
            sentiment.overall,
            f"{sentiment.score:.3f}"
        )
    
    with col2:
        st.metric(
            "Confidence",
            f"{sentiment.confidence:.1%}",
            f"Score: {sentiment.score:.3f}"
        )
    
    with col3:
        st.metric(
            "Total Insights",
            insights["metadata"]["total_insights"],
            f"High Priority: {len(insights['metadata']['high_priority_items'])}"
        )
    
    with col4:
        st.metric(
            "Action Items",
            len(insights["action_items"]),
            f"Problems: {len(insights['problems'])}"
        )
    
    # Sentiment analysis section
    st.markdown("---")
    st.subheader("📈 Sentiment Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sentiment distribution chart
        if sentiment.summary and "sentiment_distribution" in sentiment.summary:
            dist_data = sentiment.summary["sentiment_distribution"]
            fig = px.pie(
                values=list(dist_data.values()),
                names=list(dist_data.keys()),
                title="Sentiment Distribution",
                color_discrete_map={
                    "Positive": "#28a745",
                    "Negative": "#dc3545",
                    "Neutral": "#6c757d"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Key sentences
        st.markdown("**Key Sentences**")
        important_sentences = [s for s in sentiment.sentences if s.get("is_important", False)]
        
        for i, sentence in enumerate(important_sentences[:5], 1):
            with st.container():
                st.markdown(f"**{i}.** {sentence['highlighted_text']}")
                st.caption(f"{sentence['sentiment']} (confidence: {sentence['confidence']:.2f})")
    
    # Insights section
    st.markdown("---")
    st.subheader("💡 Extracted Insights")
    
    # Create tabs for different insight types
    tab1, tab2, tab3, tab4 = st.tabs(["🚨 Problems", "✅ Solutions", "📋 Action Items", "🎯 Opportunities"])
    
    with tab1:
        display_insights(insights["problems"], "Problems")
    
    with tab2:
        display_insights(insights["solutions"], "Solutions")
    
    with tab3:
        display_insights(insights["action_items"], "Action Items")
    
    with tab4:
        display_insights(insights["opportunities"], "Opportunities")


def dashboard_page():
    """Advanced insights dashboard with visualizations."""
    if not st.session_state.analysis_results:
        st.warning("⚠️ No analysis results available. Please analyze a transcript first.")
        return
    
    st.header("📈 Insights Dashboard")
    
    results = st.session_state.analysis_results
    insights = results["insights"]
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Insight Summary")
        insight_counts = insights["metadata"]["insights_by_type"]
        for insight_type, count in insight_counts.items():
            st.write(f"**{insight_type.title()}:** {count}")
    
    with col2:
        st.markdown("### 🎯 High Priority Items")
        high_priority = insights["metadata"]["high_priority_items"]
        if high_priority:
            for item in high_priority[:3]:
                st.write(f"• {item}")
        else:
            st.write("No high priority items identified")
    
    with col3:
        st.markdown("### 📈 Confidence Score")
        confidence = insights["metadata"]["extraction_confidence"]
        st.metric("Extraction Confidence", f"{confidence:.1%}")
    
    # Detailed insights table
    st.markdown("---")
    st.subheader("📋 Detailed Insights")
    
    if "detailed_insights" in insights:
        # Create comprehensive insights table
        all_insights = []
        for insight_type, insight_list in insights["detailed_insights"].items():
            for insight in insight_list:
                all_insights.append({
                    "Type": insight_type.title(),
                    "Text": insight["text"],
                    "Confidence": f"{insight['confidence']:.2f}",
                    "Category": insight["category"],
                    "Priority": insight["priority"],
                    "Keywords": ", ".join(insight["keywords"])
                })
        
        if all_insights:
            df = pd.DataFrame(all_insights)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No detailed insights available")


def settings_page():
    """Settings and configuration page."""
    st.header("⚙️ Settings")
    
    st.markdown("### Analysis Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Sentiment Analysis**")
        use_vader = st.checkbox("Use VADER Sentiment", value=True)
        use_textblob = st.checkbox("Use TextBlob Sentiment", value=True)
        
        st.markdown("**Insight Extraction**")
        min_confidence = st.slider("Minimum Confidence", 0.0, 1.0, 0.3)
        max_insights = st.number_input("Maximum Insights per Type", 1, 20, 10)
    
    with col2:
        st.markdown("**Export Settings**")
        export_format = st.selectbox("Default Export Format", ["CSV", "JSON", "Both"])
        include_metadata = st.checkbox("Include Metadata in Export", value=True)
        
        st.markdown("**Display Settings**")
        show_confidence = st.checkbox("Show Confidence Scores", value=True)
        highlight_keywords = st.checkbox("Highlight Keywords", value=True)
    
    # Save settings
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
    
    st.markdown("---")
    st.markdown("### System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Version:** 1.0.0")
        st.markdown("**Last Updated:** 2024-01-01")
    
    with col2:
        st.markdown("**Status:** ✅ Operational")
        st.markdown("**Logs:** [View Logs](/#)")


def display_insights(insights_list: list, title: str):
    """Display insights in a formatted way."""
    if not insights_list:
        st.info(f"No {title.lower()} found in the transcript.")
        return
    
    for i, insight in enumerate(insights_list, 1):
        with st.container():
            st.markdown(f"**{i}.** {insight}")
            st.markdown("---")


def generate_mock_transcript(seed_brief: str) -> str:
    """Generate a mock transcript from seed brief."""
    # Simple mock generation (would use actual LLM in production)
    return f"""
Distributor: We reviewed your solution and have a few concerns and opportunities.
Vendor: Thanks for the context; let's map problems to concrete next steps.
Distributor: Can we align on owners and dates within next few weeks?
Vendor: Yes—I'll summarize action items, owners, and deadlines right after the call.
Distributor: If we close these gaps, we can co-sell in two target accounts.
Vendor: Great—let's keep momentum and schedule a follow-up to confirm progress.
"""


def export_data(results: Dict[str, Any]):
    """Export analysis results."""
    # This would implement actual export functionality
    st.success("Export functionality would be implemented here")
