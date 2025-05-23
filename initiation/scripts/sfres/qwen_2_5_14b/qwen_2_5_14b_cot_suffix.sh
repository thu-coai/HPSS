python judge_vllm_aspects.py \
    --input_file ../data/sfres/sfres_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfres/cot/cot_suffix.py \
    --save_path ../initiation/results/sfres/cot \
    --suffix_name cot_suffix_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfres/criteria/criteria_human.json \
    --max 5 \
    --dataset sfres

