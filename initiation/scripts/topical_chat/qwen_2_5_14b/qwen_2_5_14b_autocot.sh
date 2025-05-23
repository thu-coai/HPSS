python judge_vllm_aspects.py \
    --input_file ../data/topical_chat/topical_chat_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/topical_chat/autocot/autocot.py \
    --save_path ../initiation/results/topical_chat/autocot \
    --suffix_name autocot_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/topical_chat/criteria/criteria_human_scale_3.json \
    --autocot ../auxiliary/topical_chat/autocot/autocot_human_criteria_qwen_2_5_14b_scale_3.json \
    --max 3 \
    --dataset topical_chat
