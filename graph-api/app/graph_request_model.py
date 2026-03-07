from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Node(BaseModel):
    id: Optional[str]
    type: str
    properties: Dict[str, Any] = {}
    metadata: Optional[Dict[str, Any]] = None
    page_content: Optional[str] = None

class Relationship(BaseModel):
    source: Node
    target: Node
    type: str
    properties: Dict[str, Any] = {}

class GraphRequest(BaseModel):
    nodes: List[Node]
    relationships: List[Relationship]
    source: Optional[Node] = None