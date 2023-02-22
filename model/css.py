# -*- coding: utf-8 -*-s
from pydantic import BaseModel, Field
from typing import List, Dict


class CssModel(BaseModel):
    """
    FIXME: 赋值方式很蠢
    css属性的中杠线'-'统一使用下划线'_'
    """
    tag_name: str = Field(..., description='css的标签名')
    attrs: Dict[str, str] = Field(default=[], description='css属性列表')

    def __init__(self, tag_name, **kwargs):
        super().__init__(tag_name=tag_name, attrs=dict(), **kwargs)
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

    class Config:
        title = 'css样例测试'
        schema_extra = {'examples': {
            'tag_name': 'QPushButton',
            'background_color': 'red',
            'color': 'white',
        }}


class MultiCssModel(BaseModel):
    data: Dict[str, CssModel] = Field(default=dict(), description='css列表')

    def __str__(self):
        if not self.data:
            return ''
        return "\n\n".join([css.__str__() for css in self.data.values()])

    @staticmethod
    def single_class():
        return CssModel

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
