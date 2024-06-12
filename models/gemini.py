import argparse
import os

from dotenv import load_dotenv
import google.generativeai as genai


class Gemini_Model:
    def __init__(self, model: str, api_key: str):
        genai.configure(api_key=api_key)
        self.gemini = genai.GenerativeModel(model)

    def generate_text(self, prompt):
        completion = self.gemini.generate_content(prompt)
        return completion.text


if __name__ == "__main__":

    # load .env file
    load_dotenv()

    # get api key
    API_KEY: str = os.getenv("GEMINI_API_KEY")

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", default="gemini-1.5-pro")
    args = parser.parse_args()

    # initialize model
    gpt = Gemini_Model(model=args.model, api_key=API_KEY)

    # generate try:
    prompt = input("Enter a prompt: ")

    print(gpt.generate_text(prompt))
