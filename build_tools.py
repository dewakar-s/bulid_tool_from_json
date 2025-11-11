import requests
from pydantic import BaseModel, Field, create_model
from langchain_core.tools import StructuredTool

def build_tool_from_json(tool_data: dict) -> StructuredTool:
    """
    Dynamically build a StructuredTool from JSON metadata.
    """

    # 1️⃣ Build input schema
    DynamicSchema = create_model(
        f"{tool_data['tool_name']}Input",
        **{k: (eval(v), Field(...)) for k, v in tool_data["args_schema"].items()},
        __base__=BaseModel
    )

    # 2️⃣ Build dynamic function
    def dynamic_func(**kwargs):
        url = tool_data["api_url"].format(**kwargs)
        try:
            response = requests.get(url)
            response.raise_for_status()
            return {
                "status": "success",
                "message": f"Fetched {kwargs}",
                "products": [response.json()]
            }
        except requests.HTTPError:
            return {"status": "failed", "message": f"Product {kwargs} not found", "products": []}
        except Exception as e:
            return {"status": "failed", "message": str(e), "products": []}

    # 3️⃣ Build the StructuredTool
    tool = StructuredTool.from_function(
        func=dynamic_func,
        args_schema=DynamicSchema,
        description=tool_data["description"]
    )

    return tool
