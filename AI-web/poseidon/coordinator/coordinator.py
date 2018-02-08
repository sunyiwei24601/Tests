# -*- coding: utf-8 -*-
__author__ = 'hand'

from poseidon.service.aiService import AIService

class Coordinator():
    '''global dict used to store the outputs of all nodes ie all inputs of the next nodes, any node will look its
        input pipe keys at this dict, if all input pipe keys has been found at this dict, then this node can be
        executed
    '''
    task_tmp_vars = {}

    #used to store the all outputs of nodes which has no next node, and then return this result, if the task failed,
    # there will be the failed node id in it.
    global_result_vars = {'flag':'ko'}

    @staticmethod
    def clearGlobalVars():
        Coordinator.task_tmp_vars = {}
        Coordinator.global_result_vars = {'flag':'ko'}

    '''scan all nodes recursively, execute the nodes can be executed after being auto-judged
    Params:
            nodesTaskInfo:all nodes contain all in and out pipelines and their flow source and target,the
        format as below:
        {'11':{'in_pipes':[],'out_pipes':['out1'],'tasks':{'in_tasks':[],'out_tasks':[{'11:out1':'22:in1'}],'executed':'0','nodeOpts':{}}},
         '22':{}
         ...
        }
    '''
    @staticmethod
    def executeNodes(nodesTaskInfo,f,username,taskname):
        try:
            #define a flag used to indicates there are no node can be executed,as long as there is one node can be executed, then this flag is True
            hasUnExecutedNodes = False
            #used to store the num of nodes can not be executed, if it equals to the len(nodesTaskInfo), then it indicates
            # there is no nodes can be executed, then we terminate the process
            unExecutedNodes = 0
            for tid in nodesTaskInfo:
                #see if current can be executed
                comCode = nodesTaskInfo[tid]['nodeOpts']['comCode']
                f.write('\n处理ID为 %s 的节点%s...\n' % (tid,comCode))
                if Coordinator.canBeExecuted(tid,comCode,nodesTaskInfo,f):
                    #表示节点开始执行
                    f.write('\n$$$$执行ID为 %s 的节点%s开始\n' % (tid,comCode))
                    #get the result of the node like {'nodeid:out1':'val1','nodeid:out2':'val2'}
                    result = Coordinator.executeNode(tid,nodesTaskInfo,f,username,taskname)
                    # f.write('\n$$$$ the result of %s node %s is:\n %s' % (tid, comCode, result.__str__()[:200]))

                    # if result is 0 which indicates this node was failed, as long as one node failed, we terminate the
                    # whole task
                    if result == 0:
                        Coordinator.global_result_vars['error_tid'] = tid
                        #表示节点执行失败
                        f.write('\n$$$$执行ID为 %s 的节点%s失败\n' % (tid,comCode))
                        f.write('\n$$$$执行ID为 %s 的节点%s结束\n' % (tid,comCode))
                        return
                    '''
                    find keys of the out_tasks
                        1.null:indicates this node is the final node,map the tid ie node id to the result
                    in 'global_result_vars'
                        2.not null:like below
                            'out_tasks':{'11:out1':'22:in1'}
                        map value(like '22:in1') of out_tasks to result in 'task_tmp_vars',if the len(out_tasks) is more than 1,
                    then the len(result) is more than 1 too,map them separately
                  '''
                    out_tasks = nodesTaskInfo[tid]['tasks']['out_tasks']
                    f.write('\n当前节点的输出任务是:\n %s\n'% out_tasks.__str__()[:200])

                    # f.write('\n $$$$执行任务ID:%s 节点为:%s...结束\n' % (tid,comCode))

                    if not out_tasks:
                        Coordinator.global_result_vars[tid] = result
                        f.write('\nID:%s为当前没有输出任务的节点,将其保存到 global_result_vars 中 \n' % (tid))
                        f.write('\n当前 global_result_vars 为:\n%s' % Coordinator.global_result_vars.__str__()[:200])
                    else:
                        for out_task in out_tasks:
                            out_task_source = out_task.keys()[0]
                            out_task_target = out_task[out_task_source]

                            #1.grab the value from result by key of out_tasks
                            value = result[out_task_source]
                            f.write('\n从task_tmp_vars的输出任务%s中找出此节点的值:\n%s'%(out_task_source,value.__str__()[:200]))
                            #2.map the value of out_task_key to the value in the task_tmp_vars
                            Coordinator.task_tmp_vars[out_task_target] = value
                            f.write('\n将key:%s映射到task_tmp_vars的value:%s中\n'% (out_task_target,value.__str__()[:200]))
                    #表示节点执行结束
                    f.write('\n$$$$执行ID为 %s 的节点%s结束\n' % (tid,comCode))
                else:
                    unExecutedNodes = unExecutedNodes+1
                    hasUnExecutedNodes = True
            #如果该节点需要的前置节点并没有完成，就会不断地循环直到可以完成为止
            if hasUnExecutedNodes and unExecutedNodes != len(nodesTaskInfo):
                f.write('\n%%%%正在递归执行节点中...\n')
                f.write('\n扫描节点任务信息:\n%s' % nodesTaskInfo.__str__()[:200])
                Coordinator.executeNodes(nodesTaskInfo,f,username,taskname)
            else:
                Coordinator.global_result_vars['flag'] = 'ok'
                f.write('\n任务完成!!!\n')
        except Exception as e:
            f.write("*****************Sorry:\n %s" % e)
            print("*****************Sorry:\n %s" % e)
            return 0
        finally:
            f.close()
    '''
    see if the node can be executed,nodesTaskInfo is like below:
    {'11':{'in_pipes':[],'out_pipes':['out1'],'tasks':{'in_tasks':{},'out_tasks':{'11:out1':'22:in1'},'executed':'0','nodeOpts':{}}},
     '22':{}
     ...
    }
    '''
    @staticmethod
    def canBeExecuted(tid,comCode,nodesTaskInfo,f):
        flag = False
        f.write('\n判断ID为：%s 的节点%s是否可以执行...\n' % (tid,comCode))
        #if this node has been executed already,then it can not be executed again
        executedFlag = nodesTaskInfo[tid]['executed']
        if executedFlag == 1:
            f.write('\nID为 %s 的节点%s已经执行成功\n'% (tid,comCode))
            return False

        #get all ins pipeline of the node :['in1','in2']
        in_pipes = nodesTaskInfo[tid]['in_pipes']
        #if the in_pipes is [] which indicates this node is a source node which has no in pipelines
        if not in_pipes:
            f.write('\n这是一个原节点，ID为：%s 节点名称为：%s,可以执行\n'% (tid,comCode))
            return True
        for in_pipe in in_pipes:
            #1.concatenate the tid(eg:11) and in_pipe(eg:in1) to 11:in1 which is the format of the keys in
            #the global 'task_tmp_vars'
            key = '%s:%s' % (tid,in_pipe)

            #2.if this key can be found in the 'task_tmp_vars'
            task_tmp_var = Coordinator.task_tmp_vars.get(key,'')
            if not task_tmp_var:
                f.write('\nID为 %s 的节点%s不能被执行, 因为输入口%s中没有数据, 先执行其他节点.\n'% (tid,comCode,key))
                #as long as one of input keys of node does not exist, this node can not be executed
                return False
        #if all the input keys can be found,then this node can be executed
        f.write('\n输入数据准备完毕，ID为 %s 的节点%s可以执行\n'% (tid,comCode))
        return True

    '''
    execute the node,nodesTaskInfo is like below:
    {'11':{'in_pipes':[],'out_pipes':['out1'],'tasks':{'in_tasks':{},'out_tasks':{'11:out1':'22:in1'},'executed':'0','nodeOpts':{}}},
     '22':{}
     ...
    }
    '''
    @staticmethod
    def executeNode(tid,nodesTaskInfo,f,username,taskname):

        #we gotta prepare the jobj,ins,outs of the node,then we execute this node

        #get all in_pipes of this node
        in_pipes = nodesTaskInfo[tid]['in_pipes']

        #assemble ins param of the component like {in1:xx,in2:xx}
        ins = {}
        for in_pipe in in_pipes:
            in_pipe_key = '%s:%s' % (tid,in_pipe)
            ins[in_pipe] = Coordinator.task_tmp_vars[in_pipe_key]
        #get custom setting ie jobj of node
        jobj = nodesTaskInfo[tid]['nodeOpts']
        #get outs param of the node
        outs = nodesTaskInfo[tid]['out_pipes']

        #get the comCode of node by tid ie node id and the nodes aka the jobj which is the custom settings of user
        comCode = jobj['comCode']
        result = AIService.aiTasks(comCode,tid,jobj,ins,outs,f,username,taskname)

        #set the 'executed' flag to be 1 which indicates this node has been executed successfully
        if result != 0:
            f.write('\nID为 %s 的节点输出结果不是0,执行成功,将"executed"标志设置为1\n' % tid)
            nodesTaskInfo[tid]['executed'] = 1
        return result