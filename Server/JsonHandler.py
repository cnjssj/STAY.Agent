from typing import Type, TypeVar, Generic
import json

# 泛型类型变量
T = TypeVar('T')

class JSONHandler(Generic[T]):
    def __init__(self, data_type: Type[T]):
        self.data_type = data_type

    def serialize(self, data: T) -> str:
        if hasattr(data, "__dict__"):
            # 将对象转换为字典
            data_dict = data.__dict__
        else:
            # 如果数据类型没有 __dict__，直接返回
            data_dict = data
        return json.dumps(data_dict) + '\n'

    def deserialize(self, data_str: str) -> T:
        data_dict = json.loads(data_str)
        return self.data_type(**data_dict)
