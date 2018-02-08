__author__ = 'hand'
from taskAnalyzer import TaskAnalyzer
from coordinator import Coordinator

class TaskCleaner():
    #clear the mark of the last task in order to run the next task initially
    @staticmethod
    def cleanTask():
        TaskAnalyzer.clearGlobalVars()
        Coordinator.clearGlobalVars()
