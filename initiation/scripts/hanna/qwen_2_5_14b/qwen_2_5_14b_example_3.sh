python judge_vllm_aspects.py \
    --input_file ../data/hanna/hanna_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/hanna/example/example.py \
    --save_path ../initiation/results/hanna/example \
    --suffix_name example_3_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/hanna/criteria/criteria_human_scale_5.json \
    --fewshot ../auxiliary/hanna/example/few_shot_hanna_scale_5_number_3_train.json \
    --train \
    --max 5 \
    --dataset hanna
