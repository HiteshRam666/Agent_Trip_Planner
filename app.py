from fastapi import FastAPI
from pydantic import BaseModel 
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse 
from langchain_core.messages import HumanMessage
from utils.save_to_document import save_document
import os 

app = FastAPI() 

class QueryRequest(BaseModel):
    query: str 

@app.post("/query")
async def query_agent_travel(query: QueryRequest):
    try:
        print(query) 
        graph = GraphBuilder(model_provider="openai")
        react_app = graph() 

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        # Convert query string to LangChain HumanMessage
        messages = {"messages": [HumanMessage(content=query.query)]}

        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content 
     
        else:
            final_output = str(output)

        saved_path = save_document(response_text = final_output)

        return {"answer": final_output, "saved_file": saved_path}
    except Exception as e:
        return JSONResponse(status_code=500, content = {"error": str(e)})