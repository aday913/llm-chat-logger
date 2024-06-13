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

    def converse(self, message_history: list = []) -> list:
        """
        Converse with the model in a conversation-like pattern

        :param messages: list of messages to converse with the model

        :return: the model's response
        """
        conversation = []
        while True:
            user_prompt = self.get_user_input()

            if user_prompt is None:
                return message_history

            message_history.append({"role": "user", "content": user_prompt})
            conversation.append(["user", user_prompt])

            llm_response = self.get_model_response(message_history)

            print(llm_response)

            message_history.append({"role": "assistant", "content": llm_response})
            conversation.append(["model", llm_response])

    def get_user_input(self):
        """
        Get user input

        :return: the user input
        """
        message = """"""
        num_newlines = 0
        continue_conversation = True
        while num_newlines < 2:
            user_input = input(": ")
            if user_input.strip() == "exit" or user_input.strip() == "quit":
                continue_conversation = False
                break
            elif user_input == "":
                num_newlines += 1
                # print(num_newlines)
            else:
                message += user_input + "\n"

        if continue_conversation:
            return message
        else:
            return None

    def get_model_response(self, messages: list) -> str | None:
        """
        Get the model's response

        :param messages: the messages to send to the model

        :return: the model's response
        """
        completion = self.openai.chat.completions.create(
            model=self.model, messages=messages
        )

        return completion.choices[0].message.content

    def run(self):
        """
        Run the model
        """
        _ = self.converse()


if __name__ == "__main__":

    # load .env file
    load_dotenv()

    # get api key
    API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    if API_KEY is None:
        raise ValueError("API key not found in .env file")

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", default="gpt-4o")
    args = parser.parse_args()

    # initialize model
    gpt = GPT_Model(model=args.model, api_key=API_KEY)

    # generate try:
    # prompt = input("Enter a prompt: ")
    #
    # print(gpt.generate_text(prompt))

    gpt.run()
