from gams import *
import sys
import os
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
        self.time_len = self.total_sim_time//Nz
        self.startDirect = 1
        self.startDirectSa = 1
        self.startDirectT = 1
        self.MV_num = 2
        self.cal_vertex_num = 0

        self.vertex_set = None
        self.vertex_setNum = 0
        self.targetMinFId = 10
        self.targetVertex = None
        self.targetDirect = None

        self.criticalVertex = []
        self.curBlkMaxSV = -1
        self.curBlkMinSV = -1
        self.similar_vertex = []

        self.ws = GamsWorkspace(working_directory = os.getcwd())
        self.db = self.ws.add_database()
        self.opt = self.ws.add_options()
        self.opt.defines["gdxincname"] = self.db.name
        self.opt.all_model_types = "sbb"
        self.opt.optcr = 0

        self.infeasible_sol_number = 0
        self.error_result = []

        self.drawing = 1

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
        else :
            self.jobGAMSfile = "alcoholicCSTRNz1.gms"
        
        pass

    def setStartDirect(self, directSa, directT):
        self.startDirectSa = directSa
        self.startDirectT = directT

        self.startDirect = directSa
        pass

    def setMVnumber(self, num):
        self.MV_num = num
        pass

    def connectVertex(self,blkNum,inputVertex,VertexList):
        print("connect VertexList")
        #print("input vertex",inputVertex)
        lastblklen = blkNum*self.time_len
        #print("lastblklen :",lastblklen)
        newVertexList = []
        for v in VertexList :
            temp = inputVertex.copy()
            newlist = [x+lastblklen for x in v]
            temp.extend(newlist)
            newVertexList.append(temp)
        #print(newVertexList)
        return newVertexList

    def genVertexList(self,v_num,blk_len,num) :
        print("create VertexList")
        VertexList = []
        VertexList.append([])
        for i in range(v_num):
            if i == 0:
                original = list(np.linspace(1,blk_len,num=num,endpoint=False))
                original = [int(v) for v in original]
                for i in original:
                    VertexList.append([i])
            else:
                for x in itertools.combinations_with_replacement(original, i+1):
                    if len(list(x)) == len(set(x)):
                        VertexList.append(list(x))
        print(len(VertexList))
        return VertexList

    def crtTotalVertexList(self,v_num,num):
        blk_len = self.time_len
        vertex1 = self.genVertexList(v_num,blk_len,num)
        vertex2 = vertex1.copy()
        VertexList = []
        for i in range(len(vertex1)):
            for j in range(len(vertex2)):
                if (len(vertex1[i]) + len(vertex2[j])) > v_num :
                    continue
                else:
                    VertexList.append([vertex1[i],vertex2[j]])
        print(VertexList)
        return VertexList    

    def getData(self,vertex,startDirect):
        vertex_Sa, vertex_T = vertex
        vertexSa = self.db.get_parameter("vertex")
        vertexSa.clear()
        vertexT = self.db.get_parameter("vertexT")
        vertexT.clear()

        v_len_Sa = len(vertex_Sa)
        v_len_T = len(vertex_T)
    
        d_cur_Sa = startDirect[0]
        d_cur_T = startDirect[1]
        shift_Sa = 0
        shift_T  = 0
        for i in range(1,self.total_sim_time+1):
            if shift_Sa < v_len_Sa :
                if(i >= vertex_Sa[shift_Sa]):
                    d_cur_Sa = -d_cur_Sa
                    shift_Sa += 1
            if shift_T < v_len_T :
                if(i >= vertex_T[shift_T]):
                    d_cur_T = -d_cur_T
                    shift_T += 1
            vertexSa.add_record(str(i)).value = d_cur_Sa
            vertexT.add_record(str(i)).value = d_cur_T
        print(self.db.get_parameter("vertex").get_number_records())
        print(self.db.get_parameter("vertexT").get_number_records())

        DataFId = self.ws.add_job_from_file(self.jobGAMSfile)
        DataFId.run(self.opt,databases = self.db)
        FId = DataFId.out_db["z"].last_record().level
        ms = DataFId.out_db["ms"].find_record().value
        ss = DataFId.out_db["ss"].find_record().value

        print(FId)

        s = []
        for rec in DataFId.out_db["S"] :
            s.append(rec.level)
        c = []
        for rec in DataFId.out_db["C"] :
            c.append(rec.level)
        p = []
        for rec in DataFId.out_db["P"] :
            p.append(rec.level)
        v = []
        for rec in DataFId.out_db["V"] :
            v.append(rec.level)
        Fin = []
        for rec in DataFId.out_db["Fin"] :
            Fin.append(rec.level)
        Fout = []
        for rec in DataFId.out_db["Fout"] :
            Fout.append(rec.level)
        Sa = []
        for rec in DataFId.out_db["Sa"] :
            Sa.append(rec.level)
        T = []
        for rec in DataFId.out_db["T"] :
            T.append(rec.level)
        norm_Sa = []

        if ms > 2 or ss > 1:
            print(ms,ss)
            print("Infeasible solution found.",ms,ss)
            self.infeasible_sol_number += 1
        print("get Result Data finished")
        if self.startDirect == 1:
            direct_str = "p"
        elif self.startDirect == -1:
            direct_str = "n"
        datafilename = "alcoholicCSTRNz"+str(self.Nz)+direct_str+".gdx"
        DataFId.out_db.export(datafilename)
  
        print("Content of GDX file '"+datafilename+"':")

        if self.drawing == 1 :

            t = np.linspace(0, self.total_sim_time, self.total_sim_time)
            plt.plot(t, s, 'y-', label='s', linewidth=2)
            plt.plot(t, c, 'r-', label='c', linewidth=2)
            plt.plot(t, p, 'g-', label='p', linewidth=2)
            plt.axhline(y=40,color='k', linestyle='--',linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('Conc (g/L)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')
            plt.show()

            plt.plot(t, v, 'b-', label='v', linewidth=2)
            plt.axhline(y=3,color='k', linestyle='--',linewidth=2)
            plt.axhline(y=1.5,color='k', linestyle='--',linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('volume (L)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')
            plt.show()

            plt.plot(t, Fin, 'b-', label='Fin', linewidth=2)
            plt.plot(t, Fout, 'r-', label='Fout', linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('flow rate (L/hr)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')
            plt.show()

            plt.plot(t, Sa, 'b-', label='Sa', linewidth=2)
            plt.axhline(y=100,color='b', linestyle='--',linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('Conc (g/L)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')

            plt.plot(t, T, 'b-', label='T', linewidth=2)
            plt.axhline(y=30,color='b', linestyle='--',linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('Temp (C)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')
            plt.show()

        #this using for call data from gdx file
        #subprocess.call(["gdxdump", os.path.join(self.ws.working_directory, "data.gdx")])
        exit()

    def calFId(self,vertexList):
        x = []
        y = []
        f = []

        v_i = 0
        BlkDirect = self.startDirect
        minFId = 10.0
        criticalvertex = None
        while v_i < len(vertexList):
            vertexBlk = list(vertexList[v_i])
            v_len = len(vertexBlk)
            print(v_i)
            print(f"vertex: {vertexBlk}")
            print(f"vertex length: {v_len}")
            print(f"block start direction: {BlkDirect}")
            vertex = self.db.get_parameter("vertex")
            vertex.clear()

            shift = 0
            direct_current = BlkDirect
            for i in range(1,self.total_sim_time+1):
                if shift == v_len :
                    vertex.add_record(str(i)).value = direct_current
                    continue
                if(i >= vertexBlk[shift]):
                    direct_current = -direct_current
                    shift += 1
                else :
                    pass
                vertex.add_record(str(i)).value = direct_current
            print(self.db.get_parameter("vertex").get_number_records())

            BlkFId = self.ws.add_job_from_file(self.jobGAMSfile)
            BlkFId.run(self.opt,databases = self.db)
            FId = BlkFId.out_db["z"].last_record().level
            ms = BlkFId.out_db["ms"].find_record().value
            ss = BlkFId.out_db["ss"].find_record().value
            print(f"vertex {vertexBlk} FId: {FId}")
            print(ms,ss)
            if ms > 2 or ss > 1:
                print("Infeasible solution found.",ms,ss)
                self.infeasible_sol_number += 1

            if len(vertexBlk) == 0 :
                x.append(0)
                y.append(0)
                f.append(FId)
            elif len(vertexBlk) == 1 :
                x.append(0)
                y.append(vertexBlk[0])
                f.append(FId)
            elif len(vertexBlk) == 2 :
                x.append(vertexBlk[0])
                y.append(vertexBlk[1])
                f.append(FId)
            else :
                pass
                
            print(x[-1],y[-1],f[-1])

            if FId < minFId :
                if FId < 0.01 :
                    self.error_result.append(vertexBlk.copy())
                else :
                    criticalvertex = vertexBlk.copy()
                    minFId = FId
                    spec = v_i
            # consider close result for future opt
            if abs(FId-minFId) < 0.00001 :
                if len(self.similar_vertex) >= 10 :
                    self.similar_vertex.pop()
                self.similar_vertex.insert(0,{"Block":-1, "vertex":vertexBlk.copy(), "FId":FId})
            v_i += 1
            self.cal_vertex_num += 1
        print("search finished")
        print(minFId,criticalvertex,spec)

        with open('EXresultNz'+str(self.Nz)+'_'+str(240)+'.csv','w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for i in range(len(x)) :
                writer.writerow([x[i],y[i],f[i]])

        plt.scatter(x, y, marker='.',c=f)
        plt.title("ex full region plot")
        plt.gray()
        plt.show()

        spec_x = x[spec-25:spec+25]
        spec_y = y[spec-25:spec+25]
        spec_f = f[spec-25:spec+25]

        plt.scatter(spec_x, spec_y, marker='.',c=spec_f)
        plt.title("spec region plot")
        plt.gray()
        plt.show()

        return minFId, criticalvertex

    def solve_EX(self,num=20):
        v_num = self.Nz*self.MV_num
        vertex_p = list(np.linspace(1,240,num=num,endpoint=False,dtype=np.int))
        if num >= 240 :
            vertex_p = list(range(1,241))
        vertex_list = list(itertools.combinations(vertex_p,1))
        #print(vertex_list)
        vertex_list2 = list(itertools.combinations(vertex_p,2))
        vertex_list.extend(vertex_list2)
        #print(vertex_list)
        
        vertex_list.clear()
        vertex_list = vertex_list2
        print(len(vertex_list))
        input()

        minFId, critical_vertex =self.calFId(vertex_list)

        print(f"FId:{minFId}, critical vertex:{critical_vertex}")

        return minFId, critical_vertex

    def solve_multithreading(self,vertex_Sa,vertex_T):
        direct = [(+1,+1),(-1,+1),(+1,-1),(-1,-1)]

        min_direct = None
        minFId = 1.0

        db = self.ws.add_database()
        vertexSa = db.add_parameter("vertex", 1, "list of direction of each time point in time horizon for uncertain parameter Sa")
        vertexT = db.add_parameter("vertexT", 1, "list of direction of each time point in time horizon for uncertain parameter T")
        v_len_Sa = len(vertex_Sa)
        v_len_T = len(vertex_T)
        for d in direct :
            vertexSa.clear()
            vertexT.clear()
            d_cur_Sa = d[0]
            d_cur_T = d[1]
            shift_Sa = 0
            shift_T  = 0
            for i in range(1,self.total_sim_time+1):
                if shift_Sa < v_len_Sa :
                    if(i >= vertex_Sa[shift_Sa]):
                        d_cur_Sa = -d_cur_Sa
                        shift_Sa += 1
                if shift_T < v_len_T :
                    if(i >= vertex_T[shift_T]):
                        d_cur_T = -d_cur_T
                        shift_T += 1
                vertexSa.add_record(str(i)).value = d_cur_Sa
                vertexT.add_record(str(i)).value = d_cur_T

            print(vertex_Sa)
            print(vertex_T)
            print(d)
            """k = 0
            for rec in db["vertex"] :
                print(k,rec.value)
                k += 1
            k = 0
            for rec in db["vertexT"] :
                print(k,rec.value)
                k += 1"""
            
            job = self.ws.add_job_from_file(self.jobGAMSfile)
            opt = self.ws.add_options()
            opt.defines["gdxincname"] = db.name
            opt.all_model_types = "sbb"
            opt.optcr = 0
            job.run(opt,databases = db)
            FId = job.out_db.get_variable("z").first_record().level
            if FId < minFId :
                min_direct = d
                minFId = FId
        print(f"vertex Sa: {vertex_Sa}, vertex T: {vertex_T}\nmin direct: {min_direct}, min FId: {minFId}")
        return minFId, min_direct

    def read_lines(self,filename):
        with open(filename, 'rU') as data:
            reader = csv.reader(data)
            for row in reader:
                yield [ float(i) for i in row ]

    def read_csv_data(self,filename):
        datas = list(self.read_lines(filename))
        min_FId = datas[28676][2]
        min_x = datas[28676][0]
        min_y = datas[28676][1]
        i = 0

        x = []
        y = []
        f = []
        """for row in datas :
            if min_x-30 < row[0] < min_x+30 and min_y-30 < row[1] < min_y+30 :
                x.append(row[0])
                y.append(row[1])
                f.append(min_FId/row[2])"""
        for row in datas :
            x.append(row[0])
            y.append(row[1])
            f.append(min_FId/row[2])
        
        print(min(f))
        print(max(f))

        plt.scatter(x, y, marker='.',c=f)
        plt.title("EX total plot")
        plt.gray()
        plt.show()

# Nz2: [(176,239),()]

if __name__ == "__main__":
    clear_gmsfile.clearfile()
    cstr_test = AlcoholicCSTR(3)
    cstr_test.setStartDirect(-1,-1)
    cstr_test.setMVnumber(2)

    cstr_test.getData(vertex=[(202,),()],startDirect=(-1,-1))
    exit()
      
    vertex_p = list(np.linspace(1,120,num=12,endpoint=False,dtype=np.int))
    vertexSa_list = list(itertools.combinations(vertex_p,1))
    vertexT_list = list(itertools.combinations(vertex_p,3))
    #cstr_test.solve_EX(num=240)
    """cstr_test.read_csv_data('EXresultNz1_240refine.csv')
    exit()"""

    #text vertex [[1,232],[45,178],[69,158],[105,204],[33,240]]
    #vertexSa_list = [[1,232],[45,178],[69,158],[105,204],[33,240],[123,156,170,200],[130,156,170,200],[140,156,170,200],[123,156,177,200],[123,156,180,200],[123,156,190,200]]
    print(vertexSa_list)
    print(vertexT_list)
    print(len(vertexSa_list))
    print(len(vertexT_list))
    print(f"total vertex num: {len(vertexSa_list)*len(vertexT_list)}")
    input()

    timer = timer.MyTimer()
    lock = threading.Lock()
    def run_scenario(cstr_test, mult_p):
        obj, direct = cstr_test.solve_multithreading(mult_p[0],mult_p[1])
        lock.acquire()
        print("Scenario mult_p=" + str(mult_p) + ", Obj:" + str(obj))
        if obj < cstr_test.targetMinFId :
            cstr_test.targetMinFId = obj
            cstr_test.targetVertex = mult_p.copy()
            cstr_test.targetDirect = direct
        lock.release()

    #thread define here
    
    t_num = 0
    t_limit = 100
    t_list = []
    for vSa in vertexSa_list :
        for vT in vertexT_list :
            v_temp = [vSa,vT]
            t = threading.Thread(target=run_scenario, args=(cstr_test, v_temp))
            t_list.append(t)

    for t in t_list :
        t.start()
        while True :
            if len(threading.enumerate()) < 8:
                t_num += 1
                print(f"finished t: {t_num}")
                break

    for t in t_list :
        t.join()

    print(cstr_test.targetMinFId)
    print(cstr_test.targetVertex)
    print(cstr_test.targetDirect)

    timer.getTime(kind="process")
    timer.getTime(kind="real")
    exit()