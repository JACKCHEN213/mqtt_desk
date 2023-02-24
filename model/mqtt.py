# -*- coding: utf-8 -*-
from typing import Union
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

    def __str__(self):
        if self.username:
            return f'mqtt://{self.username}:{self.password}@{self.ip}:{self.port}'
        return f'mqtt://{self.ip}:{self.port}'

    def validate_ip(self) -> Union[bool, str]:
        ips = self.ip.split('.')
        if len(ips) != 4:
            return 'ip地址位数非法'
        for ip in ips:
            if ip != str(int(ip)):
                return f'ip段内容{ip}错误'
            if 0 > int(ip) or int(ip) > 255:
                return f'ip段长度{ip}错误'
        return True

    def validate_config(self) -> Union[bool, str]:
        if not self.ip:
            return 'mqtt的主机必须'
        if isinstance(ip_validate := self.validate_ip(), str):
            return ip_validate
        if not self.port:
            return 'mqtt的端口必须'
        if 0 > self.port or self.port > 65536:
            return 'mqtt的端口错误'
        return True


__all__ = ['MqttConfig', 'generate_client_id']
