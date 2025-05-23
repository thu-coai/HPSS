python judge_vllm_aspects.py \
    --input_file ../data/hanna/hanna_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/hanna/criteria/wo_criteria.py \
    --save_path ../initiation/results/hanna/criteria \
    --suffix_name wo_criteria_qwen_2_5_14b.jsonl \
    --max 5 \
    --dataset hanna

