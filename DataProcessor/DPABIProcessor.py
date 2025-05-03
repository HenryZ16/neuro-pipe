from LLMAgent import LLMEnhancedAligner
import os


class DPABIProcessor:
    """
    `config: dict` is from DPABI_V9.0_250415/DPARSF/DPARSF_run.m
    """

    aligner: LLMEnhancedAligner = None
    working_dir: str = "./sub-02CB"
    config: dict = {
        "DPARSFVersion": None,
        "WorkingDir": None,
        "DataProcessDir": None,
        "SubjectID": None,
        "TimePoints": None,
        "TR": None,
        "IsNeedConvertFunDCM2IMG": None,
        "IsRemoveFirstTimePoints": None,
        "RemoveFirstTimePoints": None,
        "IsSliceTiming": None,
        "SliceTiming": {
            "SliceNumber": None,
            "TR": None,
            "TA": None,
            "SliceOrder": None,
            "ReferenceSlice": None,
        },
        "IsRealign": None,
        "IsNormalize": None,
        "IsNeedConvertT1DCM2IMG": None,
        "Normalize": {
            "BoundingBox": None,
            "VoxSize": None,
            "AffineRegularisationInSegmentation": None,
        },
        "IsSmooth": None,
        "Smooth": {"FWHM": None},
        "IsDetrend": None,
        "IsCovremove": None,
        "Covremove": {
            "PolynomialTrend": None,
            "HeadMotion": None,
            "WholeBrain": None,
            "CSF": None,
            "WhiteMatter": None,
            "OtherCovariatesROI": None,
        },
        "MaskFile": None,
        "IsCalALFF": None,
        "CalALFF": {"AHighPass_LowCutoff": None, "ALowPass_HighCutoff": None},
        "IsFilter": None,
        "Filter": {
            "Timing": "AfterNormalize",
            "ALowPass_HighCutoff": None,
            "AHighPass_LowCutoff": None,
            "AAddMeanBack": None,
        },
        "IsCalReHo": None,
        "CalReHo": {"ClusterNVoxel": None, "smReHo": None},
        "IsCalFC": None,
        "IsExtractROISignals": None,
        "CalFC": {"IsMultipleLabel": None, "ROIDef": None},
        "StartingDirName": None,
    }

    def preprocess_data(self, input: dict) -> dict:
        self.config["DPARSFVersion"] = "NOUSE"
        self.config["WorkingDir"] = os.path.abspath(self.working_dir)
        pass

    def generate_report(self) -> str:
        pass
