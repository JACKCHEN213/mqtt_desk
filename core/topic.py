# -*- coding: utf-8 -*-
import pathlib
from config import CONFIG_DIR, TOPIC_CONFIG_FILE
from config.configuration import Configuration
from config.drive import Json


class Topic:
    obj = None

    @classmethod
    def save_topic(cls, obj):
        cls.obj = obj
        return cls.__save_topic
    
    @classmethod
    def __save_topic(cls):
        topic = cls.obj.ui.topic.currentText()
        content = cls.obj.ui.publish_text.toPlainText()
        cls.obj.topic_list[topic] = content
        Configuration.save_config(pathlib.Path(CONFIG_DIR) / TOPIC_CONFIG_FILE, cls.obj.topic_list, Json)
        cls.obj.set_topic_list()
        cls.obj.ui.topic.setCurrentText(topic)
        cls.obj.ui.publish_text.setPlainText(cls.obj.topic_list[topic])
        cls.obj.message('topic保存成功', show_status=False)
        cls.obj.logger.info(f'topic保存成功, {topic}')
        cls.obj.logger.debug(content)

    @classmethod
    def change_topic(cls, obj):
        cls.obj = obj
        return cls.__change_topic
    
    @classmethod
    def __change_topic(cls):
        if cls.obj.ui.topic.currentIndex() == -1:
            return
        topic = cls.obj.ui.topic.currentText()
        if cls.obj.topic_list.get(topic, None) is None:
            return
        cls.obj.ui.publish_text.setPlainText(cls.obj.topic_list[topic])
    
    @classmethod
    def save_config(cls, obj):
        cls.obj = obj
        return cls.__save_config
    
    @classmethod
    def __save_config(cls):
        cls.obj.load_input_config()
        cls.obj.mqtt_config.config_name = cls.obj.ui.config_name.text()
        filepath = pathlib.Path(CONFIG_DIR + cls.obj.ui.config_name.text() + '.ini')
        Configuration.save_config(filepath, cls.obj.get_save_data())
        cls.obj.message('配置保存成功')
        cls.obj.logger.info(f'配置保存成功, {filepath.__str__()}')

        cls.obj.mqtt_config.config_file = filepath
        cls.obj.config_list = cls.obj.get_configuration_files()
        cls.obj.set_config_list()
        for file, config in cls.obj.config_list.items():
            if file != filepath:
                continue
            cls.obj.mqtt_config = config
            cls.obj.ui.config_list.setCurrentText(config.config_name)
            cls.obj.set_mqtt_config()
    
    @classmethod
    def load_config(cls, obj):
        cls.obj = obj
        return cls.__load_config
    
    @classmethod
    def __load_config(cls):
        for file, config in cls.obj.config_list.items():
            if config.config_name == cls.obj.ui.config_list.currentText():
                cls.obj.mqtt_config = config
                cls.obj.set_mqtt_config()
                return
        for file, config in cls.obj.config_list.items():
            if file.stem == cls.obj.ui.config_list.currentText():
                cls.obj.mqtt_config = config
                cls.obj.set_mqtt_config()
                return
