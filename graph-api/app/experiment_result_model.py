from typing import List
from pydantic import BaseModel

class ExperimentDetail(BaseModel):
    id: int
    text: str
    stats_direct: dict
    stats_transformed: dict
    stats_clique_transformed: dict
    similarity: float
    graph_edit_distance: float