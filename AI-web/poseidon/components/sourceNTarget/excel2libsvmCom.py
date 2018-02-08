# -*- coding: utf-8 -*-
'''
specify the excel file path as a data source and convert it to a libsvm file,return the path of libsvm file in hdfs
'''
from poseidon.util.sparkUtil import SparkUtil
from poseidon.util.commonUtil import CommonUtil
import xlrd

class Excel2libsvmCom():

    def __init__(self):
        pass
    '''
    tid:the node id
    jobj:options ie attributes of this component
        inpath:local path of excel file
        sheetIndex:the sheet index of the excel file
        labeled_outpath:file contains labeled records
        unlabeled_outpath:file contains unlabeled records
    outs is a array contains:
        out1      return path of libsvm file which contains labeled records
        out2      return path of libsvm file which coatains unlabeled records
    '''
    @staticmethod
    def excel2libsvmConverter(tid, jobj, ins, outs,f):
        try:
            f.write('\n#####正在检查excel2libsvm组件参数:\n')
            f.write('tid:%s\n'%tid)
            f.write('jobj:%s\n'%jobj.__str__())
            f.write('ins:%s\n'%ins.__str__())
            f.write('outs:%s\n'%outs.__str__())
            res = {}
            comOpts = jobj.get('optsEntity') #user-defined opts

            inpath = comOpts.get('inpath','')
            sheetIndex = comOpts.get('sheetIndex','')
            labeled_outpath = comOpts.get('labeled_outpath','')
            unlabeled_outpath = comOpts.get('unlabeled_outpath','')


            #generate the libsvm file by excel file
            CommonUtil.excel2libsvm(inpath,sheetIndex,labeled_outpath,unlabeled_outpath)

            if 'out1' in outs:
                key = '%s:%s' % (tid,'out1')
                res[key] = 'libsvm:%s' % labeled_outpath
            if 'out2' in outs:
                key = '%s:%s' % (tid,'out2')
                res[key] = 'libsvm:%s' % unlabeled_outpath
            f.write('\n#####excel2libsvm组件输出为:\n%s' % res.__str__())
            return res
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            # f.close()
            return 0



