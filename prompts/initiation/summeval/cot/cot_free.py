base_prompt = """[Instruction]
Please act as an impartial judge and evaluate the quality of the summary to the news article displayed below on its {aspect}. You must directly output your rating of the summary on a scale of {min} to {max} without any explanation by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]".

Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the summary. {criteria}
2. Be as objective as possible.

[Article]
{document}

[The Start of the Summary]
{summary}
[The End of the Summary]"""