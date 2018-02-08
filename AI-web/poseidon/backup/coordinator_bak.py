__author__ = 'hand'

from poseidon.service.aiService import AIService
import json

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

    '''scan all nodes recursively, execute the nodes can be executed after auto-judged
    Params:
            nodesTaskInfo:all nodes contain all in and out pipelines and their flow source and target,the
        format as below:
        {'11':{'in_pipes':[],'out_pipes':['out1'],'tasks':{'in_tasks':{},'out_tasks':{'11:out1':'22:in1'},'executed':'0','nodeOpts':{}}},
         '22':{}
         ...
        }
    '''
    @staticmethod
    def executeNodes(nodesTaskInfo,f):
        try:
            #define a flag used to indicates there are no node can be executed,as long as there is one node can be executed, then this flag is True
            hasUnExecutedNodes = False
            #used to store the num of nodes can not be executed, if it equals to the len(nodesTaskInfo), then it indicates
            # there is no nodes can be executed, then we terminate the process
            unExecutedNodes = 0
            for tid in nodesTaskInfo:

                #see if current can be executed
                comCode = nodesTaskInfo[tid]['nodeOpts']['comCode']
                f.write('\n&&&& handling %s node\n' % (tid))
                if Coordinator.canBeExecuted(tid,nodesTaskInfo,f):
                    f.write('\n$$$$ execute %s node %s\n' % (tid,comCode))
                    #get the result of the node like {'nodeid:out1':'val1','nodeid:out2':'val2'}
                    result = Coordinator.executeNode(tid,nodesTaskInfo,f)
                    f.write('\n$$$$ the result of %s node %s is:\n %s' % (tid, comCode, result.__str__()))
                    # if result is 0 which indicates this node was failed, as long as one node failed, we terminate the
                    # whole task
                    if result == 0:
                        Coordinator.global_result_vars['error_tid'] = tid
                        Coordinator.global_result_vars['flag'] = 'ko'
                        return
                    '''
                    find keys of the out_tasks
                        1.null:indicates this node is the final node,map the tid ie node id to the result
                    in 'global_result_vars'
                        2.not null:like below
                            'out_tasks':{'11:out1':'22:in1'}
                        map value(like '22:in1') of out_tasks to result in 'task_tmp_vars',if the len(a) is more than 1,
                    then the len(result) is more than 1 too,map them separately
                  '''
                    out_tasks = nodesTaskInfo[tid]['tasks']['out_tasks']
                    f.write('\n#### the out_tasks of the current node is:\n %s\n'% out_tasks.__str__())
                    if not out_tasks:
                        Coordinator.global_result_vars[tid] = result
                        f.write('\n#### The %s node ie the current node has no out tasks,so put its result into global_result_vars \n' % (tid))
                        f.write('\n#### Now the global_result_vars is:\n%s' % Coordinator.global_result_vars.__str__())
                    else:
                        for out_task_key in out_tasks:
                            f.write('\n#### find value from result of the current node by %s in out_tasks:\n'%out_task_key)
                            #1.grab the value from result by key of out_tasks
                            value = result[out_task_key]
                            f.write(value.__str__())
                            #2.map the value of out_task_key to the value in the task_tmp_vars
                            Coordinator.task_tmp_vars[out_tasks[out_task_key]] = value
                            f.write('\n#### map the key %s to   %s   in task_tmp_vars\n'% (out_tasks[out_task_key],value.__str__()))
                else:
                    unExecutedNodes = unExecutedNodes+1
                    hasUnExecutedNodes = True

            if hasUnExecutedNodes and unExecutedNodes != len(nodesTaskInfo):
                f.write('\n%%%% execute Nodes recursively...\n')
                f.write('\n%%%% scan the nodesTaskInfo:\n%s' % nodesTaskInfo.__str__())
                Coordinator.executeNodes(nodesTaskInfo,f)
            else:
                f.write('\n%%%% Job done,congrats!!!!!!!\n')
        except Exception as e:
            f.close()
            print("*****************Sorry:\n %s" % e)
            return 0
    '''
    see if the node can be executed,nodesTaskInfo is like below:
    {'11':{'in_pipes':[],'out_pipes':['out1'],'tasks':{'in_tasks':{},'out_tasks':{'11:out1':'22:in1'},'executed':'0','nodeOpts':{}}},
     '22':{}
     ...
    }
    '''
    @staticmethod
    def canBeExecuted(tid,nodesTaskInfo,f):
        flag = False
        f.write('\n#####judge if the %s node can be executed or not\n' % tid)
        #if this node has been executed already,then it can not be executed again
        executedFlag = nodesTaskInfo[tid]['executed']
        if executedFlag == 1:
            f.write('\n#### %s node has been executed successfully\n'% (tid))
            return False

        #get all ins pipeline of the node :['in1','in2']
        in_pipes = nodesTaskInfo[tid]['in_pipes']
        #if the in_pipes is [] which indicates this node is a source node which has no in pipelines
        if not in_pipes:
            f.write('\n#### %s node can be executed,because this is a source node\n'% (tid))
            return True
        for in_pipe in in_pipes:
            #1.concatenate the tid(eg:11) and in_pipe(eg:in1) to 11:in1 which if the format of the keys in
            #the global 'task_tmp_vars'
            key = '%s:%s' % (tid,in_pipe)

            #2.if this key can be found in the 'task_tmp_vars'
            task_tmp_var = Coordinator.task_tmp_vars.get(key,'')
            if not task_tmp_var:
                f.write('\n#### %s node can not be executed, because its ins pipeline %s has no value, execute other node firstly\n'% (tid,key))
                #as long as one of input keys of node does not exist,then this node can not be executed
                return False
        #if all the input keys can be found,then this node can be executed
        f.write('\n#### %s node can be executed, because its all ins pipeline has been prepared\n'% (tid))
        return True

    '''
    execute the node,nodesTaskInfo is like below:
    {'11':{'in_pipes':[],'out_pipes':['out1'],'tasks':{'in_tasks':{},'out_tasks':{'11:out1':'22:in1'},'executed':'0','nodeOpts':{}}},
     '22':{}
     ...
    }
    '''
    @staticmethod
    def executeNode(tid,nodesTaskInfo,f):

        #we gotta prepare the jobj,ins,outs of the node,then we can execute this node

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
        result = AIService.aiTasks(comCode,tid,jobj,ins,outs,f)

        #set the 'executed' flag to be 1 which indicates this node has been executed successfully
        if result != 0:
            f.write('\n#### The result of %s node is not 0 which indicates success, so set the "executed" flag to 1\n' % tid)
            nodesTaskInfo[tid]['executed'] = 1
        return result