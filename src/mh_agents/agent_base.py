import os
from openai import OpenAI
import logging
from dotenv import load_dotenv


class AgenticBase:
    def __init__(self, model: str, logger: logging.Logger = None):
        self.model = model
        try:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception:
            load_dotenv('../.env')
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            raise e

        if logger is None:
            self.logger = setup_logger(__name__)
        else:
            self.logger = logger

    def run(self):
        raise NotImplementedError("Subclasses must implement this method")


def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
