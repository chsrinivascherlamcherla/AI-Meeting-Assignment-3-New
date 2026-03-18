from typing import TypedDict, List

class MeetingState(TypedDict):
    transcript: str
    topic: str
    summary: str
    action_items: List[str]
    prioritized_actions: str