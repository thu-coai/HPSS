python judge_vllm_aspects.py \
    --input_file ../data/summeval/summeval_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/summeval/criteria/wo_criteria.py \
    --save_path ../initiation/results/summeval/criteria \
    --suffix_name wo_criteria_qwen_2_5_14b.jsonl \
    --max 5 \
    --dataset summeval

