TEI = """{instruction}{reference_1}{dialectic}{cot}

{rule}{autocot}
{example}
[Prompt]
{prompt}
{metrics}
{reference_2}
[The Start of the Story]
{story}
[The End of the Story]"""


TIE = """{instruction}{reference_1}{dialectic}{cot}

{example}
[Prompt]
{prompt}
{metrics}
{reference_2}
[The Start of the Story]
{story}
[The End of the Story]

{rule}{autocot}"""


ITE = """{example}
[Prompt]
{prompt}
{metrics}
{reference_2}
[The Start of the Story]
{story}
[The End of the Story]

{instruction}{reference_1}{dialectic}{cot}

{rule}{autocot}"""


IET = """{example}
[Prompt]
{prompt}
{metrics}
{reference_2}
[The Start of the Story]
{story}
[The End of the Story]

{rule}{autocot}
{instruction}{reference_1}{dialectic}{cot}"""


EIT = """{rule}{autocot}
{example}
[Prompt]
{prompt}
{metrics}
{reference_2}
[The Start of the Story]
{story}
[The End of the Story]

{instruction}{reference_1}{dialectic}{cot}"""


ETI = """{rule}{autocot}
{instruction}{reference_1}{dialectic}{cot}

{example}
[Prompt]
{prompt}
{metrics}
{reference_2}
[The Start of the Story]
{story}
[The End of the Story]"""


instruction_1 = """[Instruction]
Please act as an impartial judge and evaluate the quality of the story generated according to a prompt displayed below on its {aspect}. """


instruction_2 = """[Instruction]
Please act as an impartial judge and evaluate the quality of the story generated according to a prompt displayed above on its {aspect}."""


rule_1 = """Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the story. {criteria}
2. Be as objective as possible.
"""


rule_2 = """Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the story. 
2. Be as objective as possible.
"""


metrics_prompt = """
[Questions about Story]
Here are some questions about the story. You can do the evaluation based on thinking about all the questions.
{metrics}
"""


example_prompt = """
Here are some examples and their corresponding ratings:
{example}

Following these examples, evaluate the story generated according to a prompt displayed below on its {aspect}:"""


prefix_cot = """Begin your evaluation by providing a short explanation. After providing your explanation, you must rate the story on a scale of {min} to {max} by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]"."""

suffix_cot = """You must rate the story on a scale of {min} to {max} first by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]". And then provide your explanation."""

cot_free = """You must directly output your rating of the story on a scale of {min} to {max} without any explanation by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]". """


reference_1 = """You will be given the prompt, the generated story and a high-quality reference story."""


reference_2 = """
[The Start of Reference Story]
{reference}
[The End of Reference Story]
"""


dialectic = """Please generate your own story for the given prompt first and take into account your own story to evaluate the quality of the given story."""


autocot_prompt = """
Evaluation Steps:
{autocot}
"""
