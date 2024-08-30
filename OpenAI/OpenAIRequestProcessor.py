from typing import List
import openai
from pydantic import BaseModel
import json
from ServiceAPI.Tools.Calculator import CalculateExpression

class OpenAIRequestProcessor:
    def __init__(self, api_key: str):
        self.client = openai.Client(api_key=api_key)
        self.default_model = 'gpt-4o-2024-08-06'

    def process_request(self, user_input: str, system_prompt: str, tools: List[BaseModel], model: str = None) -> str:
        if model is None:
            model = self.default_model

        # 构建消息列表
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        # 创建工具列表，用于 Function Calling
        pydantic_tools = [openai.pydantic_function_tool(tool) for tool in tools]

        # 调用 OpenAI 的 ServiceAPI
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            tools=pydantic_tools
        )

        # 提取 ServiceAPI 的响应结果
        function_call = response.choices[0].message.tool_calls[0] # ChatCompletionMessageToolCall(id='call_5fwzwTCZ1tDW9KlSufiXWsqH', function=Function(arguments='{"expression":"(x + y + z) / 3"}', name='CalculateExpression'), type='function')
        # 解析 `arguments` 字符串为字典
        arguments = json.loads(function_call.function.arguments) # {'expression': '(x + y + z) / 3'}
        # 从字典中提取 `expression`
        expression = arguments.get('Expression') # (x + y + z) / 3
        return expression


# 使用示例
if __name__ == "__main__":
    # 初始化处理器
    api_key = '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'  # 替换为你的 OpenAI ServiceAPI 密钥
    processor = OpenAIRequestProcessor(api_key=api_key)

    # 配置不同的 prompt 和工具
    system_prompt = (
        "用户输入一句话描述他们的计算需求，要求将需求转换成一个数学表达式，"
        "表达式中只允许使用两个或三个操作数，并且用 `x`, `y`, `z` 表示操作数。"
        "请将生成的表达式以FunctionCalling的形式输出，并调用指定的API来执行计算。"
    )
    tools = [CalculateExpression]

    # 处理请求
    user_input = "求三个数的平均数"
    Expression = processor.process_request(user_input, system_prompt, tools)

    print(f"生成的数学表达式: {Expression}")
