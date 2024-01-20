import os
import numpy as np
from openai import OpenAI

class Evaluation:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def get_completion(
        self,
        messages: list[dict[str, str]],
        model: str = 'gpt-3.5-turbo-1106',
        max_tokens=1000,
        temperature=0,
        stop=None,
        seed=123,
        tools=None,
        logprobs=None,
        top_logprobs=None,
    ) -> str:
        """Return the completion of the prompt."""
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
    
    def file_reader(self, path):
        fname = os.path.join(path)
        with open(fname, 'r') as f:
            system_message = f.read()
        return system_message

    def evaluate(self, prompt: str, user_message: str, context: str, use_test_data: bool = False) -> str:
        """Return the classification of the hallucination."""
        API_RESPONSE = self.get_completion(
            [
                {
                    "role": "system",
                    "content": prompt.replace("{Context}", context).replace("{Question}", user_message)
                }
            ],
            model='gpt-3.5-turbo-1106',
            logprobs=True,
            top_logprobs=1,
        )

        system_msg = str(API_RESPONSE.choices[0].message.content)

        for i, logprob in enumerate(API_RESPONSE.choices[0].logprobs.content[0].top_logprobs, start=1):
            output = f'\nhas_sufficient_context_for_answer: {system_msg}, \nlogprobs: {logprob.logprob}, \naccuracy: {np.round(np.exp(logprob.logprob)*100,2)}%\n'
            print(output)
            if system_msg == 'true' and np.round(np.exp(logprob.logprob)*100,2) >= 95.00:
                classification = 'true'
            elif system_msg == 'false' and np.round(np.exp(logprob.logprob)*100,2) >= 95.00:
                classification = 'false'
            else:
                classification = 'false'
        return classification
    
    def main(self, user_message: str, context: str, use_test_data: bool = False) -> str:
        """Return the classification of the hallucination."""
        prompt_message = self.file_reader('src/prompts/generic-evaluation-prompt.txt')
        ans = self.evaluate(prompt=prompt_message, user_message=user_message, context=context)
        return ans