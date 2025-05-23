opro_prompt = """## Instruction:
Your task is to decide the selection strategy of different parts of a prompt to enhance the performance of LLM using this prompt. 
The selection range of each part is as follows:

- Part 0: [0,1,2,3,4]
- Part 1: [0,1,2]
- Part 2: [0,1,2]
- Part 3: [0,1]
- Part 4: [0,1]
- Part 5: [0,1,2,3]
- Part 6: [0,1,2]
- Part 7: [0,1,2,3,4,5]

The previous selection strategy and performance are as follows:

{history}

Your goal is to generate a new selection strategy of these parts to improve the performance of LLM using this prompt. The selection strategy you generate should not be identical to any previous ones. You should generate the new selection strategy without any explanation by strictly following this format: "{{"Part 0" : x, "Part 1" : x, ..., "Part 7" : x}}", for example: "{{"Part 0" : 2, "Part 1" : 1, ..., "Part 7" : 0}}". Each part must be selected strictly according to the selection range."""