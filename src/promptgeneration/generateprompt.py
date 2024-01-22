import os
from dotenv import load_dotenv
from langchain import PromptTemplate
from openai import OpenAI

class ChatBot:
    def __init__(self, client: OpenAI):
        self.client = client
    
    def file_reader(self, path):
        """
        Reads content from a file and returns it.

        Args:
            path (str): The path to the file.

        Returns:
            str: The content of the file.
        """
        fname = os.path.join(path)
        with open(fname, 'r') as f:
            system_message = f.read()
        return system_message
    
    def get_completion(
        self,
        messages,
        model='gpt-4-1106-preview',
        max_tokens=1000,
        temperature=0,
        stop=None,
        seed=123,
        tools=None,
        logprobs=None,
        top_logprobs=None,
    ):
        """
        Sends a request to OpenAI's chat API to get a completion.

        Args:
            messages (list): List of message objects representing the conversation.
            model (str): The model to use for the completion.
            max_tokens (int): The maximum number of tokens in the completion.
            temperature (float): Controls randomness in the response.
            stop (str): Text to stop generation at.
            seed (int): Seed for reproducibility.
            tools (list): List of tool names to use for the completion.
            logprobs (int): Include log probabilities in the response.
            top_logprobs (int): Number of logprobs to return.

        Returns:
            dict: The completion response from OpenAI.
        """
        params = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stop": stop,
            "seed": seed,
            "logprobs": logprobs,
            "top_logprobs": top_logprobs,
        }
        if tools:
            params["tools"] = tools

        completion = self.client.chat.completions.create(**params)
        return completion

    def generate_prompt(self, context, num_test_output):
        """
        Generates a prompt for the chatbot using a predefined template.

        Args:
            context (str): The context to include in the prompt.
            num_test_output (str): The number of test outputs to include in the prompt.

        Returns:
            str: The generated prompt.
        """
        autoprompt = self.file_reader(path='./src/prompts/automatic-prompt-generation-prompt.txt')
        sent = autoprompt.replace("{context}", context).replace("{num_test_output}", num_test_output)
        res = self.get_completion(
                    [
                        {"role": "user", "content": sent},
                    ],
                    logprobs=True,
                    top_logprobs=1,
                )

        return res.choices[0].message.content
