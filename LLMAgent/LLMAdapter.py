import requests
from ollama import chat
from ollama import ChatResponse
import re


class LLMAdapter:
    """
    LLMAdapter suggests parameter optimization for all modules in the pipeline.
    """

    api_key: str = None
    api_url: str = "https://api.deepseek.com"
    think_pattern: str = r"<think>[\s\S]*</think>"
    config_interact: dict = {
        "model": "deepseek-r1:14b",
        "messages": {
            "role": "system",
            "content": """According to the input, your reply must ONLY contain the path of data that will be processed, without any explanation. It must be a Windows or UNIX-like path. If there's no data path in the input, set it as None.""",
        },
    }
    config: dict = {
        "model": "deepseek-r1:14b",
        "messages": {
            "role": "system",
            "content": "According to the input json file, suggest the parameters for the Data Processing Assistant for Resting-State fMRI (DPARSF). The json file is shown as follows:",
        },
    }

    """Useful functions"""

    def get_key(self, key_path: str):
        """
        Get the API key from the file
        """
        try:
            with open(key_path, "r") as file:
                key = file.read().strip()
        except FileNotFoundError:
            print(f"Error: The file {key_path} does not exist.")
            key = None
        except Exception as e:
            print(f"Error: {e}")
            key = None
        if key is None:
            print("Error: The API key is not found.")
            raise ValueError("API key is not found.")

    def remove_think(self, text: str) -> str:
        """
        Remove the thinking process from the text.
        """
        context = re.sub(self.think_pattern, "", text)
        return context.strip()

    """Useful functions"""

    def preprocess_input(self, json_input: dict) -> dict:
        pass

    def handle_errors(self, error: Exception) -> str:
        pass

    # images is a List
    def analyze_image_quality(self, images) -> dict:
        pass

    def suggest_alignment_parameters(self, metadata: dict) -> dict:
        pass
