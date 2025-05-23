base_prompt = """[Instruction]
Please act as an impartial judge and evaluate the quality of the story generated according to a prompt displayed below on its {aspect}. Begin your evaluation by providing a short explanation. After providing your explanation, you must rate the story on a scale of {min} to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]".

Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the story. {criteria}
2. Be as objective as possible.

[Prompt]
{prompt}

[Questions about the Story]
Here are at most three questions about the story, which are presented from most important to least important. You can do the evaluation based on thinking about all the questions.
{metrics}

[The Start of the Story]
{story}
[The End of the Story]"""