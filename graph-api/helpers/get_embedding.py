import numpy as np
import torch
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from sklearn.metrics.pairwise import cosine_similarity

def extract_triples(json_data):
    return [[l['source'], l['relation'], l['target']] for l in json_data['links']]

def to_real_vector(vec):
    if np.iscomplexobj(vec):
        return np.concatenate([vec.real, vec.imag])
    return vec

def get_graph_embedding(model, tf, current_triples):
    nodes = set()
    for t in current_triples:
        nodes.add(t[0])
        nodes.add(t[2])
    
    node_ids = torch.tensor([tf.entity_to_id[name] for name in nodes])
    embeddings = model.entity_representations[0](indices=node_ids)
    mean_embedding = torch.mean(embeddings, dim=0).detach().cpu().numpy()
    return mean_embedding

def get_graph_similarity(json_data1, json_data2):
    triples1 = extract_triples(json_data1)
    triples2 = extract_triples(json_data2)

    all_triples = np.array(triples1 + triples2)
    tf_combined = TriplesFactory.from_labeled_triples(all_triples)

    result = pipeline(
        training=tf_combined,
        testing=tf_combined,
        model='RotatE',
        training_loop='sLCWA',
        training_kwargs=dict(batch_size=256),
        epochs=100,
        device='cuda',
        random_seed=42
    )
    model = result.model

    vec1 = get_graph_embedding(model, tf_combined, triples1)
    vec2 = get_graph_embedding(model, tf_combined, triples2)

    v1_real = to_real_vector(vec1)
    v2_real = to_real_vector(vec2)

    sim = cosine_similarity(v1_real.reshape(1, -1), v2_real.reshape(1, -1))[0][0]

    final_score = ((sim + 1) / 2) * 100

    print(f"Podobieństwo grafów: {final_score:.2f}%")
    return {
        "cosine_similarity": float(sim),
        "percentage_similarity": float(final_score)
    }