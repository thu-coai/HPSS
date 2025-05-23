python judge_vllm_aspects.py \
    --input_file ../data/sfres/sfres_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfres/criteria/wo_criteria.py \
    --save_path ../initiation/results/sfres/criteria \
    --suffix_name wo_criteria_qwen_2_5_14b.jsonl \
    --max 5 \
    --dataset sfres

