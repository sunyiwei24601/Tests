# -*- coding: utf-8 -*-

from pyspark.sql import Column, Row
from pyspark.sql.types import DoubleType, IntegerType, StringType, ArrayType
from poseidon.util.sparkUtil import SparkUtil
from pyspark.sql import DataFrame


class TypeConversionCom():
    """
    对数据进行类型转换
    """

    @staticmethod
    def typeConversionComProcesser(tid, jobj, ins, outs, f, username, taskname):
        try:
            f.write('\n#####正在检查类型转换组件参数:\n')
            f.write('tid:%s\n' % tid)
            f.write('jobj:%s\n' % jobj.__str__())
            f.write('ins:%s\n' % ins.__str__())
            f.write('outs:%s\n' % outs.__str__())
            res = {}
            spark = SparkUtil.getSpark()[1]
            comOpts = jobj.get('optsEntity')  # user-defined opts
            column_double = comOpts.get('column_double', '') # 获取用户输入需要转换为double类型的字段名
            column_int = comOpts.get('column_int', '') # 获取用户输入需要转换为int类型的字段名
            column_string = comOpts.get('column_string', '') # 获取用户输入需要转换为string类型的字段名
            column_list = comOpts.get('column_list', '') # 获取用户需要转换为list类型的字段名
            # if_save = comOpts.get('if_save', '').lower() # 获取用户输入是否保存的标记
            in1 = ins.get('in1', '')

            if type(in1) == DataFrame:
                return TypeConversionCom.df_conversion(column_double, column_int, column_string, column_list,
                                                       tid, in1, outs, res, f)
            else:
                db_table = in1.split(":")[1]
                sql_script = "select * from %s" % db_table
                return TypeConversionCom.sql_conversion(spark, sql_script, column_double, column_int, column_string,
                                                        column_list, tid, in1, outs, res, f)

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0

    @staticmethod
    def sql_conversion(spark, sql_script, column_double, column_int, column_string, column_list, tid, in1, outs, res, f):
        """
        捕获到sql脚本，执行此方法
        """
        df = spark.sql(sql_script)
        # df.show()
        # 如果用户什么都不输入
        if column_double == "" and column_int == "" and column_string == "" and column_list == "":
            if 'out1' in outs or 'out2' in outs:
                key = '%s:%s' % (tid, 'out1')
                res[key] = df
                # df.show()
            return res
        else:
            return TypeConversionCom.convert(column_double, column_int, column_string,column_list, tid, df, outs, res, f)

    @staticmethod
    def df_conversion(column_double, column_int, column_string, column_list, tid, in1, outs, res, f):
        """
        捕获到df格式，执行此方法
        """
        df = in1
        df.show()
        # 如果用户什么都不输入
        if column_double == "" and column_int == "" and column_string == "" and column_list == "":
            if 'out1' in outs or 'out2' in outs:
                key = '%s:%s' % (tid, 'out1')
                res[key] = df
            return res
        else:
            return TypeConversionCom.convert(column_double, column_int, column_string, column_list, tid, df, outs, res, f)

    @staticmethod
    def convert(column_double, column_int, column_string, column_list, tid, df, outs, res, f):
        """
        字段类型转换
        :param column_double:
        :param column_int:
        :param column_string:
        :param column_list:
        :param tid:
        :param df:
        :param outs:
        :param res:
        :param f:
        :return:
        """

        # 需要转换为double的类型
        if column_double:
            f.write("\n将输入数据类型转换为浮点型...\n")
            column_input_list = column_double.split(",")
            for col in column_input_list:
                # 取消保留原列的功能
                ## col_del.append(col)
                col_double = 'df.%s.astype(DoubleType())' % col
                col_double = eval(col_double)
                # 取消保留原列的功能
                ## new_col = "new_" + col  # 创建新的字段名
                df = df.withColumn(col, col_double)

        # 需要转换为int的类型
        if column_int:
            f.write("\n将输入数据类型转换为整型...\n")
            column_input_list = column_int.split(",")
            for col in column_input_list:
                # 取消保留原列的功能
                ## col_del.append(col)
                col_int = 'df.%s.astype(IntegerType())' % col
                col_int = eval(col_int)
                # 取消保留原列的功能
                ## new_col = "new_" + col  # 创建新的字段名
                df = df.withColumn(col, col_int)

        # 需要转换为string的类型
        if column_string:
            f.write("\n将输入数据类型转换为字符串类型...\n")
            column_input_list = column_string.split(",")
            for col in column_input_list:
                # 取消保留原列的功能
                ## col_del.append(col)
                col_string = 'df.%s.astype(StringType())' % col
                col_string = eval(col_string)
                # 取消保留原列的功能
                ## new_col = "new_" + col  # 创建新的字段名
                df = df.withColumn(col, col_string)


        if 'out1' in outs or 'out2' in outs:
            key = '%s:%s' % (tid, 'out1')
            df.show()
            res[key] = df
        f.write('\n##### 类型转换成功！\n')
        return res