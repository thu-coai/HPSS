python judge_vllm_aspects.py \
    --input_file ../data/sfhot/sfhot_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/sfhot/reference/reference.py \
    --save_path ../initiation/results/sfhot/reference \
    --suffix_name self_generated_reference_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/sfhot/criteria/criteria_human.json \
    --reference \
    --max 5 \
    --dataset sfhot

