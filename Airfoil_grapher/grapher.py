import numpy as np
import matplotlib.pyplot as plt
from os import walk


def getPolarData(linelist: list):
    rawdata = {"alpha": [], "CL": [], "CD": [], "CDp": [], "CM": []}
    for i in range(12, len(linelist)):
        linedata = linelist[i].replace("-", " -").split()
        rawdata["alpha"].append(float(linedata[0]))
        rawdata["CL"].append(float(linedata[1]))
        rawdata["CD"].append(float(linedata[2]))
        rawdata["CDp"].append(float(linedata[3]))
        rawdata["CM"].append(float(linedata[4]))
    return rawdata


def getCpData(linelist: list):
    data = {"Top":{"x": [], "y": [], "Cp": []}, "Bottom":{"x": [], "y": [], "Cp": []}}
    rawdata = {"x": [], "y": [], "Cp": []}
    for i in range(3, len(linelist)):
        linedata = linelist[i].replace("-", " -").split()
        rawdata["x"].append(float(linedata[0]))
        rawdata["y"].append(float(linedata[1]))
        rawdata["Cp"].append(float(linedata[2]))
    try:
        halfIndex = rawdata["x"].index(0.00000)
    except ValueError:
        try: 
            halfIndex = rawdata["x"].index(-0.00001)
        except ValueError:
            try:
                halfIndex = rawdata["x"].index(0.00001)
            except ValueError:
                try:
                    halfIndex = rawdata["x"].index(0.00002)
                except ValueError:
                    halfIndex = rawdata["x"].index(-0.00003)

    data["Top"]["x"] = rawdata["x"][0:halfIndex+1]
    data["Top"]["y"] = rawdata["y"][0:halfIndex+1]
    data["Top"]["Cp"] = rawdata["Cp"][0:halfIndex+1]
    data["Bottom"]["x"] = rawdata["x"][halfIndex:]
    data["Bottom"]["y"] = rawdata["y"][halfIndex:]
    data["Bottom"]["Cp"] = rawdata["Cp"][halfIndex:]
    return data


def GeneratePolars():
    fs = []
    for (dirpath, dirnames, filenames) in walk("Polar_airfoils"):
        fs.extend(filenames)
        break

    for f in fs:
        print(f)
        rawfile = open("Polar_airfoils/"+f)
        rawdata = getPolarData(rawfile.readlines())
        rawfile.close()
        nameAndRange = f.split("_")
        foilname = nameAndRange[0].split(".")[0]
        alphaRange = [-8.0, 20]
        # print(rawdata["CL"])

        # plot cl vs alpha
        plt.plot(rawdata["alpha"], rawdata["CL"])
        plt.axis('auto')
        plt.ylim(top=3, bottom=-3)
        plt.ylabel("Cl")

        plt.xlim(left=alphaRange[0], right=alphaRange[1])
        plt.xticks(np.arange(alphaRange[0], alphaRange[1], 2.0))
        plt.xlabel("alpha")

        plt.title(foilname)
        plt.grid()
        plt.savefig("Polar_airfoils_graphs/{}_{}_{}.png".format(foilname,
                                                                alphaRange[0], alphaRange[1]), format="png")
        plt.close()

        # plot Cl vs Cd
        plt.plot(rawdata["CD"], rawdata["CL"])
        plt.axis('auto')
        plt.ylim(top=2, bottom=-2)
        plt.ylabel("Cl")

        plt.xlim(left=0, right=0.3)
        plt.xticks(np.arange(0, 0.3, 0.05))
        plt.xlabel("CD")

        plt.title(foilname)
        plt.grid()

        plt.show()
        plt.savefig("Polar_airfoils_graphs/{}_{}_{}_CL_CD.png".format(foilname,
                                                                      alphaRange[0], alphaRange[1]), format="png")
        plt.close()


def generateCpDist():
    fs = []
    for (dirpath, dirnames, filenames) in walk("Cp_airfoils"):
        fs.extend(filenames)
        break

    for f in fs:
        print(f)
        rawfile = open("Cp_airfoils/"+f)
        rawdata = getCpData(rawfile.readlines())
        rawfile.close()
        foilname = f.split(".")[0]
        # print(rawdata["CL"])

        # plot Cp vs 1/c Top
        plt.plot(rawdata["Top"]["x"], rawdata["Top"]["Cp"])
        plt.plot(rawdata["Bottom"]["x"], rawdata["Bottom"]["Cp"])
        plt.axis('auto')
        plt.ylim(top=-2, bottom=1)
        plt.ylabel("Cp")

        plt.xlim(0, 1)
        #plt.xticks(np.arange(alphaRange[0], alphaRange[1], 5.0))
        plt.xlabel("1/c")

        plt.title(foilname)
        plt.grid()
        plt.savefig("Cp_airfoils_graphs/{}.png".format(foilname), format="png")
        plt.close()


def generateSingleplot():
    walkdir = "Polar_airfoils" if input("Polar or Cp (0,1): ") == "0" else "Cp_airfoils"
    fs = []
    for (dirpath, dirnames, filenames) in walk(walkdir):
        fs.extend(filenames)
        break

    print("files to use:")
    i = 0
    for f in fs:
        print(i,":", f)
        i+=1

    fileind = int(input("select a file using the number infront: "))
    print("chosen file: ", fs[fileind])
    print(walkdir)

    rawfile = open(walkdir +"/"+ fs[fileind])
    if walkdir == "Polar_airfoils":
        rawdata = getPolarData(rawfile.readlines())
        # plot cl vs alpha
        plt.plot(rawdata["alpha"], rawdata["CL"])
        plt.axis('auto')
        plt.ylim(top=3, bottom=-1)
        plt.ylabel("Cl")

        plt.xlim(left=rawdata["alpha"][0], right=rawdata["alpha"][-1])
        plt.xticks(np.arange(rawdata["alpha"][0], rawdata["alpha"][-1], 1.0))
        plt.xlabel("alpha")

        plt.title(input("enter plot title: "))
        plt.grid()
        plt.show()
        plt.savefig(input("enter savefile name: "), format="png")
        plt.close()

        # plot Cl vs Cd
        plt.plot(rawdata["CD"], rawdata["CL"])
        plt.axis('auto')
        plt.ylim(top=2, bottom=-2)
        plt.ylabel("Cl")

        plt.xlim(left=0, right=0.3)
        plt.xticks(np.arange(0, 0.3, 0.05))
        plt.xlabel("CD")

        plt.title(input("enter plot title: "))
        plt.grid()
        plt.show()
        plt.savefig(input("enter savefile name: "), format="png")
        plt.close()
    else:
        print("else")
        rawdata = getCpData(rawfile.readlines())
    rawfile.close()



def main():
    #generateCpDist()
    #GeneratePolars()
    generateSingleplot()
    pass


if __name__ == '__main__':
    main()
