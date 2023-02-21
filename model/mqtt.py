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

    config_name: str = Field(default='', description='mqtt配置文件名称')
    config_file: str = Field(default='', description='mqtt配置文件路径')

    is_connected: bool = Field(default=False, description='是否连接成功')
    retries: int = Field(default=0, description='连接次数')
    max_retries: int = Field(default=3, description='最大的连接尝试次数')
    retries_interval: int = Field(default=2, description='默认连接间隔为5秒')
    current_retries: int = Field(default=0, description='当前连接的次数')
    connection_time: int = Field(default=0, description='连接时间')

    def get_save_data(self):
        return {
            'ip': self.ip,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'config_name': self.config_name,
        }

    def __eq__(self, other):
        """
        只比较配置信息
        """
        if self.ip != other.ip:
            return False
        if self.port != other.port:
            return False
        if self.username != other.username:
            return False
        if self.password != other.password:
            return False
        return True


__all__ = ['MqttConfig']
