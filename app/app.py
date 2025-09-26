import streamlit as st
import json
import pandas as pd
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from sentiment import analyze_sentiment
from extractor import extract_insights, generate_mock_transcript

def save_transcript(transcript):
    """Save transcript to JSON file"""
    with open('data/transcript.json', 'w') as f:
        json.dump({"text": transcript}, f)

def load_transcript():
    """Load transcript from JSON file"""
    try:
        with open('data/transcript.json', 'r') as f:
            return json.load(f).get('text', '')
    except FileNotFoundError:
        return ""

def main():
    st.set_page_config(page_title="MeetMogger AI", layout="wide")
    
    st.title("📞 MeetMogger AI - Call Intelligence")
    st.write("Paste your call transcript below to analyze sentiment and extract insights.")
    with st.expander("Generate mock transcript from a seed brief"):
        seed = st.text_area("Seed Brief:", key="seed_brief", height=120, placeholder="Distributor profile + challenges...")
        if st.button("Generate Transcript"):
            mock = generate_mock_transcript(seed)
            # Put into session and textarea default
            st.session_state["generated_transcript"] = mock
    
    # Transcript input
    transcript = st.text_area(
        "Call Transcript:",
        height=300,
        placeholder="Paste the call transcript here...",
        value=st.session_state.get("generated_transcript", load_transcript())
    )
    
    if st.button("Analyze Transcript"):
        if not transcript.strip():
            st.warning("Please enter a transcript to analyze.")
            return
            
        save_transcript(transcript)
        
        with st.spinner("Analyzing..."):
            # Sentiment Analysis
            sentiment = analyze_sentiment(transcript)
            
            # Extract Insights
            insights = extract_insights(transcript)
            
            # Display Results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Sentiment Analysis")
                st.metric("Overall Sentiment", sentiment["overall"])
                st.write(f"**Score:** {sentiment['score']:.2f}")
                
                # Key sentences with highlighted words
                if sentiment.get("sentences"):
                    st.markdown("**Key Sentences**")
                    # Show important sentences first
                    important = [s for s in sentiment["sentences"] if s.get("is_important")] or sentiment["sentences"]
                    for i, s in enumerate(important[:5], 1):
                        highlighted = s.get("highlighted_text") or s.get("text", "")
                        st.markdown(f"{i}. {highlighted}")
                        st.caption(f"{s.get('sentiment', 'Neutral')} (polarity {s.get('polarity', 0.0):.2f})")
                
                st.subheader("🔍 Identified Problems")
                for i, problem in enumerate(insights["problems"], 1):
                    st.write(f"{i}. {problem}")
                    
            with col2:
                st.subheader("💡 Suggested Solutions")
                for i, solution in enumerate(insights["solutions"], 1):
                    st.write(f"{i}. {solution}")
                    
                st.subheader("✅ Action Items")
                for i, action in enumerate(insights["action_items"], 1):
                    st.write(f"{i}. {action}")
                
                # Export to CSV
                if insights["action_items"]:
                    df = pd.DataFrame({"Action Items": insights["action_items"]})
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Export Action Items",
                        csv,
                        "meetmogger_action_items.csv",
                        "text/csv",
                        key='download-csv'
                    )

if __name__ == "__main__":
    main()