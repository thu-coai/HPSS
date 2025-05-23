base_prompt = """[Instruction]
Please act as an impartial judge and evaluate the quality of the story generated according to a prompt displayed below on its {aspect}. Please generate your own story for the given prompt first. Then, begin your evaluation by providing a short explanation which takes into account your own story. After providing your explanation, you must rate the response on a scale of {min} to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]".

Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the story. {criteria}
2. Be as objective as possible.

[Prompt]
{prompt}

[The Start of the Story]
{story}
[The End of the Story]"""