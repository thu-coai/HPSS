TEI = """{instruction}{reference_1}{dialectic}{cot}

{rule}{autocot}
{example}
[Conversation History]
{context}
{metrics}
[Corresponding Fact]
{fact}
{reference_2}
[The Start of the Response]
{response}
[The End of the Response]"""


TIE = """{instruction}{reference_1}{dialectic}{cot}

{example}
[Conversation History]
{context}
{metrics}
[Corresponding Fact]
{fact}
{reference_2}
[The Start of the Response]
{response}
[The End of the Response]

{rule}{autocot}"""


ITE = """{example}
[Conversation History]
{context}
{metrics}
[Corresponding Fact]
{fact}
{reference_2}
[The Start of the Response]
{response}
[The End of the Response]

{instruction}{reference_1}{dialectic}{cot}

{rule}{autocot}"""


IET = """{example}
[Conversation History]
{context}
{metrics}
[Corresponding Fact]
{fact}
{reference_2}
[The Start of the Response]
{response}
[The End of the Response]

{rule}{autocot}
{instruction}{reference_1}{dialectic}{cot}"""


EIT = """{rule}{autocot}
{example}
[Conversation History]
{context}
{metrics}
[Corresponding Fact]
{fact}
{reference_2}
[The Start of the Response]
{response}
[The End of the Response]

{instruction}{reference_1}{dialectic}{cot}"""


ETI = """{rule}{autocot}
{instruction}{reference_1}{dialectic}{cot}

{example}
[Conversation History]
{context}
{metrics}
[Corresponding Fact]
{fact}
{reference_2}
[The Start of the Response]
{response}
[The End of the Response]"""


instruction_1 = """[Instruction]
Please act as an impartial judge and evaluate the quality of the response for the next turn in the conversation displayed below on its {aspect}. The response concerns an interesting fact, which will be provided as well. """


instruction_2 = """[Instruction]
Please act as an impartial judge and evaluate the quality of the response for the next turn in the conversation displayed above on its {aspect}. The response concerns an interesting fact, which will be provided as well. """


rule_1 = """Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the response. {criteria}
2. Be as objective as possible.
"""


rule_2 = """Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the response. 
2. Be as objective as possible.
"""


metrics_prompt = """
[Questions about Response]
Here are some questions about the response. You can do the evaluation based on thinking about all the questions.
{metrics}
"""


example_prompt = """
Here are some examples and their corresponding ratings:
{example}

Following these examples, evaluate the quality of the response for the next turn in the conversation displayed below on its {aspect}:"""


prefix_cot = """Begin your evaluation by providing a short explanation. After providing your explanation, you must rate the response on a scale of {min} to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]". """


suffix_cot = """You must rate the response on a scale of {min} to {max} first by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]". And then provide your explanation. """

cot_free = """You must directly output your rating of the response on a scale of {min} to {max} without any explanation by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]". """


reference_1 = """You will also be given a high-quality reference response with the conversation. """


dialectic = """Please generate your own response for the next turn in the conversation first and take into account your own response to evaluate the quality of the given response."""


reference_2 = """
[The Start of Reference Response]
{reference}
[The End of Reference Response]
"""

autocot_prompt = """
Evaluation Steps:
{autocot}
"""
