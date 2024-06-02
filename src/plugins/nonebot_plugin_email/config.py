from pydantic import BaseModel
from nonebot import get_plugin_config


class Config(BaseModel):
    """Plugin Config Here"""
    superusers: list[str] = []


config = get_plugin_config(Config)
