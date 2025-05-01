import json
import os


class ResultExporter:
    def export_json(self, results: dict) -> str:
        pass

    def generate_qc_report(self):
        """
        Generate a PDF
        """
        pass

    # data is an array
    def save_nifti(self, data) -> bool:
        pass
