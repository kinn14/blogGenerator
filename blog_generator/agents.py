# Create agents

from llm_model import Llm
from config import llm_model_type, llm_model_name
from langchain_core.messages import (
    SystemMessage, 
    HumanMessage, 
    AIMessage,
    AnyMessage,
    )
from langchain_core.tools import tool
from langgraph.graph import add_messages
from typing_extensions import TypedDict
from typing import Annotated, Optional



class BlogMessageState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    topic: Optional[str] = None  # Stores the topic
    title: Optional[str] = None  # Stores the topic
    content: Optional[str] = None  # Stores the topic
    u_feedback: Optional[str] = None  # Stores the topic
    

class Agents():

    def __init__(self) -> None:
        # initialize llm
        self.blog_generator_model = Llm(llm_model_type, llm_model_name).get_llm_model()

    def title_generator(self, state : BlogMessageState) -> BlogMessageState:
        """
            Generate a maximum 100 character title for a blog of a given topic.
            Args: 
                topic_name : string
            Return:
                title_name : string
        """
        if state.get('topic') is None:
            state['topic'] = state["messages"][-1].content
        system_message = SystemMessage(content=f"Create a 100 character title for a blog on topic {state['topic']}")
        state['title'] = self.blog_generator_model.invoke([system_message]).content
        title_msg = AIMessage(content=f"The title for the topic {state['topic']} is : {state['title']}. Are you happy with it?")
        state['messages'].append(title_msg)
        return state

    # Define user feedback node
    def user_feedback(self, state:BlogMessageState) :
        """
            Function picks the last generated title for given topic and asks if the user is content or not.
            Args :
                title_name : string

            Return :
                Updated state based on user response
        """
        # state['u_feedback'] = input(f"\nAre you happy with the title {state['title']}? (yes/no): ").strip().lower()
        if state['u_feedback'] is None:
            state['u_feedback'] = 'yes'
        feedback_msg = HumanMessage(content=f"User feedback : {state['u_feedback']}")
        state['messages'].append(feedback_msg)
        return state
    
    def content_generator(self, state : BlogMessageState) :
        """
            Creates 500 lines of content for a blog of a given topic.
            Args: 
                topic_name : string
            Return:
                topic_content : string
        """
        system_message = SystemMessage(content=f"Generate 500 words content on {state['title']}")
        content_msg = self.blog_generator_model.invoke([system_message])
        state['content'] = content_msg.content
        state['messages'].append(content_msg)
        return state
    