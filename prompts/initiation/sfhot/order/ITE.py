base_prompt = """[Structured Data Experssion]
{expression}

[The Start of the Natural Language Sentence]
{sentence}
[The End of the Natural Language Sentence]

[Instruction]
Please act as an impartial judge and evaluate the quality of a natural language sentence generated according to a structured data expression displayed above on its {aspect}. Begin your evaluation by providing a short explanation. After providing your explanation, you must rate the sentence on a scale of {min} to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]".

Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the sentence. {criteria}
2. Be as objective as possible."""