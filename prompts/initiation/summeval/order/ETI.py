base_prompt = """Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the summary. {criteria}
2. Be as objective as possible.

[Instruction]
Please act as an impartial judge and evaluate the quality of the summary to the news article displayed below on its {aspect}. Begin your evaluation by providing a short explanation. After providing your explanation, you must rate the summary on a scale of {min} to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]".

[Article]
{document}

[The Start of the Summary]
{summary}
[The End of the Summary]"""