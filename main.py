from LLMAgent.LLMAdapter import LLMAdapter


def main():
    # 初始化适配器
    adapter = LLMAdapter()

    # 获取用户输入
    user_input = input("请输入处理指令：")

    try:
        # 执行处理管线
        adapter.process_pipeline(user_input)
        print("数据处理完成")
    except Exception as e:
        print(f"处理失败: {str(e)}")


if __name__ == "__main__":
    main()
