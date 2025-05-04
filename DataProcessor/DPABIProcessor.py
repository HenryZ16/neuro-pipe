from LLMAgent import LLMEnhancedAligner
import os
import matlab.engine


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
        "SubjectID": {'Sub_01'},
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
    # def preprocess_data(self, input: dict) -> dict:
    def preprocess_data(self,working_dir: str = None):
        eng = matlab.engine.start_matlab()
        Cfg = eng.struct()
        
        # 设置基本参数
        Cfg['DPARSFVersion'] = 'V9.0_250415'
        # Cfg['WorkingDir'] = r'D:\Code\neuro-pipe\Test_Data'
        Cfg['WorkingDir'] = working_dir
        Cfg['DataProcessDir'] = Cfg['WorkingDir']
        # Cfg['SubjectID'] = eng.cellstr(['Sub_01'])
        # Cfg['SubjectID'] = eng.cellstr([])
        Cfg['TimePoints'] = 0
        Cfg['TR'] = 0
        Cfg['IsNeedConvertFunDCM2IMG'] = 0
        Cfg['IsApplyDownloadedReorientMats'] = 0
        Cfg['IsRemoveFirstTimePoints'] = 1
        Cfg['RemoveFirstTimePoints'] = 10
        
        # 切片时间校正设置
        Cfg['IsSliceTiming'] = 1
        Cfg['SliceTiming'] = eng.struct()
        Cfg['SliceTiming']['SliceNumber'] = 0
        Cfg['SliceTiming']['SliceOrder'] = matlab.int32([i for i in range(1, 34, 2)] + [i for i in range(2, 33, 2)])
        Cfg['SliceTiming']['ReferenceSlice'] = 0
        Cfg['SliceTiming']['TR'] = 0
        Cfg['SliceTiming']['TA'] = 0
        
        # 头动校正设置
        Cfg['IsRealign'] = 1
        Cfg['IsCalVoxelSpecificHeadMotion'] = 0
        Cfg['IsNeedReorientFunImgInteractively'] = 1
        
        # T1像处理设置
        Cfg['IsNeedConvertT1DCM2IMG'] = 0
        Cfg['IsNeedReorientCropT1Img'] = 0
        Cfg['IsNeedReorientT1ImgInteractively'] = 1
        Cfg['IsBet'] = 1
        Cfg['IsAutoMask'] = 1
        Cfg['IsNeedT1CoregisterToFun'] = 1
        Cfg['IsNeedReorientInteractivelyAfterCoreg'] = 0
        
        # 分割设置
        Cfg['IsSegment'] = 2
        Cfg['Segment'] = eng.struct()
        Cfg['Segment']['AffineRegularisationInSegmentation'] = 'mni'
        Cfg['IsDARTEL'] = 1
        
        # 协变量去除设置
        Cfg['IsCovremove'] = 1
        Cfg['Covremove'] = eng.struct()
        Cfg['Covremove']['Timing'] = 'AfterRealign'
        Cfg['Covremove']['PolynomialTrend'] = 1
        Cfg['Covremove']['HeadMotion'] = 4
        Cfg['Covremove']['IsHeadMotionScrubbingRegressors'] = 0
        Cfg['Covremove']['HeadMotionScrubbingRegressors'] = eng.struct()
        Cfg['Covremove']['HeadMotionScrubbingRegressors']['FDType'] = 'FD_Power'
        Cfg['Covremove']['HeadMotionScrubbingRegressors']['FDThreshold'] = 0.5
        Cfg['Covremove']['HeadMotionScrubbingRegressors']['PreviousPoints'] = 1
        Cfg['Covremove']['HeadMotionScrubbingRegressors']['LaterPoints'] = 2
        Cfg['Covremove']['WhiteMatter'] = 0
        
        # 白质、脑脊液等设置
        Cfg['Covremove']['WM'] = eng.struct()
        Cfg['Covremove']['WM']['IsRemove'] = 1
        Cfg['Covremove']['WM']['Mask'] = 'SPM'
        Cfg['Covremove']['WM']['MaskThreshold'] = 0.99
        Cfg['Covremove']['WM']['Method'] = 'Mean'
        Cfg['Covremove']['WM']['CompCorPCNum'] = 5
        
        Cfg['Covremove']['CSF'] = eng.struct()
        Cfg['Covremove']['CSF']['IsRemove'] = 1
        Cfg['Covremove']['CSF']['Mask'] = 'SPM'
        Cfg['Covremove']['CSF']['MaskThreshold'] = 0.99
        Cfg['Covremove']['CSF']['Method'] = 'Mean'
        Cfg['Covremove']['CSF']['CompCorPCNum'] = 5
        
        Cfg['Covremove']['WholeBrain'] = eng.struct()
        Cfg['Covremove']['WholeBrain']['IsRemove'] = 0
        Cfg['Covremove']['WholeBrain']['IsBothWithWithoutGSR'] = 0
        Cfg['Covremove']['WholeBrain']['Mask'] = 'SPM'
        Cfg['Covremove']['WholeBrain']['Method'] = 'Mean'
        
        Cfg['Covremove']['OtherCovariatesROI'] = matlab.double([])
        Cfg['Covremove']['IsAddMeanBack'] = 0
        
        # 滤波设置
        Cfg['IsFilter'] = 1
        Cfg['Filter'] = eng.struct()
        Cfg['Filter']['Timing'] = 'AfterNormalize'
        Cfg['Filter']['ALowPass_HighCutoff'] = 0.1
        Cfg['Filter']['AHighPass_LowCutoff'] = 0.01
        Cfg['Filter']['AAddMeanBack'] = 'Yes'
        
        # 标准化设置
        Cfg['IsNormalize'] = 3
        Cfg['Normalize'] = eng.struct()
        Cfg['Normalize']['Timing'] = 'OnFunctionalData'
        Cfg['Normalize']['BoundingBox'] = matlab.double([[-90, -126, -72], [90, 90, 108]])
        Cfg['Normalize']['VoxSize'] = matlab.double([3, 3, 3])
        Cfg['Normalize']['AffineRegularisationInSegmentation'] = 'mni'
        
        # 平滑设置
        Cfg['IsSmooth'] = 1
        Cfg['Smooth'] = eng.struct()
        Cfg['Smooth']['Timing'] = 'OnResults'
        Cfg['Smooth']['FWHM'] = matlab.double([4, 4, 4])
        
        # 其他设置
        Cfg['MaskFile'] = 'Default'
        Cfg['IsWarpMasksIntoIndividualSpace'] = 0
        Cfg['IsDetrend'] = 0
        
        # ALFF分析设置
        Cfg['IsCalALFF'] = 1
        Cfg['CalALFF'] = eng.struct()
        Cfg['CalALFF']['AHighPass_LowCutoff'] = 0.01
        Cfg['CalALFF']['ALowPass_HighCutoff'] = 0.1
        
        # Scrubbing设置
        Cfg['IsScrubbing'] = 0
        Cfg['Scrubbing'] = eng.struct()
        Cfg['Scrubbing']['Timing'] = 'AfterPreprocessing'
        Cfg['Scrubbing']['FDType'] = 'FD_Power'
        Cfg['Scrubbing']['FDThreshold'] = 0.5
        Cfg['Scrubbing']['PreviousPoints'] = 1
        Cfg['Scrubbing']['LaterPoints'] = 2
        Cfg['Scrubbing']['ScrubbingMethod'] = 'cut'
        
        # ReHo分析设置
        Cfg['IsCalReHo'] = 1
        Cfg['CalReHo'] = eng.struct()
        Cfg['CalReHo']['ClusterNVoxel'] = 27
        Cfg['CalReHo']['SmoothReHo'] = 0
        Cfg['CalReHo']['smReHo'] = 0
        
        # 度中心性分析设置
        Cfg['IsCalDegreeCentrality'] = 1
        Cfg['CalDegreeCentrality'] = eng.struct()
        Cfg['CalDegreeCentrality']['rThreshold'] = 0.25
        
        # 功能连接分析设置
        Cfg['IsCalFC'] = 0
        Cfg['IsExtractROISignals'] = 1
        Cfg['CalFC'] = eng.struct()
        Cfg['CalFC']['IsMultipleLabel'] = 1
        Cfg['CalFC']['ROIDef'] = matlab.double([])
        Cfg['IsDefineROIInteractively'] = 0
        
        # CWAS分析设置
        Cfg['IsCWAS'] = 0
        Cfg['CWAS'] = eng.struct()
        Cfg['CWAS']['Regressors'] = matlab.double([])
        Cfg['CWAS']['iter'] = 0
        
        # VMHC分析设置
        Cfg['IsNormalizeToSymmetricGroupT1Mean'] = 1
        Cfg['IsSmoothBeforeVMHC'] = 1
        Cfg['IsCalVMHC'] = 1
        
        # 其他参数
        Cfg['FunctionalSessionNumber'] = 1
        Cfg['StartingDirName'] = 'FunRaw'
        
        assert os.path.isdir(os.path.join(Cfg['WorkingDir'], Cfg['StartingDirName']))
        print(os.listdir(os.path.join(Cfg['WorkingDir'], Cfg['StartingDirName'])))
        Cfg['SubjectID'] = eng.cellstr(os.listdir(os.path.join(Cfg['WorkingDir'], Cfg['StartingDirName'])))

        eng.DPARSF_run(Cfg, nargout=0)


        eng.quit()

    def generate_report(self) -> str:
        pass

if __name__ == "__main__":
    dpabi_processor = DPABIProcessor()
    dpabi_processor.preprocess_data('D:\\Code\\neuro-pipe\\Test_Data')