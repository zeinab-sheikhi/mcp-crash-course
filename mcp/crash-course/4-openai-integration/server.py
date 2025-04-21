import os 
import json
from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    name="Knowledge Base",
    host="0.0.0.0", 
    port=8050,
)


@mcp.tool()
def get_knowledge_base() -> str:
    """Retrieve the entire knowledge base as a formatted string.
    Returns:
        A formatted string containing all Q&A pairs from the knowledge base.
    """
    try:
        kb_path = os.path.join(os.path.dirname(__file__), "data", "kb.json")
        with open(kb_path, "r") as f:
            kb_data = json.load(f)
        
        # Fromat the knowledge base as the string
        kb_text = "Here is the retrieved knowledge base:\n\n"
        
        if isinstance(kb_data, list):
            for i, item in enumerate(kb_data, 1):
                if isinstance(item, dict):
                    question = item.get("question", "Uknown Question")
                    answer = item.get("answer", "Unknown Answer")
                else:
                    question = f"Item {i}"
                    answer = str(item)
                
                kb_text += f"Q{i}: {question}\n"
                kb_text += f"A{i}: {answer}\n"
        else:
            kb_text += f"Knowledge base content: {json.dumps(kb_data, indent=2)}\n\n"
        
        return kb_text
    except FileNotFoundError:
        print("Knowledge base file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON in knowledge base file.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    mcp.run(transport="stdio")

