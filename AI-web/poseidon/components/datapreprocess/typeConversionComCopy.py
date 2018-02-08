# -*- coding: utf-8 -*-

from pyspark.sql import Column, Row
from pyspark.sql.types import DoubleType, IntegerType, StringType, ArrayType
from poseidon.util.sparkUtil import SparkUtil
from pyspark.sql import DataFrame


class TypeConversionCom():
    """
    对数据进行类型转换
    """
    def __init__(self , tid, jobj, ins, outs):
        self.res = {}
        self.spark = SparkUtil.getSpark()[1]
        self.comOpts = jobj.get('optsEntity')  # user-defined opts
        self.column_double = self.comOpts.get('column_double', '')  # 获取用户输入需要转换为double类型的字段名
        self.column_int = self.comOpts.get('column_int', '')  # 获取用户输入需要转换为int类型的字段名
        self.column_string = self.comOpts.get('column_string', '')  # 获取用户输入需要转换为string类型的字段名
        self.column_list = self.comOpts.get('column_list', '')  # 获取用户需要转换为list类型的字段名
        self.ins = ins
        self.outs = outs
        self.in1 = ins.get('in1', '')
        self.tid = tid
        self.jobj = jobj

    def typeConversion(self, f):
        try:
            f.write('\n#####check params in typeConversion in TypeConversionCom:\n')
            f.write('tid:%s\n' % self.tid)
            f.write('jobj:%s\n' % self.jobj.__str__())
            f.write('ins:%s\n' % self.ins.__str__())
            f.write('outs:%s\n' % self.outs.__str__())


            if type(self.in1) == DataFrame:
                return self.df_conversion(self.spark, self.column_double, self.column_int, self.column_string, self.column_list,
                                                self.tid, self.in1, self.outs, self.res)
            else:
                db_table = self.in1.split(":")[1]
                sql_script = "select * from %s" % db_table
                return self.sql_conversion(self.spark, sql_script, self.column_double, self.column_int, self.column_string,
                                                        self.column_list, self.tid, self.in1, self.outs, self.res)

        except Exception as e:
            f.close()
            print("*****************Sorry:\n %s" % e)
            return 0

    @classmethod
    def sql_conversion(cls, spark, sql_script, column_double, column_int, column_string, column_list, tid, in1, outs, res):
        """
        捕获到sql脚本，执行此方法
        """
        global df2,x

        df = spark.sql(sql_script)
        # 需要转换为double的类型
        if column_double:
            column_input_list = column_double.split(",")
            for col in column_input_list:
                col_double = 'df.%s.astype(DoubleType())' % col
                # exec_str = compile(col_double, '', 'exec')
                # exec (exec_str)
                col_double = eval(col_double)
                new_col = "new_" + col
                df2 = df.withColumn(new_col, col_double)
                # df2.show()
        # 需要转换为int的类型
        if column_int:
            column_input_list = column_int.split(",")
            for col in column_input_list:
                col_int = 'df.%s.astype(IntegerType())' % col
                # exec_str = compile(col_int, '', 'exec')
                # exec (exec_str)
                col_int = eval(col_int)
                new_col = "new_" + col
                if df2:
                    df2 = df2.withColumn(new_col, col_int)
                else:
                    df2 = df.withColumn(new_col, col_int)
                df2.show()
        # 需要转换为string的类型
        if column_string:
            column_input_list = column_string.split(",")
            for col in column_input_list:
                col_string = 'df.%s.astype(StringType())' % col
                # exec_str = compile(str, '', 'exec')
                # exec (exec_str)
                col_string = eval(col_string)
                new_col = "new_" + col
                if df2:
                    df2 = df2.withColumn(new_col, col_string)
                else:
                    df2 = df.withColumn(new_col, col_string)
        """
        # 需要转换为list的类型
        if column_list:
            column_input_list = column_list.split(",")
            for col in column_input_list:
                new_rdd = df.rdd.map(cls.mapfunc(x, col))
                df2 = spark.createDataFrame(new_rdd)

                # rows = df.select(col).collect() # 获取所有col字段的数据以数组形式保存
                # for row in rows:
                #     data = row[col] # 单个字段内的一条数据
                #     data_list = eval(data) # 转换为list格式
                #     new_col = "new_" + col
                #     str = 'Row(%s=data_list)' % ("new_"+col)
                #     new_row = eval(str)
        """

        if 'out1' in outs:
            key = '%s:%s' % (tid, 'out1')
            res[key] = df2
        return res

    @classmethod
    def df_conversion(cls, spark, column_double, column_int, column_string, column_list, tid, in1, outs, res):
        """
        捕获到df格式，执行此方法
        """
        global df2
        df = in1
        # 需要转换为double的类型
        if column_double:
            column_input_list = column_double.split(",")
            for col in column_input_list:
                col_double = 'df.%s.astype(DoubleType())' % col
                # exec_str = compile(str, '', 'exec')
                # exec(exec_str)
                col_double = eval(col_double)
                new_col = "new_"+col
                df2 = df.withColumn(new_col, col_double)

        # 需要转换为int的类型
        if column_int:
            column_input_list = column_int.split(",")
            for col in column_input_list:
                col_int = 'df.%s.astype(IntegerType())' % col
                # exec_str = compile(str, '', 'exec')
                # exec(exec_str)
                col_int = eval(col_int)
                new_col = "new_"+col
                if df2:
                    df2 = df2.withColumn(new_col, col_int)
                else:
                    df2 = df.withColumn(new_col, col_int)

        # 需要转换为string的类型
        if column_string:
            column_input_list = column_string.split(",")
            for col in column_input_list:
                col_string = 'df.%s.astype(StringType())' % col
                # exec_str = compile(str, '', 'exec')
                # exec(exec_str)
                col_string = eval(col_string)
                new_col = "new_"+col
                if df2:
                    df2 = df2.withColumn(new_col, col_string)
                else:
                    df2 = df.withColumn(new_col, col_string)
        """
        # 需要转换为list的类型
        if column_list:
            column_input_list = column_list.split(",")
            for col in column_input_list:
                new_rdd = df.rdd.map(cls.mapfunc(x, col))
                df2 = spark.createDataFrame(new_rdd)
        """

        if 'out1' in outs:
            key = '%s:%s' % (tid, 'out1')
            res[key] = df2
        return res
    """
    @staticmethod
    def mapfunc(x, col):
        data_list = eval(x.col)
        row = 'Row(%s=data_list)' % ("new_"+col)
        row = eval(row)
        return row
    """

