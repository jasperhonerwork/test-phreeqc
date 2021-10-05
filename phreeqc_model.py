import subprocess

class phreeqcModel():
    def __init__(self):
        """Setting up and running phreeqc"""
        self.phBin = ""
        self.phDb = ""
        self.inputFile = ""
        self.outputFile = ""

    def runModel(self):
        """Run Phreeqc"""
        phProc = subprocess.Popen([self.phBin, self.inputFile, self.outputFile, self.phDb],
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

        # with phProc.stdout:
        #    for line in iter(phProc.stdout.readline, b''):
        #        print(line.decode('utf-8',"ignore"))
        with phProc.stderr:
            for line in iter(phProc.stderr.readline, b''):
                print(line[:-1].decode('utf-8', "ignore"))
        phProc.wait()




