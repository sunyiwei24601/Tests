
from poseidon.components.textAnalysis.word2vecCom import Word2vecComponent
from poseidon.components.textAnalysis.tokenizerCom import TokenizerCom
from poseidon.components.machineLearning.mutiClassification.randomForestCom import RandomForestCom
from poseidon.components.sourceNTarget.hiveTable import HiveTable
from poseidon.components.machineLearning.prediction.predictionCom import PredictionCom
from poseidon.components.sourceNTarget.libsvmCom import LibsvmCom
from poseidon.components.sourceNTarget.df2csvCom import Df2csvCom
from poseidon.components.datapreprocess.dfSplitCom import DfSplitCom
from poseidon.components.machineLearning.evaluation.multiclassClassificationEvaluatorCom import MulticlassClassificationEvaluatorCom
from poseidon.components.datapreprocess.sqlCom import SQLCom
from poseidon.components.machineLearning.mutiClassification.naiveBayesCom import NaiveBayesCom
from poseidon.components.machineLearning.mutiClassification.multilayerPerceptronClassifierCom import MultilayerPerceptronClassifierCom
from poseidon.components.datapreprocess.ssqlCom import SSQLCom
from poseidon.components.datapreprocess.naFillerCom import NaFillerCom
from poseidon.components.datapreprocess.typeConversionCom import TypeConversionCom
from poseidon.components.machineLearning.clustering.kmeans import KmeansClusterCom
from poseidon.components.machineLearning.model.modelCom import ModelCom
from poseidon.components.machineLearning.evaluation.clusterEvaluatorCom import ClusterEvaluatorCom
from poseidon.components.datapreprocess.standardScalerCom import StandardScalerCom

class AIService():
    # this method is for machine learning
    @staticmethod
    def aiTasks(com_code, tid, jobj, ins, outs, f, username, taskname):
        # print(com_code)
        try:
            str = "{0}.{1}Processer(tid, jobj, ins, outs, f, username, taskname)".format\
                (com_code.replace(com_code[0], com_code[0].capitalize(), 1), com_code)
            eval_res = eval(str)
            return eval_res
        except Exception as e:
            print("*****************Sorry:\n %s" % e)
            f.write("*****************Sorry:\n %s" % e)
            f.close()
            return 0

        # if com_code == "randomForestCom":
        #     return RandomForestCom.randomForestComProcesser(tid, jobj, ins, outs, f,username,taskname)
        # elif com_code == "hiveTable":
        #     return HiveTable.hiveTableProcesser(tid, jobj, ins, outs,f)
        # elif com_code == "predictionCom":
        #     return PredictionCom.predictionComProcesser(tid, jobj, ins, outs,f)
        # elif com_code == "libsvmCom":
        #     return LibsvmCom.libsvmComProcesser(tid, jobj, ins, outs,f)
        # elif com_code == "multiclassClassificationEvaluatorCom":
        #     return MulticlassClassificationEvaluatorCom.multiclassClassificationEvaluatorComProcesser(tid, jobj, ins, outs,f)
        # elif com_code == "dfSplitCom":
        #     return DfSplitCom.dfSplitComProcesser(tid, jobj, ins, outs,f)
        # elif com_code == "df2csvCom":
        #     return Df2csvCom.df2csvComProcesser(tid, jobj, ins, outs,f)
        # elif com_code == "sqlCom":
        #     return SqlCom.sqlComProcesser(tid, jobj, ins, outs,f)
        # elif com_code == "naiveBayesCom":
        #     return NaiveBayesCom.naiveBayesComProcesser(tid, jobj, ins, outs,f,username,taskname)
        # elif com_code == "multilayerPerceptronClassifierCom":
        #     return MultilayerPerceptronClassifierCom.multilayerPerceptronClassifierComProcesser(tid, jobj, ins, outs,f,username,taskname)
        # elif com_code == "SSQLCom":
        #     return SSQLCom.SSQLComProcesser(tid, jobj, ins, outs,f,username,taskname)
        # elif com_code == "typeConversionCom":
        #     return TypeConversionCom.typeConversionComProcesser(tid, jobj, ins, outs,f,username,taskname)
        # else:
        #     str = '%s.%sProcesser(tid, jobj, ins, outs,f,username,taskname)' % (com_code,com_code)
        #     evalres = eval(str)
        #     return evalres

    # this method is for machine text analysis
    @staticmethod
    def doTextAnalysisAction(action_name, jobj):
        if action_name == "tokenizer":
            return TokenizerCom.jieba_tokenizer(jobj)
        elif action_name == "word2vec":
            return Word2vecComponent.word2vecTrainer(jobj, "default.emotion_train_tokenized")
        # elif action_name == "stringIndexer":
        #     return StringIndexerComCopy.stringIndexerTrainer1(jobj, "default.sample_svm_data")
        elif action_name == "indexToString":
            # do sth
            pass
        else:
            # do sth
            pass

    # this method is for machine text analysis
    @staticmethod
    def doTextAnalysisAction_bak(action_name, jobj):
        if action_name == "tokenizer":
            return TokenizerCom.jieba_tokenizer(jobj)
        elif action_name == "word2vec":
            return Word2vecComponent.word2vecTrainer(jobj, "default.emotion_train_tokenized")
        # elif action_name == "stringIndexer":
        #     return StringIndexerComCopy.stringIndexerTrainer1(jobj, "default.sample_svm_data")
        elif action_name == "indexToString":
            # do sth
            pass
        else:
            # do sth
            pass

