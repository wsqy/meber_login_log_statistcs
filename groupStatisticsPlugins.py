# encoding=utf-8
import pandas as pd
import time
from lookupName import findname, findChannelPath


def topChannel(id_path):

    if (not id_path) or (len(id_path) < 2):
        return 0
    return id_path.split(",")[1]


def group_by_day(datetime):
    """将时间格式转化为年_月_日 的形式
    2016/9/11 9:59:02 --> 2016-9-11
    """
    time_form = str(datetime.year) + "-" + str(datetime.month) + "-" + str(datetime.day)
    return time_form


def group_by_hour(datetime):
    """将时间格式转化为年-月-日 时 的形式
    2016/9/11 9:59:02 --> 2016-9-11 9
    """
    time_form = str(datetime.year) + "-" + str(datetime.month) + "-" + str(datetime.day) + "-" + str(datetime.hour)
    return time_form


def group_by_time(datetime):
    """将时间格式转化为时刻的形式
    2016/9/11 9:59:02 --> 9
    """
    return datetime.hour


def gameChannelDay(df):
    """将DataFrame object 按渠道,游戏,粒度为天进行统计
    """
    login_data = group_by_day(df.iloc[0]["login_time"])
    dataframe = []
    col = ["mll_second_id", "channel_id", "channel_name", "top_channel_id", "top_channel_name",
           "game_id", "game_name", "mll_date", "mll_count", "mll_create_time",
           "mll_update_time", "mll_status", ]
    game_channel_group = df.groupby(["gameid", "channel_id"])
    for id, group in game_channel_group:
        if len(group) != 0:
            top_channel_id = topChannel(findChannelPath(id[1]))
            data_line = {
                "mll_second_id": 0,
                "channel_id": id[1],
                "channel_name": findname("channel", id[1]),
                "top_channel_id": top_channel_id,
                "top_channel_name": findname("channel", top_channel_id),
                "game_id": id[0],
                "game_name": findname("game", id[0]),
                "mll_date": login_data,
                "mll_count": len(group),
                "mll_create_time": int(time.time()),
                "mll_update_time": int(time.time()),
                "mll_status": 1,
            }
            dataframe.append(data_line)
    member_count = pd.DataFrame(dataframe, columns=col)
    return member_count


def gameChannelHour(df):
    """
    将DataFrame object 按渠道,游戏,粒度为小时进行统计
    """
    pass


def gameHour(df):
    """
    将DataFrame object 按游戏, 粒度为小时进行统计
    """
    login_data = group_by_day(df.iloc[0]["login_time"])
    df_hour = df.groupby(df["login_time"].apply(group_by_time))
    col = ["mll_second_id", "game_id", "game_name", "mll_date", "mll_datetime",
           "mll_count", "mll_create_time", "mll_update_time", "mll_status"]
    dataframe = []
    for hour_name, hour_group in df_hour:
        if len(hour_group) != 0:
            game_group = hour_group.groupby("gameid")
            for id, group in game_group:
                if len(group) != 0:
                    id = int(id)
                    data_line = {
                        "mll_second_id": 0,
                        "game_id": id,
                        "game_name": findname("game", id),
                        "mll_date": login_data,
                        "mll_datetime": hour_name,
                        "mll_count": len(group),
                        "mll_create_time": int(time.time()),
                        "mll_update_time": int(time.time()),
                        "mll_status": 1,
                    }
                    dataframe.append(data_line)
    member_count = pd.DataFrame(dataframe, columns=col,)
    return member_count


def channelHour(df):
    """
    将DataFrame object 按渠道, 粒度为小时进行统计
    """
    login_data = group_by_day(df.iloc[0]["login_time"])
    df_hour = df.groupby(df["login_time"].apply(group_by_time))
    col = ["mll_second_id", "channel_id", "channel_name", "top_channel_id", "top_channel_name",
           "mll_date", "mll_datetime", "mll_count", "mll_create_time", "mll_update_time", "mll_status"]
    dataframe = []
    for hour_name, hour_group in df_hour:
        if len(hour_group) != 0:
            channel_group = hour_group.groupby("channel_id")
            for id, group in channel_group:
                if len(group) != 0:
                    top_channel_id = topChannel(findChannelPath(id))
                    data_line = {
                        "mll_second_id": 0,
                        "channel_id": id,
                        "channel_name": findname("channel", id),
                        "top_channel_id": top_channel_id,
                        "top_channel_name": findname("channel", top_channel_id),
                        "mll_date": login_data,
                        "mll_datetime": hour_name,
                        "mll_count": len(group),
                        "mll_create_time": int(time.time()),
                        "mll_update_time": int(time.time()),
                        "mll_status": 1,
                    }
                    dataframe.append(data_line)
    member_count = pd.DataFrame(dataframe, columns=col)
    return member_count
