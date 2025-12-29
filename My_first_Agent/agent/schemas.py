from pydantic import BaseModel

class SQLQuery(BaseModel):
    prompt: str

class AnalysisInput(BaseModel):
    data: str
    prompt: str

class VisualizationInput(BaseModel):
    data: str
    visualization_goal: str
    