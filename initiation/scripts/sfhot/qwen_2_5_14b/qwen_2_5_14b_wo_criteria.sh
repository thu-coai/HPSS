python judge_vllm_aspects.py \
    --input_file ../data/sfhot/sfhot_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfhot/criteria/wo_criteria.py \
    --save_path ../initiation/results/sfhot/criteria \
    --suffix_name wo_criteria_qwen_2_5_14b.jsonl \
    --max 5 \
    --dataset sfhot

