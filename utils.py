import json
import os
from item import Item
from factors import *
import numpy as np
import math
from vllm import LLM
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("/path/to/Qwen2.5-14B-Instruct", trust_remote_code=True)
llm = LLM("/path/to/Qwen2.5-14B-Instruct", tensor_parallel_size=4, trust_remote_code=True, max_model_len=8192)

def softmax_sampling(x, temperature=10.0):
    x = np.array(x)
    e_x = np.exp(x / temperature)
    probs = e_x / e_x.sum(axis=0)
    return probs, np.random.choice(len(probs), p=probs)


def random_sampling(x):
    return np.random.choice(x)


def load_one(path, aspect, criteria, cot, scale, autocot, metrics, Example, reference, order, dataset, model):
    with open(path, "r", encoding='utf-8') as f:
        metrics_ = json.load(f)
    item = Item(model, dataset, criteria, cot, scale, autocot, metrics, Example, reference, order, tokenizer=tokenizer, llm=llm)
    item.correlation = metrics_[aspect]['correlation']
    return item


def load_results(path, aspect, dataset, model):
    items = []
    criteria = []
    cots = []
    scales = []
    autocots = []
    metrics = []
    examples = []
    references = []
    orders = []
    
    if dataset == "topical_chat":
        scale = "3"
    elif dataset == "summeval" or dataset == "sfhot" or dataset == "sfres" or dataset == "hanna":
        scale = "5"
    
    # Scoring Scale
    if scale == "5":
        item = load_one(os.path.join(path, "scale_3.json"), aspect, "Human", "Prefix", "3", "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
        items.append(item)
        scales.append(item)
        
    # Baseline (MT-Bench)
    item = load_one(os.path.join(path, "baseline.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
    items.append(item)
    
    criteria.append(item)
    cots.append(item)
    scales.append(item)
    autocots.append(item)
    metrics.append(item)
    examples.append(item)
    references.append(item)
    orders.append(item)
    
    # Scoring Scale
    if scale == "3":
        item = load_one(os.path.join(path, "scale_5.json"), aspect, "Human", "Prefix", "5", "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
        items.append(item)
        scales.append(item)
    
    item = load_one(os.path.join(path, "scale_10.json"), aspect, "Human", "Prefix", "10", "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
    items.append(item)
    scales.append(item)
    
    item = load_one(os.path.join(path, "scale_50.json"), aspect, "Human", "Prefix", "50", "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
    items.append(item)
    scales.append(item)
    
    item = load_one(os.path.join(path, "scale_100.json"), aspect, "Human", "Prefix", "100", "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
    items.append(item)
    scales.append(item)
    
    # In-Context Example
    item = load_one(os.path.join(path, "example_3.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "Example3", "NoReference", "TEI", dataset, model)
    items.append(item)
    examples.append(item)
    
    item = load_one(os.path.join(path, "example_5.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "Example5", "NoReference", "TEI", dataset, model)
    items.append(item)
    examples.append(item)
    
    item = load_one(os.path.join(path, "example_10.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "Example10", "NoReference", "TEI", dataset, model)
    items.append(item)
    examples.append(item)
    
    # Criteria
    item = load_one(os.path.join(path, "wo_criteria.json"), aspect, "NoCriteria", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
    items.append(item)
    criteria.append(item)
    
    item = load_one(os.path.join(path, "self_generated_criteria.json"), aspect, "LLM", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
    items.append(item)
    criteria.append(item)
    
    # Reference
    item = load_one(os.path.join(path, "self_generated_reference.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "Reference", "TEI", dataset, model)
    items.append(item)
    references.append(item)
    
    item = load_one(os.path.join(path, "dialectic.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "Dialectic", "TEI", dataset, model)
    items.append(item)
    references.append(item)
    
    # Chain-of-Thought
    item = load_one(os.path.join(path, "cot_suffix.json"), aspect, "Human", "Suffix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
    items.append(item)
    cots.append(item)
    
    item = load_one(os.path.join(path, "cot_free.json"), aspect, "Human", "Free", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
    items.append(item)
    cots.append(item)
    
    # AutoCoT
    item = load_one(os.path.join(path, "autocot.json"), aspect, "Human", "Prefix", scale, "AutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", dataset, model)
    items.append(item)
    autocots.append(item)
    
    # Metrics
    item = load_one(os.path.join(path, "metrics.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "Metrics", "NoExample", "NoReference", "TEI", dataset, model)
    items.append(item)
    metrics.append(item)
    
    # Order
    item = load_one(os.path.join(path, "tie.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TIE", dataset, model)
    items.append(item)
    orders.append(item)
    
    item = load_one(os.path.join(path, "ite.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "ITE", dataset, model)
    items.append(item)
    orders.append(item)
    
    item = load_one(os.path.join(path, "iet.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "IET", dataset, model)
    items.append(item)
    orders.append(item)
    
    item = load_one(os.path.join(path, "eit.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "EIT", dataset, model)
    items.append(item)
    orders.append(item)
    
    item = load_one(os.path.join(path, "eti.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "ETI", dataset, model)
    items.append(item)
    orders.append(item)
    
    return items, criteria, cots, scales, autocots, metrics, examples, references, orders
