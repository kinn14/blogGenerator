# Create agents

from llm_model import Llm
from config import llm_model_type, llm_model_name
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import MessagesState



class Agents():

    def __init__(self) -> None:
        # initialize llm
        self.blog_generator_model = Llm(llm_model_type, llm_model_name).get_llm_model()

        # invoke llm to check the working
        system_message = SystemMessage(
            content="You are a helpful blog generator assistant. Your are tasked to generate title and "
            "content of the given topic."
            )
        
        ai_message = AIMessage(
            content="Hello ! How can I assist you with blog generation today ? Do you have a topic in mind?"
        )
        
        # messages = self.blog_generator_model.invoke(
        #     [system_message] + [ai_message]
        #     )
        # print(messages)


    def title_generator(self, state : MessagesState) -> MessagesState:
        """
            Generate a maximum 100 character title for a blog of a given topic.
            Args: 
                topic_name : string
            Return:
                title_name : string
        """
        topic = state["messages"][-1].content
        system_message = SystemMessage(content=topic)
        title = self.blog_generator_model.invoke([system_message])
        new_state = MessagesState(state["messages"] + [title])
        return new_state

    # Define user feedback node
    def user_feedback(self, state:MessagesState) :
        """
            Function picks the last generated title for given topic and asks if the user is content or not.
            Args :
                title_name : string

            Return :
                Updated state based on user response
        """
        feedback = input(f"\nAre you happy with the title {state.messages[-1].content}? (yes/no): ").strip().lower()
        feedback_msg = HumanMessage(content=f"User feedback : {feedback}")
        new_state = MessagesState(state["messages"] + [feedback_msg])
        return new_state
    
    def content_generator(self, state : MessagesState) -> str:
        """
            Creates 500 lines of content for a blog of a given topic.
            Args: 
                topic_name : string
            Return:
                topic_content : string
        """
        system_message = SystemMessage(content=state[-2].content)
        return  self.blog_generator_model.invoke([system_message]).content
    

    # IF TITLE AND CONTENT GENERATORS WERE TO BE USED AS TOOLS
    # def bind_and_generate_model(self) :
    #     tools = [self.title_generator, self.content_generator]
    #     self.blog_generator_model = self.model.bind_tools(tools=tools)
    #     return self.blog_generator_model
    
    def call_model(self, state:MessagesState):
            # # Overriding all previous messages from state while defining new topic
            # # Thus my topic name will always be as state['messages'][0]
            # initial_state = MessagesState(messages=state["messages"][-1])
            return {"messages":self.blog_generator_model.invoke( state["messages"])}
