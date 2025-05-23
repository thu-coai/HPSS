model=$1
dataset=$2
result_dir=../initiation/metrics/${dataset}/${model}
mkdir -p ${result_dir}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/baseline \
    --file_name ${model} \
    --result_dir ${result_dir} \
    --result_name baseline.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/example \
    --file_name example_3_${model} \
    --result_dir ${result_dir} \
    --result_name example_3.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/example \
    --file_name example_5_${model} \
    --result_dir ${result_dir}\
    --result_name example_5.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/example \
    --file_name example_10_${model} \
    --result_dir ${result_dir} \
    --result_name example_10.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/reference \
    --file_name self_generated_reference_${model} \
    --result_dir ${result_dir} \
    --result_name self_generated_reference.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/reference \
    --file_name dialectic_${model} \
    --result_dir ${result_dir} \
    --result_name dialectic.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/metrics \
    --file_name ${model} \
    --result_dir ${result_dir} \
    --result_name metrics.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/criteria \
    --file_name wo_criteria_${model} \
    --result_dir ${result_dir} \
    --result_name wo_criteria.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/criteria \
    --file_name self_generated_criteria_${model} \
    --result_dir ${result_dir} \
    --result_name self_generated_criteria.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/cot \
    --file_name cot_free_${model} \
    --result_dir ${result_dir} \
    --result_name cot_free.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/cot \
    --file_name cot_suffix_${model} \
    --result_dir ${result_dir} \
    --result_name cot_suffix.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/autocot \
    --file_name autocot_${model} \
    --result_dir ${result_dir} \
    --result_name autocot.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/scale \
    --file_name 3_${model} \
    --result_dir ${result_dir} \
    --result_name scale_3.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/scale \
    --file_name 10_${model} \
    --result_dir ${result_dir} \
    --result_name scale_10.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/scale \
    --file_name 50_${model} \
    --result_dir ${result_dir} \
    --result_name scale_50.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/scale \
    --file_name 100_${model} \
    --result_dir ${result_dir} \
    --result_name scale_100.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/order \
    --file_name eit_${model} \
    --result_dir ${result_dir} \
    --result_name eit.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/order \
    --file_name eti_${model} \
    --result_dir ${result_dir} \
    --result_name eti.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/order \
    --file_name iet_${model} \
    --result_dir ${result_dir} \
    --result_name iet.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/order \
    --file_name ite_${model} \
    --result_dir ${result_dir} \
    --result_name ite.json \
    --dataset ${dataset}


python evaluation_aspects.py \
    --input_path ../initiation/results/${dataset}/order \
    --file_name tie_${model} \
    --result_dir ${result_dir} \
    --result_name tie.json \
    --dataset ${dataset}