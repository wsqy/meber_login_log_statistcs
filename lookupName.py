# encoding=utf-8
from __future__ import print_function
from models import CyGame, CyDepartment
import models
from settings import output_base_dir, db_200_config, db_32_config
import settings
import redis
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import ProgrammingError
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

"""
1.程序维护的字典里寻找
2.内存里查找
3.本地数据库里查找
4.生产数据库里查找
5.找不到，则设置为0
从高级别的查找到,必须同步更新到低级别中
"""
game_dict = {}
channel_dict = {}
nameMap = {
    "game": game_dict,
    "channel": channel_dict,
}
type_map_model = {
    "game": CyGame,
    "channel": CyDepartment,
}


class filterReaponse(object):
    def __init__(self):
        self.__status = False
        self.__errorCode = 500
        self.__errorMessage = None
        self.__name = ""

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, vaule):
        self.__status = vaule

    @property
    def errorCode(self):
        return self.__errorCode

    @errorCode.setter
    def errorCode(self, vaule):
        self.__errorCode = vaule

    @property
    def errorMessage(self):
        return self.__errorMessage

    @errorMessage.setter
    def errorMessage(self, vaule):
        self.__errorMessage = vaule

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, vaule):
        self.__name = vaule


def seachLocal(model_type="game", filter_id=1, resultResponse=None):
    """从全局定义中查找
    """
    if not resultResponse:
        resultResponse = filterReaponse()
    name_dict = nameMap.get(model_type, False)
    if not name_dict:
        resultResponse.errorCode = 501
        resultResponse.errorMessage = "数据%s模型不存在" % model_type
        return resultResponse
    name = name_dict.get(filter_id, False)
    if not name:
        resultResponse.errorCode = 502
        resultResponse.errorMessage = "%s没有对应的name" % filter_id
        return resultResponse
    resultResponse.status = True
    resultResponse.name = name
    return resultResponse


def setLocal(model_type="game", filter_id=1, name=""):
    """更新全局的映射表
    """
    name_dict = nameMap.get(model_type, False)
    name_dict[filter_id] = name


def seachRedis(model_type="game", filter_id=1, resultResponse=None):
    """从redis查找
    """
    # print("查找redis")
    if not resultResponse:
        resultResponse = filterReaponse()
    if model_type == "game":
        redis_key = "%s:%s" % (settings.redis_con.get('gamePrefix'), str(filter_id))
    elif model_type == "channel":
        redis_key = "%s:%s" % (settings.redis_con.get('channelPrefix'), str(filter_id))
    r = redis.StrictRedis(host=settings.redis_con.get('host'),
                          port=settings.redis_con.get('port'),
                          db=settings.redis_con.get('db'),
                          password=settings.redis_con.get('password'),
                          )
    name = r.get(redis_key)
    if not name:
        resultResponse.errorCode = 502
        resultResponse.errorMessage = "%s没有对应的name" % id
        return resultResponse
    resultResponse.status = True
    resultResponse.name = name
    return resultResponse


def setRedis(model_type="game", filter_id=1, name=""):
    """更新redis
    """
    print("更新redis:%s-->%s" % (filter_id, name))
    if model_type == "game":
        redis_key = "%s:%s" % (settings.redis_con.get('gamePrefix'), str(filter_id))
    elif model_type == "channel":
        redis_key = "%s:%s" % (settings.redis_con.get('channelPrefix'), str(filter_id))
    r = redis.StrictRedis(host=settings.redis_con.get('host'),
                          port=settings.redis_con.get('port'),
                          db=settings.redis_con.get('db'),
                          password=settings.redis_con.get('password'),
                          )
    name = r.set(redis_key, name)


def seachLocalDatabase(model_type="game", filter_id=1, db_con=None, resultResponse=None):
    """从数据库里开始查找
    """
    # print("查找数据库")
    if not db_con:
        db_con = db_200_config
    model = type_map_model.get(model_type, "0")
    if not resultResponse:
        resultResponse = filterReaponse()

    if str(model) not in models.__all__:
        resultResponse.errorCode = 501
        resultResponse.errorMessage = "数据%s模型不存在" % model
    conn = 'mysql+mysqlconnector://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % db_con
    # 初始化数据库连接, echo=False则不显示执行的sql语句
    engine = create_engine(conn, echo=False, )
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    # 创建session对象:
    session = DBSession()
    try:
        seach_names = session.query(model).filter_by(id=int(filter_id))
        results = []
        for seach_name in seach_names:
            results.append(seach_name.name)
        resultResponse.status = True
        resultResponse.name = results[0]
    except ProgrammingError:
        resultResponse.errorCode = 500
        resultResponse.errorMessage = "数据库连接错误"
    finally:
        # 关闭session:
        session.close()
        return resultResponse


def setLocalDatabase(model_type="game", filter_id=1, name="", db_con=None):
    """更新本地数据库
    """
    pass


def seachRemoteDatabase(model=CyGame, id=1, resultResponse=None):
    """本地都查找不到则向生产数据库请求
    """
    pass


def findname(model_type="game", filter_id=1):
    resultResponse = filterReaponse()
    # 先从全局定义查找
    # resultResponse = seachLocal(model_type, filter_id, resultResponse)
    # # 找到则返回
    # if resultResponse.status:
    #     return resultResponse.name
    #
    # # 没找到去redis里找
    # resultResponse = seachRedis(model_type, filter_id, resultResponse)
    # if resultResponse.status:
    #     # 找到则更新全局定义，并返回
    #     setLocal(model_type, filter_id, resultResponse.name)
    #     return resultResponse.name

    # 没找到去本地数据库里找
    resultResponse = seachLocalDatabase(model_type, filter_id, None, resultResponse)
    if resultResponse.status:
        # 找到则更新全局定义和redis，并返回
        # setLocal(model_type, filter_id, resultResponse.name)
        # setRedis(model_type, filter_id, resultResponse.name)
        return resultResponse.name

    # 如果还没找找到，则应该调用相应的api查找;接口暂未完成先直接返回
    return resultResponse.name


def findChannelPath(filter_id):
    conn = 'mysql+mysqlconnector://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % db_200_config
    # 初始化数据库连接:
    engine = create_engine(conn, echo=False, )

    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)

    # 创建session对象:
    session = DBSession()

    # 查询指定channel_id的id_path
    channels = session.query(CyDepartment).filter(CyDepartment.id == int(filter_id))
    for channel in channels:
        return channel.id_path


if __name__ == "__main__":
    conn = 'mysql+mysqlconnector://%(User)s:%(Passwd)s@%(IP)s:%(Port)s/%(Database)s' % setting.db_200_config
    # 初始化数据库连接:
    engine = create_engine(conn, echo=False, )

    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)

    # 创建session对象:
    session = DBSession()
    # 查询game表中的全部数据
    game_dates = session.query(CyDepartment)[:10]
    for game_date in game_dates:
        print(game_date.id, game_date.name)

    # 查询指定game_id的game_name
    game_dates = session.query(CyDepartment).filter_by(id=11)
    results = []
    for game_date in game_dates:
        results.append(game_date.name)
    print(results)
    len_results = len(results)
    if len_results == 0:
        print(-200)
    elif len_results > 1:
        print(results[0])
    else:
        print(-300)

    # 关闭session:
    session.close()
