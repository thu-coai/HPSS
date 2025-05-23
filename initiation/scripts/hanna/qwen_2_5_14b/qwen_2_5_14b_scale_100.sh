python judge_vllm_aspects.py \
    --input_file ../data/hanna/hanna_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/hanna/baseline/baseline.py \
    --save_path ../initiation/results/hanna/scale \
    --suffix_name 100_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/hanna/criteria/criteria_human_scale_100.json \
    --max 100 \
    --dataset hanna
