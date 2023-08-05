def table(name=None, primary_key="id", column_map=None):
    """数据据保存的表名"""
    def decorate(clazz):
        setattr(clazz, "__table_name", clazz.__name__ if name is None else name)
        setattr(clazz, "__primary_key", primary_key)
        setattr(clazz, "__column_map", None if column_map is None else column_map)
        return clazz
    return decorate
