python judge_vllm_aspects.py \
    --input_file ../data/hanna/hanna_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/hanna/autocot/autocot.py \
    --save_path ../initiation/results/hanna/autocot \
    --suffix_name autocot_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/hanna/criteria/criteria_human_scale_5.json \
    --autocot ../auxiliary/hanna/autocot/autocot_human_criteria_qwen_2_5_14b_scale_5.json \
    --max 5 \
    --dataset hanna
