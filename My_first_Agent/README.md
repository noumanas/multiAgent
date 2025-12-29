# Multi-Agent Data Analysis System

This project is a FastAPI-based AI Agent capable of querying and analyzing data from local files (CSV and Parquet) using natural language. It leverages OpenAI's GPT models to translate user prompts into SQL queries executed via DuckDB.

## Features

- **Multi-Agent Capabilities**: Supports specialized 'agents' for different data domains:
  - **Tracks Agent**: Queries and analyzes music track metrics (e.g., Spotify streams, TikTok views) from `tracks_cleaned_data.csv`.
  - **Sales Agent**: Queries and analyzes sales data (e.g., revenue, dates) from `sales_data.parquet`.
- **Natural Language Parsing**: Converts English questions into SQL queries automatically.
- **Streaming Responses**: Returns agent thought processes and results in real-time via Server-Sent Events (SSE).
- **Visualization**: Can generate Python code for data visualizations (using Matplotlib).

## Project Structure

- `main.py`: Entry point for the FastAPI application.
- `agent/`: Contains the agent logic, router, tools, and prompts.
- `utils/`: Utility scripts (e.g., OpenAI client configuration).
- `data/`: Directory for storing datasets (`tracks_cleaned_data.csv`, `sales_data.parquet`).

## Prerequisites

- Python 3.8+
- An OpenAI API Key

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd My_first_Agent
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment:**
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. **Start the Server:**
   ```bash
   uvicorn main:app --reload
   ```
   The server will start at `http://127.0.0.1:8000`.

2. **Interacting with the Agent:**
   You can send POST requests to the `/agent` endpoint.

   **Example Request (Tracks):**
   ```bash
   curl -X POST "http://127.0.0.1:8000/agent?prompt=Which%20track%20has%20the%20most%20spotify%20streams%3F&agentType=tracks"
   ```

   **Example Request (Sales):**
   ```bash
   curl -X POST "http://127.0.0.1:8000/agent?prompt=Total%20sales%20volume%20by%20date&agentType=sales"
   ```

## API Endpoints

### `POST /agent`
- **Query Parameters:**
  - `prompt` (str): The question or task for the agent.
  - `agentType` (str, optional): The type of agent to use. Options: `tracks` (default), `sales`.
- **Response**: A streaming event stream of the agent's actions and final answer.
