const API_URL = 'http://localhost:8000/api';

export const API_ENDPOINTS = {
  API_URL,
  RANDOM_TEXT: `${API_URL}/random-text`,
  GRAPH: `${API_URL}/graph`,
  GRAPH_PNG: `${API_URL}/graph/visualization`,
  HYPERGRAPH: `${API_URL}/hypergraph`,
  HYPERGRAPH_PNG: `${API_URL}/hypergraph/visualization`,
  TRANSFORM_CLIQUE: `${API_URL}/hypergraph/transformation/clique`,
  TRANSFORM_LLM: `${API_URL}/hypergraph/transformation/selected_clique`,
} as const;