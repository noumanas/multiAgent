TRACK_TOOLS = [
    {
        "type":"function",
        "function":{
            "name":"lookup_track_data",
            "description":"fetch music track data using SQL",
            "parameters":{
                "type":"object",
                "properties":{"prompt":{"type":"string"}},
                "required":["prompt"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"analyze_track_data",
            "description":"Analyze music track data",
            "parameters":{
                "type":"object",
                "properties":{
                    "data":{"type":"string"},
                    "prompt":{"type":"string"}
                },
                "required":["data","prompt"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"generate_visualization",
            "description":"Generate visualization code",
            "parameters":{
                "type":"object",
                "properties":{
                    "data":{"type":"string"},
                    "visualization_goal":{"type":"string"}
                },
                "required":["data","visualization_goal"]
            }
        }
    }
]

SALES_TOOLS = [
    {
        "type":"function",
        "function":{
            "name":"lookup_sales_data",
            "description":"fetch store sales data using SQL",
            "parameters":{
                "type":"object",
                "properties":{"prompt":{"type":"string"}},
                "required":["prompt"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"analyze_sales_data",
            "description":"Analyze store sales data",
            "parameters":{
                "type":"object",
                "properties":{
                    "data":{"type":"string"},
                    "prompt":{"type":"string"}
                },
                "required":["data","prompt"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"generate_visualization",
            "description":"Generate visualization code",
            "parameters":{
                "type":"object",
                "properties":{
                    "data":{"type":"string"},
                    "visualization_goal":{"type":"string"}
                },
                "required":["data","visualization_goal"]
            }
        }
    }
]

SYSTEM_PROMPTS = {
    "tracks": "You are a Music Track Analyst. Help users understand Spotify streams, TikTok reach, and YouTube views.",
    "sales": "You are a Store Sales Analyst. Help users understand store revenue, quantity sold, and promotions."
}