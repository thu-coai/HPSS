import json
import re
import numpy as np
import os
import argparse
import scipy.stats
from scipy.stats import spearmanr, kendalltau
import math


def extract_number(s):
    pattern_1 = r'\[\[((?:1000(?:\.0*)?|[0-9]{1,3}(?:\.\d*)?))\]\]'
    pattern_2 = r'\[((?:1000(?:\.0*)?|[0-9]{1,3}(?:\.\d*)?))\]'
    pattern_3 = r'Rating: ((?:1000(?:\.0*)?|[0-9]{1,3}(?:\.\d*)?))'
    pattern_4 = r'((?:1000(?:\.0*)?|[0-9]{1,3}(?:\.\d*)?))'
    match_1 = re.search(pattern_1, s)
    match_2 = re.search(pattern_2, s)
    match_3 = re.search(pattern_3, s)
    match_4 = re.search(pattern_4, s)
    if match_1:
        return float(match_1.group(1))
    elif match_2:
        return float(match_2.group(1))
    elif match_3:
        return float(match_3.group(1))
    elif match_4:
        return float(match_4.group(1))
    
    return 2.51


def correlation_dataset(v, u):
    return {
        "Pearson" : np.corrcoef(v, u)[0, 1],
        "Spearman" : spearmanr(v, u)[0],
        "Kendall" : kendalltau(v, u)[0]
    }


def correlation_summary(v, u, strip=16):
    p, s, k = 0, 0, 0
    length = 0 
    for i in range(len(v) // strip):
        vs = v[i * strip: (i + 1) * strip]
        us = u[i * strip: (i + 1) * strip]
        if np.isnan(scipy.stats.spearmanr(vs, us)[0]):
            continue

        p += np.corrcoef(vs, us)[0, 1]
        s += spearmanr(vs, us)[0]
        k += kendalltau(vs, us)[0]
        length += 1

    return {
        "Pearson" : p / length,
        "Spearman" : s / length,
        "Kendall" : k / length
    }
    

def entropy(v, n):
    en = 0
    for k in v.keys():
        en += (v[k] / n) * np.log2(v[k] / n)
    return -en


def count_frequencies(arr):
    frequency_dict = {}
    for num in arr:
        if num in frequency_dict:
            frequency_dict[num] += 1
        else:
            frequency_dict[num] = 1
    sorted_frequency_dict = {float(k): v for k, v in sorted(frequency_dict.items())}
    return sorted_frequency_dict


def kl_divergence(P_input, Q_input):
    P = {}
    Q = {}
    total = 0
    for key in sorted(P_input.keys()):
        key_ = round(key, 0)
        P[key_] = P.get(key_, 0) + P_input[key]
        total += P_input[key]
    
    for key in sorted(Q_input.keys()):
        key_ = round(key, 0)
        Q[key_] = Q.get(key_, 0) + Q_input[key]
    
    kl_div = 0
    for key in P:
        if key in Q:
            if P[key] == 0:
                continue
            P[key] /= total
            Q[key] /= total
            kl_div += P[key] * math.log(P[key] / Q[key])
    return kl_div


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default="")
    parser.add_argument('--result_dir', type=str, default="")
    parser.add_argument('--result_name', type=str, default="")
    parser.add_argument('--dataset', type=str, default="")
    parser.add_argument('--aspect', type=str, default="")
    args = parser.parse_args()
    
    result = {}
    average = {}
    auto_scores = []
    human_scores = []
    with open(args.input_file, "r", encoding='utf-8') as f:
        data = [json.loads(line) for line in f.readlines()]
    
    if args.dataset == "summeval":
        data.sort(key=lambda x: x['doc_id'])
    else:
        data.sort(key=lambda x: x['id'])
    
    for i, d in enumerate(data):
        score = extract_number(d['judgment'])     
        auto_scores.append(score)
        human_scores.append(d['scores'][args.aspect])
        d[f'{args.aspect}_score'] = score
    auto_scores = np.array(auto_scores)
    human_scores = np.array(human_scores)
    
    if args.dataset == "summeval":
        result[args.aspect] = {
            "correlation": correlation_summary(auto_scores, human_scores),
            "human_scores_distribution": count_frequencies(human_scores),
            "auto_scores_distribution": count_frequencies(auto_scores),
            "human_scores_entropy": entropy(count_frequencies(human_scores), len(data)),
            "auto_scores_entropy": entropy(count_frequencies(auto_scores), len(data)),
            "kl_divergence": kl_divergence(count_frequencies(human_scores), count_frequencies(auto_scores))
        }

        average["Pearson"] = average.get("Pearson", 0) + correlation_summary(auto_scores, human_scores)["Pearson"]
        average["Spearman"] = average.get("Spearman", 0) + correlation_summary(auto_scores, human_scores)["Spearman"]
        average["Kendall"] = average.get("Kendall", 0) + correlation_summary(auto_scores, human_scores)["Kendall"]
    else:
        result[args.aspect] = {
            "correlation": correlation_dataset(auto_scores, human_scores),
            "human_scores": count_frequencies(human_scores),
            "auto_scores": count_frequencies(auto_scores),
            "human_scores_entropy": entropy(count_frequencies(human_scores), len(data)),
            "auto_scores_entropy": entropy(count_frequencies(auto_scores), len(data)),
            "kl_divergence": kl_divergence(count_frequencies(human_scores), count_frequencies(auto_scores))
        }

        average["Pearson"] = average.get("Pearson", 0) + correlation_dataset(auto_scores, human_scores)["Pearson"]
        average["Spearman"] = average.get("Spearman", 0) + correlation_dataset(auto_scores, human_scores)["Spearman"]
        average["Kendall"] = average.get("Kendall", 0) + correlation_dataset(auto_scores, human_scores)["Kendall"]

    if not os.path.exists(args.result_dir):
        os.makedirs(args.result_dir)
    with open(os.path.join(args.result_dir, args.result_name), "w", encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
