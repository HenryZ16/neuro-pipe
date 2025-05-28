# from LLMAgent import LLMEnhancedAligner
import os
import matlab.engine
import sys
from io import StringIO


class DPABIProcessor:
    """
    `config: dict` is from DPABI_V9.0_250415/DPARSF/DPARSF_run.m
    """

    # aligner: LLMEnhancedAligner = None
    working_dir: str = "./sub-02CB"
    config: dict = {
        "DPARSFVersion": None,
        "WorkingDir": None,
        "DataProcessDir": None,
        "SubjectID": {"Sub_01"},
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

    def preprocess_data(self, input: dict):
        eng = matlab.engine.start_matlab()
        Cfg = eng.struct()
        Cfg["DPARSFVersion"] = input["DPARSFVersion"]
        Cfg["WorkingDir"] = input["WorkingDir"]
        Cfg["DataProcessDir"] = input["DataProcessDir"]
        Cfg["SubjectID"] = input["SubjectID"]
        Cfg["TimePoints"] = input["TimePoints"]
        Cfg["TR"] = input["TR"]
        Cfg["IsNeedConvertFunDCM2IMG"] = input["IsNeedConvertFunDCM2IMG"]
        Cfg["IsApplyDownloadedReorientMats"] = input["IsApplyDownloadedReorientMats"]
        Cfg["IsRemoveFirstTimePoints"] = input["IsRemoveFirstTimePoints"]
        Cfg["RemoveFirstTimePoints"] = input["RemoveFirstTimePoints"]

        # 切片时间校正设置
        Cfg["IsSliceTiming"] = input["IsSliceTiming"]
        Cfg["SliceTiming"] = eng.struct()
        Cfg["SliceTiming"]["SliceNumber"] = input["SliceTiming"]["SliceNumber"]
        Cfg["SliceTiming"]["SliceOrder"] = input["SliceTiming"]["SliceOrder"]
        Cfg["SliceTiming"]["ReferenceSlice"] = input["SliceTiming"]["ReferenceSlice"]
        Cfg["SliceTiming"]["TR"] = input["SliceTiming"]["TR"]
        Cfg["SliceTiming"]["TA"] = input["SliceTiming"]["TA"]

        # 头动校正设置
        Cfg["IsRealign"] = input["IsRealign"]
        Cfg["IsCalVoxelSpecificHeadMotion"] = input["IsCalVoxelSpecificHeadMotion"]
        Cfg["IsNeedReorientFunImgInteractively"] = input[
            "IsNeedReorientFunImgInteractively"
        ]

        # T1像处理设置
        Cfg["IsNeedConvertT1DCM2IMG"] = input["IsNeedConvertT1DCM2IMG"]
        Cfg["IsNeedReorientCropT1Img"] = input["IsNeedReorientCropT1Img"]
        Cfg["IsNeedReorientT1ImgInteractively"] = input[
            "IsNeedReorientT1ImgInteractively"
        ]
        Cfg["IsBet"] = input["IsBet"]
        Cfg["IsAutoMask"] = input["IsAutoMask"]
        Cfg["IsNeedT1CoregisterToFun"] = input["IsNeedT1CoregisterToFun"]
        Cfg["IsNeedReorientInteractivelyAfterCoreg"] = input[
            "IsNeedReorientInteractivelyAfterCoreg"
        ]

        # 分割设置
        Cfg["IsSegment"] = input["IsSegment"]
        Cfg["Segment"] = eng.struct()
        Cfg["Segment"]["AffineRegularisationInSegmentation"] = input["Segment"][
            "AffineRegularisationInSegmentation"
        ]
        Cfg["IsDARTEL"] = input["IsDARTEL"]

        # 协变量去除设置
        Cfg["IsCovremove"] = input["IsCovremove"]
        Cfg["Covremove"] = eng.struct()
        Cfg["Covremove"]["Timing"] = input["Covremove"]["Timing"]
        Cfg["Covremove"]["PolynomialTrend"] = input["Covremove"]["PolynomialTrend"]
        Cfg["Covremove"]["HeadMotion"] = input["Covremove"]["HeadMotion"]
        Cfg["Covremove"]["IsHeadMotionScrubbingRegressors"] = input["Covremove"][
            "IsHeadMotionScrubbingRegressors"
        ]
        Cfg["Covremove"]["HeadMotionScrubbingRegressors"] = eng.struct()
        Cfg["Covremove"]["HeadMotionScrubbingRegressors"]["FDType"] = input[
            "Covremove"
        ]["HeadMotionScrubbingRegressors"]["FDType"]
        Cfg["Covremove"]["HeadMotionScrubbingRegressors"]["FDThreshold"] = input[
            "Covremove"
        ]["HeadMotionScrubbingRegressors"]["FDThreshold"]
        Cfg["Covremove"]["HeadMotionScrubbingRegressors"]["PreviousPoints"] = input[
            "Covremove"
        ]["HeadMotionScrubbingRegressors"]["PreviousPoints"]
        Cfg["Covremove"]["HeadMotionScrubbingRegressors"]["LaterPoints"] = input[
            "Covremove"
        ]["HeadMotionScrubbingRegressors"]["LaterPoints"]
        Cfg["Covremove"]["WhiteMatter"] = input["Covremove"]["WhiteMatter"]

        # 白质、脑脊液等设置
        Cfg["Covremove"]["WM"] = eng.struct()
        Cfg["Covremove"]["WM"]["IsRemove"] = input["Covremove"]["WM"]["IsRemove"]
        Cfg["Covremove"]["WM"]["Mask"] = input["Covremove"]["WM"]["Mask"]
        Cfg["Covremove"]["WM"]["MaskThreshold"] = input["Covremove"]["WM"][
            "MaskThreshold"
        ]
        Cfg["Covremove"]["WM"]["Method"] = input["Covremove"]["WM"]["Method"]
        Cfg["Covremove"]["WM"]["CompCorPCNum"] = input["Covremove"]["WM"][
            "CompCorPCNum"
        ]

        Cfg["Covremove"]["CSF"] = eng.struct()
        Cfg["Covremove"]["CSF"]["IsRemove"] = input["Covremove"]["CSF"]["IsRemove"]
        Cfg["Covremove"]["CSF"]["Mask"] = input["Covremove"]["CSF"]["Mask"]
        Cfg["Covremove"]["CSF"]["MaskThreshold"] = input["Covremove"]["CSF"][
            "MaskThreshold"
        ]
        Cfg["Covremove"]["CSF"]["Method"] = input["Covremove"]["CSF"]["Method"]
        Cfg["Covremove"]["CSF"]["CompCorPCNum"] = input["Covremove"]["CSF"][
            "CompCorPCNum"
        ]

        Cfg["Covremove"]["WholeBrain"] = eng.struct()
        Cfg["Covremove"]["WholeBrain"]["IsRemove"] = input["Covremove"]["WholeBrain"][
            "IsRemove"
        ]
        Cfg["Covremove"]["WholeBrain"]["IsBothWithWithoutGSR"] = input["Covremove"][
            "WholeBrain"
        ]["IsBothWithWithoutGSR"]
        Cfg["Covremove"]["WholeBrain"]["Mask"] = input["Covremove"]["WholeBrain"][
            "Mask"
        ]
        Cfg["Covremove"]["WholeBrain"]["Method"] = input["Covremove"]["WholeBrain"][
            "Method"
        ]

        Cfg["Covremove"]["OtherCovariatesROI"] = input["Covremove"][
            "OtherCovariatesROI"
        ]
        Cfg["Covremove"]["IsAddMeanBack"] = input["Covremove"]["IsAddMeanBack"]

        # 滤波设置
        Cfg["IsFilter"] = input["IsFilter"]
        Cfg["Filter"] = eng.struct()
        Cfg["Filter"]["Timing"] = input["Filter"]["Timing"]
        Cfg["Filter"]["ALowPass_HighCutoff"] = input["Filter"]["ALowPass_HighCutoff"]
        Cfg["Filter"]["AHighPass_LowCutoff"] = input["Filter"]["AHighPass_LowCutoff"]
        Cfg["Filter"]["AAddMeanBack"] = input["Filter"]["AAddMeanBack"]

        # 标准化设置
        Cfg["IsNormalize"] = input["IsNormalize"]
        Cfg["Normalize"] = eng.struct()
        Cfg["Normalize"]["Timing"] = input["Normalize"]["Timing"]
        Cfg["Normalize"]["BoundingBox"] = input["Normalize"]["BoundingBox"]
        Cfg["Normalize"]["VoxSize"] = input["Normalize"]["VoxSize"]
        Cfg["Normalize"]["AffineRegularisationInSegmentation"] = input["Normalize"][
            "AffineRegularisationInSegmentation"
        ]

        # 平滑设置
        Cfg["IsSmooth"] = input["IsSmooth"]
        Cfg["Smooth"] = eng.struct()
        Cfg["Smooth"]["Timing"] = input["Smooth"]["Timing"]
        Cfg["Smooth"]["FWHM"] = input["Smooth"]["FWHM"]

        # 其他设置
        Cfg["MaskFile"] = input["MaskFile"]
        Cfg["IsWarpMasksIntoIndividualSpace"] = input["IsWarpMasksIntoIndividualSpace"]
        Cfg["IsDetrend"] = input["IsDetrend"]

        # ALFF分析设置
        Cfg["IsCalALFF"] = input["IsCalALFF"]
        Cfg["CalALFF"] = eng.struct()
        Cfg["CalALFF"]["AHighPass_LowCutoff"] = input["CalALFF"]["AHighPass_LowCutoff"]
        Cfg["CalALFF"]["ALowPass_HighCutoff"] = input["CalALFF"]["ALowPass_HighCutoff"]

        # Scrubbing设置
        Cfg["IsScrubbing"] = input["IsScrubbing"]
        Cfg["Scrubbing"] = eng.struct()
        Cfg["Scrubbing"]["Timing"] = input["Scrubbing"]["Timing"]
        Cfg["Scrubbing"]["FDType"] = input["Scrubbing"]["FDType"]
        Cfg["Scrubbing"]["FDThreshold"] = input["Scrubbing"]["FDThreshold"]
        Cfg["Scrubbing"]["PreviousPoints"] = input["Scrubbing"]["PreviousPoints"]
        Cfg["Scrubbing"]["LaterPoints"] = input["Scrubbing"]["LaterPoints"]
        Cfg["Scrubbing"]["ScrubbingMethod"] = input["Scrubbing"]["ScrubbingMethod"]

        # ReHo分析设置
        Cfg["IsCalReHo"] = input["IsCalReHo"]
        Cfg["CalReHo"] = eng.struct()
        Cfg["CalReHo"]["ClusterNVoxel"] = input["CalReHo"]["ClusterNVoxel"]
        Cfg["CalReHo"]["SmoothReHo"] = input["CalReHo"]["SmoothReHo"]
        Cfg["CalReHo"]["smReHo"] = input["CalReHo"]["smReHo"]

        # 度中心性分析设置
        Cfg["IsCalDegreeCentrality"] = input["IsCalDegreeCentrality"]
        Cfg["CalDegreeCentrality"] = eng.struct()
        Cfg["CalDegreeCentrality"]["rThreshold"] = input["CalDegreeCentrality"][
            "rThreshold"
        ]

        # 功能连接分析设置
        Cfg["IsCalFC"] = input["IsCalFC"]
        Cfg["IsExtractROISignals"] = input["IsExtractROISignals"]
        Cfg["CalFC"] = eng.struct()
        Cfg["CalFC"]["IsMultipleLabel"] = input["CalFC"]["IsMultipleLabel"]
        Cfg["CalFC"]["ROIDef"] = input["CalFC"]["ROIDef"]
        Cfg["IsDefineROIInteractively"] = input["IsDefineROIInteractively"]

        # CWAS分析设置
        Cfg["IsCWAS"] = input["IsCWAS"]
        Cfg["CWAS"] = eng.struct()
        Cfg["CWAS"]["Regressors"] = input["CWAS"]["Regressors"]
        Cfg["CWAS"]["iter"] = input["CWAS"]["iter"]

        # VMHC分析设置
        Cfg["IsNormalizeToSymmetricGroupT1Mean"] = input[
            "IsNormalizeToSymmetricGroupT1Mean"
        ]
        Cfg["IsSmoothBeforeVMHC"] = input["IsSmoothBeforeVMHC"]
        Cfg["IsCalVMHC"] = input["IsCalVMHC"]

        # 其他参数
        Cfg["FunctionalSessionNumber"] = input["FunctionalSessionNumber"]
        Cfg["StartingDirName"] = input["StartingDirName"]

        stdout_buffer = StringIO()
        stderr_buffer = StringIO()
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = stdout_buffer
        sys.stderr = stderr_buffer
        try:
            assert os.path.isdir(
                os.path.join(Cfg["WorkingDir"], Cfg["StartingDirName"])
            )
            eng.DPARSF_run(Cfg, nargout=0)
            eng.quit()
        except Exception as e:
            import traceback

            traceback.print_exc(file=sys.stderr)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            captured_stdout = stdout_buffer.getvalue()
            captured_stderr = stderr_buffer.getvalue()
            return captured_stdout, captured_stderr

    def generate_report(self) -> str:
        pass


if __name__ == "__main__":
    cfg: dict = {
        "DPARSFVersion": "V9.0_250415",
        "WorkingDir": "D:\\Code\\neuro-pipe\\ProcessingDemoData",
        "DataProcessDir": "D:\\Code\\neuro-pipe\\ProcessingDemoData",
        "SubjectID": {
            "sub02"
        },  # This would need to be converted to MATLAB cell array if using MATLAB engine
        "TimePoints": 0,
        "TR": 0,
        "IsNeedConvertFunDCM2IMG": 0,
        "IsApplyDownloadedReorientMats": 0,
        "IsRemoveFirstTimePoints": 1,
        "RemoveFirstTimePoints": 10,
        # Slice timing correction settings
        "IsSliceTiming": 1,
        "SliceTiming": {
            "SliceNumber": 0,
            "SliceOrder": list(range(1, 34, 2))
            + list(range(2, 33, 2)),  # Would need to convert to MATLAB int32 array
            "ReferenceSlice": 0,
            "TR": 0,
            "TA": 0,
        },
        # Head motion correction settings
        "IsRealign": 1,
        "IsCalVoxelSpecificHeadMotion": 0,
        "IsNeedReorientFunImgInteractively": 1,
        # T1 image processing settings
        "IsNeedConvertT1DCM2IMG": 0,
        "IsNeedReorientCropT1Img": 0,
        "IsNeedReorientT1ImgInteractively": 1,
        "IsBet": 1,
        "IsAutoMask": 1,
        "IsNeedT1CoregisterToFun": 1,
        "IsNeedReorientInteractivelyAfterCoreg": 0,
        # Segmentation settings
        "IsSegment": 2,
        "Segment": {"AffineRegularisationInSegmentation": "mni"},
        "IsDARTEL": 1,
        # Covariate removal settings
        "IsCovremove": 1,
        "Covremove": {
            "Timing": "AfterRealign",
            "PolynomialTrend": 1,
            "HeadMotion": 4,
            "IsHeadMotionScrubbingRegressors": 0,
            "HeadMotionScrubbingRegressors": {
                "FDType": "FD_Power",
                "FDThreshold": 0.5,
                "PreviousPoints": 1,
                "LaterPoints": 2,
            },
            "WhiteMatter": 0,
            "WM": {
                "IsRemove": 1,
                "Mask": "SPM",
                "MaskThreshold": 0.99,
                "Method": "Mean",
                "CompCorPCNum": 5,
            },
            "CSF": {
                "IsRemove": 1,
                "Mask": "SPM",
                "MaskThreshold": 0.99,
                "Method": "Mean",
                "CompCorPCNum": 5,
            },
            "WholeBrain": {
                "IsRemove": 0,
                "IsBothWithWithoutGSR": 0,
                "Mask": "SPM",
                "Method": "Mean",
            },
            "OtherCovariatesROI": [],  # Would need to be matlab.double array
            "IsAddMeanBack": 0,
        },
        # Filter settings
        "IsFilter": 1,
        "Filter": {
            "Timing": "AfterNormalize",
            "ALowPass_HighCutoff": 0.1,
            "AHighPass_LowCutoff": 0.01,
            "AAddMeanBack": "Yes",
        },
        # Normalization settings
        "IsNormalize": 3,
        "Normalize": {
            "Timing": "OnFunctionalData",
            "BoundingBox": [
                [-90, -126, -72],
                [90, 90, 108],
            ],  # Would need to be matlab.double array
            "VoxSize": [3, 3, 3],  # Would need to be matlab.double array
            "AffineRegularisationInSegmentation": "mni",
        },
        # Smoothing settings
        "IsSmooth": 1,
        "Smooth": {
            "Timing": "OnResults",
            "FWHM": [4, 4, 4],  # Would need to be matlab.double array
        },
        # Other settings
        "MaskFile": "Default",
        "IsWarpMasksIntoIndividualSpace": 0,
        "IsDetrend": 0,
        # ALFF analysis settings
        "IsCalALFF": 1,
        "CalALFF": {"AHighPass_LowCutoff": 0.01, "ALowPass_HighCutoff": 0.1},
        # Scrubbing settings
        "IsScrubbing": 0,
        "Scrubbing": {
            "Timing": "AfterPreprocessing",
            "FDType": "FD_Power",
            "FDThreshold": 0.5,
            "PreviousPoints": 1,
            "LaterPoints": 2,
            "ScrubbingMethod": "cut",
        },
        # ReHo analysis settings
        "IsCalReHo": 1,
        "CalReHo": {"ClusterNVoxel": 27, "SmoothReHo": 0, "smReHo": 0},
        # Degree centrality analysis settings
        "IsCalDegreeCentrality": 1,
        "CalDegreeCentrality": {"rThreshold": 0.25},
        # Functional connectivity analysis settings
        "IsCalFC": 0,
        "IsExtractROISignals": 1,
        "CalFC": {
            "IsMultipleLabel": 1,
            "ROIDef": [],  # Would need to be matlab.double array
        },
        "IsDefineROIInteractively": 0,
        # CWAS analysis settings
        "IsCWAS": 0,
        "CWAS": {"Regressors": [], "iter": 0},  # Would need to be matlab.double array
        # VMHC analysis settings
        "IsNormalizeToSymmetricGroupT1Mean": 1,
        "IsSmoothBeforeVMHC": 1,
        "IsCalVMHC": 1,
        # Other parameters
        "FunctionalSessionNumber": 1,
        "StartingDirName": "FunImg",
    }
    dpabi_processor = DPABIProcessor()
    out, err = dpabi_processor.preprocess_data(cfg)
    print()
    print()
    print()
    print()
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(out)
    print("<<<<<<<<<<<<<<")
    print(err)
