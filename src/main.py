from openai import OpenAI
import json
import dotenv
import os
import logging

from utils import (
    upload_file_to_openai,
    generate_pdf_input,
    delete_file_from_openai,
    fetch_lexicon,
    fetch_prompt,
    setup_logger
)


def default_params():
    url = "https://admin.waggel.co.uk/claim/attachment?id=clm-f1d461ce-4e6c-433a-ab93-c7eba7b9c49c&attachmentId=5062418c-c7d2-4493-8a05-3a39485318c4"
    filename = "file_5062418c-c7d2-4493-8a05-3a39485318c4.pdf"
    claim_id = "clm-f1d461ce-4e6c-433a-ab93-c7eba7b9c49c"
    MEDICAL_HISTORY_PATH = "../data/file_5062418c-c7d2-4493-8a05-3a39485318c4.pdf"
    POLICY_WORDING_PATH = "../data/GeneralPolicyWording-V18.pdf"
    return (url, filename, claim_id, MEDICAL_HISTORY_PATH, POLICY_WORDING_PATH)


def perpetual_chat_loop(client: OpenAI, conversation: list, logger: logging.Logger):
    while True:
        user_input = input("\nKlaimzy: Anything else I can assist you with? Press 'q' to quit.\n> ")
        if user_input == 'q':
            break
        else:
            conversation.append({"role": "user", "content": user_input})
            logger.info('> Generating response...')
            response = client.responses.create(
                model="gpt-4.1",
                input=conversation
            )
            print('> Klaimzy:')
            print(response.output[0].content[0].text)


if __name__ == "__main__":
    url, filename, claim_id, MEDICAL_HISTORY_PATH, POLICY_WORDING_PATH = default_params()
    # logger = setup_logger(__name__, logging.WARNING)
    logger = setup_logger(__name__, logging.DEBUG)
    welcome_message = """

    ⚡️⚡️⚡️⚡️ Hi Zach! I'm klaimzy! Here to help you process claims FAST! ⚡️⚡️⚡️⚡️

        ██╗  ██╗██╗      █████╗ ██╗███╗   ███╗███████╗██╗   ██╗
        ██║ ██╔╝██║     ██╔══██╗██║████╗ ████║╚══███╔╝╚██╗ ██╔╝
        █████╔╝ ██║     ███████║██║██╔████╔██║  ███╔╝  ╚████╔╝ 
        ██╔═██╗ ██║     ██╔══██║██║██║╚██╔╝██║ ███╔╝    ╚██╔╝  
        ██║  ██╗███████╗██║  ██║██║██║ ╚═╝ ██║███████╗   ██║   
        ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝   ╚═╝   

        ‼️⚠️ WARNING: I'm make mistakes 😵‍💫😵! Fact check wherever unsure! ⚠️⚠️

        Lets get started!
        I'm currently analyzing the medical history to provide you with a summary...

    """
    print(welcome_message)
    input("Press Enter to continue...")
    print("🔄 Starting analysis...")

    dotenv.load_dotenv('../.env')
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    logger.info('> Uploading medical history to OpenAI...')
    medical_history_file = upload_file_to_openai(client, MEDICAL_HISTORY_PATH)
    pdf_input = generate_pdf_input(client, medical_history_file.id, prompt="Attached is the medical history:")

    logger.info('> Upload policy wording to OpenAI...')
    policy_wording_file = upload_file_to_openai(client, POLICY_WORDING_PATH)
    policy_wording_input = generate_pdf_input(client, policy_wording_file.id, prompt="Attached is the official policy wording:")

    # Small esoteric lexicon
    logger.debug('> Fetching lexicon...')
    lexicon = fetch_lexicon()

    # The text instruction
    logger.debug('> Fetching prompt...')
    prompt = fetch_prompt()

    logger.debug('> Init conversation...')
    conversation = [
            {"role": "user", "content": prompt},   # 1. Text instruction
            {"role": "system", "content": f"Lexicon: {lexicon}"},   # 2. Lexicon as structured JSON
            pdf_input,   # 3. PDF file
            policy_wording_input   # 4. PDF file
        ]

    # init prompt with:
    # - prompt
    # - pdf
    # - lexicon
    response = client.responses.create(
        model="gpt-4.1",
        input=conversation
    )

    print('> Klaimzy:')
    print(response.output[0].content[0].text)

    perpetual_chat_loop(client, conversation, logger)

    logger.info('> Deleting medical history & policy wording from OpenAI...')
    delete_file_from_openai(client, medical_history_file.id)
    delete_file_from_openai(client, policy_wording_file.id)
