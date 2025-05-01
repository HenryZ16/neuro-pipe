from LLMAdapter import LLMAdapter
import matlab.engine
import os


class LLMEnhancedAligner:
    llm: LLMAdapter = None
    matlab_eng: matlab.engine.MatlabEngine = None

    def __init__(self, script_paths: list[str]):
        self.matlab_eng = matlab.engine.start_matlab()
        for script_path in script_paths:
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"Script path {script_path} does not exist.")
            self.matlab_eng.addpath(script_path)

    def calibrate_images(self, input: dict) -> dict:
        pass

    def evaluate_alignment(self, results: dict) -> dict:
        pass

    def optimize_parameters(self) -> dict:
        pass
