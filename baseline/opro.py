import os
import traceback
import argparse
import json
from tqdm import trange
from item import *
from factors import *
from dataset2aspects import dataset2aspects
from HPSS.baseline.opro_prompts.opro_prompt import opro_prompt
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("/path/to/Qwen2.5-14B-Instruct", trust_remote_code=True)
llm = LLM("/path/to/Qwen2.5-14B-Instruct", tensor_parallel_size=4, trust_remote_code=True, max_model_len=8192)

def strategy_generate(prompt, args):
    if args.model == "qwen_2_5_14b":
        messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
        ]
        params_dict = {
            "n": 1,
            "best_of": 1,
            "temperature": 1.0,
            "seed" : args.seed,
            "top_p": 1.0,
            "max_tokens": 4096,
            "logprobs": None,
        }
        sampling_params = SamplingParams(**params_dict)
        prompt = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
        )
        outputs = llm.generate([prompt], sampling_params)
        generation = outputs[0].outputs[0].text
    return generation


def get_item(response, args) -> Item:
    strategy = json.loads(response.strip())
    state_name = ""
    for i in range(8):
        state_name += FACTORS[i][strategy[f"Part {i}"]]
        if i != 7:
            state_name += "_"
    return Item(args.model, args.dataset, state_name=state_name, tokenizer=tokenizer, llm=llm)


def item_2_str(state_name):
    response = {}
    state_name = state_name.split("_")
    for idx in range(8):
        for i, factor in enumerate(FACTORS[idx]):
            if factor == state_name[idx]:
                response[f"Part {idx}"] = i
    return str(response)


def load_one(path, aspect, criteria, cot, scale, autocot, metrics, example, reference, order, dataset, model):
    with open(path, "r", encoding='utf-8') as f:
        metrics_ = json.load(f)
    item = Item(model, dataset, criteria, cot, scale, autocot, metrics, example, reference, order, tokenizer=tokenizer, llm=llm)
    item.correlation = metrics_[aspect]['correlation']
    return item

    
def load_initiation(path, args):
    seed_data = []
    
    if args.dataset == "topical_chat":
        scale = "3"
    elif args.dataset == "summeval" or args.dataset == "sfhot" or args.dataset == "sfres" or args.dataset == "hanna":
        scale = "5"
    
    # Scoring Scale
    if scale == "5":
        item = load_one(os.path.join(path, "scale_3.json"), aspect, "Human", "Prefix", "3", "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
        seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    # Baseline (MT-Bench)
    item = load_one(os.path.join(path, "baseline.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
    
    # Scoring Scale
    if scale == "3":
        item = load_one(os.path.join(path, "scale_5.json"), aspect, "Human", "Prefix", "5", "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
        seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
    
    item = load_one(os.path.join(path, "scale_10.json"), aspect, "Human", "Prefix", "10", "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
    
    item = load_one(os.path.join(path, "scale_50.json"), aspect, "Human", "Prefix", "50", "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
    
    item = load_one(os.path.join(path, "scale_100.json"), aspect, "Human", "Prefix", "100", "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    # In-Context Example
    item = load_one(os.path.join(path, "example_3.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "Example3", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    item = load_one(os.path.join(path, "example_5.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "Example5", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    item = load_one(os.path.join(path, "example_10.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "Example10", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    # Criteria
    item = load_one(os.path.join(path, "wo_criteria.json"), aspect, "NoCriteria", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    item = load_one(os.path.join(path, "self_generated_criteria.json"), aspect, "LLM", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    # Reference
    item = load_one(os.path.join(path, "self_generated_reference.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "Reference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    
    item = load_one(os.path.join(path, "dialectic.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "Dialectic", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    # Chain-of-Thought
    item = load_one(os.path.join(path, "cot_suffix.json"), aspect, "Human", "Suffix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
    
    item = load_one(os.path.join(path, "cot_free.json"), aspect, "Human", "Free", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    # AutoCoT
    item = load_one(os.path.join(path, "autocot.json"), aspect, "Human", "Prefix", scale, "AutoCoT", "NoMetrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    # Metrics
    item = load_one(os.path.join(path, "metrics.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "Metrics", "NoExample", "NoReference", "TEI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    # Order
    item = load_one(os.path.join(path, "tie.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "TIE", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    item = load_one(os.path.join(path, "ite.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "ITE", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    item = load_one(os.path.join(path, "iet.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "IET", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    item = load_one(os.path.join(path, "eit.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "EIT", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    item = load_one(os.path.join(path, "eti.json"), aspect, "Human", "Prefix", scale, "NoAutoCoT", "NoMetrics", "NoExample", "NoReference", "ETI", args.dataset, args.model)
    seed_data.append({
            "strategy" : item_2_str(item.state_name()),
            "state_name" : item.state_name(),
            "prompt" : item.construct_prompt()[0],
            "correlation" : item.correlation
        })
        
    return seed_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default="qwen_2_5_14b")
    parser.add_argument('--budget', type=int, default=10)
    parser.add_argument('--show_num', type=int, default=20)
    parser.add_argument('--dataset', type=str, default="summeval")
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--history_path', type=str, default="")
    parser.add_argument('--initiation_path', type=str, default="initiation/metrics/")
    parser.add_argument('--output_path', type=str, default="opro_results")
    args = parser.parse_args()
    
    args.initiation_path = os.path.join(os.path.join(args.initiation_path, args.dataset), args.model)

    for aspect in dataset2aspects[args.dataset]:
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
        
        if args.history_path:
            with open(args.history_path, "r", encoding='utf-8') as f:
                steps = json.load(f)  
        else:
            steps = load_initiation(args.initiation_path, args)

        for i in trange(args.budget):
            history = sorted(steps, key=lambda k: k['correlation']['Spearman'])

            history_prompt = ""
            for j in history[-args.show_num:]:
                history_prompt += "Prompt: {}\nScore: {}\n\n".format(j['strategy'], j['correlation']['Spearman'])
            
            optimization_prompt = opro_prompt.format(history=history_prompt)
            
            try:
                new_strategy = strategy_generate(optimization_prompt, args)
                new_item = get_item(new_strategy, args)
                new_item.evaluate(os.path.join(output_path, f"{aspect}_{i}_{new_item.state_name()}.jsonl"), aspect)
                
                steps.append({
                    "id" : i,
                    "strategy" : item_2_str(new_item.state_name()),
                    "state_name" : new_item.state_name(),
                    "prompt" : new_item.construct_prompt()[0],
                    "correlation" : new_item.correlation,
                    "optimization_prompt" : optimization_prompt
                })
                print(f"Step: {i}, Strategy: {new_strategy}")
                print(f"Step: {i}, State Name: {new_item.state_name()}, Correlation: {new_item.correlation['Spearman']}")

                with open(os.path.join(output_path, "log.json"), 'w', encoding='utf-8') as f:
                    json.dump(steps, f, indent=4, ensure_ascii=False)
            except Exception as e:
                traceback.print_exc()
                continue
        
        mx = 0
        state_name = ""
        for step in steps:
            if mx < step["correlation"]["Spearman"]:
                mx = step["correlation"]["Spearman"]
                state_name = step["state_name"]
        test_item = Item(args.model, args.dataset, state_name=state_name, tokenizer=tokenizer, llm=llm, type="test", prompt="")
        test_item.evaluate(os.path.join(output_path, f"test_results.jsonl"), aspect)
        steps.append({
            "step" : args.budget,
            "item" : state_name,
            "test_correlation" : test_item.correlation["Spearman"],
        })
        with open(os.path.join(output_path, "log.json"), "w", encoding='utf-8') as f:
            json.dump(steps, f, ensure_ascii=False, indent=4)
