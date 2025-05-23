TEI = """{instruction}{reference_1}{dialectic}{cot}

{rule}{autocot}
{example}
[Article]
{document}
{metrics}
{reference_2}
[The Start of the Summary]
{summary}
[The End of the Summary]"""


TIE = """{instruction}{reference_1}{dialectic}{cot}

{example}
[Article]
{document}
{metrics}
{reference_2}
[The Start of the Summary]
{summary}
[The End of the Summary]

{rule}{autocot}"""


ITE = """{example}
[Article]
{document}
{metrics}
{reference_2}
[The Start of the Summary]
{summary}
[The End of the Summary]

{instruction}{reference_1}{dialectic}{cot}

{rule}{autocot}"""


IET = """{example}
[Article]
{document}
{metrics}
{reference_2}
[The Start of the Summary]
{summary}
[The End of the Summary]

{rule}{autocot}
{instruction}{reference_1}{dialectic}{cot}"""


EIT = """{rule}{autocot}
{example}
[Article]
{document}
{metrics}
{reference_2}
[The Start of the Summary]
{summary}
[The End of the Summary]

{instruction}{reference_1}{dialectic}{cot}"""


ETI = """{rule}{autocot}
{instruction}{reference_1}{dialectic}{cot}

{example}
[Article]
{document}
{metrics}
{reference_2}
[The Start of the Summary]
{summary}
[The End of the Summary]"""


instruction_1 = """[Instruction]
Please act as an impartial judge and evaluate the quality of the summary to the news article displayed below on its {aspect}. """


instruction_2 = """[Instruction]
Please act as an impartial judge and evaluate the quality of the summary to the news article displayed above on its {aspect}."""


rule_1 = """Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the summary. {criteria}
2. Be as objective as possible.
"""


rule_2 = """Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the summary. 
2. Be as objective as possible.
"""


metrics_prompt = """
[Questions about Summary]
Here are some questions about the summary. You can do the evaluation based on thinking about all the questions.
{metrics}
"""


example_prompt = """
Here are some examples and their corresponding ratings:
{example}

Following these examples, evaluate the quality of the summary to the news article displayed below on its {aspect}:"""


prefix_cot = """Begin your evaluation by providing a short explanation. After providing your explanation, you must rate the summary on a scale of {min} to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]"."""

suffix_cot = """You must rate the summary on a scale of {min} to {max} first by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]". And then provide your explanation."""

cot_free = """You must directly output your rating of the summary on a scale of {min} to {max} without any explanation by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]". """


reference_1 = """You will be given the news article, the summary and a high-quality reference summary."""


reference_2 = """
[The Start of Reference Summary]
{reference}
[The End of Reference Summary]
"""


dialectic = """Please generate your own summary for the news article first and take into account your own summary to evaluate the quality of the given summary."""


autocot_prompt = """
Evaluation Steps:
{autocot}
"""
