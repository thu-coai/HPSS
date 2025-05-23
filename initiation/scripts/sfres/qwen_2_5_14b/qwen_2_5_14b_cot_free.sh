python judge_vllm_aspects.py \
    --input_file ../data/sfres/sfres_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfres/cot/cot_free.py \
    --save_path ../initiation/results/sfres/cot \
    --suffix_name cot_free_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfres/criteria/criteria_human.json \
    --max 5 \
    --dataset sfres

