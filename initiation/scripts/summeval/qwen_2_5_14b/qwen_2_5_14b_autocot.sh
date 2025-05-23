python judge_vllm_aspects.py \
    --input_file ../data/summeval/summeval_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/summeval/autocot/autocot.py \
    --save_path ../initiation/results/summeval/autocot \
    --suffix_name autocot_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/summeval/criteria/criteria_human.json \
    --autocot ../auxiliary/summeval/autocot/autocot_human_criteria_qwen_2_5_14b_scale_5.json \
    --max 5 \
    --dataset summeval
