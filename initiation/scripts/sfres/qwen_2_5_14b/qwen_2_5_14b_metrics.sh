python judge_vllm_aspects.py \
    --input_file ../data/sfres/sfres_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfres/metrics/metrics.py \
    --save_path ../initiation/results/sfres/metrics \
    --suffix_name qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfres/criteria/criteria_human.json \
    --metrics \
    --max 5 \
    --dataset sfres
