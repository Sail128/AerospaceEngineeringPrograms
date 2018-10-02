import subprocess as sp
import threading
from os import walk
from numpy import arange
import grapher
from time import sleep


class xfoilThread(threading.Thread):
    def __init__(self, threadID, filename, alfas=[0.0], itterations=70):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.filename = filename
        self.output = "Polar"
        self.alfarange = alfas
        self.itterations = itterations
        self.Re = 1000000
        self.Mach = 0.79
        self.cpalfa = 0.0

        self.xfoil = None

    def setAlfas(self, alfas):
        self.alfarange = alfas

    def setOutput(self, output):
        self.output = output

    def setCpAlfa(self, alfa):
        self.cpalfa = alfa

    def command(self, cmd):
        self.xfoil.stdin.write(cmd + '\n')
        #print(cmd)

    def run(self):
        startupinfo = sp.STARTUPINFO()
        startupinfo.dwFlags |= sp.STARTF_USESHOWWINDOW
        self.xfoil = sp.Popen(['xfoil.exe'],
                              stdin=sp.PIPE,
                              stdout=0,
                              stderr=None,
                              startupinfo=startupinfo,
                              encoding='utf8'
                              )

        self.command("NORM")
        self.command("LOAD {}".format(self.filename))
        self.command("MDES")  # open airfoil design
        self.command("FILT")  # smooth variations in the airfoil file
        self.command("EXEC")  # execute smoothing
        self.command("")  # get back to main mene
        self.command("PANE")  # generate airfoil panels for calculations
        self.command("OPER")  # open operations
        # set number of itterations
        self.command("ITER {}".format(self.itterations))
        self.command("Re {}".format(self.Re))  # set reynolds
        self.command("Mach {}".format(self.Mach))  # set mach
        self.command("VISC {}".format(self.Re))  # set viscous
        # setup finished
        # calculate polar or cp
        if self.output == "Polar":
            self.command("PACC")  # open polar file
            self.command("Polar_{}_{}_{}".format(
                self.filename, self.alfarange[0], self.alfarange[-1]))  # give the file a name
            self.command("")  # skip dump file
            for alfa in self.alfarange:
                #    self.command("INIT")
                self.command("ALFA {}".format(alfa))
        if self.output == "Cp":
            #    self.command("INIT")
            self.command("ALFA {}".format(self.cpalfa))
            self.command("CPWR Cp_{}".format(self.filename))
        else:
            pass

        # self.command("PACC")#close polar file
        # self.command("VISC")#reset environment
        self.command("")  # exit to main menu
        self.command("QUIT")  # quit the program

        self.xfoil.terminate()

        print("thread {}, for {}, is finished".format(
            self.threadID, self.filename))


def xfoilProcess(infile, alfas=[0.0], output="Polar", iterr=5, Re=1000000, Mach=0.0, cpalfa=0.0):
    # setup log files for output
    logfile = open("log_{}.log".format(infile.split(".")[0]), "w")
    errorlogfile = open("log_{}.errorlog".format(infile.split(".")[0]), "w")

    startupinfo = sp.STARTUPINFO()
    startupinfo.dwFlags |= sp.STARTF_USESHOWWINDOW
    ps = sp.Popen(['xfoil.exe'],
                  stdin=sp.PIPE,
                  stdout=logfile,
                  stderr=errorlogfile,
                  startupinfo=startupinfo,
                  encoding='utf8'
                  )

    def command(cmd):
        print(cmd)
        ps.stdin.write(cmd+'\n')
        #psout = []
        # while True:
        #    line = ps.stdout.readline()
        #    psout.append(line)
        #    print(line)
        #    if line == '' and ps.poll() != None:
        #        break
        # print(''.join(psout))

    command("NORM")
    command("LOAD {}".format(infile))
    command("MDES")  # open airfoil design
    command("FILT")  # smooth variations in the airfoil file
    command("EXEC")  # execute smoothing
    command("")  # get back to main mene
    command("PANE")  # generate airfoil panels for calculations
    command("OPER")  # open operations
    command("ITER {}".format(iterr))  # set number of itterations
    command("Re {}".format(Re))  # set reynolds
    command("Mach {}".format(Mach))  # set mach
    command("VISC {}".format(Re))  # set viscous
    # setup finished
    # calculate polar or cp
    if output == "Polar":
        command("PACC")  # open polar file
        # give the file a name
        command("Polar_{}_{}_{}".format(infile, Re, Mach))
        command("")  # skip dumpfile
        for alfa in alfas:
            # sleep(0.01)
            # command("INIT")
            command("ALFA {}".format(alfa))
    if output == "Cp":
        #command("INIT")
        command("ALFA {}".format(cpalfa))
        command("CPWR Cp_{}".format(infile))
    else:
        pass

    command("PACC")  # close polar file
    command("VISC")  # reset environment
    command("")  # exit to main menu
    command("QUIT")  # quit the program

    # ps.terminate()

    logfile.close()
    errorlogfile.close()


def generatePolarFiles():
    airfoilfiles = []

    alfas = arange(-8.0, 20.0, 0.25).tolist()

    for (dirpath, dirnames, filenames) in walk("airfoils"):
        airfoilfiles.extend(filenames)
        break

    #xfoilProcess("airfoils/{}".format(airfoilfiles[0]), alfas=alfas)

    i = 0
    for f in airfoilfiles:
    #    foilthreads.append(xfoilThread(
    #        i, "airfoils/{}".format(f), alfas=alfas))
        #xfoilProcess("airfoils/{}".format(f), alfas=alfas, output="Cp", cpalfa=1.0)
        xfoilProcess("airfoils/{}".format(f), alfas=alfas, output="Polar", cpalfa=1.0, Mach=0.0)
        i += 1

def main():
    generatePolarFiles()
    #f= "K-3_BL576_int06.dat"
    #alfas = arange(-10.0, 20.0, 0.25).tolist()
    #xfoilProcess("airfoils/{}".format(f), Re=10000000 ,alfas=alfas, output="Polar", cpalfa=0.0)


if __name__ == '__main__':
    main()
