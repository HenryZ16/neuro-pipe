import json
import os


class JSONInput:
    file_path: str = None
    parameters: dict = None

    def validate_format(self) -> bool:
        pass

    def parse_content(self) -> dict:
        pass
