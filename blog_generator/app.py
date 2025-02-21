from langgraph.graph import (
    START,
    END,
    StateGraph,
)
from agents import Agents, BlogMessageState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage


class BlogGeneratorGraph:

    def __init__(self):
        self.agents = Agents()
        self.model = self.agents.blog_generator_model

    def route_content_or_regenerate_title(self, state:BlogMessageState):
        if  'yes' in state['u_feedback'].lower():
            return 'content_generator'
        elif 'no' in  state['u_feedback'].lower():
            return 'title_generator'
        else :
            return 'user_feedback'

    def create_application_graph(self):
        graph_builder = StateGraph(BlogMessageState)
        graph_builder.add_node('title_generator', self.agents.title_generator)
        graph_builder.add_node('feedback', self.agents.user_feedback)
        graph_builder.add_node('content_generator', self.agents.content_generator)
        
        graph_builder.add_edge('title_generator', 'feedback')
        graph_builder.add_conditional_edges('feedback', self.route_content_or_regenerate_title)
        graph_builder.add_edge('content_generator', END)

        graph_builder.set_entry_point('title_generator')

        graph = graph_builder.compile()

        return graph


topic_name = 'Modern Mathematics'
graph = BlogGeneratorGraph().create_application_graph()
messages = graph.invoke({"messages":[HumanMessage(content=topic_name)]})

for m in messages['messages']:
    m.pretty_print()
