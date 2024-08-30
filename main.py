from Server.JsonHandler import JSONHandler
import Server.TcpServer as TcpServer

from OpenAI.OpenAIRequestProcessor import OpenAIRequestProcessor
import API.Tools.Calculator as CalculatorTool
import API.Messages.Calculator as CalculatorMessage

if __name__ == "__main__":
    # 初始化OpenAI请求处理器
    api_key = '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'
    processor = OpenAIRequestProcessor(api_key=api_key)

    # 配置服务器
    config = TcpServer.ServerConfig(host="127.0.0.1", port=25001)
    request_handler = JSONHandler(CalculatorMessage.ClientRequest)
    response_handler = JSONHandler(CalculatorMessage.ServerResponse)

    server = TcpServer.TCPServer(config, request_handler)

    # 自定义接收逻辑并处理请求
    def custom_receive(client_socket, data_handler: JSONHandler[CalculatorMessage.ClientRequest]):
        while True:
            received_data = client_socket.recv(1024).decode()
            if not received_data:
                break
            client_request = data_handler.deserialize(received_data)
            print("收到客户端请求:", client_request.request)

            # 配置不同的 prompt 和工具
            system_prompt = (
                "用户输入一句话描述他们的计算需求，要求将需求转换成一个数学表达式，"
                "表达式中只允许使用两个或三个操作数，并且用 `x`, `y`, `z` 表示操作数。"
                "请将生成的表达式以FunctionCalling的形式输出，并调用指定的API来执行计算。"
            )
            tools = [CalculatorTool.CalculateExpression]

            # 调用OpenAI API处理请求
            expression = processor.process_request(client_request.request, system_prompt, tools)

            # 构建响应并发送回客户端
            server_response = CalculatorMessage.ServerResponse(expression)
            response_data = response_handler.serialize(server_response)

            client_socket.sendall(response_data.encode())


    # 自定义发送逻辑（在这个例子中，服务器不主动发送数据，只是响应）
    def custom_send(client_socket, data_handler: JSONHandler[CalculatorMessage.ServerResponse]):
        pass  # 服务器在本示例中不需要主动发送数据


    # 动态设置回调函数
    server.set_receive_callback(custom_receive)
    server.set_send_callback(custom_send)

    server.start()
