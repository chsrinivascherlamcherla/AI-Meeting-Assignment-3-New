import streamlit as st
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

# Modular Imports
from state import MeetingState
from agents.topic_agent import topic_extraction_agent
from agents.summary_agent import summary_agent
from agents.action_agent import action_item_agent
from agents.priority_agent import priority_classification_agent
from agents.audio_feature import transcribe_audio

# Load API Keys from .env
load_dotenv()

# --- 1. LangGraph Orchestration Setup ---
def build_graph():
    workflow = StateGraph(MeetingState)

    # Add specialized agent nodes
    workflow.add_node("extract_topic", topic_extraction_agent)
    workflow.add_node("generate_summary", summary_agent)
    workflow.add_node("extract_actions", action_item_agent)
    workflow.add_node("prioritize_actions", priority_classification_agent)

    # Define the execution flow
    workflow.set_entry_point("extract_topic")
    workflow.add_edge("extract_topic", "generate_summary")
    workflow.add_edge("generate_summary", "extract_actions")
    workflow.add_edge("extract_actions", "prioritize_actions")
    workflow.add_edge("prioritize_actions", END)

    return workflow.compile()

app_graph = build_graph()

# --- 2. Streamlit UI Logic ---

# Page Config
st.set_page_config(page_title="AI Meeting Notes Expert", page_icon="🎙️", layout="wide")

# Light Background Styling (Custom CSS)
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
    }
    /* Headers */
    h1, h2, h3 {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    /* Cards/Containers for results */
    .result-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# App Title
st.title("🎙️ AI Meeting Notes Assistant")
st.markdown("Generate structured insights from your team syncs using **LangGraph** multi-agent workflows.")

# Sidebar for Inputs
with st.sidebar:
    st.header("Input Source")
    input_mode = st.radio("Choose format:", ["Text File (.txt)", "Audio File (HF Whisper)"])
    
    transcript_text = ""
    
    if input_mode == "Text File (.txt)":
        uploaded_file = st.file_uploader("Upload meeting transcript", type=['txt'])
        if uploaded_file:
            transcript_text = uploaded_file.read().decode("utf-8")
    
    else:
        audio_file = st.file_uploader("Upload meeting audio", type=['mp3', 'wav', 'm4a'])
        if audio_file:
            with st.spinner("Transcribing via Hugging Face..."):
                try:
                    transcript_text = transcribe_audio(audio_file)
                    st.success("Transcription complete!")
                except Exception as e:
                    st.error(f"Transcription failed: {e}")

# Main Logic Execution
if st.button("Generate Meeting Notes") and transcript_text:
    with st.spinner("Agents are collaborating on your notes..."):
        # Initialize the shared state
        initial_state = {
            "transcript": transcript_text,
            "topic": "",
            "summary": "",
            "action_items": [],
            "prioritized_actions": ""
        }
        
        # Invoke the LangGraph
        final_state = app_graph.invoke(initial_state)
        
        # Display Results in Columns
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📌 Topic")
            st.info(final_state["topic"])
            
            st.markdown("### 📝 Executive Summary")
            st.write(final_state["summary"])
            
        with col2:
            st.markdown("### ✅ Task Assignments")
            # Usually action_items is a list, we join for display
            tasks = "\n".join(final_state["action_items"])
            st.success(tasks)
            
            st.markdown("### ⚡ Priority Matrix")
            st.warning(final_state["prioritized_actions"])

        # Download Button
        full_report = f"""TOPIC: {final_state['topic']}\n\nSUMMARY:\n{final_state['summary']}\n\nTASKS:\n{tasks}\n\nPRIORITIES:\n{final_state['prioritized_actions']}"""
        st.download_button("Download Full Report", full_report, file_name="meeting_notes.txt")

elif not transcript_text:
    st.info("Waiting for a transcript or audio file to be uploaded.")