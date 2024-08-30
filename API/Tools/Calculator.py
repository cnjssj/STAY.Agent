from pydantic import BaseModel


class CalculateExpression(BaseModel):
    Expression: str


CalculatorTools = [
    {
        "type": "function",
        "function": {
            "name": "CalculateExpression",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "unit": {"type": "string", "enum": ["c", "f"]},
                },
                "required": ["location", "unit"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": ["symbol"],
                "additionalProperties": False,
            },
        },
    },
]