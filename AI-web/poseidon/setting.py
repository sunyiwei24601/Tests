# _*_ coding: utf-8 _*_

#调试模式是否开启
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
#session必须要设置key
SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#mysql数据库连接信息,这里改为自己的账号
SQLALCHEMY_DATABASE_URI = "mysql://root:a123@10.211.54.196:3306/world"

#hadoop client
HADOOP_CLIENT_URL = "http://192.168.11.188:50070/"
# HADOOP_CLIENT_URL = "http://192.168.11.176:50070/"

# LOGS PATH:used to store the logs of ai task and this path is local path
LOG_DIR = "/storeage/glzheng/windowspy/poseidon_ai_ware/tasks"

#task path: used to store the model generated during task and this path is hdfs path
TASK_DIR = "/tmp/poseidon_ai/tasks"
INTERMEDIA_HIVE_DB = "intermedia"
# 存放聚类评估的表
INTERMEDIA_HIVE_TABLE = "cluster_evaluator"

# mysql setting
MYSQL_HOST= "192.168.11.189"
MYSQL_USER="dsmp"
MYSQL_PASSWD="dsmp"
MYSQL_DB = "dsmp"


# insecureHdfsClient setting
INSECUREHDS_CLIENT_NAME = "glzheng"

# hive setting
HIVE_USER = "hadoop"
HIVE_HOST = "192.168.11.189"
HIVE_PORT = "10000"

# hdfs setting
HDFS_HOST = "http://dasrv03.novalocal:50070/"
HDFS_USER = "glzheng"

# the path which convert dataframe to csv
DFTOCSV_PATH = "/glzheng/df2csv_test222.csv"

# spark setting
SPARK_HOME = "/usr/hdp/2.5.3.0-37/spark2/"
PYSPARK_PATH = "/storeage/glzheng/anaconda3/envs/python27_glzheng/bin/python"
APP_NAME = "poseidon"
MASTER = "yarn"
UI_PORT = "4444"
DIST_FILES = "file:/usr/hdp/2.5.3.0-37/spark2/python/lib/pyspark.zip,file:/usr/hdp/2.5.3.0-37/spark2/python/lib/py4j-0.10.3-src.zip"
EXECUTORENV_KEY = "PYTHONPATH"
EXECUTORENV_VALUE = "pyspark.zip:py4j-0.10.3-src.zip"
# SPARK_SQL_WAREHOUSE_DIR = "/apps/hive/warehouse"

