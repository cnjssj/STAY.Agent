from dataclasses import dataclass

# 客户端请求的数据结构
@dataclass
class ClientRequest:
    request: str


# 服务器响应的数据结构
@dataclass
class ServerResponse:
    expression: str
