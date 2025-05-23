python judge_vllm_aspects.py \
    --input_file ../data/summeval/summeval_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/summeval/example/example.py \
    --save_path ../initiation/results/summeval/example \
    --suffix_name example_3_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/summeval/criteria/criteria_human.json \
    --fewshot ../auxiliary/summeval/example/few_shot_summeval_scale_5_number_3_train.json \
    --train \
    --max 5 \
    --dataset summeval
