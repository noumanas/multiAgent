import pandas as pd
import duckdb
from utils.openai_client import client, MODEL

TRACKS_DATA_PATH = "data/tracks_cleaned_data.csv"
SALES_DATA_PATH = "data/sales_data.parquet"

TRACKS_SQL_PROMPT = """
Generate an SQL query for the 'tracks' table.
Prompt: {prompt}
Columns: {columns}
Hints:
- release_date: 'YYYY-MM-DD'
- is_selected: 0 or 1
- Metrics: deezer_reach_total, spotify_playlist_reach_total, spotify_streams_total, tiktok_reach_total, tiktok_views_total, youtube_likes_total, youtube_video_views_total
Rules: Return SQL only. Use GROUP BY for aggregations. Sum metrics when grouping. Use LIMIT 100 if raw data.
"""

SALES_SQL_PROMPT = """
Generate an SQL query for the 'sales' table.
Prompt: {prompt}
Columns: {columns}
Hints:
- On_Promo: 0 = No, 1 = Yes (Integer)
- Sold_Date: 'YYYY-MM-DD'
Rules: Return SQL only. Use GROUP BY for aggregations. Sum Total_Sale_Value when grouping. Use LIMIT 100 if raw data.
"""

def lookup_track_data(prompt: str)-> str:
    df = pd.read_csv(TRACKS_DATA_PATH)
    duckdb.sql("CREATE TABLE IF NOT EXISTS tracks as SELECT * FROM df")
    sql_prompt = TRACKS_SQL_PROMPT.format(prompt=prompt, columns=list(df.columns))
    res = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": sql_prompt }])
    sql = res.choices[0].message.content.strip().replace("```sql", "").replace("```", "")
    print(f"DEBUG: Track SQL: {sql}")
    result = duckdb.sql(sql).df()
    if len(result) > 100: return result.head(100).to_string(index=False) + "\n(Result truncated)"
    return result.to_string(index=False)

def analyze_track_data(data: str, prompt: str)-> str:
    analysis_prompt = f"Analyze music track data:\n{data}\n\nQuestion: {prompt}"
    res = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": analysis_prompt}])
    return res.choices[0].message.content

def lookup_sales_data(prompt: str)-> str:
    df = pd.read_parquet(SALES_DATA_PATH)
    duckdb.sql("CREATE TABLE IF NOT EXISTS sales as SELECT * FROM df")
    sql_prompt = SALES_SQL_PROMPT.format(prompt=prompt, columns=list(df.columns))
    res = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": sql_prompt }])
    sql = res.choices[0].message.content.strip().replace("```sql", "").replace("```", "")
    print(f"DEBUG: Sales SQL: {sql}")
    result = duckdb.sql(sql).df()
    if len(result) > 100: return result.head(100).to_string(index=False) + "\n(Result truncated)"
    return result.to_string(index=False)

def analyze_sales_data(data: str, prompt: str)-> str:
    analysis_prompt = f"Analyze store sales data:\n{data}\n\nQuestion: {prompt}"
    res = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": analysis_prompt}])
    return res.choices[0].message.content

def generate_visualization(data: str,  visualization_goal: str) -> str:
    viz_prompt = f"""
Write python matplotlib code.
Data:
{data}

Goal:
{visualization_goal}

Return code only.
""" 
    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": viz_prompt}]
    )

    return res.choices[0].message.content
