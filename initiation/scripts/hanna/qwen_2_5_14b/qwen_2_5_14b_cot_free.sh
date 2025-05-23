python judge_vllm_aspects.py \
    --input_file ../data/hanna/hanna_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/hanna/cot/cot_free.py \
    --save_path ../initiation/results/hanna/cot \
    --suffix_name cot_free_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/hanna/criteria/criteria_human_scale_5.json \
    --max 5 \
    --dataset hanna

