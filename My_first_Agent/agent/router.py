import json
from utils.openai_client import client, MODEL
from agent.prompts import TRACK_TOOLS, SALES_TOOLS, SYSTEM_PROMPTS
from agent import tools

TOOL_MAP = {
    "lookup_track_data":tools.lookup_track_data,
    "analyze_track_data":tools.analyze_track_data,
    "lookup_sales_data":tools.lookup_sales_data,
    "analyze_sales_data":tools.analyze_sales_data,
    "generate_visualization":tools.generate_visualization
}

def run_agent(user_prompt: str, agentType: str = "tracks"):
    system_prompt = SYSTEM_PROMPTS.get(agentType, SYSTEM_PROMPTS["tracks"])
    tools_list = TRACK_TOOLS if agentType == "tracks" else SALES_TOOLS

    messages=[
        {"role":  "system" , "content": system_prompt},
        {"role": "user", "content":user_prompt}
    ]

    for _ in range(5): # guardrail
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools_list,
            stream=True
        )

        # Accumulators
        collected_content = []
        tool_calls_accumulator = {} # index -> tool_call_data

        for chunk in stream:
            delta = chunk.choices[0].delta
            
            # Handle Content
            if delta.content:
                yield delta.content
                collected_content.append(delta.content)

            # Handle Tool Calls
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index
                    if idx not in tool_calls_accumulator:
                        tool_calls_accumulator[idx] = {
                            "id": tc.id,
                            "function": {
                                "name": tc.function.name,
                                "arguments": ""
                            },
                            "type": tc.type
                        }
                    
                    if tc.function.name:
                        tool_calls_accumulator[idx]["function"]["name"] = tc.function.name
                    if tc.function.arguments:
                        tool_calls_accumulator[idx]["function"]["arguments"] += tc.function.arguments

        # Process Results after stream is done
        
        # 1. If we got content, append assistant message
        if collected_content:
            full_content = "".join(collected_content)
            messages.append({"role": "assistant", "content": full_content})

        # 2. If NO tool calls, we are done
        if not tool_calls_accumulator:
            return

        # 3. If we HAVE tool calls, rebuild the message object and execute
        # Reconstruct the tool_calls list from the accumulator
        tool_calls_list = []
        for idx in sorted(tool_calls_accumulator.keys()):
            tc_data = tool_calls_accumulator[idx]
            tool_calls_list.append({
                "id": tc_data["id"],
                "type": tc_data["type"],
                "function": {
                    "name": tc_data["function"]["name"],
                    "arguments": tc_data["function"]["arguments"]
                }
            })
        
        # Append the assistant's tool call message
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": tool_calls_list
        })

        # Execute tools
        for tc in tool_calls_list:
            fn = TOOL_MAP[tc["function"]["name"]]
            try:
                args = json.loads(tc["function"]["arguments"])
                print(f"DEBUG: Calling tool {tc['function']['name']} with args {args}")
                result = fn(**args)
            except Exception as e:
                result = f"Error executing tool: {e}"
            
            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": str(result)
            })
    
    yield "\n\n(Agent stopped - max steps reached)"