base_prompt = """[Instruction]
Please act as an impartial judge and evaluate the quality of a natural language sentence generated according to a structured data expression displayed below on its {aspect}. Begin your evaluation by providing a short explanation. After providing your explanation, you must rate the sentence on a scale of 1 to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]".

Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the sentence. {criteria}
2. Be as objective as possible.

[Structured Data Experssion]
{expression}

[Questions about the Sentence]
Here are at most three questions about the sentence, which are presented from most important to least important. You can do the evaluation based on thinking about all the reference.
{metrics}

[The Start of the Natural Language Sentence]
{sentence}
[The End of the Natural Language Sentence]"""