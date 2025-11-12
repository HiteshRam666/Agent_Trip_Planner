from langgraph.graph.message import MessagesState
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition 
from utils.model_loader import ModelLoader 
from tools.arithmetic_tool import currency_convertor, add, multiply
from tools.currency_conversion_tool import CurrencyConvertorTool
from tools.place_search_tool import PlaceSearchTool

class GraphBuilder():
    def __init__(self, model_provider: str = "openai"): 
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        self.tools = []
        self.system_prompt = SYSTEM_PROMPT

        self.graph = None

        self.place_search_tools = PlaceSearchTool().place_search_tool_list 
        self.currency_convertor_tools = CurrencyConvertorTool().currency_converter_tool_list

        self.tools.extend(self.place_search_tools)
        self.tools.extend(self.currency_convertor_tools)

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)

    def agent_function(self, state: MessagesState):
        """
        Agent Function
        """
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question 
        response = self.llm_with_tools.invoke(input_question) 
        return {"messages": [response]}       

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)

        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent") 
        graph_builder.add_edge("agent", END)

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()