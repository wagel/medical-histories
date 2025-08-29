from mh_agents.agent_base import AgenticBase
import logging


class ExtractInfoAgent(AgenticBase):
    def __init__(self, model: str, logger: logging.Logger = None):
        super().__init__(model, logger)

    def instructions(self):
        return """
        You are a helpful assistant that extracts information from a medical history.
        """

    def run(self):
        pass