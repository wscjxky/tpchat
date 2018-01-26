#-*- coding: utf-8 -*-
import os
import threading


class FFmepgThread(threading.Thread):
    tasks = []
    condi = threading.Condition()
    ffmpeg = 'C:/Users/Administrator/Desktop/ffmpeg-win32-static/bin/ffmpeg'

    def __init__(self, signal):
        threading.Thread.__init__(self)
        self.signal = signal

    def run(self):
        while True:
            if len(self.tasks) == 0:
                self.signal.clear()
                self.signal.wait()
            self.condi.acquire()
            task = self.tasks.pop()
            self.condi.release()
            command = self.ffmpeg + ' -i ' + task['vPath'] + ' -f image2 -ss ' + task['time'] + ' -y ' + task['dPath']
            os.system(command)

    def addTask(self, srcPath, second, desPath):
        task = {'vPath': srcPath, 'time': second, 'dPath': desPath}
        self.condi.acquire()
        self.tasks.insert(0, task)
        self.condi.release()
        self.signal.set()