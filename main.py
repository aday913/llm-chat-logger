import argparse
import datetime
import os

from dotenv import load_dotenv
from models.gemini import Gemini_Model
from models.gpt import GPT_Model

LLM_MODELS = [
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.0-pro",
]


def main(
    openai_key: str | None,
    gemini_key: str | None,
    model: str,
    prompt: str,
    output: str,
    continue_file: str,
):
    if model == "gpt":
        model = "gpt-4o"
    elif model == "gemini":
        model = "gemini-1.5-pro"

    if model not in LLM_MODELS:
        raise ValueError(f"Model '{model}' not found")

    if model.startswith("gpt") and openai_key:
        llm = GPT_Model(model=model, api_key=openai_key)
    elif model.startswith("gemini") and gemini_key:
        llm = Gemini_Model(model=model, api_key=gemini_key)
    else:
        raise ValueError("API key not found")

    llm.run()


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Communicate with an LLM model and save the conversation to a markdown file"
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="The model to use",
        required=False,
        default="gpt-4o",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        help="The prompt name to start the conversation",
        required=False,
        default="default_ai",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output file name",
        required=False,
        default=f"{datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%I%M%S')}.md",
    )
    parser.add_argument(
        "-c",
        "--continue-file",
        type=str,
        help="Previous output file name to continue the conversation",
        required=False,
        default="",
    )
    args = parser.parse_args()

    main(
        openai_key=os.getenv("OPENAI_API_KEY"),
        gemini_key=os.getenv("GEMINI_API_KEY"),
        model=args.model.strip(),
        prompt=args.prompt.strip(),
        output=args.output.strip(),
        continue_file=args.continue_file.strip(),
    )
