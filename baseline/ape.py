import os
import subprocess
import argparse
import json
from HPSS.factors import *
from dataset2aspects import dataset2aspects
from HPSS.baseline.ape_prompts.resample_prompt import resample_prompt
from args import inference_parser
from vllm_inference import inference
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("/path/to/Qwen2.5-14B-Instruct", trust_remote_code=True)
llm = LLM("/path/to/Qwen2.5-14B-Instruct", tensor_parallel_size=4, trust_remote_code=True, max_model_len=8192)


def prompt_resampling(prompt, args):
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


def get_val_res(aspect, dataset, save_path):
    result_dir = save_path.rsplit("/", maxsplit=1)[0]
    result_name = save_path.rsplit("/", maxsplit=1)[1].replace(".jsonl", "_metrics.json")
    result = subprocess.run(
        ['python', 'validation.py', 
         '--input_file', save_path,
         '--result_dir', result_dir,
         '--result_name', result_name,
         '--dataset', dataset,
         '--aspect', aspect], capture_output=True, text=True)
    if result.returncode != 0:
        print(result)

    with open(os.path.join(result_dir, result_name), "r", encoding='utf-8') as f:
        d = json.load(f)
    return d[aspect]['correlation']


class APEItem():
    def __init__(self, prompt, args, tokenizer=None, llm=None, type="valid"):
        self.prompt = prompt
        self.args = args
        
        self.tokenizer = tokenizer
        self.llm = llm
        self.type = type
    
    def evaluate(self, save_path):
        args_ = ['--input_file', f'data/{self.args.dataset}/{self.args.dataset}_{self.type}_{self.args.model}.json',
                 '--base_prompt', self.prompt,
                 '--save_file', save_path,
                 '--dataset', self.args.dataset,
                 '--aspect', aspect]
        
        args_ = inference_parser.parse_args(args_)
        inference(self.tokenizer, self.llm, args_)
        self.correlation = get_val_res(aspect, self.args.dataset, save_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default="qwen_2_5_14b")
    parser.add_argument('--budget', type=int, default=70)
    parser.add_argument('--batch_size', type=int, default=5)
    parser.add_argument('--dataset', type=str, default="hanna")
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--history_path', type=str, default="")
    parser.add_argument('--output_path', type=str, default="ape_results")
    args = parser.parse_args()
    
    if args.dataset == "topical_chat":
        from ape_prompts.topical_chat import base_prompt
        with open("auxiliary/topical_chat/criteria/criteria_human_scale_3.json", "r", encoding='utf-8') as f:
            criteria = json.load(f)
        Max_ = 3
    elif args.dataset == "hanna":
        from ape_prompts.hanna import base_prompt
        with open("auxiliary/hanna/criteria/criteria_human_scale_5.json", "r", encoding='utf-8') as f:
            criteria = json.load(f)
        Max_ = 5
    elif args.dataset == "summeval":
        from ape_prompts.summeval import base_prompt
        with open(f"auxiliary/summeval/criteria/criteria_human.json", "r", encoding='utf-8') as f:
            criteria = json.load(f)
        Max_ = 5
    elif args.dataset == "sfhot":
        from ape_prompts.sfhot import base_prompt
        with open(f"auxiliary/sfhot/criteria/criteria_human.json", "r", encoding='utf-8') as f:
            criteria = json.load(f)
        Max_ = 5
    elif args.dataset == "sfres":
        from ape_prompts.sfres import base_prompt
        with open(f"auxiliary/sfres/criteria/criteria_human.json", "r", encoding='utf-8') as f:
            criteria = json.load(f)
        Max_ = 5
    
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
        
        if aspect == "groundedness":
            Min = 0
            Max = 1
        else:
            Min = 1
            Max = Max_

        criteria_prompt = base_prompt.format(aspect=aspect, criteria=criteria[aspect], min=Min, max=Max)
        item = APEItem(criteria_prompt, args, tokenizer=tokenizer, llm=llm)
        item.evaluate(os.path.join(output_path, f"{aspect}_{0}.jsonl"))
        
        cost = 0
        items = [item]
        logs = []
        while cost < args.budget:
            new_items = []
            for item in items:
                new_prompt = prompt_resampling(resample_prompt.format(prompt=item.prompt), args)
                new_item = APEItem(new_prompt, args, tokenizer=tokenizer, llm=llm)
                try:
                    new_item.evaluate(os.path.join(output_path, f"{aspect}_{cost + 1}.jsonl"))
                except:
                    continue
                new_items.append(new_item)
                cost += 1
                logs.append({
                    "step" : cost,
                    "sample_prompt" : resample_prompt.format(prompt=item.prompt),
                    "prompt" : new_item.prompt,
                    "correlation" : new_item.correlation
                })
                print(f"Step: {cost}, Aspect: {aspect}, Correlation: {new_item.correlation['Spearman']}")
                print('-' * 120)
                if cost >= args.budget:
                    break
            
            items = items + new_items
            items.sort(key=lambda x: x.correlation["Spearman"])
            items = items[-args.batch_size:]
        
        test_item = items[-1]
        test_item.type = "test"
        test_item.evaluate(os.path.join(output_path, f"test_results.jsonl"))
        logs.append({
            "step" : cost,
            "test_correlation" : test_item.correlation,
        })
        with open(os.path.join(output_path, f"log.json"), "w", encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)
            