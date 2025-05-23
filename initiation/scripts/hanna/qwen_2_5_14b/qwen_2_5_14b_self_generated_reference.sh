python judge_vllm_aspects.py \
    --input_file ../data/hanna/hanna_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/hanna/reference/reference.py \
    --save_path ../initiation/results/hanna/reference \
    --suffix_name self_generated_reference_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/hanna/criteria/criteria_human_scale_5.json \
    --reference \
    --max 5 \
    --dataset hanna

