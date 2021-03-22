from gams import *
import sys
import os
import numpy as np
import itertools
import matplotlib.pyplot as plt

import clear_gmsfile
import mytimer as timer

class AlcoholicCSTR():
    class Block(object):
        def __init__(self,shift_time=-1,Vertex=[],MaxSV=-1,MinSV=-1,passFId=0.0):
            self.shift = shift_time
            self.BlkVertex = Vertex
            self.BlkMaxSV = MaxSV
            self.BlkMinSV = MinSV
            self.passFId = passFId
            pass

        def showBlockData(self):
            print(f"Block shift: {self.shift}")
            print(f"Block vertex: {self.BlkVertex}")
            print(f"Block MAXSV: {self.BlkMaxSV}")
            print(f"Block MINSV: {self.BlkMinSV}")
            print(f"Block SV range value: {self.passFId}")
    
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
        else :
            self.jobGAMSfile = "alcoholicCSTRNz1.gms"
        
        self.BlockList = []
        for i in range(self.Nz):
            self.BlockList.append(self.Block())
        pass

    def setStartDirect(self, directSa, directT):
        self.startDirectSa = directSa
        self.startDirectT = directT
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

    def genVertexList_byInput(self,inputVertex,n):
        v_range = 10
        #v_range_set = np.empty((v_len,num),dtype= np.float)
        v_range_set = None
        for v in inputVertex :
            if v_range_set is None :
                v_range_set = np.linspace(v-v_range,v+v_range,num=n+1,dtype=np.int)
            else :
                temp_set = np.linspace(v-v_range,v+v_range,num=n+1,dtype=np.int)
                v_range_set = np.vstack((v_range_set,temp_set))
        vertexList = []
        for i in range(len(v_range_set)-1):
            if i == 0:
                for x in itertools.product(v_range_set[i],v_range_set[i+1]):
                    vertexList.append(list(x))
            else:
                for x in itertools.product(vertexList,v_range_set[i+1]):
                    temp = []
                    for item in x :
                        if isinstance(item,list):
                            temp.extend(item)
                        else:
                            temp.append(item)
                    vertexList.append(temp)
        print(vertexList)
        return vertexList        

    def getData(self,vertex,startDirect):
        dataVertex = vertex.copy()
        
        vertex = self.db.get_parameter("vertex")
        vertex.clear()

        v_len = len(dataVertex)

        shift = 0
        direct_current = startDirect
        for i in range(1,self.total_sim_time+1):
            if shift == v_len :
                vertex.add_record(str(i)).value = direct_current
                continue
            if(i >= dataVertex[shift]):
                direct_current = -direct_current
                shift += 1
            else :
                pass
            vertex.add_record(str(i)).value = direct_current
        print(self.db.get_parameter("vertex").get_number_records())

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
        for norm_t in range(len(Sa)) :
            norm_Sa.append(100)

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
            plt.plot(t, s, 'b-', label='s', linewidth=2)
            plt.plot(t, c, 'k-', label='c', linewidth=2)
            plt.plot(t, p, 'g-', label='p', linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('Conc (g/L)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')
            plt.show()

            plt.plot(t, v, 'b-', label='v', linewidth=2)
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

            plt.plot(t, norm_Sa, 'b--', label='nominal Sa', linewidth=2)
            plt.plot(t, Sa, 'b-', label='Sa', linewidth=2)
            plt.grid(color='y', linestyle='--', linewidth=1, alpha=0.3)
            plt.ylabel('Conc (g/L)')
            plt.xlabel('time (hr)')
            plt.legend(loc='best')
            plt.show()

        #this using for call data from gdx file
        #subprocess.call(["gdxdump", os.path.join(self.ws.working_directory, "data.gdx")])
        exit()

    def searchMinFId(self,vertexList,BlkNum):
        v_i = 0
        minFId = 1.0
        criticalvertex = None
        while v_i < len(vertexList):
            vertexSa, vertexT = vertexList[v_i]
            print(v_i)
            print(f"block :{BlkNum}")
            print(f"vertex Sa: {vertexSa}")
            print(f"vertex T: {vertexT}")
            print(f"block start direction: Sa {self.startDirectSa}, T {self.startDirectT}")
            vertex = self.db.get_parameter("vertex")
            vertex.clear()
            vertex_T = self.db.get_parameter("vertexT")
            vertex_T.clear()

            shift = 0
            direct_current = self.startDirectSa
            v_len = len(vertexSa)
            for i in range(1,self.total_sim_time+1):
                if shift == v_len :
                    vertex.add_record(str(i)).value = direct_current
                    continue
                if(i >= vertexSa[shift]):
                    direct_current = -direct_current
                    shift += 1
                else :
                    pass
                vertex.add_record(str(i)).value = direct_current
            print(self.db.get_parameter("vertex").get_number_records())
        
            shift = 0
            direct_current = self.startDirectT
            v_len = len(vertexT)
            for i in range(1,self.total_sim_time+1):
                if shift == v_len :
                    vertex_T.add_record(str(i)).value = direct_current
                    continue
                if(i >= vertexT[shift]):
                    direct_current = -direct_current
                    shift += 1
                else :
                    pass
                vertex_T.add_record(str(i)).value = direct_current
            print(self.db.get_parameter("vertexT").get_number_records())

            BlkFId = self.ws.add_job_from_file(self.jobGAMSfile)
            BlkFId.run(self.opt,databases = self.db)
            FId = BlkFId.out_db["z"].last_record().level
            ms = BlkFId.out_db["ms"].find_record().value
            ss = BlkFId.out_db["ss"].find_record().value
            print(f"block {BlkNum} FId: {FId}")
            print(ms,ss)
            if ms > 2 or ss > 1:
                print("Infeasible solution found.",ms,ss)
                self.infeasible_sol_number += 1
            if FId < minFId :
                if FId < 0.01 :
                    self.error_result.append([vertexSa,vertexT].copy())
                else :
                    criticalvertex = [vertexSa,vertexT]
                    minFId = FId
            # consider close result for future opt
            if abs(FId-minFId) < 0.00001 :
                if len(self.similar_vertex) >= 10 :
                    self.similar_vertex.pop()
                self.similar_vertex.insert(0,{"Block":BlkNum, "vertex":[vertexSa,vertexT].copy(), "FId":FId})
            v_i += 1
            self.cal_vertex_num += 1
        print("search finished")
        print(minFId,criticalvertex)
        return minFId, criticalvertex

    def searchMinFid(self,vertexList,BlkNum,BlkDirect):
        v_i = 0
        minFId = 1.0
        criticalvertex = None
        while v_i < len(vertexList):
            vertexBlk = vertexList[v_i]
            v_len = len(vertexBlk)
            print(v_i)
            print(f"block {BlkNum} vertex: {vertexBlk}")
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
            print(f"block {BlkNum} FId: {FId}")
            print(ms,ss)
            if ms > 2 or ss > 1:
                print("Infeasible solution found.",ms,ss)
                self.infeasible_sol_number += 1
            if FId < minFId :
                if FId < 0.01 :
                    self.error_result.append(vertexBlk.copy())
                else :
                    criticalvertex = vertexBlk.copy()
                    minFId = FId
            # consider close result for future opt
            if abs(FId-minFId) < 0.00001 :
                if len(self.similar_vertex) >= 10 :
                    self.similar_vertex.pop()
                self.similar_vertex.insert(0,{"Block":BlkNum, "vertex":vertexBlk.copy(), "FId":FId})
            v_i += 1
            self.cal_vertex_num += 1
        print("search finished")
        print(minFId,criticalvertex)
        return minFId, criticalvertex

    def solve(self,vertexNum):
        n = 0
        shiftLeftNum = self.Nz*self.MV_num

        FId = 1000
        lastBlkVertex = None
        while n < self.Nz :
            self.criticalVertex.clear()
            vertexList = self.genVertexList(v_num=shiftLeftNum,blk_len=self.time_len,num=vertexNum)
            #vertexList.insert(0,[214])
            #vertexList.insert(0,[173, 187, 200, 213])
            print(vertexList)
            blk_len = self.time_len*(n+1)
            if n == 0 :
                passFId, passVertex= self.searchMinFid(vertexList=vertexList,BlkNum=n,BlkDirect=self.startDirect)
            else:
                vertexList = self.connectVertex(blkNum=n,inputVertex=lastBlkVertex,VertexList=vertexList)
                if blk_len > self.total_sim_time :
                    blk_len = self.total_sim_time
                passFId, passVertex= self.searchMinFid(vertexList=vertexList,BlkNum=n,BlkDirect=self.startDirect)
            
            print("pass result:",passFId,passVertex)
            lastBlkVertex = passVertex

            self.BlockList[n].shift = len(passVertex)
            self.BlockList[n].BlkVertex = passVertex.copy()
            self.BlockList[n].BlkMaxSV = None
            self.BlockList[n].BlkMinSV = None
            self.BlockList[n].passFId = passFId
            
            if passFId < FId :
                FId = passFId
            clear_gmsfile.clearfile()
            shiftLeftNum = shiftLeftNum - len(passVertex) 
            print(f"Block[{n+1}] pass FId: {passFId}")
            print(f"Block[{n+1}] critical vertex: {passVertex}")
            #input()
            n += 1

        for n in range(self.Nz) :
            self.BlockList[n].showBlockData()
        return FId

    def solve_v2(self,vertexNum):
        n = 0
        shiftLeftNum = self.Nz*self.MV_num

        FId = 1000
        lastBlkVertex = None
        while n < self.Nz :
            self.criticalVertex.clear()
            vertexList = self.crtTotalVertexList(v_num=shiftLeftNum,num=vertexNum)
            print(len(vertexList))
            if n == 0 :
                passFId, passVertex= self.searchMinFId(vertexList=vertexList,BlkNum=n)
            else:
                vertexList = self.connectVertex(blkNum=n,inputVertex=lastBlkVertex,VertexList=vertexList)
                passFId, passVertex= self.searchMinFId(vertexList=vertexList,BlkNum=n)
            
            print("pass result:",passFId,passVertex)
            lastBlkVertex = passVertex

            self.BlockList[n].shift = len(passVertex)
            self.BlockList[n].BlkVertex = passVertex.copy()
            self.BlockList[n].BlkMaxSV = None
            self.BlockList[n].BlkMinSV = None
            self.BlockList[n].passFId = passFId
            
            if passFId < FId :
                FId = passFId
            clear_gmsfile.clearfile()
            shiftLeftNum = shiftLeftNum - len(passVertex) 
            print(f"Block[{n+1}] pass FId: {passFId}")
            print(f"Block[{n+1}] critical vertex: {passVertex}")
            #input()
            n += 1

        for n in range(self.Nz) :
            self.BlockList[n].showBlockData()
        return FId

if __name__ == "__main__":
    clear_gmsfile.clearfile()
    timer = timer.MyTimer()
    cstr_test = AlcoholicCSTR(1)
    cstr_test.setStartDirect(-1,-1)
    cstr_test.setMVnumber(2)
    resultFId = cstr_test.solve_v2(20)
    print("  ")
    print("Result FId:",resultFId)
    print("total calculate vertex:",cstr_test.cal_vertex_num)
    print("other possible vertex:")
    exit()
    #cstr_test.getData(vertex=[167,179],startDirect=-1)
    resultFId = cstr_test.solve(20)
    print("  ")
    print("Result FId:",resultFId)
    print("total calculate vertex:",cstr_test.cal_vertex_num)
    print("other possible vertex:")
    for dic in cstr_test.similar_vertex :
        print(dic)
    timer.getTime(kind="process")
    timer.getTime(kind="real")