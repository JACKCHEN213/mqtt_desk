# -*- coding: utf-8 -*-
import json
import pyperclip


class DataFormat:
    obj = None

    @classmethod
    def json_format(cls, obj):
        cls.obj = obj
        return cls.__json_format
    
    @classmethod
    def __json_format(cls):
        json_text = cls.obj.mqtt_ui.json_content.toPlainText()
        if not json_text:
            cls.obj.message('请输入json文件', _type='error')
            return
        try:
            json_data = json.loads(json_text)
            cls.obj.message('json校验成功')
            cls.obj.mqtt_ui.json_content.setPlainText(json.dumps(json_data, ensure_ascii=False, indent=2))
        except Exception as e:
            repr(e)
            cls.obj.message('不是一个有效的json', _type='error')
            
    @classmethod
    def json_copy(cls, obj):
        cls.obj = obj
        return cls.__json_copy
    
    @classmethod
    def __json_copy(cls):
        if not cls.obj.mqtt_ui.json_content.toPlainText():
            cls.obj.message('内容为空，不能复制', show_status=True, _type='warning')
            return
        pyperclip.copy(cls.obj.mqtt_ui.json_content.toPlainText())
        cls.obj.message('成功复制到剪切板', show_status=True)
    
    @classmethod
    def json_compress(cls, obj):
        cls.obj = obj
        return cls.__json_compress
    
    @classmethod
    def __json_compress(cls):
        if not cls.obj.mqtt_ui.json_content.toPlainText():
            cls.obj.message('内容为空，不能压缩', show_status=True, _type='warning')
            return
        try:
            data = json.loads(cls.obj.mqtt_ui.json_content.toPlainText())
            cls.obj.mqtt_ui.json_content.setPlainText(json.dumps(data, ensure_ascii=False))
            cls.obj.message('json压缩成功')
        except Exception as e:
            repr(e)
            cls.obj.message('不是一个有效的json', _type='error')
