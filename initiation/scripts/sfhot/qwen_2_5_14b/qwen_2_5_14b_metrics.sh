python judge_vllm_aspects.py \
    --input_file ../data/sfhot/sfhot_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfhot/metrics/metrics.py \
    --save_path ../initiation/results/sfhot/metrics \
    --suffix_name qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfhot/criteria/criteria_human.json \
    --metrics \
    --max 5 \
    --dataset sfhot
