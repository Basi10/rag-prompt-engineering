import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def get_completion(
        self,
        messages,
        model='gpt-3.5-turbo-1106',
        max_tokens=500,
        temperature=0,
        stop=None,
        seed=123,
        tools=None,
        logprobs=None,
        top_logprobs=None,
    ):
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

    def generate_test_data(self, prompt, context, num_test_output):
        API_RESPONSE = self.get_completion(
            [
                {"role": "user", "content": prompt.replace("{context}", context).replace("{num_test_output}", num_test_output)}
            ],
            logprobs=True,
            top_logprobs=1,
        )

        system_msg = API_RESPONSE.choices[0].message.content
        return system_msg

    def main(self, text_values, num_test_output):
        prompt_message = self.file_reader("./src/prompts/data-generation-prompt.txt")
        ans = self.generate_test_data(prompt=prompt_message, context="\n".join(text_values), num_test_output=num_test_output)
        return ans


