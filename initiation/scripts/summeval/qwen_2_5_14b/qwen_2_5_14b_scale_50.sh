python judge_vllm_aspects.py \
    --input_file ../data/summeval/summeval_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/summeval/baseline/baseline.py \
    --save_path ../initiation/results/summeval/scale \
    --suffix_name 50_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/summeval/criteria/criteria_human.json \
    --max 50 \
    --dataset summeval

