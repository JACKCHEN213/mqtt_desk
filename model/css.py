# -*- coding: utf-8 -*-s
from dataclasses import dataclass


@dataclass
class CssModel:
    """
    FIXME: 赋值方式很蠢
    css属性的中杠线'-'统一使用下划线'_'
    """
    tag_name: str = ''  # css的标签名
    attrs = []  # css属性列表

    def __init__(self, tag_name, **kwargs):
        self.tag_name = tag_name
        self.attrs = dict()  # css属性列表
        for field, value in kwargs.items():
            if self.attrs.get(field, None) is None:
                self.attrs[field] = value

    def __str__(self):
        ret_str = self.tag_name + " {\n"
        for field, value in self.attrs.items():
            ret_str += "    " + field.replace('_', '-') + ": " + value + ";\n"
        ret_str += "}"
        return ret_str

    def dict(self):
        return {
            'tag_name': self.tag_name,
            'attrs': self.attrs,
        }

    class Config:
        title = 'css样例测试'
        schema_extra = {'examples': {
            'tag_name': 'QPushButton',
            'background_color': 'red',
            'color': 'white',
        }}


@dataclass
class MultiCssModel:
    data = dict()  # css列表

    def __str__(self):
        if not self.data:
            return ''
        return "\n\n".join([css.__str__() for css in self.data.values()])

    @staticmethod
    def single_class():
        return CssModel

    def dict(self):
        return {
            'data': self.data,
        }

    class Config:
        title = 'css样例测试'
        schema_extra = {'examples': {
            'data': {
                'xx': {
                    'tag_name': 'xx',
                    'attrs': {'background_color': 'red', 'color': 'red'}
                },
                'div': {
                    'tag_name': 'div',
                    'attrs': {'id_background_color': 'red'}
                }
            }
        }}


if __name__ == "__main__":
    cm = CssModel(tag_name='xx', background_color='red', color='red')
    print(cm.Config.schema_extra['examples'])
    print(cm.dict())
    mcm = MultiCssModel()
    mcm.data[cm.tag_name] = cm
    mcm.data['div'] = CssModel(tag_name='div', id_background_color='red')
    print(mcm.dict())
