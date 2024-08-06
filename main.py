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


def save_conversation_to_file(conversation: list, output: str):
    """
    Save the conversation to a markdown file

    :param conversation: the conversation as a list of lists. Each list contains the talker and the try:
        
    :param output: the output file path
    """
    with open(output, "w") as f:
        for talker, message in conversation:
            f.write(f"*{str(talker).capitalize()}*:\n\n")
            f.write(f"{message}\n\n")
            f.write("---\n\n")


def get_prompt_text(prompt: str) -> str:
    """
    Get the text of a prompt file

    :param prompt: the prompt name (without the .md extension)

    :return: the text of the prompt file
    """
    text = """"""
    with open(f"prompts/{prompt}.md", "r") as f:
        for line in f:
            text += line.strip() + "\n"
    return text


def parse_previous_conversation_file(file_path: str) -> list:
    """
    Parse a previous conversation file

    :param file_path: the file path to the previous conversation file

    :return: the conversation as a list of lists. Each list contains the talker and the text
    """
    conversation = []
    full_text = """"""
    with open(file_path, "r") as f:
        for line in f:
            full_text += line.strip() + "\n"

    for message in full_text.split("---\n\n"):
        if message:
            if "*User*:" in message:
                talker = "user"
                text = message.replace("*User*:", "").strip()
            elif "*Model*:" in message:
                talker = "model"
                text = message.replace("*Model*:", "").strip()
            else:
                raise ValueError(f"No talker found in message: {message}")
            conversation.append([talker, text])

    return conversation


def main(
    openai_key: str | None,
    gemini_key: str | None,
    model: str,
    prompt: str,
    output: str,
    continue_file: str | None,
):
    try:
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

        # load prompt
        prompt_text = get_prompt_text(prompt)

        # load previous conversation, if any
        if continue_file:
            previous_conversation = parse_previous_conversation_file(continue_file)
            formatted_previous_conversation = llm.format_previous_conversation(
                previous_conversation
            )
        else:
            previous_conversation = []
            formatted_previous_conversation = []

        conversation = llm.converse(
            prompt=prompt_text,
            message_history=formatted_previous_conversation,
            conversation=previous_conversation,
        )
        # for talker, message in conversation:
        #     print(f"{talker.capitalize()}: {len(message)} characters")

        # save conversation to file
        save_conversation_to_file(conversation, output)
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Exiting...")


if __name__ == "__main__":
    load_dotenv()

    output_path = os.getenv("DEFAULT_DIR")
    if output_path is None:
        raise FileNotFoundError("Output directory not found in .env file")
    if not os.path.exists(output_path):
        raise FileNotFoundError(
            f"Configured output directory '{output_path}' not found"
        )

    parser = argparse.ArgumentParser(
        description="Communicate with an LLM model and save the conversation to a markdown file"
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="The model to use (gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo, gemini-1.5-pro, gemini-1.5-flash, gemini-1.0-pro)",
        required=False,
        default="gpt-4o",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        help="The prompt name to start the conversation (without the .md extension)",
        required=False,
        default="default_ai",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output file name",
        required=False,
        default=f"{output_path}/{datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%I%M%S')}.md",
    )
    parser.add_argument(
        "-c",
        "--continue-file",
        type=str,
        help="Previous output file name to continue the conversation. Will overwrite the output file name.",
        required=False,
        default=None,
    )
    args = parser.parse_args()

    if not os.path.exists(f"prompts/{args.prompt}.md"):
        raise FileNotFoundError(f"Prompt file 'prompts/{args.prompt}.md' not found")
    if args.continue_file and not os.path.exists(args.continue_file):
        raise FileNotFoundError(f"Continue file '{args.continue_file}' not found")
    if args.continue_file:
        args.output = args.continue_file

    main(
        openai_key=os.getenv("OPENAI_API_KEY"),
        gemini_key=os.getenv("GEMINI_API_KEY"),
        model=args.model.strip(),
        prompt=args.prompt.strip(),
        output=args.output.strip(),
        continue_file=args.continue_file,
    )
