base_prompt = """[Instruction]
Please act as an impartial judge and evaluate the quality of the story generated according to a prompt displayed below on its {aspect}. Begin your evaluation by providing a short explanation. After providing your explanation, you must rate the story on a scale of {min} to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]".

Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the story. {criteria}
2. Be as objective as possible.

Here are some examples and their corresponding ratings:
{example}

Following these examples, evaluate the quality of the response for the next turn in the conversation displayed below on its {aspect}:
[Prompt]
{prompt}

[The Start of the Story]
{story}
[The End of the Story]"""