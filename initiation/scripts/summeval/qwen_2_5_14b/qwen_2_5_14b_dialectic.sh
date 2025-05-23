python judge_vllm_aspects.py \
    --input_file ../data/summeval/summeval_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/summeval/reference/dialectic.py \
    --save_path ../initiation/results/summeval/reference \
    --suffix_name dialectic_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/summeval/criteria/criteria_human.json \
    --max 5 \
    --dataset summeval
