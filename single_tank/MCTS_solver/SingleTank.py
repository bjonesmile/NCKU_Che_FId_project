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

class SingleTank():

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
            self.jobGAMSfile = "singletankNz1.gms"
        elif  Nz == 2:
            self.jobGAMSfile = "singletankNz2.gms"
        elif  Nz == 3:
            self.jobGAMSfile = "singletankNz3.gms"
        elif  Nz == 4:
            self.jobGAMSfile = "singletankNz4.gms"
        elif  Nz == 5:
            self.jobGAMSfile = "singletankNz5.gms"
        elif  Nz == 8:
            self.jobGAMSfile = "singletankNz8.gms"
        elif  Nz == 10:
            self.jobGAMSfile = "singletankNz10.gms"
        else :
            self.jobGAMSfile = "singletankNz1.gms"
        
    def setStartDirect(self, d):
        self.startDirect = d
        pass

    def get_detail_file(self,vertex_F):
        t_num = len(vertex_F)
        F_step = self.total_sim_time//self.Nz
        F_list = np.linspace(F_step,self.total_sim_time,num = self.Nz,endpoint=True,dtype=np.int)
        F_list[-1] = self.total_sim_time
        print(F_list)

        t_sting = "\n"
        for t in range(t_num):
            t_sting += "\t    t"+str(t+1)+"\n"
        qout_string = "\n"
        for q in range(self.Nz):
            qout_string += "\t    qout"+str(q+1)+"(m)\n"
        qout_eq_string = "qout1(m)$(ord(m) lt "+str(F_list[0])+") ..    qout(m+1) =e= qout(m) ;\n"
        for q in range(1,self.Nz):
            qout_eq_string += "\tqout"+str(q)+"(m)$((ord(m) gt "+str(F_list[q-1])+") and (ord(m) lt "+str(F_list[q])+")) ..    qout(m+1) =e= qout(m) ;\n"
        file_string = """
        Sets
            m      discretize of time horizon /1*"""+str(self.total_sim_time)+"""/;
        Parameters"""+t_sting+"""
            A      bottom area of tank    /5/
            h0     initial value for stata var h /5.0/
        """

        file_string +="""
        $if not set gdxincname $abort 'no include file name for data file provided'
        $gdxin %gdxincname%
        $load vertex vertexT
        $gdxin

        Variables
            qout(m)     flow rate of water out of tank controlled by valve
            z           object function
            FId         flexibility index
            ;
        Positive Variable
            h(m)        height of tank
            theta(m)    uncertainty parameter
            ;
        Equations
            eq(m)       'A*dh/dt=theta-qout'
            ineq1(m)    h upper-bound
            ineq2(m)    h lowwer-bound
            ineq3(m)    qout upper-bound
            ineq4(m)    qout lowwer-bound
            uncertain(m)"""
        
        file_string += qout_string
        file_string += """\t    obj;
            ;
        eq(m)$(ord(m) lt 800) ..   A*(h(m+1)-h(m)) =e=  1/2*(theta(m+1)-qout(m+1)+theta(m)-qout(m)) ;
        uncertain(m) ..            theta(m) =e= (0.5+0.5*FId*vertex(m)) ;
        ineq1(m) ..                h(m) =l= 10 ;
        ineq2(m) ..                h(m) =g= 1 ;
        ineq3(m) ..                qout(m) =l= 0.7 ;
        ineq4(m) ..                qout(m) =g= 0 ;
        """
        file_string += qout_eq_string
        file_string += "\th.fx('1') = h0;\n"

        return file_string

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
        h = []
        for rec in job.out_db["h"] :
            h.append(rec.level)
        qout = []
        for rec in job.out_db["qout"] :
            qout.append(rec.level)
        theta = []
        for rec in job.out_db["theta"] :
            theta.append(rec.level)
        
        print(FId)
        if ms > 2 or ss > 1:
            print(ms,ss)
            print("Infeasible solution found.",ms,ss)
            self.infeasible_sol_number += 1
        print("get Result Data finished")
        if self.startDirect == 1:
            direct_str = "p"
        elif self.startDirect == -1:
            direct_str = "n"
        datafilename = "sigletankdataNz"+str(self.Nz)+direct_str+".gdx"
        job.out_db.export(datafilename)
  
        print("Content of GDX file '"+datafilename+"':")

        if self.drawing == True :

            t = np.linspace(0, self.total_sim_time, self.total_sim_time)
            plt.plot(t, h, 'b-', label='h', linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.axhline(y=10,color='k', linestyle='--',linewidth=2)
            plt.axhline(y=1,color='k', linestyle='--',linewidth=2)
            plt.ylabel('water level (m)')
            plt.xlabel('time (min)')
            plt.legend(loc='upper left')
            plt.show()

            plt.plot(t, qout, 'r-', label='qout', linewidth=2)
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
                elif vertex_F[shift] == 0 :
                    shift += 1
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

    def solve_detail(self,vertex_F,org_min_dist):
        dist = org_min_dist
        cur_vertex = vertex_F
        min_FId = 100
        critical_vertex = None

        while dist != 1 :
            dist = dist//2
            poss_vertex_list = self.crtGridVertexList(vertex=cur_vertex,v_range=dist)
            #print(poss_vertex_list)
            for vertex in poss_vertex_list:
                f = self.solve_result(vertex)
                if f < min_FId:
                    min_FId = f
                    critical_vertex = vertex.copy()
            cur_vertex = critical_vertex
            print(cur_vertex)

        return critical_vertex

if __name__ == "__main__":
    test = SingleTank(3)
    test.setStartDirect(-1)
    timer = timer.MyTimer()
    result_vertex = test.solve_detail([120,380,620],20)
    using_time = timer.getTime(kind='real')
    print(result_vertex)
    print('using time:',using_time)

    exit()
