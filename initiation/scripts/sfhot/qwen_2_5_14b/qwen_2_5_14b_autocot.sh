python judge_vllm_aspects.py \
    --input_file ../data/sfhot/sfhot_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfhot/autocot/autocot.py \
    --save_path ../initiation/results/sfhot/autocot \
    --suffix_name autocot_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfhot/criteria/criteria_human.json \
    --autocot ../auxiliary/sfhot/autocot/autocot_human_criteria_qwen_2_5_14b_scale_5.json \
    --max 5 \
    --dataset sfhot
