# -*- coding: utf-8 -*-

__author__ = 'hand'

'''
 analyze the json to be tasks contains the information of all nodes
'''
class TaskAnalyzer():
    nodesTaskInfo = {}
    username = 'unknown-user'
    taskname = 'unknown-task'
    '''{'11':{'in_pipes':[],'out_pipes':['out1'],'tasks':{'in_tasks':[],'out_tasks':[{'11:out1':'22:in1'}],'executed':'0','nodeOpts':{}}},
     '22':{}
     ...
    }
    '''
    @staticmethod
    def clearGlobalVars():
        TaskAnalyzer.nodesTaskInfo = {}
        TaskAnalyzer.username = 'unknown-user'
        TaskAnalyzer.taskname = 'unknown-task'
    @staticmethod
    def analyzeGraphJson(obj):
        try:
            source = obj.get('source','')
            nodes = source.get('nodes','')
            edges = source.get('edges','')

            for edge in edges:
                sourceNodeId = edge['source']
                targetNodeId = edge['target']
                sourceTaskAttrV = TaskAnalyzer.nodesTaskInfo.get(sourceNodeId,'')
                targetTaskAttrV = TaskAnalyzer.nodesTaskInfo.get(targetNodeId,'')
                if not sourceTaskAttrV:
                    sourceTaskAttrV = {'in_pipes':[],'out_pipes':[],'tasks':{'in_tasks':[],'out_tasks':[]},'executed':'0','nodeOpts':{}}
                    TaskAnalyzer.nodesTaskInfo[sourceNodeId] = sourceTaskAttrV
                if not targetTaskAttrV:
                    targetTaskAttrV = {'in_pipes':[],'out_pipes':[],'tasks':{'in_tasks':[],'out_tasks':[]},'executed':'0','nodeOpts':{}}
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
               3.append 'sourceNodeId:sourceAnchor':'targetNodeId:targetAnchor' dictionary to 'out_tasks' array of sourceTaskAttrV
               4.append 'sourceNodeId:sourceAnchor':'targetNodeId:targetAnchor' dictionary to 'in_tasks' array of targetTaskAttrV
               note:one in can be connected by mutiple outs of other nodes and one out can connect to mutiple ins of other nodes
               '''
                task_key = '%s:%s' % (sourceNodeId,sourceAnchor)
                task_value = '%s:%s' % (targetNodeId,targetAnchor)
                source_out_tasks = sourceTaskAttrV['tasks']['out_tasks']
                source_out_tasks.append({task_key:task_value})
                target_in_tasks = targetTaskAttrV['tasks']['in_tasks']
                target_in_tasks.append({task_key:task_value})

                '''
                5.get each nodeOpts from nodes of graph json and set this to the nodesTaskInfo if it has no related nodeOpts
               '''
                if not TaskAnalyzer.nodesTaskInfo[sourceNodeId].get('nodeOpts'):
                    source_nodeOpts = TaskAnalyzer.getNodeByNodeId(sourceNodeId,nodes)['nodeOpts']
                    source_nodeOpts['id'] = sourceNodeId
                    TaskAnalyzer.nodesTaskInfo[sourceNodeId]['nodeOpts'] = source_nodeOpts
                if not TaskAnalyzer.nodesTaskInfo[targetNodeId].get('nodeOpts'):
                    target_nodeOpts = TaskAnalyzer.getNodeByNodeId(targetNodeId,nodes)['nodeOpts']
                    target_nodeOpts['id'] = targetNodeId
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
    jobj ={
    "source":{
        "nodes":[
            {
                "nodeOpts":{
                    "comCode":"libsvmCom",
                    "optsEntity":{
                        "dfspath":"/glzheng/tmp/risk_labeled_out.txt"
                    },
                    "comName":"libsvm文件"
                },
                "title":"libsvm文件",
                "anchorPoints":[
                    [
                        0.25,
                        1
                    ],
                    [
                        0.5,
                        1
                    ]
                ],
                "shape":"customNode",
                "y":40,
                "x":100,
                "id":"a9c64c2a"
            },
            {
                "nodeOpts":{
                    "comCode":"libsvmCom",
                    "optsEntity":{
                        "dfspath":"/glzheng/tmp/risk_labeled_out.txt"
                    },
                    "comName":"libsvm文件"
                },
                "title":"libsvm文件",
                "anchorPoints":[
                    [
                        0.25,
                        1
                    ],
                    [
                        0.5,
                        1
                    ]
                ],
                "shape":"customNode",
                "y":40,
                "x":300,
                "id":"302a3867"
            },
            {
                "nodeOpts":{
                    "comCode":"randomForestCom",
                    "optsEntity":{
                        "impurity":"gini",
                        "labelCol":"label",
                        "featuresCol":"features",
                        "numTrees":"20",
                        "maxDepth":"5",
                        "minInfoGain":"0.0",
                        "maxBins":"32"
                    },
                    "comName":"随机森林"
                },
                "title":"随机森林",
                "anchorPoints":[
                    [
                        0.5,
                        0
                    ],
                    [
                        0.5,
                        1
                    ]
                ],
                "shape":"customNode",
                "y":140,
                "x":160,
                "id":"af10231f"
            },
            {
                "nodeOpts":{
                    "comCode":"multiclassClassificationEvaluatorCom",
                    "optsEntity":{
                        "labelCol":"label",
                        "predictionCol":"prediction",
                        "metricName":"f1"
                    },
                    "comName":"多分类评估"
                },
                "title":"多分类评估",
                "anchorPoints":[
                    [
                        0.5,
                        0
                    ],
                    [
                        0.5,
                        1
                    ]
                ],
                "shape":"customNode",
                "y":330,
                "x":90,
                "id":"8778ea1c"
            },
            {
                "nodeOpts":{
                    "comCode":"predictionCom",
                    "optsEntity":{
                        "predictionCol":"prediction",
                        "probabilityCol":"probability",
                        "originalCol":"",
                        "featuresCol":"features"
                    },
                    "comName":"预测"
                },
                "title":"预测",
                "anchorPoints":[
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
                "shape":"customNode",
                "y":230,
                "x":250,
                "id":"3fb40c09"
            },
            {
                "nodeOpts":{
                    "comCode":"df2csvCom",
                    "optsEntity":{
                        "outpath":"/glzheng/tmp/risk_predictions_9-21.txt"
                    },
                    "comName":"df2csv"
                },
                "title":"df2csv",
                "anchorPoints":[
                    [
                        0.5,
                        0
                    ],
                    [
                        0.5,
                        1
                    ]
                ],
                "shape":"customNode",
                "y":360,
                "x":350,
                "id":"ac7b0fd5"
            }
        ],
        "edges":[
            {
                "target":"af10231f",
                "sourceAnchor":"out2",
                "source":"a9c64c2a",
                "shape":"polyLineFlow",
                "targetAnchor":"in1",
                "id":"5f18d034",
                "controlPoints":[
                    {
                        "y":80.5,
                        "x":140
                    },
                    {
                        "y":139.5,
                        "x":200
                    }
                ]
            },
            {
                "target":"3fb40c09",
                "sourceAnchor":"out2",
                "source":"302a3867",
                "shape":"polyLineFlow",
                "targetAnchor":"in2",
                "id":"12b21397",
                "controlPoints":[
                    {
                        "y":80.5,
                        "x":340
                    },
                    {
                        "y":229.5,
                        "x":290
                    }
                ]
            },
            {
                "target":"3fb40c09",
                "sourceAnchor":"out1",
                "source":"af10231f",
                "shape":"polyLineFlow",
                "targetAnchor":"in1",
                "id":"b72ddc3f",
                "controlPoints":[
                    {
                        "y":180.5,
                        "x":200
                    },
                    {
                        "y":229.5,
                        "x":269.75
                    }
                ]
            },
            {
                "target":"8778ea1c",
                "sourceAnchor":"out1",
                "source":"3fb40c09",
                "shape":"polyLineFlow",
                "targetAnchor":"in1",
                "id":"61232c2d",
                "controlPoints":[
                    {
                        "y":270.5,
                        "x":290
                    },
                    {
                        "y":329.5,
                        "x":130
                    }
                ]
            },
            {
                "target":"ac7b0fd5",
                "sourceAnchor":"out1",
                "source":"3fb40c09",
                "shape":"polyLineFlow",
                "targetAnchor":"in1",
                "id":"107c26a3",
                "controlPoints":[
                    {
                        "y":270.5,
                        "x":290
                    },
                    {
                        "y":359.5,
                        "x":390
                    }
                ]
            }
        ]
    },
    "guides":[

    ]
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
    TaskAnalyzer.analyzeGraphJson(jobj)
    lines = TaskAnalyzer.nodesTaskInfo
    for line in lines:
        print('%s %s' % (line,lines[line]))
    # print(TaskAnalyzer.nodesTaskInfo)




