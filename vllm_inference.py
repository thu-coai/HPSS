import json
import re
import argparse
import os
import dataclasses
import multiprocessing
lock = multiprocessing.Lock()
from vllm import SamplingParams


def extract_base_prompt(filename):
    if not os.path.isfile(filename):
        return filename
    with open(filename, 'r', encoding='utf-8') as file:
        file_content = file.read()
    local_namespace = {}
    exec(file_content, {}, local_namespace)
    return local_namespace['base_prompt']


@dataclasses.dataclass
class Sample:
    prompt: str
    fact: str
    reference: str
    response: str
    criteria: str
    aspect: str
    example: str
    metrics: str
    autocot: str
    

def prompt_construct(sample: Sample, args):
    base_prompt = extract_base_prompt(args.base_prompt)
    if args.dataset == "topical_chat" and sample.aspect == 'groundedness':
        Min = 0
        if args.max == 3:
            Max = 1
        else:
            Max = args.max
    else:
        Min = 1
        Max = args.max
    
    if args.dataset == "topical_chat":
        prompt = base_prompt.format(context=sample.prompt, fact=sample.fact, response=sample.response, reference=sample.reference, criteria=sample.criteria, aspect=sample.aspect, example=sample.example, metrics=sample.metrics, autocot=sample.autocot, min=Min, max=Max)
    elif args.dataset == "summeval":
        prompt = base_prompt.format(document=sample.prompt, summary=sample.response, reference=sample.reference, criteria=sample.criteria, aspect=sample.aspect, example=sample.example, metrics=sample.metrics, autocot=sample.autocot, min=Min, max=Max)
    elif args.dataset == "sfhot" or args.dataset == "sfres":
        prompt = base_prompt.format(expression=sample.prompt, sentence=sample.response, reference=sample.reference, criteria=sample.criteria, aspect=sample.aspect, example=sample.example, metrics=sample.metrics, autocot=sample.autocot, min=Min, max=Max)
    elif args.dataset == "hanna":
        prompt = base_prompt.format(prompt=sample.prompt, story=sample.response, reference=sample.reference, criteria=sample.criteria, aspect=sample.aspect, example=sample.example, metrics=sample.metrics, autocot=sample.autocot, min=Min, max=Max)
    return prompt


def inference(tokenizer, llm, args):
    save_path = args.save_file.rsplit('/', maxsplit=1)[0]
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    
    with open(args.input_file, "r", encoding='utf-8') as f:
        docs = json.load(f)
    for i in range(len(docs)):
        docs[i]['id'] = i
    print(f">>> loaded {len(docs)} docs from {args.input_file}")

    criteria_ = {}
    if args.criteria != "":
        with open(args.criteria, "r", encoding='utf-8') as f:
            criteria_ = json.load(f)

    example_ = {}
    if args.example != "":
        with open(args.example, "r", encoding='utf-8') as f:
            example_ = json.load(f)

    autocot_ = {}
    if args.autocot != "":
        with open(args.autocot, "r", encoding='utf-8') as f:
            autocot_ = json.load(f)
            
    params_dict = {
        "n": 1,
        "best_of": 1,
        "temperature": args.temperature,
        "seed" : args.seed,
        "top_p": 1.0,
        "max_tokens": 4096,
        "logprobs": None,
    }

    sampling_params = SamplingParams(**params_dict)
    
    prompts = []
    for doc in docs:
        if args.reference:
            reference = doc['generated_reference']
        else:
            reference = ""
            
        if args.example != "":
            if args.valid:
                example = example_[args.aspect][str(doc['id'])]
            else:
                example = example_[args.aspect]
        else:
            example = ""

        if args.criteria != "":
            criteria = criteria_[args.aspect]
        else:
            criteria = ""
            
        if args.metrics:
            metrics = doc[f"metrics_{args.aspect}"]
        else:
            metrics = ""
            
        if args.autocot != "":
            autocot = autocot_[args.aspect]
        else:
            autocot = ""

        if args.dataset == "topical_chat":
            sample = Sample(doc['source'], doc['context'], reference, doc['system_output'], criteria, args.aspect, example, metrics, autocot)
        elif args.dataset == "summeval":
            sample = Sample(doc['source'], "", reference, doc['system_output'], criteria, args.aspect, example, metrics, autocot)
        elif args.dataset == "sfhot" or args.dataset == "sfres":
            sample = Sample(doc['source'], "", reference, doc['system_output'], criteria, args.aspect, example, metrics, autocot)
        elif args.dataset == "hanna":
            sample = Sample(doc['prompt'], "", reference, doc['story'], criteria, args.aspect, example, metrics, autocot)
            
        prompt = prompt_construct(sample, args)
        messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
        ]
        prompt = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
        )
        prompts.append(prompt)
    
    outputs = llm.generate(prompts, sampling_params)

    with open(args.save_file, "w", encoding='utf-8') as f:
        f.write("")
    
    for i, output in enumerate(outputs):
        generated_text = output.outputs[0].text
        doc = docs[i]

        doc["judge_prompt"] = prompts[i]
        doc["judgment"] = generated_text

        with lock:
            with open(args.save_file, "a", encoding='utf-8') as f:
                f.write(json.dumps(doc, ensure_ascii=False))
                f.write('\n')
