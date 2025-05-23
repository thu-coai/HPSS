python judge_vllm_aspects.py \
    --input_file ../data/topical_chat/topical_chat_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/topical_chat/metrics/metrics.py \
    --save_path ../initiation/results/topical_chat/metrics \
    --suffix_name qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/topical_chat/criteria/criteria_human_scale_3.json \
    --metrics \
    --max 3 \
    --dataset topical_chat
