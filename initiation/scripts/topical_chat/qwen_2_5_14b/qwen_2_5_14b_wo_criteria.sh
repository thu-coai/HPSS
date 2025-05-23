python judge_vllm_aspects.py \
    --input_file ../data/topical_chat/topical_chat_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/topical_chat/criteria/wo_criteria.py \
    --save_path ../initiation/results/topical_chat/criteria \
    --suffix_name wo_criteria_qwen_2_5_14b.jsonl \
    --max 3 \
    --dataset topical_chat

