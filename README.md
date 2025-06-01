# NeuroPipe
### Introduction
NeuroPipe是一个接受用户以自然语言描述的，预处理.nii文件的AI智能体
- 用户描述需要处理哪里的数据
- LLMAdapter将用户的指令传递给LLM。LLM提取出数据路径
- LLMAdapter根据LLM传回的路径，将数据路径的目录结构，和.nii文件头，结合预设的参数列表传给LLM。LLM返回一个设置完成的参数列表
- LLMAdapter根据传回的参数列表，将参数传递给DPABIProcessor
- DPABIProcessor将参数传递给对应的MATLAB函数DPARSF_run执行预处理
- 预处理执行完成以后，DPABIProcessor返回执行结果与报错给LLMAdapter
- LLMAdapter将DPABIProcessor返回的结果交由LLM分析
- 最后LLMAdapter输出LLM返回的分析报告

整个过程无需用户手动填入预处理参数，LLM会生成参数建议，并自动调用对应MATLAB函数。如果中途发生错误，例如用户指令不包含路径，用户传入的路径错误，或是在预处理的过程中出现报错，NeuroPipe都可以提示用户应该如何更正

### External
需要将以下内容放至本目录中：
- 课程提供的`sub-02CB`数据

此外，需要在MATLAB中添加以下外部包
- `DPABI_V9.0_250415`
- `SPM12`

### Requirements
- MATLAB 2024b
  - SPM 25.01.02
  - Image Processing Toolbox 24
- Python 3.12
- `requirements.txt`
- 在`api-key.txt`中存放你的api-key

### Design
#### JSONInput
使用json包实现该类。相较类图，已移除`validate_format`和`parse_content`函数
- 传入json路径进行初始化。初始化函数会检查json文件是否存在，是否符合格式
- 使用下标访问获取json中的内容。也可直接获取类中的`parameters: dict`参数

#### MatlabInterface
直接使用Matlab提供的matlabengine包

### Run
使用 `python ./main.py` 运行。然后，根据程序提示，输入你希望大模型生成参数的数据路径
