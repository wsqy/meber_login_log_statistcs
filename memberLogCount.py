# coding:utf-8
import time
import pandas as pd
import sys
import os
from sqlalchemy import create_engine
from settings import output_base_dir, db_200_config, db_32_config
from groupStatisticsPlugins import gameChannelDay, gameHour, channelHour
from models import GameChannelDay, ChannelHour, GameHour
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def member_login_count_by_csv(filename):
    """
    将每日登录文件 按分组插件样式处理好
    """
    conn = 'mysql+mysqlconnector://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % db_32_config
    # 初始化数据库连接:
    my_engine = create_engine(conn, echo=False, )
    # 打开文件并且将login_time指定为时间格式
    df = pd.read_csv(filename, parse_dates=['login_time'])
    # if not groupType:
    #     groupType = (gameChannelDay, gameHour, ChannelHour)
    # 根据分组接口获得分组统计结果
    game_channel_day_data = gameChannelDay(df)
    pd.io.sql.to_sql(game_channel_day_data, GameChannelDay.__tablename__, my_engine, if_exists='append', index=False)
    # game_hour_data = gameHour(df)
    # pd.io.sql.to_sql(game_hour_data, GameHour.__tablename__, my_engine, if_exists='append', index=False)
    # channel_hour_data = channelHour(df)
    # pd.io.sql.to_sql(channel_hour_data, ChannelHour.__tablename__, my_engine, if_exists='append', index="mll_id")


def member_login_count_by_directory(dir):
    for file in os.listdir(dir):
        base = os.path.join(dir, file)
        if os.path.isdir(base):
            print("%s是目录" % file)
            member_login_count_by_directory(base)
        else:
            member_login_count_by_csv(base)
        time.sleep(1)

if __name__ == "__main__":
    s1 = time.time()
    member_login_count_by_csv(filename=r"/home/qy/pandas/test/csv_input/2016_9_11.csv")
    # member_login_count_by_directory(r"/home/qy/pandas/test/csv_input")
    s2 = time.time()
    print(s2 - s1)
