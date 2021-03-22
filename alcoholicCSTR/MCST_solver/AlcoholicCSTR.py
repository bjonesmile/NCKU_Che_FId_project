from gams import *
import sys
import os
import psutil
import gc
import threading
import numpy as np
import itertools
import matplotlib.pyplot as plt
import csv

import clear_gmsfile
import mytimer as timer

class AlcoholicCSTR():
    def __init__(self, Nz):
        """
        docstring
        """
        self.Nz = Nz
        self.total_sim_time = 240
        self.startDirectSa = None
        self.startDirectT = None
        self.MV_num = 2

        self.ws = GamsWorkspace(working_directory = os.getcwd())
        self.db = self.ws.add_database()
        self.opt = self.ws.add_options()
        self.opt.defines["gdxincname"] = self.db.name
        self.opt.all_model_types = "sbb"
        self.opt.optcr = 0

        self.db.add_parameter("vertex", 1, "list of direction of each time point in time horizon for uncertain parameter Sa")
        self.db.add_parameter("vertexT", 1, "list of direction of each time point in time horizon for uncertain parameter T")

        #do auto build GmsFile according to Nz
        if Nz == 1 :
            self.jobGAMSfile = "alcoholicCSTRNz1.gms"
        elif  Nz == 2:
            self.jobGAMSfile = "alcoholicCSTRNz2.gms"
        elif  Nz == 3:
            self.jobGAMSfile = "alcoholicCSTRNz3.gms"
        elif  Nz == 4:
            self.jobGAMSfile = "alcoholicCSTRNz4.gms"
        elif  Nz == 5:
            self.jobGAMSfile = "alcoholicCSTRNz5.gms"
        elif  Nz == 6:
            self.jobGAMSfile = "alcoholicCSTRNz6.gms"
        elif  Nz == 8:
            self.jobGAMSfile = "alcoholicCSTRNz8.gms"
        elif  Nz == 10:
            self.jobGAMSfile = "alcoholicCSTRNz10.gms"
        elif  Nz == 12:
            self.jobGAMSfile = "alcoholicCSTRNz12.gms"
        elif  Nz == 15:
            self.jobGAMSfile = "alcoholicCSTRNz15.gms"
        elif  Nz == 20:
            self.jobGAMSfile = "alcoholicCSTRNz20.gms"
        elif  Nz == 30:
            self.jobGAMSfile = "alcoholicCSTRNz30.gms"
        elif  Nz == 40:
            self.jobGAMSfile = "alcoholicCSTRNz40.gms"
        elif  Nz == 50:
            self.jobGAMSfile = "alcoholicCSTRNz50.gms"
        elif  Nz == 60:
            self.jobGAMSfile = "alcoholicCSTRNz60.gms"
        elif  Nz == 70:
            self.jobGAMSfile = "alcoholicCSTRNz70.gms"
        elif  Nz == 80:
            self.jobGAMSfile = "alcoholicCSTRNz80.gms"
        elif  Nz == 90:
            self.jobGAMSfile = "alcoholicCSTRNz90.gms"
        elif  Nz == 100:
            self.jobGAMSfile = "alcoholicCSTRNz100.gms"
        elif  Nz == 120:
            self.jobGAMSfile = "alcoholicCSTRNz120.gms"
        elif  Nz == 150:
            self.jobGAMSfile = "alcoholicCSTRNz150.gms"
        elif  Nz == 240:
            self.jobGAMSfile = "alcoholicCSTRNz240.gms"
        else :
            print("cant find select gams file, auto choose Nz1")
            self.jobGAMSfile = "alcoholicCSTRNz1.gms"
        
        pass

    def setStartDirect(self, directSa, directT):
        self.startDirectSa = directSa
        self.startDirectT = directT
        pass

    def set_jobGAMSfile(self,file_name):
        self.jobGAMSfile = file_name
        pass

    def crtGridVertexList(self,vertex,v_range,n=3):
        up_limit = self.total_sim_time
        lo_limit = 1


        v_range_set = None
        for v in vertex :
            if v_range_set is None :
                v_range_set = np.linspace(v-v_range,v+v_range,num=n,dtype=np.int)
                for v_i in range(len(v_range_set)) :
                    if v_range_set[v_i] > up_limit :
                        v_range_set[v_i] = up_limit
                    elif v_range_set[v_i] < lo_limit :
                        v_range_set[v_i] = lo_limit
                    else :
                        pass
                    
            else :
                temp_set = np.linspace(v-v_range,v+v_range,num=n,dtype=np.int)
                for v_i in range(len(temp_set)) :
                    if temp_set[v_i] > up_limit :
                        temp_set[v_i] = up_limit
                    elif temp_set[v_i] < lo_limit :
                        temp_set[v_i] = lo_limit
                    else :
                        pass
                v_range_set = np.vstack((v_range_set,temp_set))
        
        vertexList = []
        if len(v_range_set.shape) == 1:
            for v in v_range_set:
                vertexList.append([v])
            return vertexList
        
        for i in range(len(v_range_set)-1):
            if i == 0:
                for x in itertools.product(v_range_set[i],v_range_set[i+1]):
                    vertexList.append(list(x))
            else:
                newVertexList = []
                for x in itertools.product(vertexList,v_range_set[i+1]):
                    temp = []
                    for item in x :
                        if isinstance(item,list):
                            temp.extend(item)
                        else:
                            temp.append(item)
                    newVertexList.append(temp)
                vertexList.clear()
                vertexList = newVertexList
        return vertexList

    def checkVertex(self,vertex):
        for shift in vertex:
            if shift <= 0 :
                vertex.remove(shift)
            elif shift > self.total_sim_time :
                vertex.remove(shift)
        return vertex

    def solve_result(self,vertex_Sa,vertex_T):
        print("gams solve parameter vertex :",vertex_Sa,vertex_T)

        db = self.ws.add_database()
        vertexSa = db.add_parameter("vertex", 1, "list of direction of each time point in time horizon for uncertain parameter Sa")
        vertexT = db.add_parameter("vertexT", 1, "list of direction of each time point in time horizon for uncertain parameter T")
        v_len_Sa = len(vertex_Sa)
        v_len_T = len(vertex_T)

        vertexSa.clear()
        vertexT.clear()
        d_cur_Sa = self.startDirectSa
        d_cur_T = self.startDirectT
        shift_Sa = 0
        shift_T  = 0
        for i in range(1,self.total_sim_time+1):
            if shift_Sa < v_len_Sa :
                if vertex_Sa[shift_Sa] == 't':
                    shift_Sa = 1000
                elif (i >= vertex_Sa[shift_Sa]):
                    d_cur_Sa = -d_cur_Sa
                    shift_Sa += 1
                    
            if shift_T < v_len_T :
                if vertex_T[shift_T] == 't':
                    shift_T = 1000
                elif (i >= vertex_T[shift_T]):
                    d_cur_T = -d_cur_T
                    shift_T += 1
            vertexSa.add_record(str(i)).value = d_cur_Sa
            vertexT.add_record(str(i)).value = d_cur_T

        job = self.ws.add_job_from_file(self.jobGAMSfile)
        opt = self.ws.add_options()
        opt.defines["gdxincname"] = db.name
        opt.all_model_types = "sbb"
        opt.optcr = 0
        job.run(opt,databases = db)
        FId = job.out_db.get_variable("z").first_record().level

        print(f"vertex Sa: {vertex_Sa}, vertex T: {vertex_T}\nFId: {FId}")
        return FId

    def get_data(self,vertex_Sa,vertex_T,drawing=True,save=False):
        print("gams output data parameter vertex :",vertex_Sa,vertex_T)

        db = self.ws.add_database()
        vertexSa = db.add_parameter("vertex", 1, "list of direction of each time point in time horizon for uncertain parameter Sa")
        vertexT = db.add_parameter("vertexT", 1, "list of direction of each time point in time horizon for uncertain parameter T")
        v_len_Sa = len(vertex_Sa)
        v_len_T = len(vertex_T)

        vertexSa.clear()
        vertexT.clear()
        d_cur_Sa = self.startDirectSa
        d_cur_T = self.startDirectT
        shift_Sa = 0
        shift_T  = 0
        for i in range(1,self.total_sim_time+1):
            if shift_Sa < v_len_Sa :
                if vertex_Sa[shift_Sa] == 't':
                    shift_Sa = 1000
                elif (i >= vertex_Sa[shift_Sa]):
                    d_cur_Sa = -d_cur_Sa
                    shift_Sa += 1
                    
            if shift_T < v_len_T :
                if vertex_T[shift_T] == 't':
                    shift_T = 1000
                elif (i >= vertex_T[shift_T]):
                    d_cur_T = -d_cur_T
                    shift_T += 1
            vertexSa.add_record(str(i)).value = d_cur_Sa
            vertexT.add_record(str(i)).value = d_cur_T

        job = self.ws.add_job_from_file(self.jobGAMSfile)
        opt = self.ws.add_options()
        opt.defines["gdxincname"] = db.name
        opt.all_model_types = "sbb"
        opt.optcr = 0
        job.run(opt,databases = db)
        FId = job.out_db["z"].last_record().level
        ms = job.out_db["ms"].find_record().value
        ss = job.out_db["ss"].find_record().value

        print("FId value:",FId)

        s = []
        for rec in job.out_db["S"] :
            s.append(rec.level)
        c = []
        for rec in job.out_db["C"] :
            c.append(rec.level)
        p = []
        for rec in job.out_db["P"] :
            p.append(rec.level)
        v = []
        for rec in job.out_db["V"] :
            v.append(rec.level)
        Fin = []
        for rec in job.out_db["Fin"] :
            Fin.append(rec.level)
        Fout = []
        for rec in job.out_db["Fout"] :
            Fout.append(rec.level)
        Sa = []
        for rec in job.out_db["Sa"] :
            Sa.append(rec.level)
        T = []
        for rec in job.out_db["T"] :
            T.append(rec.level)
        D_rate = [(fin+fout)/2/vol for fin, fout, vol in zip(Fin,Fout,v)]
        Dmu_ratio = []
        for rec, D in zip(job.out_db["mu"],D_rate):
            Dmu_ratio.append(rec.level/D)
        direct_Sa = []
        for rec in job.out_db["vertex"]:
            if rec.value == 1:
                direct_Sa.append(0.15)
            else:
                direct_Sa.append(-0.15)
        direct_T = []
        for rec in job.out_db["vertexT"]:
            if rec.value == 1:
                direct_T.append(-0.2)
            else:
                direct_T.append(-0.5)

        print(ms,ss)
        if ms > 2 or ss > 1:
            print("Infeasible solution found.",ms,ss)
        print("get Result Data finished")

        FId_value = int(round(FId,4)*10000)
        datafilename = "alcoholicCSTRNz"+str(self.Nz)+"FId"+str(FId_value)
        job.out_db.export(datafilename+".gdx")
        print("Content of GDX file '"+datafilename+".gdx"+"':")

        dataIMGdirname = "alcoholicCSTRNz"+str(self.Nz)+"FId"+str(FId_value)
        my_path = os.path.dirname(__file__)
        result_dir = os.path.join(my_path, dataIMGdirname+'Results/')
        if not os.path.isdir(result_dir) and save:
            os.makedirs(result_dir)
        
        # some const for plottinf fig
        p_lb = 40.0
        v_lb = 1.5
        v_ub = 3.0
        s_lb = 0.5
        s_ub = 100
        c_lb = 0.0
        c_ub = 8
        x_corr = -6
        circle_rad = 6

        if drawing :
            # draw state variable
            t = np.linspace(0, self.total_sim_time, self.total_sim_time)
            plt.plot(t, s, 'y-', label='s', linewidth=2)
            for x, y in zip(t,s):
                if y >= s_ub or y <= s_lb:
                    plt.annotate(str(int(x)),xy=(x, y), xytext=(x+x_corr,y-4),xycoords='data', color='red')
                    plt.plot(x, y, 'o', ms=circle_rad * 2, mec='r', mfc='none', mew=2)
            plt.plot(t, c, 'r-', label='c', linewidth=2)
            for x, y in zip(t,c):
                if y >= c_ub or y <= c_lb:
                    plt.annotate(str(int(x)),xy=(x, y), xytext=(x+x_corr,y-4),xycoords='data', color='red')
                    plt.plot(x, y, 'o', ms=circle_rad * 2, mec='r', mfc='none', mew=2)
            plt.plot(t, p, 'g-', label='p', linewidth=2)
            for x, y in zip(t,p):
                if y <= p_lb :
                    plt.annotate(str(int(x)),  xy=(x, y), xytext=(x+x_corr,y-4),xycoords='data', color='red')
                    plt.plot(x, y, 'o', ms=circle_rad * 2, mec='r', mfc='none', mew=2)
            plt.axhline(y=40,color='k', linestyle='--',linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('Conc (g/L)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')
            if save == True :
                plt.savefig(result_dir+'SV_SCP.png')
            plt.show()
            plt.clf()
            # draw volumn state variable
            plt.plot(t, v, 'b-', label='v', linewidth=2)
            for x, y in zip(t,v):
                if y >= v_ub or y <= v_lb:
                    plt.annotate(str(int(x)),xy=(x, y), xytext=(x+x_corr,y-0.1),xycoords='data', color='red')
                    plt.plot(x, y, 'o', ms=circle_rad * 2, mec='r', mfc='none', mew=2)
            plt.axhline(y=3,color='k', linestyle='--',linewidth=2)
            plt.axhline(y=1.5,color='k', linestyle='--',linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('volume (L)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')
            if save == True :
                plt.savefig(result_dir+'/SV_V.png')
            plt.show()
            # draw control variable
            plt.plot(t, Fin, 'b-', label='Fin', linewidth=2)
            plt.plot(t, Fout, 'r-', label='Fout', linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('flow rate (L/hr)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')
            if save == True :
                plt.savefig(result_dir+'/SV.png')
            plt.show()
            # draw vertex 
            plt.plot(t, Sa, 'b-', label='Sa', linewidth=2)
            plt.axhline(y=100,color='b', linestyle='--',linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.plot(t, T, 'b-', label='T', linewidth=2)
            plt.axhline(y=30,color='b', linestyle='--',linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('Conc (g/L) or Temp (C)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')
            if save == True :
                plt.savefig(result_dir+'/uncertainPara.png')
            plt.show()
            # draw dilution and mu
            plt.plot(t, Dmu_ratio, label='D/mu', linewidth=2)
            plt.plot(t, direct_Sa, label='vertex_Sa', color='r', linewidth=2)
            plt.plot(t, direct_T, label='vertex_T', color='b', linewidth=2)
            for Sa_switch in vertex_Sa :
                if Sa_switch == 't' :
                    break
                plt.axvline(x=Sa_switch,linestyle=':',color='r')
            for T_switch in vertex_T :
                if T_switch == 't' :
                    break
                plt.axvline(x=T_switch,linestyle=':',color='b')
            plt.axhline(y=1,color='k', linestyle='--',linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.legend(loc='best')
            ss_diff = sum(map(lambda x: abs(x-1), Dmu_ratio))
            print("sum of s.s.diff(1):",ss_diff)
            if save == True :
                plt.savefig(result_dir+'/D_mu.png')
            plt.show()

        #this using for call data from gdx file
        #subprocess.call(["gdxdump", os.path.join(self.ws.working_directory, "data.gdx")])

    def solve_detail(self,vertex_Sa,vertex_T,org_min_dist):
        dist = org_min_dist
        cur_vertex_Sa = vertex_Sa
        cur_vertex_T = vertex_T
        min_FId = 100
        critical_vertex = None

        while dist != 1 :
            dist = dist//2
            if cur_vertex_Sa:
                poss_vertex_Sa_list = self.crtGridVertexList(vertex=cur_vertex_Sa,v_range=dist)
            else :
                poss_vertex_Sa_list = [[]]
            if cur_vertex_T:
                poss_vertex_T_list = self.crtGridVertexList(vertex=cur_vertex_T,v_range=dist)
            else :
                poss_vertex_T_list = [[]]
            vertex_list = [(Sa,T) for Sa in poss_vertex_Sa_list for T in poss_vertex_T_list]
            #print(poss_vertex_list)
            for vertex in vertex_list:
                print(vertex)
                f = self.solve_result(vertex[0],vertex[1])
                if f < min_FId:
                    min_FId = f
                    critical_vertex = vertex
            cur_vertex = critical_vertex
            print(cur_vertex)
            pid = os.getpid()
            p = psutil.Process(pid)
            info = p.memory_full_info()
            memory = info.uss/1024/1024
            print("ex_search dist:{} memory used:{}".format(dist,memory))
            gc.collect()
        return critical_vertex

if __name__ == "__main__":
    test = AlcoholicCSTR(4)
    test.setStartDirect(-1,-1)
    timer = timer.MyTimer()
    result_vertex = test.checkVertex([120,380])
    using_time = timer.getTime(kind='real')
    print(result_vertex)
    print('using time:',using_time)

    exit()