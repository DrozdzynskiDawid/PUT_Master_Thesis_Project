from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GraphNode(BaseModel):
    id: Any
    label: Optional[str] = None 
    type: Optional[str] = None
    extra: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"

class GraphLink(BaseModel):
    source: Any
    target: Any
    label: Optional[str] = None
    class Config:
        extra = "allow"

class NodeLinkGraphModel(BaseModel):
    directed: bool = True
    multigraph: bool = False
    graph: Dict[str, Any] = {}
    nodes: List[GraphNode]
    links: List[GraphLink]