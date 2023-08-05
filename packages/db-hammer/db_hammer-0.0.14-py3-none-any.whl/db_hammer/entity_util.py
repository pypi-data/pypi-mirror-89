import datetime

from db_hammer.util.date import date_to_str


def get_entity_dict(entity):
    """获取对象的所的字段"""
    dd = dir(entity)
    _dict = {}
    column_map = getattr(entity, "__column_map", None)
    for d in dd:
        if not d.startswith("__") and (column_map is None or d in column_map.keys()):
            _dict[d] = getattr(entity, d)
    return _dict


def tag_value(value):
    if value is None:
        return "%s", "null"
    else:
        if isinstance(value, str):
            return "%s", value
        elif isinstance(value, (datetime.datetime, datetime.date)):
            return "%s", date_to_str(value)
        elif isinstance(value, int):
            return "%d", value
        elif isinstance(value, float):
            return "%f", value
        else:
            raise Exception(f"不支持的类型:{value}-{type(value)}")


def insert_sql(entity) -> (str, []):
    dd = get_entity_dict(entity)
    values_tag = []
    values = {}
    table_name = getattr(entity, "__table_name")
    for d in dd:
        value = getattr(entity, d)
        values_tag.append(f":{d}")  # 占位符
        values[d] = value
    return f"""INSERT INTO {table_name}({",".join(dd)}) VALUES ({",".join(values_tag)})""", values


def update_sql(entity, pass_null=False):
    primary_key = getattr(entity, "__primary_key")
    table_name = getattr(entity, "__table_name")
    where = ""
    values_tag = []
    values = {}
    dd = get_entity_dict(entity)
    for d in dd:
        value = getattr(entity, d)
        if value is None or value == "":
            if pass_null:
                continue
        values_tag.append(f"{d}=:{d}")
        values[d] = value
    if isinstance(primary_key, list):
        for k in primary_key:
            value = getattr(entity, k)
            values_tag.append(f"{k}=:{k}")
            values[k] = value
        if where == "":
            where += ' '.join(values_tag)
        else:
            where += ' AND '.join(values_tag)
    else:
        value = getattr(entity, primary_key)
        if where == "":
            where += f' {primary_key}=:{primary_key}'
        else:
            where += f' AND {primary_key}=:{primary_key}'

        values[primary_key] = value

    return f"""UPDATE {table_name} SET {",".join(values_tag)} WHERE{where}""", values


def delete_sql(entity):
    primary_key = getattr(entity, "__primary_key")
    table_name = getattr(entity, "__table_name")
    where = ""
    values_tag = []
    values = {}
    if isinstance(primary_key, list):
        for k in primary_key:
            value = getattr(entity, k)
            values_tag.append(f"{k}=:{k}")
            values[k] = value
        if where == "":
            where += ' '.join(values_tag)
        else:
            where += ' AND '.join(values_tag)
    else:
        value = getattr(entity, primary_key)
        if where == "":
            where += f' {primary_key}=:{primary_key}'
        else:
            where += f' AND {primary_key}=:{primary_key}'

        values[primary_key] = value
    return f"""DELETE FROM {table_name} WHERE{where}""", values
