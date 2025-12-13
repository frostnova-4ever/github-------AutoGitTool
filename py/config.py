import yaml
import os
from pathlib import Path

class ConfigManager:
    """配置管理类，用于加载和管理YAML配置文件"""
    
    def __init__(self, config_path=None):
        """
        初始化配置管理器
        
        参数:
            config_path: 配置文件路径，如果为None则使用默认路径
        """
        # 设置默认配置文件路径
        if config_path is None:
            # 获取当前文件目录
            current_dir = Path(__file__).parent.parent
            config_path = os.path.join(current_dir, 'demo', 'config.yaml')
        
        self.config_path = config_path
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file)
                if self.config is None:
                    self.config = {}
        except FileNotFoundError:
            # 配置文件不存在，使用默认配置
            self.config = {}
        except yaml.YAMLError:
            # 解析配置文件失败，使用默认配置
            self.config = {}
        except Exception:
            # 加载配置文件失败，使用默认配置
            self.config = {}
    
    def get(self, key_path, default=None):
        """
        获取配置值
        
        参数:
            key_path: 配置键路径，使用点分隔（例如：'server.host'）
            default: 如果键不存在则返回的默认值
        
        返回:
            配置值或默认值
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path, value):
        """
        设置配置值
        
        参数:
            key_path: 配置键路径，使用点分隔（例如：'server.host'）
            value: 要设置的配置值
        """
        keys = key_path.split('.')
        config = self.config
        
        # 遍历键路径，创建不存在的嵌套键
        for key in keys[:-1]:
            if key not in config or not isinstance(config[key], dict):
                config[key] = {}
            config = config[key]
        
        # 设置最后一个键的值
        config[keys[-1]] = value
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(self.config, file, default_flow_style=False, allow_unicode=True, indent=2)
            return True
        except Exception:
            return False
    
    def get_all_config(self):
        """获取所有配置"""
        return self.config

# 创建全局配置实例
global_config = ConfigManager()

# 提供便捷的函数接口
def load_config(config_path=None):
    """加载配置文件"""
    if config_path:
        global_config.__init__(config_path)
    else:
        global_config.load_config()

def get_config(key_path, default=None):
    """获取配置值"""
    return global_config.get(key_path, default)

def set_config(key_path, value):
    """设置配置值"""
    global_config.set(key_path, value)

def save_config():
    """保存配置到文件"""
    return global_config.save_config()

def get_all_config():
    """获取所有配置"""
    return global_config.get_all_config()
