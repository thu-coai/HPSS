from factors import *
import subprocess
import os
import json
from args import inference_parser
from vllm_inference import inference

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


class Item():
    def __init__(self, model, dataset, criteria=None, cot=None, scale=None, autocot=None, metrics=None, example=None, reference=None, order=None, state_name=None, tokenizer=None, llm=None, prompt="", type="valid"):
        self.model = model
        self.dataset = dataset
        self.correlation = {}
        
        self.criteria = criteria
        self.cot = cot
        self.scale = scale
        self.autocot = autocot
        self.metrics = metrics
        self.example = example
        self.reference = reference
        self.order = order
        
        self.prompt = prompt
        self.tokenizer = tokenizer
        self.llm = llm
        self.type = type

        if state_name is not None:
            state_name = state_name.split("_")
            for idx in range(8):
                for factor in FACTORS[idx]:
                    if factor == state_name[idx]:
                        setattr(self, FACTORS_name[idx], factor)
    
    
    def state_name(self):
        return f"{self.scale}_{self.criteria}_{self.cot}_{self.autocot}_{self.metrics}_{self.example}_{self.reference}_{self.order}"


    def change(self, new_value):
        for idx in range(8):
            if new_value in FACTORS[idx]:
                setattr(self, FACTORS_name[idx], new_value)
    
    
    def get_item(self, idx):
        attributes = [self.scale, self.criteria, self.cot, self.autocot, self.metrics, self.example, self.reference, self.order]
        assert idx >= 0 and idx <= 7
        return attributes[idx]
    
    
    def construct_prompt(self):
        if self.dataset == "topical_chat":
            from prompts.search.topical_chat.template import TIE, TEI, EIT, ETI, IET, ITE, instruction_1, instruction_2, reference_1, reference_2, dialectic, rule_1, rule_2, metrics_prompt, example_prompt, prefix_cot, suffix_cot, cot_free, autocot_prompt
        elif self.dataset == "summeval":
            from prompts.search.summeval.template import TIE, TEI, EIT, ETI, IET, ITE, instruction_1, instruction_2, reference_1, reference_2, dialectic, rule_1, rule_2, metrics_prompt, example_prompt, prefix_cot, suffix_cot, cot_free, autocot_prompt
        elif self.dataset == "hanna":
            from prompts.search.hanna.template import TIE, TEI, EIT, ETI, IET, ITE, instruction_1, instruction_2, reference_1, reference_2, dialectic, rule_1, rule_2, metrics_prompt, example_prompt, prefix_cot, suffix_cot, cot_free, autocot_prompt
        elif self.dataset == "sfhot":
            from prompts.search.sfhot.template import TIE, TEI, EIT, ETI, IET, ITE, instruction_1, instruction_2, reference_1, reference_2, dialectic, rule_1, rule_2, metrics_prompt, example_prompt, prefix_cot, suffix_cot, cot_free, autocot_prompt
        elif self.dataset == "sfres":
            from prompts.search.sfres.template import TIE, TEI, EIT, ETI, IET, ITE, instruction_1, instruction_2, reference_1, reference_2, dialectic, rule_1, rule_2, metrics_prompt, example_prompt, prefix_cot, suffix_cot, cot_free, autocot_prompt
        
        # Order
        if self.order == "TEI":
            prompt = TEI
            prompt = prompt.replace("{instruction}", instruction_1)
        elif self.order == "TIE":
            prompt = TIE
            prompt = prompt.replace("{instruction}", instruction_1)
        elif self.order == "ETI":
            prompt = ETI
            prompt = prompt.replace("{instruction}", instruction_1)
        elif self.order == "EIT":
            prompt = EIT
            prompt = prompt.replace("{instruction}", instruction_2)
        elif self.order == "ITE":
            prompt = ITE
            prompt = prompt.replace("{instruction}", instruction_2)
        elif self.order == "IET":
            prompt = IET
            prompt = prompt.replace("{instruction}", instruction_2)
            
        # Reference
        if self.reference == "Reference":
            prompt = prompt.replace("{reference_1}", reference_1)
            prompt = prompt.replace("{reference_2}", reference_2)
            prompt = prompt.replace("{dialectic}", "")
        elif self.reference == "Dialectic":
            prompt = prompt.replace("{reference_1}", "")
            prompt = prompt.replace("{reference_2}", "")
            prompt = prompt.replace("{dialectic}", dialectic)
        else:
            prompt = prompt.replace("{reference_1}", "")
            prompt = prompt.replace("{reference_2}", "")
            prompt = prompt.replace("{dialectic}", "")
        
        # Criteria
        if self.criteria == "Human":
            prompt = prompt.replace("{rule}", rule_1)
            if self.dataset == "summeval" or self.dataset == "sfhot" or self.dataset == "sfres":
                criteria = f"auxiliary/{self.dataset}/criteria/criteria_human.json"
            elif self.dataset == "topical_chat" or self.dataset == "hanna":
                criteria = f"auxiliary/{self.dataset}/criteria/criteria_human_scale_{self.scale}.json"
        elif self.criteria == "LLM":
            prompt = prompt.replace("{rule}", rule_1)
            if self.dataset == "summeval" or self.dataset == "sfhot" or self.dataset == "sfres":
                criteria = f"auxiliary/{self.dataset}/criteria/criteria_llm_{self.model}.json"
            elif self.dataset == "topical_chat" or self.dataset == "hanna":
                criteria = f"auxiliary/{self.dataset}/criteria/criteria_llm_{self.model}_scale_{self.scale}.json"
        else:
            prompt = prompt.replace("{rule}", rule_2)
            if self.dataset == "summeval" or self.dataset == "sfhot" or self.dataset == "sfres":
                criteria = f"auxiliary/{self.dataset}/criteria/criteria_human.json"
            elif self.dataset == "topical_chat" or self.dataset == "hanna":
                criteria = f"auxiliary/{self.dataset}/criteria/criteria_human_scale_{self.scale}.json"

        # Example
        if self.example == "NoExample":
            prompt = prompt.replace("{example}", "")
        else:
            prompt = prompt.replace("{example}", example_prompt)     
        
        # Metrics
        if self.metrics == "NoMetrics":
            prompt = prompt.replace("{metrics}", "")
        else:
            prompt = prompt.replace("{metrics}", metrics_prompt)
        
        # AutoCoT
        if self.autocot == "NoAutoCoT":
            prompt = prompt.replace("{autocot}", "")
        else:
            prompt = prompt.replace("{autocot}", autocot_prompt)
        
        # CoT
        if self.cot == "Prefix":
            prompt = prompt.replace("{cot}", prefix_cot)
        elif self.cot == "Suffix":
            prompt = prompt.replace("{cot}", suffix_cot)
        else:
            prompt = prompt.replace("{cot}", cot_free)
        return prompt, criteria
    
    
    def evaluate(self, save_path, aspect):
        prompt, criteria = self.construct_prompt()
        if self.prompt != "":
            prompt = self.prompt


        args_ = ['--input_file', f'data/{self.dataset}/{self.dataset}_{self.type}_{self.model}.json',
            '--base_prompt', prompt,
            '--save_file', save_path,
            '--criteria', criteria,
            '--max', self.scale,
            '--dataset', self.dataset,
            '--aspect', aspect]
        
        
        if self.metrics == "Metrics":
            args_.append('--metrics')
        
        if self.example != "NoExample":
            args_.append('--example')
            if self.type == "valid":
                if self.example == "Example3":
                    args_.append(f"auxiliary/{self.dataset}/example/few_shot_{self.dataset}_scale_{self.scale}_number_3_train.json")
                if self.example == "Example5":
                    args_.append(f"auxiliary/{self.dataset}/example/few_shot_{self.dataset}_scale_{self.scale}_number_5_train.json")
                if self.example == "Example10":
                    args_.append(f"auxiliary/{self.dataset}/example/few_shot_{self.dataset}_scale_{self.scale}_number_10_train.json")
                args_.append('--valid')
            else:
                if self.example == "Example3":
                    args_.append(f"auxiliary/{self.dataset}/example/few_shot_{self.dataset}_scale_{self.scale}_number_3.json")
                if self.example == "Example5":
                    args_.append(f"auxiliary/{self.dataset}/example/few_shot_{self.dataset}_scale_{self.scale}_number_5.json")
                if self.example == "Example10":
                    args_.append(f"auxiliary/{self.dataset}/example/few_shot_{self.dataset}_scale_{self.scale}_number_10.json")
        
        if self.reference == "Reference":
            args_.append('--reference')
        
        if self.autocot == "AutoCoT":
            args_.append('--autocot')
            if self.criteria == "Human" or self.criteria == "NoCriteria":
                args_.append(f"auxiliary/{self.dataset}/autocot/autocot_human_criteria_{self.model}_scale_{self.scale}.json")
            else:
                args_.append(f"auxiliary/{self.dataset}/autocot/autocot_llm_criteria_{self.model}_scale_{self.scale}.json")
        
        if self.model == "gpt4o_mini":
            args_ = ['python', 'inference/judge_api.py'] + args_
            result = subprocess.run(args_, capture_output=True, text=True)
            if result.returncode != 0:
                print(result)
        else:
            args_ = inference_parser.parse_args(args_)
            inference(self.tokenizer, self.llm, args_)
        self.correlation = get_val_res(aspect, self.dataset, save_path)
        return args_