from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from state import MeetingState

def summary_agent(state: MeetingState):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    response = llm.invoke([
        SystemMessage(content="Provide a concise summary of the meeting highlights."),
        HumanMessage(content=state["transcript"])
    ])
    return {"summary": response.content}