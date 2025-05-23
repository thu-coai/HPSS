python judge_vllm_aspects.py \
    --input_file ../data/sfres/sfres_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfres/baseline/baseline.py \
    --save_path ../initiation/results/sfres/scale \
    --suffix_name 50_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfres/criteria/criteria_human.json \
    --max 50 \
    --dataset sfres

