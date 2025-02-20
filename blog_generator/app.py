from langgraph.graph import (
    START,
    END,
    StateGraph,
    MessagesState,
)
from agents import Agents
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage


class BlogGeneratorGraph:

    def __init__(self):
        self.agents = Agents()
        self.model = self.agents.blog_generator_model

    def route_content_or_regenerate_title(self, state:MessagesState):
        feedback = state.messages.pop()

        if feedback.content.lower() == 'yes':
            return self.agents.content_generator
        elif feedback.content.lower() == 'no':
            disliked_title = state.messages.pop()
            return self.agents.title_generator
        else :
            return self.agents.user_feedback


    def create_application_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node('blog_generator', self.agents.call_model)
        graph_builder.add_node('title_generator', self.agents.title_generator)
        graph_builder.add_node('feedback', self.agents.user_feedback)
        graph_builder.add_node('content_generator', self.agents.content_generator)
        
        graph_builder.add_edge(START, 'blog_generator')
        graph_builder.add_edge('blog_generator', 'title_generator')
        graph_builder.add_edge('title_generator', 'feedback')
        graph_builder.add_conditional_edges('feedback', self.route_content_or_regenerate_title)
        graph_builder.add_edge('content_generator', END)

        graph = graph_builder.compile()

        mes = graph.invoke({"messages":[HumanMessage(content="Write a blog on Modern Mathematics")]})
        for m in mes['messages']:
            m.prettyprint()




app = BlogGeneratorGraph().create_application_graph()
