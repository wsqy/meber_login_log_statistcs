# coding:utf-8
import sys
from sqlalchemy import Column, String, create_engine, DATE
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

__all__ = ['CyMemberLoginLog', 'CyGame', 'CyDepartment', ]

# 创建对象的基类 :
Base = declarative_base()


# ***************** 新库的表模型*********** #
class CyMemberLoginLog(Base):
    """创建完整日期表的基类
    from models import CyMemberLoginLog
    """
    # 表名
    __tablename__ = 'cy_member_login_log'

    # 表的对象结构
    mll_id = Column(INTEGER(unsigned=True), primary_key=True, )
    mll_second_id = Column(INTEGER(unsigned=True), default=0, )
    channel_id = Column(INTEGER(unsigned=True), default=0, )
    channel_name = Column(String(50), default="", )
    top_channel_id = Column(INTEGER(unsigned=True), default=0, )
    top_channel_name = Column(String(50), default="", )
    game_id = Column(INTEGER(unsigned=True), default=0, )
    game_name = Column(String(50), default="", )
    mll_date = Column(DATE, default="", )
    mll_datetime = Column(TINYINT, default=0, )
    mll_count = Column(INTEGER(unsigned=True), default=0, )
    mll_create_time = Column(INTEGER(unsigned=True), default=0, )
    mll_update_time = Column(INTEGER(unsigned=True), default=0, )
    mll_status = Column(TINYINT, default=0, )
    mysql_engine = 'InnoDB',
    mysql_charset = 'utf8',

    def __unicode__(self):
        return self.mll_id


class GameChannelDay(Base):
    """创建完整按天分割表的基类
    from models import GameChannelDay
    """
    # 表名
    __tablename__ = 'cy_member_login_log_game_channel_day'

    # 表的对象结构
    mll_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    mll_second_id = Column(INTEGER(unsigned=True), default=0, )
    channel_id = Column(INTEGER(unsigned=True), default=0, )
    channel_name = Column(String(50), default="", )
    top_channel_id = Column(INTEGER(unsigned=True), default=0, )
    top_channel_name = Column(String(50), default="", )
    game_id = Column(INTEGER(unsigned=True), default=0, )
    game_name = Column(String(50), default="", )
    mll_datetime = Column(TINYINT, default=0, )
    mll_count = Column(INTEGER(unsigned=True), default=0, )
    mll_create_time = Column(INTEGER(unsigned=True), default=0, )
    mll_update_time = Column(INTEGER(unsigned=True), default=0, )
    mll_status = Column(TINYINT, default=0, )
    mysql_engine = 'InnoDB',
    mysql_charset = 'utf8',

    def __unicode__(self):
        return self.mll_id


class ChannelHour(Base):
    """创建完整按天分割表的基类
    from models import ChannelHour
    """
    # 表名
    __tablename__ = 'cy_member_login_log_channel_hour'

    # 表的对象结构
    mll_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    mll_second_id = Column(INTEGER(unsigned=True), default=0, )
    channel_id = Column(INTEGER(unsigned=True), default=0, )
    channel_name = Column(String(50), default="", )
    top_channel_id = Column(INTEGER(unsigned=True), default=0, )
    top_channel_name = Column(String(50), default="", )
    mll_date = Column(DATE, default="", )
    mll_datetime = Column(TINYINT, default=0, )
    mll_count = Column(INTEGER(unsigned=True), default=0, )
    mll_create_time = Column(INTEGER(unsigned=True), default=0, )
    mll_update_time = Column(INTEGER(unsigned=True), default=0, )
    mll_status = Column(TINYINT, default=0, )
    mysql_engine = 'InnoDB',
    mysql_charset = 'utf8',

    def __unicode__(self):
        return self.mll_id


class GameHour(Base):
    """创建完整按天分割表的基类
    from models import GameHour
    """
    # 表名
    __tablename__ = 'cy_member_login_log_game_hour'

    # 表的对象结构
    mll_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    mll_second_id = Column(INTEGER(unsigned=True), default=0, )
    game_id = Column(INTEGER(unsigned=True), default=0, )
    game_name = Column(String(50), default="", )
    mll_date = Column(DATE, default="", )
    mll_datetime = Column(TINYINT, default=0, )
    mll_count = Column(INTEGER(unsigned=True), default=0, )
    mll_create_time = Column(INTEGER(unsigned=True), default=0, )
    mll_update_time = Column(INTEGER(unsigned=True), default=0, )
    mll_status = Column(TINYINT, default=0, )
    mysql_engine = 'InnoDB',
    mysql_charset = 'utf8',

    def __unicode__(self):
        return self.mll_id


#  ***************** db_sdk_moge的表数据模型***********  #
class CyGame(Base):
    """创建游戏表的基类
    from models import CyGame
    """
    # 表名
    __tablename__ = 'cy_game'
    # 表结构
    id = Column(INTEGER(unsigned=True), primary_key=True, )
    name = Column(String(30), default="", )
    nickname = Column(String(32), default="", )
    type = Column(INTEGER(unsigned=True), default=0, )
    image = Column(String(100), default="", )
    link = Column(String(200), default="", )
    lanmu = Column(INTEGER(unsigned=True), default=0, )
    isdelete = Column(TINYINT, default=0, )
    xulie = Column(INTEGER(unsigned=True), default=100000, )
    power = Column(INTEGER(unsigned=True), default=0, )
    power_stat = Column(INTEGER(unsigned=True), default=0, )
    power_plus = Column(INTEGER(unsigned=True), default=0, )
    publicity = Column(String(50), default="", )
    pinyin = Column(String(50), default="", )
    initial = Column(String(20), default="", )
    create_time = Column(INTEGER(unsigned=True), default=0, )
    publish_time = Column(INTEGER(unsigned=True), default=0, )
    is_publish = Column(TINYINT, default=0, )
    status = Column(TINYINT, default=1, )
    cooperation_status = Column(TINYINT, default=0, )
    channel_version = Column(INTEGER, default=0, )
    mysql_engine = 'InnoDB',
    mysql_charset = 'utf8',

    def __unicode__(self):
        return self.nickname


#  ***************** db_sdk_moge的表数据模型***********  #
class CyDepartment(Base):
    """创建渠道表的基类
    from models import CyDepartment
    """
    # 表名
    __tablename__ = 'cy_department'

    # 表结构
    id = Column(INTEGER(unsigned=True), primary_key=True, )
    name = Column(String(30), default="", )
    pid = Column(INTEGER(unsigned=True), default=0, )
    left_id = Column(INTEGER(unsigned=True), default=0, )
    right_id = Column(INTEGER(unsigned=True), default=0, )
    level = Column(INTEGER(unsigned=True), default=0, )
    id_path = Column(String(255), default="", )
    menuids = Column(String(800), default="", )
    mark = Column(String(20), default="", )
    remark = Column(String(255), default="", )
    create_time = Column(INTEGER(unsigned=True), default=0, )
    flag = Column(TINYINT, default=0, )
    status = Column(TINYINT, default=1, )
    mysql_engine = 'InnoDB',
    mysql_charset = 'utf8',

    def __unicode__(self):
        return self.name
