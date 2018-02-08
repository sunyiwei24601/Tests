# -*- coding: utf-8 -*-

__author__ = 'hand'

'''
 analyze the json to be tasks contains the information of all nodes
'''
class TaskAnalyzer():
    nodesTaskInfo = {}
    userid = 'unknown-user'
    taskid = 'unknown-task'
    '''{'11':{'in_pipes':[],'out_pipes':['out1'],'tasks':{'in_tasks':{},'out_tasks':{'11:out1':'22:in1'},'executed':'0','nodeOpts':{}}},
     '22':{}
     ...
    }
    '''
    @staticmethod
    #清理变量
    def clearGlobalVars():
        TaskAnalyzer.nodesTaskInfo = {}
        TaskAnalyzer.userid = 'unknown-user'
        TaskAnalyzer.taskid = 'unknown-task'
    #分析从java传来的数据
    @staticmethod
    def analyzeGraphJson(obj):
        try:
            source = obj.get('source','')
            nodes = source.get('nodes','')
            edges = source.get('edges','')

            for edge in edges:
                sourceNodeId = edge['source']
                targetNodeId = edge['target']
                #分别分配两个源数据的id
                sourceTaskAttrV = TaskAnalyzer.nodesTaskInfo.get(sourceNodeId,'')
                targetTaskAttrV = TaskAnalyzer.nodesTaskInfo.get(targetNodeId,'')
                #设置默认的属性
                if not sourceTaskAttrV:
                    sourceTaskAttrV = {'in_pipes':[],'out_pipes':[],'tasks':{'in_tasks':{},'out_tasks':{}},'executed':'0','nodeOpts':{}}
                    TaskAnalyzer.nodesTaskInfo[sourceNodeId] = sourceTaskAttrV
                if not targetTaskAttrV:
                    targetTaskAttrV = {'in_pipes':[],'out_pipes':[],'tasks':{'in_tasks':{},'out_tasks':{}},'executed':'0','nodeOpts':{}}
                    TaskAnalyzer.nodesTaskInfo[targetNodeId] = targetTaskAttrV

                '''
               1.append sourceAnchor value to out_pipes of sourceTaskAttrV if it has no this value
               2.append targetAnchor value to in_pipes of targetTaskAttrV if it has no this value
               '''
                sourceAnchor = edge['sourceAnchor']
                source_out_pipes = sourceTaskAttrV['out_pipes']
                if sourceAnchor not in source_out_pipes:
                    source_out_pipes.append(sourceAnchor)

                targetAnchor = edge['targetAnchor']
                target_in_pipes = targetTaskAttrV['in_pipes']
                if targetAnchor not in target_in_pipes:
                    target_in_pipes.append(targetAnchor)

                '''
               3.append 'sourceNodeId:sourceAnchor':'targetNodeId:targetAnchor' to 'out_tasks' dictionary of sourceTaskAttrV
               no matter if it has this key 'sourceNodeId:sourceAnchor' or not
               4.append 'sourceNodeId:sourceAnchor':'targetNodeId:targetAnchor' to 'in_tasks' dictionary of targetTaskAttrV
               no matter if it has this key 'sourceNodeId:sourceAnchor' or not
               '''

                #task_key和value是两个固定各式的字符串

                task_key = '%s:%s' % (sourceNodeId,sourceAnchor)
                task_value = '%s:%s' % (targetNodeId,targetAnchor)
                source_out_tasks = sourceTaskAttrV['tasks']['out_tasks']
                source_out_tasks[task_key] = task_value
                target_in_tasks = targetTaskAttrV['tasks']['in_tasks']
                target_in_tasks[task_key] = task_value

                '''
                5.get each nodeOpts from nodes of graph json and set this to the nodesTaskInfo if it has no related nodeOpts
               '''
                if not TaskAnalyzer.nodesTaskInfo[sourceNodeId].get('nodeOpts'):
                    source_nodeOpts = TaskAnalyzer.getNodeByNodeId(sourceNodeId,nodes)['nodeOpts']
                    TaskAnalyzer.nodesTaskInfo[sourceNodeId]['nodeOpts'] = source_nodeOpts
                if not TaskAnalyzer.nodesTaskInfo[targetNodeId].get('nodeOpts'):
                    target_nodeOpts = TaskAnalyzer.getNodeByNodeId(targetNodeId,nodes)['nodeOpts']
                    TaskAnalyzer.nodesTaskInfo[targetNodeId]['nodeOpts'] = target_nodeOpts
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            return 0
    #get node from nodes of graph json sent from java
    @staticmethod
    def getNodeByNodeId(id,nodes):
        for node in nodes:
            if node['id'] == id:
                return node

if __name__ == '__main__':
    jobj = {
    "guides": [],
    "source": {
        "nodes": [
            {
                "shape": "customNode",
                "x": 110,
                "y": 40,
                "anchorPoints": [
                    [
                        0.5,
                        1
                    ]
                ],
                "id": "11",
                "title": "hiveTable",
                "nodeOpts": {
                    "optsEntity": {
                        "dbname": "default",
                        "tablename": "sample_svm_data2"
                    },
                    "comName": "hiveTable",
                    "comCode": "hiveTable"
                }
            },
            {
                "shape": "customNode",
                "x": 110,
                "y": 150,
                "anchorPoints": [
                    [
                        0.5,
                        0
                    ],
                    [
                        0.5,
                        1
                    ]
                ],
                "id": "22",
                "title": "随机森林",
                "nodeOpts": {
                    "optsEntity": {
                        "featuresCol": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16",
                        "labelCol": "label"
                    },
                    "comName": "随机森林",
                    "comCode": "randomForestCom"
                }
            },
            {
                "shape": "customNode",
                "x": 160,
                "y": 260,
                "anchorPoints": [
                    [
                        0.25,
                        0
                    ],
                    [
                        0.5,
                        0
                    ],
                    [
                        0.5,
                        1
                    ]
                ],
                "id": "33",
                "title": "预测",
                "nodeOpts": {
                    "optsEntity": {
                        "probabilityCol": "probability",
                        "featuresCol": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16",
                        "predictionCol": "prediction",
                        "originalCol":"label"
                    },
                    "comName": "预测",
                    "comCode": "predictionCom"
                }
            },
            {
                "shape": "customNode",
                "x": 280,
                "y": 40,
                "anchorPoints": [
                    [
                        0.5,
                        1
                    ]
                ],
                "id": "44",
                "title": "hiveTable",
                "nodeOpts": {
                    "optsEntity": {
                        "dbname": "default",
                        "tablename": "sample_svm_data2"
                    },
                    "comName": "hiveTable",
                    "comCode": "hiveTable"
                }
            }
        ],
        "edges": [
            {
                "sourceAnchor": "out1",
                "targetAnchor": "in1",
                "shape": "polyLineFlow",
                "source": "11",
                "id": "80492c4f",
                "controlPoints": [
                    {
                        "x": 150,
                        "y": 80.5
                    },
                    {
                        "x": 150,
                        "y": 149.5
                    }
                ],
                "target": "22"
            },
            {
                "sourceAnchor": "out1",
                "targetAnchor": "in1",
                "shape": "polyLineFlow",
                "source": "22",
                "id": "ac9cd7f7",
                "controlPoints": [
                    {
                        "x": 150,
                        "y": 190.5
                    },
                    {
                        "x": 179.75,
                        "y": 259.5
                    }
                ],
                "target": "33"
            },
            {
                "sourceAnchor": "out1",
                "targetAnchor": "in2",
                "shape": "polyLineFlow",
                "source": "44",
                "id": "c2d54467",
                "controlPoints": [
                    {
                        "x": 320,
                        "y": 80.5
                    },
                    {
                        "x": 200,
                        "y": 259.5
                    }
                ],
                "target": "33"
            }
        ]
    }
}
    jobj2 = {
    "guides":[

    ],
    "source":{
        "nodes":[
            {
                "shape":"customNode",
                "x":150,
                "y":40,
                "id":"libsvm11",
                "title":"libsvm文件",
                "nodeOpts":{
                    "optsEntity":{
                        "dfspath":"/glzheng/spark_example_data/sample_libsvm_data.txt"
                    },
                    "comName":"libsvm文件",
                    "comCode":"libsvmCom"
                }
            },
            {
                "shape":"customNode",
                "x":340,
                "y":40,
                "id":"libsvm22",
                "title":"libsvm文件",
                "nodeOpts":{
                    "optsEntity":{
                        "dfspath":"/glzheng/spark_example_data/sample_libsvm_data.txt"
                    },
                    "comName":"libsvm文件",
                    "comCode":"libsvmCom"
                }
            },
            {
                "shape":"customNode",
                "x":210,
                "y":160,
                "id":"rf11",
                "title":"随机森林",
                "nodeOpts":{
                    "optsEntity":{
                        "optsEntity": {
                        "featuresCol": "feature",
                        "labelCol": "label"
                    },
                    "comName": "随机森林",
                    "comCode": "randomForestCom"
                    },
                    "comName":"随机森林",
                    "comCode":"randomForestCom"
                }
            },
            {
                "shape":"customNode",
                "x":310,
                "y":240,
                "id":"prediction11",
                "title":"预测",
                "nodeOpts":{
                    "optsEntity":{
                        "probabilityCol": "probability",
                        "featuresCol": "feature",
                        "predictionCol": "prediction",
                        "originalCol":"label"
                    },
                    "comName":"预测",
                    "comCode":"predictionCom"
                }
            },
            {
                "shape":"customNode",
                "x":310,
                "y":360,
                "id":"evaluation11",
                "title":"多分类评估",
                "nodeOpts":{
                    "optsEntity":{
                        "metricName":"f1",
                        "labelCol":"label",
                        "predictionCol":"prediction"
                    },
                    "comName":"多分类评估",
                    "comCode":"multiclassClassificationEvaluatorCom"
                }
            }
        ],
        "edges":[
            {
                "sourceAnchor":"out1",
                "targetAnchor":"in1",
                "shape":"polyLineFlow",
                "source":"libsvm11",
                "id":"1ba7734e",
                "controlPoints":[
                    {
                        "x":190,
                        "y":80.5
                    },
                    {
                        "x":250,
                        "y":159.5
                    }
                ],
                "target":"rf11"
            },
            {
                "sourceAnchor":"out1",
                "targetAnchor":"in1",
                "shape":"polyLineFlow",
                "source":"rf11",
                "id":"03286238",
                "controlPoints":[
                    {
                        "x":250,
                        "y":200.5
                    },
                    {
                        "x":329.75,
                        "y":239.5
                    }
                ],
                "target":"prediction11"
            },
            {
                "sourceAnchor":"out1",
                "targetAnchor":"in2",
                "shape":"polyLineFlow",
                "source":"libsvm22",
                "id":"c4293752",
                "controlPoints":[
                    {
                        "x":380,
                        "y":80.5
                    },
                    {
                        "x":350,
                        "y":239.5
                    }
                ],
                "target":"prediction11"
            },
            {
                "sourceAnchor":"out1",
                "targetAnchor":"in1",
                "shape":"polyLineFlow",
                "source":"prediction11",
                "id":"e425b720",
                "controlPoints":[
                    {
                        "x":350,
                        "y":280.5
                    },
                    {
                        "x":350,
                        "y":359.5
                    }
                ],
                "target":"evaluation11"
            }
        ]
    }
}
    TaskAnalyzer.analyzeGraphJson(jobj2)
    lines = TaskAnalyzer.nodesTaskInfo
    for line in lines:
        print('%s %s' % (line,lines[line]))
    # print(TaskAnalyzer.nodesTaskInfo)




