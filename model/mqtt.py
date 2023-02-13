# -*- coding: utf-8 -*-
from uuid import uuid4
from pydantic import BaseModel, Field


def generate_client_id(prefix='python-mqtt-'):
    """
    生成mqtt_id
    :param prefix:
    :return:
    """
    return prefix + uuid4().__str__()


class MqttConfig(BaseModel):
    """
    Mqtt配置
    """
    ip: str = Field(default='127.0.0.1', description='mqtt的主机地址')
    port: int = Field(default=1883, description='mqtt的主机端口')
    username: str = Field(default='admin', description='mqtt服务的登录用户')
    password: str = Field(default='password', description='mqtt服务的登录密码')
    client_id: str = Field(default_factory=generate_client_id, description='mqtt客户端id')

    is_connected: bool = Field(default=False, description='是否连接成功')
    retries: int = Field(default=0, description='连接次数')
    max_retries: int = Field(default=3, description='最大的连接尝试次数')
    retries_interval: int = Field(default=2, description='默认连接间隔为5秒')
    current_retries: int = Field(default=0, description='当前连接的次数')
    connection_time: int = Field(default=0, description='连接时间')


__all__ = ['MqttConfig']
