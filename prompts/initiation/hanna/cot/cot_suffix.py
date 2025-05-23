base_prompt = """[Instruction]
Please act as an impartial judge and evaluate the quality of the story generated according to a prompt displayed below on its {aspect}. You must rate the story on a scale of {min} to {max} first by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]". And then provide your explanation.

Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the story. {criteria}
2. Be as objective as possible.

[Prompt]
{prompt}

[The Start of the Story]
{story}
[The End of the Story]"""