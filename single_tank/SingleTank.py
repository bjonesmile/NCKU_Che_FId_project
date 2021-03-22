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
    class Block(object):
        def __init__(self,shift_time=-1,Vertex=[],MaxSV=-1,MinSV=-1,passFId=0.0):
            self.shift = shift_time
            self.BlkVertex = Vertex
            self.passFId = passFId
            pass

        def showBlockData(self):
            print(f"Block shift: {self.shift}")
            print(f"Block vertex: {self.BlkVertex}")
            print(f"Block pass FId value: {self.passFId}")
    
    def __init__(self, Nz):
        """
        docstring
        """
        self.Nz = Nz
        self.total_sim_time = 800
        self.time_len = self.total_sim_time//Nz
        self.startDirect = 1
        self.init_h = 5.0
        self.cal_vertex_num = 0

        self.infeasible_sol_number = 0

        self.vertex_set = None
        self.vertex_setNum = 0
        self.criticalVertex = []
        self.curBlkMaxSV = -1
        self.curBlkMinSV = -1

        self.ws = GamsWorkspace(working_directory = os.getcwd())
        self.db = self.ws.add_database()
        self.opt = self.ws.add_options()
        self.opt.defines["gdxincname"] = self.db.name
        self.opt.all_model_types = "sbb"

        self.drawing = 1

        self.db.add_parameter("vertex", 1, "list of direction of each time point in time horizon")
        
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
        
        self.BlockList = []
        for i in range(self.Nz):
            self.BlockList.append(self.Block())
        pass

    def setStartDirect(self, d):
        self.startDirect = d
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
        
        print(v_range_set.shape)
        print(v_range_set)
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
        h = []
        for rec in DataFId.out_db["h"] :
            h.append(rec.level)
        qout = []
        for rec in DataFId.out_db["qout"] :
            qout.append(rec.level)
        theta = []
        for rec in DataFId.out_db["theta"] :
            theta.append(rec.level)
        

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
        DataFId.out_db.export(datafilename)
  
        print("Content of GDX file '"+datafilename+"':")

        if self.drawing == 1 :

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
        exit()

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
            if ms > 2 or ss > 1:
                print(ms,ss)
                return False, None
            else :
                if FId < minFId :
                    criticalvertex = vertexBlk.copy()
                    minFId = FId
            
            """elif FId > lastBlkFId+0.001 :
                print(f"pass FId {FId} larger then lastBlkFId {lastBlkFId}")
                return False, None"""
            v_i += 1
            self.cal_vertex_num += 1
        print("search finished")
        print(minFId,criticalvertex)
        return minFId, criticalvertex

    def solve(self,vertexNum):
        n = 0
        shiftLeftNum = self.Nz

        FId = 1000
        lastBlkVertex = None
        while n < self.Nz :
            self.criticalVertex.clear()
            vertexList = self.genVertexList(v_num=shiftLeftNum,blk_len=self.time_len,num=vertexNum)
            print(vertexList)
            blk_len = self.time_len*(n+1)
            if n == 0 :
                passFId, passVertex= self.searchMinFid(vertexList=vertexList,BlkNum=n,BlkDirect=self.startDirect)
            else:
                vertexList = self.connectVertex(blkNum=n,inputVertex=lastBlkVertex,VertexList=vertexList)
                if blk_len > self.total_sim_time :
                    blk_len = self.total_sim_time
                passFId, passVertex= self.searchMinFid(vertexList=vertexList,BlkNum=n,BlkDirect=self.startDirect)
            
            print(passFId,passVertex)
            lastBlkVertex = passVertex
            #MaxSV, MinSV = self.getSVbyFId(SV=self.init_h,fid=passFId,blkNum=n,blk_len=blk_len,blkDirect=self.startDirect,Blkvertex=passVertex)

            self.BlockList[n].shift = len(passVertex)
            self.BlockList[n].BlkVertex = passVertex.copy()
            self.BlockList[n].passFId = passFId
            
            if passFId < FId :
                FId = passFId
            clear_gmsfile.clearfile()
            shiftLeftNum = self.Nz - len(passVertex) 
            print(f"Block[{n+1}] pass FId: {passFId}")
            print(f"Block[{n+1}] critical vertex: {passVertex}")
            #input()
            n += 1

        for n in range(self.Nz) :
            self.BlockList[n].showBlockData()
        self.criticalVertex = passVertex.copy()
        return FId

    def solve_d(self,blk_divid_num,input_vertex=None):
        org_v_range = (self.total_sim_time//self.Nz)//blk_divid_num
        cur_v_range = org_v_range//2

        loop_n = 0
        passVertex = None
        if input_vertex is None :
            last_passVertex = self.criticalVertex
        else:
            last_passVertex = input_vertex
        
        while True :
            if loop_n != 0:
                last_passVertex = passVertex
            vertexList = self.crtGridVertexList(vertex=last_passVertex,v_range=cur_v_range,n=3)     
            passFId, passVertex= self.searchMinFid(vertexList=vertexList,BlkNum=-1,BlkDirect=self.startDirect)
            clear_gmsfile.clearfile()
            print("cur_v_range :",cur_v_range)
            print("grid_n :",3)
            print(vertexList)
            print(passFId,passVertex)
            if cur_v_range == 1 and last_passVertex == passVertex :
                break
            loop_n += 1
            if cur_v_range == 1 :
                continue
            else:
                cur_v_range = cur_v_range//2
        
        return passFId, passVertex

    def get_oAry_from_csv(self,file):
        with open(file) as csv_file:
            reader = csv.reader(csv_file,delimiter=',')
            line_count = 0
            oAry = None
            for row in reader :
                ary = np.array(list(row),dtype = np.int)
                if line_count == 0:
                    oAry = ary
                else :
                    oAry = np.vstack((oAry,ary))
                line_count += 1
        return oAry

    def solve_oAry(self,oAry):
        if isinstance(oAry,np.ndarray):
            run_size = oAry.shape[0]
            blk_num = oAry.shape[1]
            blk_size = self.total_sim_time//blk_num
            blk_left = self.total_sim_time-blk_size*blk_num
            last_blk_size = blk_size+blk_left
        else:
            raise TypeError("oAry arg must be ndarray")
        print("run_size:",run_size)
        print("blk_num:",blk_num)
        print("blk_size:",blk_size)
        print("blk_left:",blk_left)
        print("last_blk_size:",last_blk_size)
        FIdary = []

        run_t = 0
        for ary in oAry :
            vertexList = []

            vertex = self.db.get_parameter("vertex")
            vertex.clear()
            t = 1
            for blk in range(blk_num):
                if ary[blk] % 2 == 1:
                    blk_direct = 1
                else :
                    blk_direct = -1
                if blk != blk_num-1:        
                    for i in range(t,blk_size+t):
                        vertex.add_record(str(i)).value = blk_direct
                    t = t+blk_size
                else:
                    for i in range(t,last_blk_size+t):
                        vertex.add_record(str(i)).value = blk_direct
            vertex_num = self.db.get_parameter("vertex").get_number_records()
            if vertex_num == self.total_sim_time :
                pass
                #print(vertex_num)
            else :
                raise ValueError(f"vertex_num :{vertex_num} not match to {self.total_sim_time}")

            BlkFId = self.ws.add_job_from_file(self.jobGAMSfile)
            BlkFId.run(self.opt,databases = self.db)
            FId = BlkFId.out_db["z"].last_record().level
            ms = BlkFId.out_db["ms"].find_record().value
            ss = BlkFId.out_db["ss"].find_record().value
            print(f"Run {run_t} FId: {FId}")
            run_t += 1
            if ms > 2 or ss > 1:
                print(ms,ss)
                raise RuntimeError("infeasible solution result")
            else :
                FIdary.append(FId)
        
        print(FIdary)
        return FIdary

    def output_OA_result(self,oAry,oa_result,removeOver=True):
        eff_avg = np.average(oa_result)
        print("effect avg:",np.average(oa_result))
        oa_result = np.array(oa_result)
        response = np.reshape(oa_result,(-1,1))
        table = np.hstack((oAry,response))
        oAryT = oAry.T

        eff = 0
        eff_ary = None
        for row in oAryT :
            pos_eff = 0
            pos_num = 0
            neg_eff = 0
            neg_num = 0
            for i in range(len(row)) :
                if row[i] == 1 :
                    pos_eff += response[i]
                    pos_num += 1
                else :
                    neg_eff += response[i]
                    neg_num += 1
            if eff == 0 :
                eff_ary = np.array([pos_eff/pos_num,neg_eff/neg_num]).reshape(-1,1)
            else :
                eff_ary = np.hstack((eff_ary,np.array([pos_eff/pos_num,neg_eff/neg_num]).reshape(-1,1)))
            eff += 1

        #plot response table
        x_eff = np.linspace(0,eff*2,eff*2)
        import string
        factorID = list(string.ascii_uppercase[:26])
        factorID.extend(["AA","AB","AC","AD","AE"])
        my_xticks = []
        for name in factorID :
            my_xticks.extend([name+'1',name+'2'])
        plt.xticks(x_eff,my_xticks)

        for i in range(eff*2):
            plt.axvline(x=x_eff[i])
            j = i//2
            if i%2 != 0 :
                continue
            x = [x_eff[i],x_eff[i+1]]
            y = [eff_ary[0][j],eff_ary[1][j]]
            plt.plot(x,y,color='black',marker='o')
        plt.xlabel("factor")
        plt.ylabel("FId value")
        plt.title("response table")
        plt.savefig("response_table_Nz"+str(self.Nz)+".png")
        plt.show()

        with open("oa_resultSingleTankNz"+str(self.Nz)+".csv",'w',newline='') as csv_file :
            writer = csv.writer(csv_file)
            writer.writerows(table)

        with open("eff_result.csv",'w',newline='') as csv_file :
            writer = csv.writer(csv_file)
            factor_name_list = []
            for i in range(31) :
                if i != 30 :
                    name = "time "+str(i*26+1)+" to "+str((i+1)*26)
                else :
                    name = "time "+str(i*26+1)+" to "+str(800)
                factor_name_list.append(name)
            
            factor_name_list = np.array(factor_name_list)
            eff_diplay = np.vstack((factor_name_list,eff_ary))
            writer.writerows(eff_diplay)

            total_diff = []
            obv_factor = []
            obv_eff = []
            for i in range(eff_ary.shape[1]) :
                diff = eff_ary[0][i] - eff_ary[1][i]
                if abs(diff) > 0.035 :
                    obv_factor.append(factor_name_list[i])
                    if diff < 0 :
                        obv_eff.append(eff_ary[0][i])
                    else :
                        obv_eff.append(eff_ary[1][i])
                total_diff.append(diff)

            eff_mean = np.mean(total_diff)
            eff_sd = np.std(total_diff,ddof=1)*0.6745 #choose 
            print("mean eff :",eff_mean)
            print("std eff :",eff_sd)

            #try using std range to chosse
            obv_factor.clear()
            obv_eff.clear()
            for i in range(eff_ary.shape[1]) :
                diff = total_diff[i]
                print(diff)
                if eff_mean-eff_sd > diff or diff > eff_mean+eff_sd :
                    print(f"block {i} is obivous factor")
                    obv_factor.append(factor_name_list[i])
                    if diff < 0 :
                        obv_eff.append(eff_ary[0][i])
                    else :
                        obv_eff.append(eff_ary[1][i])
            eff_diplay = np.vstack((eff_diplay,total_diff))
            writer.writerow(total_diff)
            writer.writerow([])

            total_Absdiff = np.array([abs(x) for x in total_diff])
            sort_i = np.argsort((-total_Absdiff))
            eff_diplay = eff_diplay[:,sort_i]

            writer.writerow(["after sort with abs value"])
            total_diff_sorted = sorted(total_diff,key= lambda x: np.abs(x),reverse=True)
            writer.writerow(total_diff_sorted)

            writer.writerows(eff_diplay)

            pos_total_diff = []
            for d in total_diff :
                if d < 0 :
                    pos_total_diff.append(-d)
                else :
                    pos_total_diff.append(d)

            obv_eff_rank = []
            t = 0
            for r in range(0,31):
                if eff_diplay[1,r] < eff_diplay[2,r] :
                    obv_eff_rank.append(float(eff_diplay[1,r]))
                else :
                    obv_eff_rank.append(float(eff_diplay[2,r]))
                pred_eff = sum(obv_eff_rank)-(len(obv_eff_rank)-1)*eff_avg
                print(f"consider {t+1} effect: {pred_eff}")
                t += 1
                if pred_eff < 0 :
                    print("with too much effect pred comes to 0!")
                    break

            plt.hist(total_diff,bins=20,edgecolor='black',histtype='bar')
            plt.show()
            pos_total_diff = np.array(pos_total_diff)
            writer.writerow(pos_total_diff)
            plt.hist(pos_total_diff,bins=20,edgecolor='black',histtype='bar')
            plt.show()

            obv_eff = np.array(obv_eff)
            pred_FId = np.sum(obv_eff)-(obv_eff.shape[0]-1)*eff_avg
            print("pred_FId:",pred_FId)
            writer.writerow(obv_factor)
            writer.writerow(obv_eff)
            writer.writerow(["eff_avg",eff_avg])
            writer.writerow(["pred_FId",pred_FId])



if __name__ == "__main__":
    block_divid_num = 10

    clear_gmsfile.clearfile()
    timer = timer.MyTimer()
    model = SingleTank(10)
    model.setStartDirect(1)
    
    oAry = model.get_oAry_from_csv(file="L32_31.csv")
    oa_result = model.solve_oAry(oAry)
    model.output_OA_result(oAry,oa_result)
    timer.getTime(kind="real")
    exit()
    model.getData(vertex=[400],startDirect=1)
    """resultFId = model.solve(block_divid_num)
    
    print("Result FId:",resultFId)
    print("block average divided point search cirtical vertex:",model.criticalVertex)
    print("total calculate vertex:",model.cal_vertex_num)
    timer.getTime(kind="process")
    t1 = timer.getTime(kind="real")"""

    finalFId, finalVertex = model.solve_d(block_divid_num,input_vertex=[667])
    print("final FId:",finalFId)
    print("grid loop search cirtical vertex:",finalVertex)
    print("total calculate vertex:",model.cal_vertex_num)
    timer.getTime(kind="process")
    t2 = timer.getTime(kind="real")
