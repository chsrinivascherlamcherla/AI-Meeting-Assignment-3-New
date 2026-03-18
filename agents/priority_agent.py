from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from state import MeetingState

def priority_classification_agent(state: MeetingState):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    items = "\n".join(state["action_items"])
    response = llm.invoke([
        SystemMessage(content="Categorize the following tasks into High, Medium, and Low priority."),
        HumanMessage(content=items)
    ])
    return {"prioritized_actions": response.content}