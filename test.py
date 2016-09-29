# coding:utf-8
import time
import pandas as pd
import sys
import os
import redis
import settings
from sqlalchemy import create_engine
from settings import output_base_dir, db_200_config, db_32_config
from groupStatisticsPlugins import gameChannelDay, gameHour, channelHour
from models import GameChannelDay, ChannelHour, GameHour
from lookupName import findname, findChannelPath, seachRedis, seachLocalDatabase
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import mysql.connector

if __name__ == "__main__":
    cnn=mysql.connector.connect(**db_32_config)
