`filterNameById`文件
```
    filteyById(db_con=None, model=CyGame, filter_id=1)
    db_con:mysql数据库连接配置文件，as:
    db_con = {
        'IP': '192.168.5.201',
        'Port': '3306',
        'Database': 'test',
        'User': 'qy',
        'Passwd': 'qy',
    }
```
    model:数据库模型,必须在model文件中已经定义好的
    filter_id:过滤name的那个ID
    返回值:
```
    filterReaponse object:
        status: 0/1
            0:
                errorCode:
                errorMessage:
                错误码：
                {
                    500 数据库连接错误
                    501 数据模型不存在
                }
            1:
                results:
```

lookupName:
