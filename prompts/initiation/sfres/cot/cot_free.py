base_prompt = """[Instruction]
Please act as an impartial judge and evaluate the quality of a natural language sentence generated according to a structured data expression displayed below on its {aspect}. You must directly output your rating of the sentence on a scale of {min} to {max} without any explanation by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]".

Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the sentence. {criteria}
2. Be as objective as possible.

[Structured Data Experssion]
{expression}

[The Start of the Natural Language Sentence]
{sentence}
[The End of the Natural Language Sentence]"""