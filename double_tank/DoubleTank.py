from gams import *
import sys
import os
import csv
import subprocess
import numpy as np
import itertools
import matplotlib.pyplot as plt

import clear_gmsfile
import mytimer as timer

class DoubleTank():

    def __init__(self, Nz):
        """
        docstring
        """
        self.Nz = Nz
        self.total_sim_time = 800
        self.startDirect = 1

        self.ws = GamsWorkspace(working_directory = os.getcwd())
        self.db = self.ws.add_database()
        self.opt = self.ws.add_options()
        self.opt.defines["gdxincname"] = self.db.name
        self.opt.all_model_types = "sbb"

        self.drawing = 1
        
        #do auto build GmsFile according to Nz
        if Nz == 1 :
            self.jobGAMSfile = "doubletankNz1.gms"
        elif  Nz == 2:
            self.jobGAMSfile = "doubletankNz2.gms"
        elif  Nz == 3:
            self.jobGAMSfile = "doubletankNz3.gms"
        elif  Nz == 4:
            self.jobGAMSfile = "doubletankNz4.gms"
        elif  Nz == 5:
            self.jobGAMSfile = "doubletankNz5.gms"
        elif  Nz == 8:
            self.jobGAMSfile = "doubletankNz8.gms"
        elif  Nz == 10:
            self.jobGAMSfile = "doubletankNz10.gms"
        else :
            self.jobGAMSfile = "doubletankNz1.gms"
        
    def setStartDirect(self, d):
        self.startDirect = d
        pass

    def getData(self,vertex_F):
        db = self.ws.add_database()
        vertex = db.add_parameter("vertex", 1, "list of direction of each time point in time horizon for uncertain parameter theta")
        vertex.clear()

        direct_current = self.startDirect
        v_len = len(vertex_F)
        shift = 0
        for i in range(1,self.total_sim_time+1):
            if shift < v_len :
                if vertex_F[shift] == 't':
                    shift = 1000
                elif (i >= vertex_F[shift]):
                    direct_current = -direct_current
                    shift += 1
            vertex.add_record(str(i)).value = direct_current

        job = self.ws.add_job_from_file(self.jobGAMSfile)
        opt = self.ws.add_options()
        opt.defines["gdxincname"] = db.name
        opt.all_model_types = "sbb"
        opt.optcr = 0
        job.run(opt,databases = db)
        FId = job.out_db.get_variable("z").first_record().level
        ms = job.out_db["ms"].find_record().value
        ss = job.out_db["ss"].find_record().value
        h1 = []
        for rec in job.out_db["h1"] :
            h1.append(rec.level)
        h2 = []
        for rec in job.out_db["h2"] :
            h2.append(rec.level)
        qin = []
        for rec in job.out_db["qin"] :
            qin.append(rec.level)
        theta = []
        for rec in job.out_db["theta"] :
            theta.append(rec.level)
        
        print(FId)
        if ms > 2 or ss > 1:
            print(ms,ss)
            print("Infeasible solution found.",ms,ss)
            exit()
        print("get Result Data finished")
        if self.startDirect == 1:
            direct_str = "p"
        elif self.startDirect == -1:
            direct_str = "n"
        datafilename = "doubletankdataNz"+str(self.Nz)+direct_str+".gdx"
        job.out_db.export(datafilename)
  
        print("Content of GDX file '"+datafilename+"':")

        if self.drawing == True :

            t = np.linspace(0, self.total_sim_time, self.total_sim_time)
            plt.plot(t, h1, color='blue', linestyle='-', label='h1', linewidth=2)
            plt.plot(t, h2, color='orange', linestyle='-', label='h2', linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.axhline(y=10,color='k', linestyle='--',linewidth=2)
            plt.axhline(y=1,color='k', linestyle='--',linewidth=2)
            plt.ylabel('water level (m)')
            plt.xlabel('time (min)')
            plt.legend(loc='upper left')
            plt.show()

            plt.plot(t, qin, 'r-', label='qout', linewidth=2)
            plt.axhline(y=0.5,color='b', linestyle='--',linewidth=2)
            plt.plot(t, theta, 'b-', label='theta', linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('flow rate (m^3/min)')
            plt.xlabel('time (min)')
            plt.legend(loc='best')
            plt.show()


        #this using for call data from gdx file
        #subprocess.call(["gdxdump", os.path.join(self.ws.working_directory, "data.gdx")])

    def solve_result(self,vertex_F):
        db = self.ws.add_database()
        vertex = db.add_parameter("vertex", 1, "list of direction of each time point in time horizon for uncertain parameter theta")
        vertex.clear()

        direct_current = self.startDirect
        v_len = len(vertex_F)
        shift = 0
        for i in range(1,self.total_sim_time+1):
            if shift < v_len :
                if vertex_F[shift] == 't':
                    shift = 1000
                elif (i >= vertex_F[shift]):
                    direct_current = -direct_current
                    shift += 1
            vertex.add_record(str(i)).value = direct_current

        job = self.ws.add_job_from_file(self.jobGAMSfile)
        opt = self.ws.add_options()
        opt.defines["gdxincname"] = db.name
        opt.all_model_types = "sbb"
        opt.optcr = 0
        job.run(opt,databases = db)
        FId = job.out_db.get_variable("z").first_record().level
        print(f"vertex Fin: {vertex_F}\nFId: {FId}")

        return FId