AI Meeting Notes Assistant
A stateful, multi-agent application built with LangGraph to automate the transformation of meeting transcripts and audio into structured, actionable insights.

Overview
This application uses a sophisticated orchestration of four specialized AI agents to process meeting data. It handles everything from raw audio transcription (via Hugging Face) to intelligent task prioritization, providing a seamless "Meeting-to-Action" workflow.

🛠️ Tech Stack
Orchestration: LangGraph (v1.111.0)

Language Models: OpenAI GPT-4o-mini

Frontend: Streamlit (Light Theme)

Audio Processing: Hugging Face Inference API (Whisper)

Environment: Python 3.12.10

IDE: VS Code

🤖 Multi-Agent Architecture
The application follows a directed acyclic graph (DAG) workflow where each agent has a single, focused responsibility:

Topic Extraction Agent: Identifies the core subject and context of the meeting.

Summary Agent: Synthesizes the conversation into a concise executive summary.

Action Item Agent: Parses the transcript to identify specific tasks assigned to team members.

Priority Agent: Evaluates extracted tasks and categorizes them by urgency (High, Medium, Low).

Audio Feature: An integrated Hugging Face module that converts spoken audio into text before the graph begins execution.

📂 Project Structure
Plaintext
ai_meeting_notes/
├── agents/
│   ├── topic_agent.py      # Identifies meeting themes
│   ├── summary_agent.py    # Generates executive summaries
│   ├── action_agent.py     # Extracts member-specific tasks
│   ├── priority_agent.py   # Classifies task urgency
│   └── audio_feature.py    # HF Whisper Integration
├── state.py                # TypedDict shared state definition
├── app.py                  # Main Streamlit & LangGraph logic
├── .env                    # API Keys (OpenAI & Hugging Face)
└── requirements.txt        # Project dependencies

🚀 Getting Started
1. Prerequisites
Ensure you are using Python 3.12.10 and VS Code 1.111.0.

2. Installation
Bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install langgraph langchain-openai streamlit huggingface_hub python-dotenv
3. Environment Setup
Create a .env file in the root directory:

Code snippet
OPENAI_API_KEY=your_openai_key_here
HF_TOKEN=your_huggingface_token_here

4. Running the Application
Bash
streamlit run app.py


Why LangGraph?
By using LangGraph instead of a linear chain, this application maintains a global state. This allows the Priority Agent to "know" what the Action Agent found without re-processing the entire transcript, ensuring higher accuracy and lower token consumption.

Multi-agent workflow diagram for AI Meeting Notes

This video explains how multi-agent systems coordinate complex tasks, which is the foundational logic used in your AI Meeting Notes application.
