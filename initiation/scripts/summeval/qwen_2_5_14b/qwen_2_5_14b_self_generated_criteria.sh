python judge_vllm_aspects.py \
    --input_file ../data/summeval/summeval_valid_qwen_2_5_14b.json \
    --base_prompt ../prompts/initiation/summeval/baseline/baseline.py \
    --save_path ../initiation/results/summeval/criteria \
    --suffix_name self_generated_criteria_qwen_2_5_14b.jsonl \
    --criteria ../auxiliary/summeval/criteria/criteria_llm_qwen_2_5_14b.json \
    --max 5 \
    --dataset summeval
