import argparse
import os

from dotenv import load_dotenv
import google.generativeai as genai


class Gemini_Model:
    def __init__(self, model: str, api_key: str):
        """
        Initialize the model

        :param model: the model to use
        :param api_key: the api key to use
        """
        genai.configure(api_key=api_key)
        self.gemini = genai.GenerativeModel(model)

    def generate_text(self, prompt: str) -> str | None:
        """
        Generate text based on a prompt

        :param prompt: the prompt to generate text from

        :return: the generated text
        """
        completion = self.gemini.generate_content(prompt)
        return completion.text

    def format_previous_conversation(self, conversation: list) -> list:
        """
        Format a previous conversation for the model

        :param conversation: the conversation to format

        :return: the formatted conversation
        """
        formatted_conversation = []
        for talker, message in conversation:
            if talker == "user":
                formatted_conversation.append({"role": "user", "parts": [message]})
            elif talker == "model":
                formatted_conversation.append({"role": "assistant", "parts": [message]})
            else:
                raise ValueError(f"Invalid talker: {talker}")
        return formatted_conversation

    def converse(
        self, prompt: str = "", message_history: list = [], conversation: list = []
    ) -> list:
        """
        Converse with the model in a conversation-like pattern

        :param messages: list of messages to converse with the model

        :return: the user/model conversation
        """
        conv_length = 0
        while True:
            user_prompt = self.get_user_input()

            if user_prompt is None:
                return conversation
            if conv_length == 0 and message_history == []:
                user_prompt = prompt + "\n" + user_prompt

            message_history.append({"role": "user", "parts": [user_prompt]})
            conversation.append(["user", user_prompt])

            llm_response = self.get_model_response(message_history)

            print("-" * 50)

            print(llm_response)

            print("-" * 50)

            message_history.append({"role": "model", "parts": [llm_response]})
            conversation.append(["model", llm_response])
            conv_length += 1

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
        completion = self.gemini.generate_content(messages)

        return completion.text


if __name__ == "__main__":

    # load .env file
    load_dotenv()

    # get api key
    API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    if API_KEY is None:
        raise Exception("API key not found")

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", default="gemini-1.5-pro")
    args = parser.parse_args()

    # initialize model
    gemini = Gemini_Model(model=args.model, api_key=API_KEY)

    # generate try:
    # prompt = input("Enter a prompt: ")
    #
    # print(gpt.generate_text(prompt))

    gemini.converse()
