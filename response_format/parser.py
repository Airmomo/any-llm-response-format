import re
import json
from pydantic import BaseModel
from response_format.base import (
    _try_parse_json_object,
    _parse_model_schema
)


PATTERN = re.compile(r"```(?:json\s+)?(\W.*?)```", re.DOTALL)
"""Regex pattern to parse the output."""

def parse_content_to_json(content: str) -> tuple[str, dict]:
    """
    解析内容到JSON对象。

    # Args:
        content (str): 需要解析的内容字符串。

    # Returns:
        tuple[str, dict]: 返回一个元组，其中第一个元素是JSON字符串，第二个元素是解析后的JSON对象。
    """
    json_text = ""
    json_object = {}
    action_match = PATTERN.search(content)
    if action_match is not None:
        json_text, json_object = _try_parse_json_object(action_match.group(1).strip())
    else:
        # 如果没有匹配到特定的字符开头，尝试直接对齐进行解码
        try:
            json_object = json.loads(content)
            json_text = content
        except json.JSONDecodeError:
            return json_text, json_object

    return json_text, json_object


def parse_model_to_json(model: BaseModel) -> tuple[str, dict]:
    """
    解析模型到JSON对象。

    # Args:
        model (BaseModel): 需要解析的模型实例。

    # Returns:
        tuple[str, dict]: 返回一个元组，其中第一个元素是JSON字符串，第二个元素是解析后的JSON对象。
    """
    json_object = _parse_model_schema(model)
    json_text = json.dumps(json_object, ensure_ascii=False, indent=2)
    return json_text, json_object
