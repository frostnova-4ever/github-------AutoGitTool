#!/usr/bin/env python3
"""
YAML配置键名常量定义
使用嵌套类结构组织settings.yaml中的所有键名信息
"""

class YAMLKeys:
    """YAML配置键名常量类，提供层级化的键名访问"""
    
    class TopLevel:
        """顶层键名"""
        TEST_KEY = "test_key"
        TEST_MODULE = "test_module_key"
        TEST_NESTED = "test_nested"
        USER_SETTINGS = "userSettings"
    
    class TestNested:
        """test_nested 下的键名"""
        KEY1 = "key1"
        KEY2 = "key1.key2"
    
    class UserSettings:
        """userSettings 下的键名"""
        ALLOWED_EXTS = "allowed_extensions"
        DEFAULT_VIEW = "default_view"
        GITHUB_REPO = "github_repo"
        LANGUAGE = "language"
        NAME = "name"
        PATH = "path"
        SHOW_HIDDEN = "show_hidden_files"
        THEME = "theme"
    
    # 所有键名的集合 - 使用类方法动态生成
    @classmethod
    def get_all_keys(cls):
        """获取所有键名的集合"""
        return {
            "top_level": [
                cls.TopLevel.TEST_KEY,
                cls.TopLevel.TEST_MODULE,
                cls.TopLevel.TEST_NESTED,
                cls.TopLevel.USER_SETTINGS
            ],
            "test_nested": [
                cls.TestNested.KEY1,
                cls.TestNested.KEY2
            ],
            "userSettings": [
                cls.UserSettings.ALLOWED_EXTS,
                cls.UserSettings.DEFAULT_VIEW,
                cls.UserSettings.GITHUB_REPO,
                cls.UserSettings.LANGUAGE,
                cls.UserSettings.NAME,
                cls.UserSettings.PATH,
                cls.UserSettings.SHOW_HIDDEN,
                cls.UserSettings.THEME
            ]
        }
    
    # 键名到描述的映射 - 使用类方法动态生成
    @classmethod
    def get_key_descriptions(cls):
        """获取键名到描述的映射"""
        return {
            cls.TopLevel.TEST_KEY: "测试键",
            cls.TopLevel.TEST_MODULE: "测试模块键",
            cls.TopLevel.TEST_NESTED: "测试嵌套键",
            cls.TestNested.KEY1: "测试嵌套键1",
            cls.TestNested.KEY2: "测试嵌套键2",
            cls.TopLevel.USER_SETTINGS: "用户设置",
            cls.UserSettings.ALLOWED_EXTS: "允许的文件扩展名列表",
            cls.UserSettings.DEFAULT_VIEW: "默认视图模式",
            cls.UserSettings.GITHUB_REPO: "GitHub仓库地址",
            cls.UserSettings.LANGUAGE: "语言设置",
            cls.UserSettings.NAME: "用户名",
            cls.UserSettings.PATH: "配置路径",
            cls.UserSettings.SHOW_HIDDEN: "是否显示隐藏文件",
            cls.UserSettings.THEME: "主题设置"
        }
    
    @classmethod
    def get_all_top_keys(cls):
        """获取所有顶层键名"""
        return cls.get_all_keys()["top_level"]
    
    @classmethod
    def get_test_keys(cls):
        """获取所有测试相关的键名"""
        return cls.get_all_keys()["test_nested"]
    
    @classmethod
    def get_user_keys(cls):
        """获取所有用户设置相关的键名"""
        return cls.get_all_keys()["userSettings"]
    
    @classmethod
    def get_key_description(cls, key):
        """获取键名的描述信息"""
        return cls.get_key_descriptions().get(key, "")

# 示例用法
if __name__ == "__main__":
    print("=== YAML配置键名信息 ===\n")
    
    print("1. 顶层键名:")
    for key in YAMLKeys.get_all_top_keys():
        print(f"   - {key}")
    
    print("\n2. userSettings键名:")
    for key in YAMLKeys.get_user_keys():
        print(f"   - {key}: {YAMLKeys.get_key_description(key)}")
    
    print("\n3. 测试嵌套键名:")
    for key in YAMLKeys.get_test_keys():
        print(f"   - {key}")
    
    print("\n=== 键名常量示例 ===")
    print(f"GitHub仓库键名: {YAMLKeys.UserSettings.GITHUB_REPO}")
    print(f"主题设置键名: {YAMLKeys.UserSettings.THEME}")
    print(f"顶层测试键名: {YAMLKeys.TopLevel.TEST_KEY}")
    print(f"测试嵌套键2: {YAMLKeys.TestNested.KEY2}")
    
    print("\n=== 通过类方法访问 ===")
    print(f"所有用户键: {YAMLKeys.get_user_keys()}")
    print(f"GitHub仓库键描述: {YAMLKeys.get_key_description(YAMLKeys.UserSettings.GITHUB_REPO)}")
