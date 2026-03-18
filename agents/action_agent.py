from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from state import MeetingState

def action_item_agent(state: MeetingState):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke([
        SystemMessage(content="Extract tasks assigned to team members. Format as: Name - Task."),
        HumanMessage(content=state["transcript"])
    ])
    return {"action_items": [response.content]}