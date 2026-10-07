from langgraph.graph import StateGraph, START, END 
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from state import BlogState
from agents import get_llm, researcher_agent, writer_agent, editor_agent

MAX_REVISION = 3

def research_node(state : BlogState) -> BlogState : 
    """
        Researcher Agent generates (or revises) the research outline
    """
    llm = get_llm()

    research_data = researcher_agent(
        llm = llm, 
        topic = state.topic, 
        audience = state.audience, 
        feedback=state.research_feedback
    )

    state.research = research_data
    state.research_feedback = ""

    return state

def human_review_research_node(state : BlogState) -> BlogState : 
    """
        Pause and ask the human to approve the research or send the feedback
    """
    decision = interrupt({
        "stage" : "researcher_review", 
        "research" : state.research, 
        "instructions" : (
            "Reply with 'approve' to continue to writing"
            "or describe what to change to send it back to the researcher. "
        )
    })

    if isinstance(decision, dict) : 
        action = decision.get("action", "approve")
        feedback = decision.get("feedback", "")
    else : 
        text = str(decision)
        action = "approve" if text.lower() in ["approve", "approved", "ok", "yes", "process", ""] else "revise"
        feedback = "" if action == "approve" else text 

    state.research_feedback = feedback
    return state

def writer_node(State : BlogState) : 
    pass

def editor_node(State : BlogState) : 
    pass