from pydantic import BaseModel, Field
from typing import List

class Node(BaseModel):
    id: str = Field(description="Unique identifier for the entity, e.g. 'Albert Einstein', 'Paris', 'Apollo 11'")
    type: str = Field(description="Type of the entity, e.g. 'Person', 'Location', 'Mission'")

class HyperEdge(BaseModel):
    relation_name: str = Field(description="Name of the relationship, e.g. 'Crew members of', 'Co-authors'")
    connected_nodes: List[str] = Field(description="List of node IDs that participate in the relationship. Should be 3 or more.")

class HyperGraphData(BaseModel):
    nodes: List[Node]
    hyperedges: List[HyperEdge]