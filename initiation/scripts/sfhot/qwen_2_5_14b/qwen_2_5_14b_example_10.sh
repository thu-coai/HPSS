python judge_vllm_aspects.py \
    --input_file ../data/sfhot/sfhot_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfhot/example/example.py \
    --save_path ../initiation/results/sfhot/example \
    --suffix_name example_10_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfhot/criteria/criteria_human.json \
    --fewshot ../auxiliary/sfhot/example/few_shot_sfhot_scale_5_number_10_train.json \
    --train \
    --max 5 \
    --dataset sfhot

