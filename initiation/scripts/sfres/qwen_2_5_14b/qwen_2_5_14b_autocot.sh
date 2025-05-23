python judge_vllm_aspects.py \
    --input_file ../data/sfres/sfres_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfres/autocot/autocot.py \
    --save_path ../initiation/results/sfres/autocot \
    --suffix_name autocot_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfres/criteria/criteria_human.json \
    --autocot ../auxiliary/sfres/autocot/autocot_human_criteria_qwen_2_5_14b_scale_5.json \
    --max 5 \
    --dataset sfres
