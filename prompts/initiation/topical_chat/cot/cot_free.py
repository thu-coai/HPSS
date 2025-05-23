base_prompt = """[Instruction]
Please act as an impartial judge and evaluate the quality of the response for the next turn in the conversation displayed below on its {aspect}. The response concerns an interesting fact, which will be provided as well. You must directly output your rating of the response on a scale of {min} to {max} without any explanation by strictly following this format: "[[rating]]", for example: "Rating: [[{max}]]".

Here are some rules of the evaluation:
1. Your evaluation should consider the {aspect} of the response. {criteria}
2. Be as objective as possible.

[Conversation History]
{context}

[Corresponding Fact]
{fact}

[The Start of the Response]
{response}
[The End of the Response]"""