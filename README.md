# NeuroPipe
### External
需要将课程提供的`sub-02CB`数据放至本项目中

### Design
#### JSONInput
使用json包实现该类。相较类图，已移除`validate_format`和`parse_content`函数
- 传入json路径进行初始化。初始化函数会检查json文件是否存在，是否符合格式
- 使用下标访问获取json中的内容。也可直接获取类中的`parameters: dict`参数

#### MatlabInterface
无需打开GUI，尝试直接调用对应函数`DPARSF_run`和`DPARSFA_run`并传参