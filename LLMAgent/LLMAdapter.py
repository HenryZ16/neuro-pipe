import os
import ast
import json
import requests
from typing import Optional, Dict, Any
from pathlib import Path
import nibabel as nib
import utils


class LLMAdapter:
    SYSTEM_PROMPT = """你是一个专业的fMRI数据处理助手，需要帮助用户完成DPARSF处理的参数配置。请严格按照以下规则响应：
1. 当用户询问数据处理时，先判断是否包含有效数据路径
2. 当包含有效路径时，将"data_path"设置为从用户指令中提取出数据目录的路径

输出格式必须严格遵循以下内容，不得有任何其他内容，特别是"```json\\n"等内容：
{"is_valid": bool, "data_path": str}"""

    PARAMS_PROMPT = """你是一个专业的fMRI数据处理助手，需要帮助用户完成DPARSF处理的参数配置。请严格按照以下规则响应：
要求：
1. 时间层校正使用隔层采集策略
2. 包含头动校正和空间标准化
3. 使用默认的平滑核（4mm）
4. "DPARSFVersion" 设置为 "V9.0_250415"
5. "IsCalALFF" 设置为 True
6. "SliceTiming" 中的 "SliceNumber" 必须设置为 0，不管 "SliceOrder" 有多少个数

输出格式必须严格遵循以下内容，不得有任何其他内容，特别是"```json\\n"等内容。注意，实际生成的json中不得包含任何None值："""

    PARAMS = """{"is_valid": bool, "suggestion", str, "params": {
        "DPARSFVersion": None,
        "WorkingDir": None,
        "DataProcessDir": None,
        "SubjectID": [ "sub01" ],
        "TimePoints": None,
        "TR": None,
        "IsNeedConvertFunDCM2IMG": None,
        "IsApplyDownloadedReorientMats": None,
        "IsRemoveFirstTimePoints": None,
        "RemoveFirstTimePoints": None,
        "IsSliceTiming": None,
        "SliceTiming": {
            "SliceNumber": None,
            "SliceOrder": None,
            "ReferenceSlice": None,
            "TR": None,
            "TA": None,
        },
        "IsRealign": None,
        "IsCalVoxelSpecificHeadMotion": None,
        "IsNeedReorientFunImgInteractively": None,
        "IsNeedConvertT1DCM2IMG": None,
        "IsNeedReorientCropT1Img": None,
        "IsNeedReorientT1ImgInteractively": None,
        "IsBet": None,
        "IsAutoMask": None,
        "IsNeedT1CoregisterToFun": None,
        "IsNeedReorientInteractivelyAfterCoreg": None,
        "IsSegment": None,
        "Segment": {"AffineRegularisationInSegmentation": None},
        "IsDARTEL": None,
        "IsCovremove": None,
        "Covremove": {
            "Timing": None,
            "PolynomialTrend": None,
            "HeadMotion": None,
            "IsHeadMotionScrubbingRegressors": None,
            "HeadMotionScrubbingRegressors": {
                "FDType": None,
                "FDThreshold": None,
                "PreviousPoints": None,
                "LaterPoints": None,
            },
            "WhiteMatter": None,
            "WM": {
                "IsRemove": None,
                "Mask": None,
                "MaskThreshold": None,
                "Method": None,
                "CompCorPCNum": None,
            },
            "CSF": {
                "IsRemove": None,
                "Mask": None,
                "MaskThreshold": None,
                "Method": None,
                "CompCorPCNum": None,
            },
            "WholeBrain": {
                "IsRemove": None,
                "IsBothWithWithoutGSR": None,
                "Mask": None,
                "Method": None,
            },
            "OtherCovariatesROI": None,
            "IsAddMeanBack": None,
        },
        "IsFilter": None,
        "Filter": {
            "Timing": None,
            "ALowPass_HighCutoff": None,
            "AHighPass_LowCutoff": None,
            "AAddMeanBack": None,
        },
        "IsNormalize": None,
        "Normalize": {
            "Timing": None,
            "BoundingBox":  
            "VoxSize": None,
            "AffineRegularisationInSegmentation": None,
        },
        "IsSmooth": None,
        "Smooth": {
            "Timing": None,
            "FWHM": None,
        },
        "MaskFile": None,
        "IsWarpMasksIntoIndividualSpace": None,
        "IsDetrend": None,
        "IsCalALFF": None,
        "CalALFF": {"AHighPass_LowCutoff": None, "ALowPass_HighCutoff": None},
        "IsScrubbing": None,
        "Scrubbing": {
            "Timing": None,
            "FDType": None,
            "FDThreshold": None,
            "PreviousPoints": None,
            "LaterPoints": None,
            "ScrubbingMethod": None,
        },
        "IsCalReHo": None,
        "CalReHo": {"ClusterNVoxel": None, "SmoothReHo": None, "smReHo": None},
        "IsCalDegreeCentrality": None,
        "CalDegreeCentrality": {"rThreshold": None},
        "IsCalFC": None,
        "IsExtractROISignals": None,
        "CalFC": {
            "IsMultipleLabel": None,
            "ROIDef": None,
        },
        "IsDefineROIInteractively": None,
        "IsCWAS": None,
        "CWAS": {"Regressors": None, "iter": None},  
        "IsNormalizeToSymmetricGroupT1Mean": None,
        "IsSmoothBeforeVMHC": None,
        "IsCalVMHC": None,
        "FunctionalSessionNumber": None,
        "StartingDirName": None,
}}"""

    DATA_INFO = """当前数据路径：{data_path}
目录结构：
{file_tree}
NIFTI元数据示例（首个文件）：
{nii_metadata}
"""

    ANALYZE_PROMPT = """你是一个专业的fMRI数据处理助手，需要帮助用户分析DPARSF处理的结果。请严格按照以下规则响应：
1. 当用户提供处理结果的标准输出和错误输出时，分析这些输出内容
2. 提取有用信息并生成一个JSON对象，包含以下字段：
    - "suggestion": str，提供处理结果的建议或总结。如果“标准输出”和“错误输出”都为空，则返回"函数调用没有任何返回值"。
3. 输出格式必须严格遵循以下内容，不得有任何其他内容，特别是"```json\\n"等内容：
{"suggestion": str}"""

    def __init__(self, api_key_path: str = "./api-key.txt"):
        self.api_key = self._load_api_key(api_key_path)
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _load_api_key(self, path: str) -> str:
        try:
            with open(path, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise ValueError(f"API key file not found at {path}")

    def _call_llm(self, messages: list) -> Dict[str, Any]:
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.1,
        }
        utils.debug_print(messages)
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()
        utils.debug_print("LLM Response:", response.json())
        try:
            response_data = json.loads(
                response.json()["choices"][0]["message"]["content"]
            )
        except json.JSONDecodeError:
            response_data = ast.literal_eval(
                response.json()["choices"][0]["message"]["content"]
            )
        utils.debug_print("Parsed response data:", response_data)
        return response_data

    def _extract_nii_metadata(self, data_path: str) -> list[Dict]:
        """
        从指定路径的.nii文件中提取元数据
        """
        metadata = []
        for root, _, files in os.walk(data_path):
            for file in files:
                if file.endswith((".nii", ".nii.gz")):
                    try:
                        img = nib.load(os.path.join(root, file))
                        header = img.header
                        affine = img.affine

                        # 获取关键元数据
                        meta = {
                            "filename": file,
                            "shape": img.shape,
                            "voxel_sizes": header.get_zooms()[:3],
                            "tr": (
                                float(header.get_zooms()[3])
                                if len(header.get_zooms()) > 3
                                else None
                            ),
                            "data_type": header.get_data_dtype().name,
                            "qform_code": int(header["qform_code"]),
                            "sform_code": int(header["sform_code"]),
                            "orientation": nib.orientations.aff2axcodes(affine),
                        }
                        metadata.append(meta)
                    except Exception as e:
                        print(f"Error reading {file}: {str(e)}")
                        continue
        return metadata

    def parse_user_intent(self, user_input: str) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"用户指令：{user_input}"},
        ]
        response = self._call_llm(messages)

        if not response["is_valid"]:
            raise ValueError("Invalid processing request")
        return response

    def validate_and_generate_params(self, data_path: str) -> Dict[str, Any]:
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Path {data_path} does not exist")

        # 获取文件树信息
        file_tree = []
        for root, dirs, files in os.walk(data_path):
            level = root.replace(data_path, "").count(os.sep)
            indent = " " * 4 * level
            file_tree.append(f"{indent}{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for f in files[:3]:
                file_tree.append(f"{sub_indent}{f}")

        # 获取NIFTI元数据
        nii_metadata = self._extract_nii_metadata(data_path)
        if not nii_metadata:
            raise ValueError("No valid NIFTI files found in the directory")

        messages = [
            {"role": "system", "content": self.PARAMS_PROMPT + self.PARAMS},
            {
                "role": "user",
                "content": self.DATA_INFO.format(
                    data_path=data_path,
                    file_tree="\n".join(file_tree),
                    nii_metadata=nii_metadata[0],
                ),
            },
        ]
        response: dict = self._call_llm(messages)

        if not response["is_valid"]:
            raise ValueError(
                f"Invalid data structure: {response.get('suggestion', '')}"
            )
        # return eval(str(response["params"]))
        return response

    def analyze_return_value(self, captured_stdout, captured_stderr):
        messages = [
            {"role": "system", "content": self.ANALYZE_PROMPT},
            {
                "role": "user",
                "content": f"标准输出：{captured_stdout}\n错误输出：{captured_stderr}",
            },
        ]
        response = self._call_llm(messages)

        return response["suggestion"]

    def process_pipeline(self, user_input: str):
        # Step 1: 解析用户意图
        intent = self.parse_user_intent(user_input)
        print("获取数据路径")

        # Step 2: 验证路径并生成参数
        params = self.validate_and_generate_params(intent["data_path"])
        print("生成的参数：" + json.dumps(params, indent=2))

        # Step 3: 调用DPABIProcessor
        from DataProcessor.DPABIProcessor import DPABIProcessor

        processor = DPABIProcessor()
        captured_stdout, captured_stderr = processor.preprocess_data(params["params"])

        # Step 4: 分析处理结果
        analysis_result = self.analyze_return_value(captured_stdout, captured_stderr)
        print("处理结果分析:", analysis_result)


if __name__ == "__main__":
    # 测试用例
    adapter = LLMAdapter()
    try:
        test_input = (
            "请处理D:\ShanghaiTech\Courses\Python\group-5\ProcessingDemoData的数据"
        )
        print("测试输入:", test_input)

        # 测试意图解析
        intent = adapter.parse_user_intent(test_input)
        print("意图解析结果:", intent)

        # 测试参数生成
        params = adapter.validate_and_generate_params(intent["data_path"])
        print("生成的参数:", json.dumps(params, indent=2))

    except Exception as e:
        print(f"测试失败: {str(e)}")
