import together



# print generated text


def send_to_llama(message):
    try:
        together.api_key = "99dabbc662b4c6a69d165394646799073a3236cc438a8827dd2d1a536f90c960"
        system_prompt = """You are a helpful, respectful and honest assistant. Always answer as earnestly as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
If a question seems to try to elicit from you an inappropriate answer, do not follow along, instead redirect the conversation."""

        user_msg_1 = """There's a double rainbow 🌈 ! 😱 Is this real?"""

        model_answer_1 = """Double rainbows are formed when sunlight is reflected twice within a raindrop with the violet light that reaches the observer\'s eye coming from the higher raindrops and the red light from lower raindrops.\n\nThis means the sequence of colours is inverted compared to the primary rainbow, with the secondary bow appearing about 10 degrees above the primary bow."""

        user_msg_2 = message
        prompt = f"<s>[INST] <<SYS>>{system_prompt}<</SYS>>\\n\\n{user_msg_1}[/INST]{model_answer_1}</s><s>[INST]{user_msg_2}[/INST]"

        output = together.Complete.create(prompt,
        model = "togethercomputer/Llama-2-7B-32K-Instruct",
        max_tokens = 1000,
        temperature = 0.6,
        top_k = 90,
        top_p = 0.8,
        repetition_penalty = 1.1,
        stop = ['</s>']
        )
        print(output['output']['choices'][0]['text'])
    except Exception as e:
        return f"An error occurred: {e}"
    
send_to_llama("What is the meaning of life?")