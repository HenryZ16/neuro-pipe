from LLMAgent.LLMAdapter import LLMAdapter
from ollama import chat
from ollama import ChatResponse
import json
import os


class Interface:
    def get_data_path(self, agent: LLMAdapter) -> str:
        """
        Get user instructions for the LLMAdapter.
        """
        print(">>> ", end="")
        instruction = input()
        file_path: str = None

        for i in range(3):
            try:
                user_instructions: dict = agent.config_interact
                response: ChatResponse = chat(
                    model=agent.config_interact["model"],
                    messages=[
                        {
                            "role": user_instructions["messages"]["role"],
                            "content": user_instructions["messages"]["content"],
                        },
                        {
                            "role": "user",
                            "content": instruction,
                        },
                    ],
                )
                file_path = agent.remove_think(response["message"]["content"])
                if not os.path.isdir(file_path):
                    raise ValueError(f"The path is not a directory: {file_path}")
            except Exception as e:
                if i < 2:
                    continue
                else:
                    print("Error: ", e)
                    raise ValueError("Failed to get the file path.")
        return file_path


if __name__ == "__main__":
    agent = LLMAdapter()
    interface = Interface()
    file_path = interface.get_data_path(agent)

    print(file_path)
