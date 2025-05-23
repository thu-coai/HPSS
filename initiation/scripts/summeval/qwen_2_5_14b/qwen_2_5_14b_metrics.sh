python judge_vllm_aspects.py \
    --input_file ../data/summeval/summeval_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/summeval/metrics/metrics.py \
    --save_path ../initiation/results/summeval/metrics \
    --suffix_name qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/summeval/criteria/criteria_human.json \
    --metrics \
    --max 5 \
    --dataset summeval
