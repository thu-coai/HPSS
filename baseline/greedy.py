import json
import argparse
import random
from dataset2aspects import dataset2aspects
import os
from HPSS.utils import *
from factors import *

def perturbation(item):
    new_item = Item(item.model, item.dataset, item.criteria, item.cot, item.scale, item.autocot, item.metrics, item.example, item.reference, item.order, tokenizer=item.tokenizer, llm=item.llm)
    factor_id = random.randint(0, 7)
    new_value_id = random_sampling(len(FACTORS[factor_id]))
    new_value = FACTORS[factor_id][new_value_id]    
    new_item.change(new_value)        
    if new_item.state_name() not in performance.keys():
        return 1, new_item
    return 0, new_item
    
    
def search(items, aspect, args):
    global performance
    output_dir = os.path.join(os.path.join(os.path.join(args.output_path, args.dataset), args.model), aspect)
    num = 0
    output_path = ""
    while True:
        folder_name = f'version_{num}'
        output_path = os.path.join(output_dir, folder_name)
        num += 1
        if os.path.exists(output_path):
            continue
        else:
            os.makedirs(output_path, exist_ok=True)
            break
    cost = 0
    cnt = 0
    logs = []
    round = 0
    while cost < args.budget:        
        logs.append({
            "step" : cost,
            "item" : items[0].state_name(),
            "correlation" : items[0].correlation["Spearman"]
        })
        
        with open(os.path.join(output_path, "log.json"), "w", encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)
            
        new_items = []
        for j, item in enumerate(items):
            new_items.append(item)
            for _ in range(5):
                flag, new_item = perturbation(item)
                if flag and cost < args.budget:
                    cost += 1
                    new_item.evaluate(os.path.join(output_path, f"{aspect}_{cost}_{new_item.state_name()}.jsonl"), aspect)
                    performance[new_item.state_name()] = new_item.correlation
                    print(f"Search {cost}, Based on {j}, State Name: {new_item.state_name()}, Correlation {new_item.correlation['Spearman']}")
                    new_items.append(new_item)
        new_items = sorted(new_items, key=lambda x: x.correlation["Spearman"], reverse=True)
        items = new_items[:args.beam_size]
        cnt += 1
        round += 1
        if round == 1000:
            break

    test_item = Item(args.model, args.dataset, state_name=items[0].state_name(), tokenizer=tokenizer, llm=llm, type="test", prompt="")
    test_item.evaluate(os.path.join(output_path, f"test_results.jsonl"), aspect)
    logs.append({
        "step" : cost,
        "item" : items[0].state_name(),
        "correlation" : items[0].correlation["Spearman"],
        "test_correlation" : test_item.correlation["Spearman"],
    })
    with open(os.path.join(output_path, "log.json"), "w", encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)
    return new_items

    
def load_initiation(path, args):
    if args.dataset == "topical_chat":
        scale = "3"
    elif args.dataset == "summeval" or args.dataset == "sfhot" or args.dataset == "sfres" or args.dataset == "hanna":
        scale = "5"
    item = load_one(os.path.join(path, "baseline.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model, "")
    return item
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default="qwen_2_5_14b")
    parser.add_argument('--dataset', type=str, default="topical_chat")
    parser.add_argument('--budget', type=int, default=70)
    parser.add_argument('--beam_size', type=int, default=1)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--initiation_path', type=str, default="initiation/metrics")
    parser.add_argument('--output_path', type=str, default="greedy_results")
    args = parser.parse_args()
    random.seed(args.seed)
    np.random.seed(args.seed)
    
    args.initiation_path = os.path.join(os.path.join(args.initiation_path, args.dataset), args.model)
    
    for aspect in dataset2aspects[args.dataset]:
        performance = {}
        item = load_initiation(args.initiation_path, args)
        performance[item.state_name()] = item.correlation
        items = [item]
        items = search(items, aspect, args)
        
        for item in items:
            print(item.state_name(), item.correlation)
    