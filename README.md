# HPSS: Heuristic Prompting Strategy Search for LLM-as-a-Judge

This is the official implementation of HPSS: Heuristic Prompting Strategy Search for LLM-as-a-Judge. 

## ⚙️ Requirements

To install requirements:

```setup
pip install -r requirements.txt
```

## 🌳 File Structure

```plaintext
HPSS
├── auxiliary
│   ├── hanna
│   ├── sfhot
│   ├── sfres
│   ├── summeval
│   └── topical_chat
├── baseline
│   ├── ape_prompts
│   ├── ape.py
│   ├── greedy.py
│   ├── opro_prompt
│   └── opro.py
├── data
│   ├── hanna
│   ├── sfhot
│   ├── sfres
│   ├── summeval
│   └── topical_chat
├── evaluation
│   ├── scripts
│   ├── dataset2aspects.py
│   └── evaluation_aspects.py
├── initiation
│   ├── metrics
│   ├── scripts
│   ├── dataset2aspects.py
│   └── judge_vllm_aspects.py
├── prompts
│   ├── initiation
│   └── search
├── README.md
├── args.py
├── dataset2aspects.py
├── factors.py
├── hpss.py
├── item.py
├── requirements.txt
├── utils.py
├── validation.py
└── vllm_inference.py
```

`auxiliary/`: Auxiliary information for factors `Autocot`, `Evaluation Criteria`, and `In-Context Example`.

`baseline/`: Existing automatic prompt optimization methods we implement.

`data/`: The validation and test dataset. Auxiliary information for factors `Reference` and `Metrics` are placed in each data sample.

`evaluation/`: Scripts for calculating the correlation coefficient.

`inference/`: Scripts for utilizing LLM-as-a-Judge to text evaluation.

`initiation/`: The implementation of the **Initialization** stage in our algorithm.

`prompts/`: Prompt templates used in HPSS.

`hpss.py`: The implementation of the **Iterative Search** stage in our algorithm.

## 🚀 Running HPSS

We have placed the results of the **Initialization** stage in `initiation/metrics/` for each dataset. You can run the following script to run HPSS to search for well-behaved prompting strategies.

```bash
python hpss.py \
    --model <model> \
    --dataset <dataset> \
    --budget <budget> \
    --beam_size <beam_size> \
    --seed <seed> \
    --temperature <temperature>
    --lambda_ <lambda_> \
    --rho <rho> \
    --g <g> \
    --initiation_path <initiation_path> \
    --output_path <output_path> \
    --aspect <aspect>
```

Here is an example:

```bash
python hpss.py
    --model qwen_2_5_14b \
    --dataset topical_chat \
    --budget 50 \
    --beam_size 5 \
    --seed 42 \
    --temperature 5.0 \
    --lambda_ 4.0 \
    --rho 0.2 \
    --g 2 \
    --initiation_path initiation/metrics \
    --output_path hpss_results \
    --aspect coherence \
```

After running the scripts, you can find the results saved in `hpss_results/`.

