python judge_vllm_aspects.py \
    --input_file ../data/hanna/hanna_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/hanna/baseline/baseline.py \
    --save_path ../initiation/results/hanna/criteria \
    --suffix_name self_generated_criteria_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/hanna/criteria/criteria_llm_qwen_2_5_14b_scale_5.json \
    --max 5 \
    --dataset hanna
