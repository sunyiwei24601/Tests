# -*- coding: utf-8 -*-
#convert excel to libsvm file
from numpy import *
import xlrd
from poseidon.util.commonUtil import CommonUtil
'''
inpath:local path excel file
    note:the last column must be label column and all the other columns are feature columns
outpath:hdfs path of libsvm file is going to be generated
    labeled_outpath:records have label
    unlabeled_outpath:records have not label, but we set the label to the default value 110, if
                      have no unlabeled data, this file will be empty.
labelIndex:label index
    format:real-number
featuresIndex:features index
    format:[1,2]
'''
def excel2libsvm(inpath,sheetIndex,labeled_outpath, unlabeled_outpath):
    client = CommonUtil.insecureHdfsClient('default','default')

    CommonUtil.delIfExistsInHdfs(client,labeled_outpath)
    CommonUtil.delIfExistsInHdfs(client,unlabeled_outpath)
    labeled_out = client.write(labeled_outpath)
    unlabeled_out = client.write(unlabeled_outpath)
    try:
        with client.write(labeled_outpath) as labeled_out,client.write(unlabeled_outpath) as unlabeled_out:
            data = xlrd.open_workbook(inpath)
            # labeled_out = open(labeled_outpath, 'w')
            # unlabeled_out = open(unlabeled_outpath, 'w')
            table = data.sheets()[sheetIndex]
            nrows = table.nrows #行数
            for x in range(nrows):
                row =table.row_values(x)
                labelstr = str(row[-1])
                featuresstr = ''

                for i in range(len(row)-1):
                    if str(row[i]) == '':
                        continue
                    featuresstr += str(i+1)+':'+str(row[i])+' '

                if labelstr == '':
                    labelstr = str(110)
                    line = labelstr+' '+featuresstr
                    #write line into the libsvm file
                    unlabeled_out.write(line+'\n')
                else:
                    line = labelstr+' '+featuresstr
                    #write line into the libsvm file
                    labeled_out.write(line+'\n')
    finally:
        pass

if __name__ == '__main__':
    inpath = '/storeage/glzheng/risk.xlsx'
    sheetIndex = 4
    labeled_outpath = '/glzheng/tmp/risk_labeled_out.txt'
    unlabeled_outpath = '/glzheng/tmp/risk_unlabeled_out.txt'
    excel2libsvm(inpath,sheetIndex,labeled_outpath,unlabeled_outpath)