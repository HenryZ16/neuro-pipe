import os


class MatlabInterface:
    matlab_path: str = None

    def execute_script(self, script: str) -> dict:
        pass

    def send_to_workspace(self, data: dict) -> None:
        pass

    # vars is a List
    def get_from_workspace(self, vars) -> dict:
        pass
