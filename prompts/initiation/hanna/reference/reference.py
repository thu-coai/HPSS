base_prompt = """[Instruction]
Please act as an impartial judge and evaluate the quality of the story generated according to a prompt displayed below on its {aspect}. You will be given the prompt, the generated story and a high-quality reference story. Begin your evaluation by providing a short explanation. After providing your explanation, you must rate the response on a scale of {min} to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]".

Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the story. {criteria}
2. Be as objective as possible.

[Prompt]
{prompt}

[The Start of Reference Story]
{reference}
[The End of Reference Story]

[The Start of the Story]
{story}
[The End of the Story]"""