TEI = """{instruction}{reference_1}{dialectic}{cot}

{rule}{autocot}
{example}
[Structured Data Experssion]
{expression}
{metrics}
{reference_2}
[The Start of the Natural Language Sentence]
{sentence}
[The End of the Natural Language Sentence]"""


TIE = """{instruction}{reference_1}{dialectic}{cot}

{example}
[Structured Data Experssion]
{expression}
{metrics}
{reference_2}
[The Start of the Natural Language Sentence]
{sentence}
[The End of the Natural Language Sentence]

{rule}{autocot}"""


ITE = """{example}
[Structured Data Experssion]
{expression}
{metrics}
{reference_2}
[The Start of the Natural Language Sentence]
{sentence}
[The End of the Natural Language Sentence]

{instruction}{reference_1}{dialectic}{cot}

{rule}{autocot}"""


IET = """{example}
[Structured Data Experssion]
{expression}
{metrics}
{reference_2}
[The Start of the Natural Language Sentence]
{sentence}
[The End of the Natural Language Sentence]

{rule}{autocot}
{instruction}{reference_1}{dialectic}{cot}"""


EIT = """{rule}{autocot}
{example}
[Structured Data Experssion]
{expression}
{metrics}
{reference_2}
[The Start of the Natural Language Sentence]
{sentence}
[The End of the Natural Language Sentence]

{instruction}{reference_1}{dialectic}{cot}"""


ETI = """{rule}{autocot}
{instruction}{reference_1}{dialectic}{cot}

{example}
[Structured Data Experssion]
{expression}
{metrics}
{reference_2}
[The Start of the Natural Language Sentence]
{sentence}
[The End of the Natural Language Sentence]"""


instruction_1 = """[Instruction]
Please act as an impartial judge and evaluate the quality of a natural language sentence generated according to a structured data expression displayed below on its {aspect}. """


instruction_2 = """[Instruction]
Please act as an impartial judge and evaluate the quality of a natural language sentence generated according to a structured data expression displayed above on its {aspect}."""


rule_1 = """Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the sentence. {criteria}
2. Be as objective as possible.
"""


rule_2 = """Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the sentence. 
2. Be as objective as possible.
"""


metrics_prompt = """
[Questions about Sentence]
Here are some questions about the sentence. You can do the evaluation based on thinking about all the questions.
{metrics}
"""


example_prompt = """
Here are some examples and their corresponding ratings:
{example}

Following these examples, evaluate the quality of a natural language sentence generated according to a structured data expression displayed below on its {aspect}:"""


prefix_cot = """Begin your evaluation by providing a short explanation. After providing your explanation, you must rate the sentence on a scale of {min} to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]"."""

suffix_cot = """You must rate the sentence on a scale of {min} to {max} first by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]". And then provide your explanation."""

cot_free = """You must directly output your rating of the sentence on a scale of {min} to {max} without any explanation by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]". """


reference_1 = """You will be given the structured data expression, the sentence and a high-quality reference sentence."""


reference_2 = """
[The Start of Reference Sentence]
{reference}
[The End of Reference Sentence]
"""


dialectic = """Please generate your own sentence according to the given structured data expression first and take into account your own sentence to evaluate the quality of the given sentence."""


autocot_prompt = """
Evaluation Steps:
{autocot}
"""
