import requests


class LLMAdapter:
    """
    LLMAdapter suggests parameter optimization for all modules in the pipeline.
    """

    config: dict = None

    def preprocess_input(self, json_input: dict) -> dict:
        pass

    def generate_matlab_code(self, params: dict) -> str:
        pass

    def handle_errors(self, error: Exception) -> str:
        pass

    # images is a List
    def analyze_image_quality(self, images) -> dict:
        pass

    def suggest_alignment_parameters(self, metadata: dict) -> dict:
        pass
