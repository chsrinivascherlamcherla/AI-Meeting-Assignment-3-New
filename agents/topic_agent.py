from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from state import MeetingState

def topic_extraction_agent(state: MeetingState):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke([
        SystemMessage(content="Identify the main subject of the meeting transcript."),
        HumanMessage(content=state["transcript"])
    ])
    return {"topic": response.content}