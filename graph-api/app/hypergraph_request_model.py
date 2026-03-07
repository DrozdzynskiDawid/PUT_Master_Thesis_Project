from pydantic import BaseModel
from typing import List

class Node(BaseModel):
    id: str
    type: str

class Hyperedge(BaseModel):
    relation_name: str
    connected_nodes: List[str]

class HypergraphRequest(BaseModel):
    nodes: List[Node]
    hyperedges: List[Hyperedge]