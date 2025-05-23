python judge_vllm_aspects.py \
    --input_file ../data/sfhot/sfhot_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfhot/cot/cot_suffix.py \
    --save_path ../initiation/results/sfhot/cot \
    --suffix_name cot_suffix_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfhot/criteria/criteria_human.json \
    --max 5 \
    --dataset sfhot

