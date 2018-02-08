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
            f.write('\n#####check params in typeConversion in TypeConversionCom:\n')
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
            if_save = comOpts.get('if_save', '').lower() # 获取用户输入是否保存的标记
            in1 = ins.get('in1', '')

            if type(in1) == DataFrame:
                return TypeConversionCom.df_conversion(spark, column_double, column_int, column_string, column_list,
                                                       if_save, tid, in1, outs, res, f)
            else:
                db_table = in1.split(":")[1]
                sql_script = "select * from %s" % db_table
                return TypeConversionCom.sql_conversion(spark, sql_script, column_double, column_int, column_string,
                                                        column_list, if_save, tid, in1, outs, res, f)

        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            f.close()
            return 0

    @staticmethod
    def sql_conversion(spark, sql_script, column_double, column_int, column_string, column_list, if_save, tid, in1, outs, res, f):
        """
        捕获到sql脚本，执行此方法
        """
        df2 = None
        df = spark.sql(sql_script)
        col_del = [] # 待删除的原字段
        # df.show()
        # 需要转换为double的类型
        if column_double:
            f.write("\n now converts datatype to DoubleType \n")
            column_input_list = column_double.split(",")
            for col in column_input_list:
                col_del.append(col)
                col_double = 'df.%s.astype(DoubleType())' % col
                # exec_str = compile(col_double, '', 'exec')
                # exec (exec_str)
                col_double = eval(col_double)
                new_col = "new_" + col # 创建新的字段名
                df2 = df.withColumn(new_col, col_double)
                # df2.show()

        # 需要转换为int的类型
        if column_int:
            f.write("\n now converts datatype to IntegerType \n")
            column_input_list = column_int.split(",")
            for col in column_input_list:
                col_del.append(col)
                col_int = 'df.%s.astype(IntegerType())' % col
                # exec_str = compile(col_int, '', 'exec')
                # exec (exec_str)
                col_int = eval(col_int)
                new_col = "new_" + col # 创建新的字段名
                if df2:
                    df2 = df2.withColumn(new_col, col_int)
                else:
                    df2 = df.withColumn(new_col, col_int)
                # df2.show()
                # df2.printSchema()

        # 需要转换为string的类型
        if column_string:
            f.write("\n now converts datatype to StringType \n")
            column_input_list = column_string.split(",")
            for col in column_input_list:
                col_del.append(col)
                col_string = 'df.%s.astype(StringType())' % col
                # exec_str = compile(str, '', 'exec')
                # exec (exec_str)
                col_string = eval(col_string)
                new_col = "new_" + col # 创建新的字段名
                if df2:
                    df2 = df2.withColumn(new_col, col_string)
                else:
                    df2 = df.withColumn(new_col, col_string)
                # df2.show()
                # df2.printSchema()

        """
        # 需要转换为list的类型
        if column_list:
            f.write("\n now converts datatype to ArrayType \n")
            column_input_list = column_list.split(",")
            for col in column_input_list:
                col_del.append(col)
                print("i am coming!!!!!!!!!!!!!!!!!!!!")
                # df_col = df.select(col)
                # df_col.show()
                # new_rdd = df_col.rdd.map(TypeConversionCom.mapfunc)
                # print("O"*80)
                # df2 = spark.createDataFrame(new_rdd)

                # rows = df.select(col).collect() # 获取所有col字段的数据以数组形式保存
                # for row in rows:
                #     data = row[col] # 单个字段内的一条数据
                #     data_list = eval(data) # 转换为list格式
                #     new_col = "new_" + col
                #     str = 'Row(%s=data_list)' % ("new_"+col)
                #     new_row = eval(str)
        """
        # 是否删除原列
        if if_save == "n":
            for col_d in col_del:
                df2 = df2.drop(col_d)
        elif if_save == "y" or "":
            pass

        if 'out1' in outs or 'out2' in outs:
        # if 'out1' in outs:
            key = '%s:%s' % (tid, 'out1')
            res[key] = df2
            df2.show()
            # df2.printSchema()
        return res

    @staticmethod
    def df_conversion(spark, column_double, column_int, column_string, column_list, if_save, tid, in1, outs, res, f):
        """
        捕获到df格式，执行此方法
        """

        df2 = None
        df = in1
        col_del = []  # 待删除的原字段
        df.show()
        # 需要转换为double的类型
        if column_double:
            f.write("\n now converts datatype to DoubleType \n")
            column_input_list = column_double.split(",")
            for col in column_input_list:
                col_del.append(col)
                col_double = 'df.%s.astype(DoubleType())' % col
                # exec_str = compile(str, '', 'exec')
                # exec(exec_str)
                col_double = eval(col_double)
                new_col = "new_"+col # 创建新的字段名
                df2 = df.withColumn(new_col, col_double)

        # 需要转换为int的类型
        if column_int:
            f.write("\n now converts datatype to IntegerType \n")
            column_input_list = column_int.split(",")
            for col in column_input_list:
                col_del.append(col)
                col_int = 'df.%s.astype(IntegerType())' % col
                # exec_str = compile(str, '', 'exec')
                # exec(exec_str)
                col_int = eval(col_int)
                new_col = "new_"+col # 创建新的字段名
                if df2:
                    df2 = df2.withColumn(new_col, col_int)
                else:
                    df2 = df.withColumn(new_col, col_int)

        # 需要转换为string的类型
        if column_string:
            f.write("\n now converts datatype to StringType \n")
            column_input_list = column_string.split(",")
            for col in column_input_list:
                col_del.append(col)
                col_string = 'df.%s.astype(StringType())' % col
                # exec_str = compile(str, '', 'exec')
                # exec(exec_str)
                col_string = eval(col_string)
                new_col = "new_"+col # 创建新的字段名
                if df2:
                    df2 = df2.withColumn(new_col, col_string)
                else:
                    df2 = df.withColumn(new_col, col_string)
        """
        # 需要转换为list的类型
        if column_list:
            f.write("\n now converts datatype to ArrayType \n")
            column_input_list = column_list.split(",")
            for col in column_input_list:
                new_rdd = df.rdd.map(TypeConversionCom.mapfunc)
                df2 = spark.createDataFrame(new_rdd)
        """
        # 是否删除原列
        if if_save == "n":
            for col_d in col_del:
                df2 = df2.drop(col_d)
        elif if_save == "y" or "":
            pass

        if 'out1' in outs or 'out2' in outs:
        # if 'out1' in outs:
            key = '%s:%s' % (tid, 'out1')
            # df2.show()
            res[key] = df2
        return res
    """
    @staticmethod
    def mapfunc(x):
        row = Row()
        # data_list = eval(x.col)
        # row = 'Row(%s=data_list)' % ("new_"+col)
        # row = eval(row)
        return row
    """