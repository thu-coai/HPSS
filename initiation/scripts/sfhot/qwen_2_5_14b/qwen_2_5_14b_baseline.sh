python judge_vllm_aspects.py \
    --input_file ../data/sfhot/sfhot_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfhot/baseline/baseline.py \
    --save_path ../initiation/results/sfhot/baseline \
    --suffix_name qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfhot/criteria/criteria_human.json \
    --max 5 \
    --dataset sfhot
