# NeuroPipe
### External
需要将以下内容放至本目录中：
- 课程提供的`sub-02CB`数据
- `DPABI_V9.0_250415`
- `REST_V1.8_130615`

### Requirements
- MATLAB 2024b
- Python 3.12
- `requirements.txt`

### Design
#### JSONInput
使用json包实现该类。相较类图，已移除`validate_format`和`parse_content`函数
- 传入json路径进行初始化。初始化函数会检查json文件是否存在，是否符合格式
- 使用下标访问获取json中的内容。也可直接获取类中的`parameters: dict`参数

#### MatlabInterface
直接使用Matlab提供的matlabengine包