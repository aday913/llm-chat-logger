import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


class GPT_Model:
    def __init__(self, model: str, api_key: str):
        """
        Initialize the model

        :param model: the model to use
        :param api_key: the api key to use
        """
        self.openai = OpenAI(api_key=api_key)
        self.model = model

        self.message_history = []

    def generate_text(self, prompt: str) -> str | None:
        """
        Generate text based on a prompt

        :param prompt: the prompt to generate text from

        :return: the generated text
        """
        completion = self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content

    def converse(self, messages: list) -> str | None:
        """
        Converse with the model in a conversation-like pattern

        :param messages: list of messages to converse with the model

        :return: the model's response
        """
        completion = self.openai.chat.completions.create(
            model=self.model, messages=messages
        )
        self.message_history.append(
            {"role": "assistant", "content": completion.choices[0].message.content}
        )
        return completion.choices[0].message.content


if __name__ == "__main__":

    # load .env file
    load_dotenv()

    # get api key
    API_KEY: str = os.getenv("OPENAI_API_KEY")

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", default="gpt-4o")
    args = parser.parse_args()

    # initialize model
    gpt = GPT_Model(model=args.model, api_key=API_KEY)

    # generate try:
    prompt = input("Enter a prompt: ")

    print(gpt.generate_text(prompt))
