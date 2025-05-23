import json
import numpy as np
import argparse
import random
from dataset2aspects import dataset2aspects
from copy import deepcopy
import os
from utils import *
from factors import *
import math
import itertools
from copy import deepcopy

all_combinations = list(itertools.product(*FACTORS))


def update_advantage(old_value, new_value, old_item, new_item):
    advantage[new_value] = (advantage[new_value] * count[new_value] + (new_item.correlation["Spearman"] * 100 - old_item.correlation["Spearman"] * 100 + advantage[old_value])) / (count[new_value] + 1)
    count[new_value] += 1
    for i in range(8):
        if new_value in FACTORS[i]:
            factor_id = i
    average = 0
    for factor in FACTORS[factor_id]:
        average += advantage[factor] / len(FACTORS[factor_id])
    for factor in FACTORS[factor_id]:
        advantage[factor] -= average


def init_advantage(values, items):
    average = 0
    for item in items:
        average += item.correlation["Spearman"] * 100 / len(items)
    for _, (value, item) in enumerate(zip(values, items)):
        advantage[value] = item.correlation["Spearman"] * 100 - average
        count[value] = 1
        count_all[value] = 1


def find_max():
    mx_state = ""
    mx_value = -100
    for combination in all_combinations:
        state_name = "_".join(combination)
        value = 0
        for factor in combination:
            value += advantage[factor]
        if value > mx_value and state_name not in performance.keys():
            mx_state = state_name
            mx_value = value
    return mx_state


def find_adj(state_name, step, lambda_):
    states = state_name.split("_")
    adjs = []
    advs = []
    ids = []
    for i, factors in enumerate(FACTORS):
        for factor in factors:
            if states[i] == factor:
                continue
            new_states = deepcopy(states)
            new_states[i] = factor
            adjs.append(factor)
            advs.append(advantage[factor] - advantage[states[i]] + lambda_ * math.sqrt(math.log(step) / count_all[factor]))
            ids.append(i)
    return adjs, advs, ids


def get_state(state_name, step, lambda_, temperature):
    advs = {}
    values = {}
    all = {}
    probs = {}
    p = []
    states = state_name.split("_")
    for i, factors in enumerate(FACTORS):
        for factor in factors:
            advs[factor] = advantage[factor] - advantage[states[i]]
            values[factor] = lambda_ * math.sqrt(math.log(step) / count_all[factor])    
            all[factor] = advs[factor] + values[factor]
            if states[i] == factor:
                continue
            p.append(all[factor])
    p, _ = softmax_sampling(p, temperature)
    cnt = 0
    for i, factors in enumerate(FACTORS):
        for factor in factors:
            if states[i] == factor:
                continue
            probs[factor] = p[cnt]
            cnt += 1
    return {
        "advantage" : deepcopy(advantage),
        "advs" : advs,
        "values" : values,
        "all" : all,
        "probs" : probs
    }
    

def perturbation(item, step, rho, temperature=10.0, lambda_=0.0):
    new_item = Item(item.model, item.dataset, item.criteria, item.cot, item.scale, item.autocot, item.metrics, item.example, item.reference, item.order, tokenizer=item.tokenizer, llm=item.llm)
    adjs, advs, ids = find_adj(item.state_name(), step, lambda_)
    _, select_id = softmax_sampling(advs, temperature)
        
    new_value = adjs[select_id]
    old_value = item.get_item(ids[select_id])
    new_item.change(new_value)

    if new_item.state_name() not in performance.keys():
        p = random.random()
        if p <= rho:
            mx_state = find_max()
            new_item = Item(item.model, item.dataset, state_name=mx_state, tokenizer=item.tokenizer, llm=item.llm)
            return 1, new_item, None, None, 0
        else:
            return 1, new_item, old_value, new_value, 1
            
    return 0, None, None, None, None
    

def search(items, aspect, args):
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
    round = 0
    rho = args.rho
    logs = []
    steps = []
    while cost < args.budget:        
        logs.append({
            "step" : cost,
            "item" : items[0].state_name(),
            "correlation" : items[0].correlation["Spearman"]
        })
        
        state_list = []
        for item in items[:args.beam_size]:
            state_list.append((item.state_name(), item.correlation["Spearman"]))
            
        new_items = []
        for j, item in enumerate(items):
            new_items.append(item)
            for _ in range(args.g):
                flag, new_item, old_value, new_value, type = perturbation(item, cost + 1, rho, args.temperature, args.lambda_)
                if flag and cost < args.budget:
                    new_item.evaluate(os.path.join(output_path, f"{aspect}_{cost}_{new_item.state_name()}.jsonl"), aspect)
                    performance[new_item.state_name()] = new_item.correlation
                    print(f"Search {cost}, Based on {j}, Type {type}: {new_item.state_name()}, Correlation {new_item.correlation['Spearman']}")
                    new_items.append(new_item)
                    
                    if type != 0:
                        steps.append({
                            "step" : cost,
                            "previous_item" : item.state_name(),
                            "previous_correlation" : item.correlation["Spearman"],
                            "item" : new_item.state_name(),
                            "correlation" : new_item.correlation["Spearman"],
                            "advantage" : new_item.correlation["Spearman"] - item.correlation["Spearman"],
                            "state_list" : state_list,
                            "state" : get_state(item.state_name(), cost + 1, args.lambda_, args.temperature)
                        })
                    else:
                        steps.append({
                            "step" : cost,
                            "item" : new_item.state_name(),
                            "correlation" : new_item.correlation["Spearman"],
                            "state_list" : state_list,
                            "state" : get_state(item.state_name(), cost + 1, args.lambda_, args.temperature)
                        })
                    with open(os.path.join(output_path, "log.json"), "w", encoding='utf-8') as f:
                        json.dump(logs, f, ensure_ascii=False, indent=4)
                    with open(os.path.join(output_path, "steps.json"), "w", encoding='utf-8') as f:
                        json.dump(steps, f, ensure_ascii=False, indent=4)
        
                    cost += 1
                    if old_value != None:
                        update_advantage(old_value, new_value, item, new_item)
                    for factor_id in range(8):
                        count_all[new_item.get_item(factor_id)] = count_all.get(new_item.get_item(factor_id), 0) + 1
                    
        
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
    with open(os.path.join(output_path, "steps.json"), "w", encoding='utf-8') as f:
        json.dump(steps, f, ensure_ascii=False, indent=4)
    return new_items
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default="qwen_2_5_14b")
    parser.add_argument('--dataset', type=str, default="topical_chat")
    parser.add_argument('--budget', type=int, default=50)
    parser.add_argument('--beam_size', type=int, default=5)
    parser.add_argument('--seed', type=int, default=2)
    
    parser.add_argument('--temperature', type=float, default=5.0)
    parser.add_argument('--lambda_', type=float, default=2.0)
    parser.add_argument('--rho', type=float, default=0.2)
    parser.add_argument('--g', type=int, default=2)
    
    parser.add_argument('--initiation_path', type=str, default="initiation/metrics")
    parser.add_argument('--output_path', type=str, default="factors_results")
    parser.add_argument('--aspect', type=str, default="")
    args = parser.parse_args()
    print(args)
    
    random.seed(args.seed)
    np.random.seed(args.seed)
    
    args.initiation_path = os.path.join(os.path.join(args.initiation_path, args.dataset), args.model)
    
    if args.aspect != "":
        aspects = [args.aspect]
    else:
        aspects = dataset2aspects[args.dataset]
    
    for aspect in aspects:
        advantage = {}
        count = {}
        count_all = {}
        performance = {}
        
        items, criteria, cots, scales, autocots, metrics, examples, references, orders = load_results(args.initiation_path, aspect, args.dataset, args.model)
        items = sorted(items, key=lambda x: x.correlation["Spearman"], reverse=True)
        for item in items:
            performance[item.state_name()] = item.correlation
        
        init_advantage(CRITERIA, criteria)
        init_advantage(COT, cots)
        init_advantage(SCALE, scales)
        init_advantage(AUTOCOT, autocots)
        init_advantage(METRICS, metrics)
        init_advantage(EXAMPLE, examples)
        init_advantage(REFERENCE, references)
        init_advantage(ORDER, orders)
        
        items = items[:args.beam_size]
        items = search(items, aspect, args)
        
        for item in items:
            print(item.state_name(), item.correlation)
    