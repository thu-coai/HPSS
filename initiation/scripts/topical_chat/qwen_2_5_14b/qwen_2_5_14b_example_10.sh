python judge_vllm_aspects.py \
    --input_file ../data/topical_chat/topical_chat_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/topical_chat/example/example.py \
    --save_path ../initiation/results/topical_chat/example \
    --suffix_name example_10_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/topical_chat/criteria/criteria_human_scale_3.json \
    --fewshot ../auxiliary/topical_chat/example/few_shot_topical_chat_scale_3_number_10_train.json \
    --train \
    --max 3 \
    --dataset topical_chat

