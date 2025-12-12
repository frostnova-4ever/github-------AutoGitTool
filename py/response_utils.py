def create_response_dict(data=None, success=None, error=None, output=None, message=None, **kwargs):
    """
    创建统一格式的响应字典
    
    Args:
        data: 成功响应的数据
        success: 是否成功（布尔值）
        error: 错误信息
        output: 命令输出或操作结果
        message: 提示消息
        **kwargs: 其他需要包含在响应中的键值对
        
    Returns:
        dict: 统一格式的响应字典
    """
    response = {}
    if success:response["success"] = success
    else:
        # 根据是否有错误自动设置success状态
        response["success"] = error is None
    # 设置错误信息
    if error:response["error"] = error
    # 设置消息
    if message:response["message"] = message
    # 设置输出
    if output:response["output"] = output
    # 设置数据
    if data:
        # 根据数据类型自动设置键名
        if isinstance(data, list):
            if "paths" not in kwargs:
                response["paths"] = data
            else:
                response["data"] = data
        elif isinstance(data, dict):
            response.update(data)
        else:
            response["data"] = data
    
    # 添加额外的键值对
    response.update(kwargs)
    return response