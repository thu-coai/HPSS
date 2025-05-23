python judge_vllm_aspects.py \
    --input_file ../data/topical_chat/topical_chat_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/topical_chat/baseline/baseline.py \
    --save_path ../initiation/results/topical_chat/baseline \
    --suffix_name qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/topical_chat/criteria/criteria_human_scale_3.json \
    --max 3 \
    --dataset topical_chat
