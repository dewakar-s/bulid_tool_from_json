from build_tools import build_tool_from_json
    
# JSON directly as a dictionary for demonstration
tool_json = {
  "tool_name": "product_fetch_tool_dummyjson",
  "description": "Fetch a single product by ID from DummyJSON API.",
  "args_schema": {
    "product_id": "int"
  },
  "api_url": "https://dummyjson.com/products/{product_id}"
}


tool = build_tool_from_json(tool_json)

# User input only
result = tool.run({"product_id": 3})
print(result)

