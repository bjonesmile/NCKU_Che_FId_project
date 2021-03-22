from gams import *
import sys
import os
import numpy as np
import itertools
import clear_gmsfile
import mytimer as timer
import clear_gmsfile

def get_model_optBlkkStateVar(blk_len, fid, opt_d):
    if opt_d > 0:
        optStateVardirection = "maximizing"
    else :
        optStateVardirection = "minimizing"

    return f'''

  Sets
       m      discretize of time horizon ;
  Parameters
       A      bottom area of tank    /5/
       blk_len    discretize time length of Block 
       h0     initial value for stata var h
       FId         flexibility index /{fid}/
       vertex(m)

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load m blk_len h0 vertex
$gdxin

  Variables
       qout(m)     flow rate of water out of tank controlled by valve
       z           object function
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
       uncertain(m)
       qout1(m)
       obj;
    ;
  eq(m)$(ord(m) lt blk_len) ..   A*(h(m+1)-h(m)) =e=  1/2*(theta(m+1)-qout(m+1)+theta(m)-qout(m)) ;
  uncertain(m) ..            theta(m) =e= (0.5+0.5*FId*vertex(m)) ;
  ineq1(m) ..                h(m) =l= 10 ;
  ineq2(m) ..                h(m) =g= 1 ;
  ineq3(m) ..                qout(m) =l= 0.7 ;
  ineq4(m) ..                qout(m) =g= 0 ;

  qout1(m)$(ord(m) lt blk_len) ..    qout(m+1) =e= qout(m) ;
  h.fx('1') = h0;

  obj .. z =e= h['{blk_len}'];
  Model single_tankNz1 /all/ ;
  Scalar ms 'model status', ss 'solve status'
  Solve single_tankNz1 using minlp {optStateVardirection} z ;
  ms=single_tankNz1.modelstat; ss=single_tankNz1.solvestat;
  '''

def get_model_optBlkFId():
    return '''

  Sets
       m      discretize of time horizon ;
  Parameters
       A      bottom area of tank    /5/
       h0     initial value for stata var h
       blk_len    block length
       vertex(m)

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load m h0 blk_len vertex
$gdxin

  Variables
       FId         flexibility index
       qout(m)     flow rate of water out of tank controlled by valve
       z           object function
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
       uncertain(m)
       qout1(m)
       obj;
    ;
  eq(m)$(ord(m) lt blk_len) ..   A*(h(m+1)-h(m)) =e=  1/2*(theta(m+1)-qout(m+1)+theta(m)-qout(m)) ;
  uncertain(m) ..            theta(m) =e= (0.5+0.5*FId*vertex(m)) ;
  ineq1(m) ..                h(m) =l= 10 ;
  ineq2(m) ..                h(m) =g= 1 ;
  ineq3(m) ..                qout(m) =l= 0.7 ;
  ineq4(m) ..                qout(m) =g= 0 ;

  qout1(m)$(ord(m) lt blk_len) ..    qout(m+1) =e= qout(m) ;

  h.fx('1') = h0;
  obj .. z =e= FId;
  Model single_tankNz1 /all/ ;
  Scalar ms 'model status', ss 'solve status'
  Solve single_tankNz1 using minlp maximizing z ;
  ms=single_tankNz1.modelstat; ss=single_tankNz1.solvestat;
  Display h.l, h.m, qout.l, qout.m, z.l, z.m; 
  execute_unload 'C:\\Users\\user\\Documents\\bjonesmile_project\DynamicSystem-CSTR-bio-alcoholic-Process\\tank1sol.gdx',qout,h ; 
  '''

def get_model_optBlkMaxSV(fid,blk_len):
    return f'''

  Sets
       m      discretize of time horizon ;
  Parameters
       A      bottom area of tank    /5/
       h0     initial value for stata var h
       blk_len    block length
       vertex(m)
       FId         flexibility index  /{fid}/
$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load m h0 blk_len vertex
$gdxin

  Variables
       qout(m)     flow rate of water out of tank controlled by valve
       z           object function
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
       uncertain(m)
       qout1(m)
       obj;
    ;
  eq(m)$(ord(m) lt blk_len) ..   A*(h(m+1)-h(m)) =e=  1/2*(theta(m+1)-qout(m+1)+theta(m)-qout(m)) ;
  uncertain(m) ..            theta(m) =e= (0.5+0.5*FId*vertex(m)) ;
  ineq1(m) ..                h(m) =l= 10 ;
  ineq2(m) ..                h(m) =g= 1 ;
  ineq3(m) ..                qout(m) =l= 0.7 ;
  ineq4(m) ..                qout(m) =g= 0 ;

  qout1(m)$(ord(m) lt blk_len) ..    qout(m+1) =e= qout(m) ;

  h.fx('1') = h0;
  obj .. z =e= h['{blk_len}'];
  Model single_tankNz1 /all/ ;
  Scalar ms 'model status', ss 'solve status'
  Solve single_tankNz1 using minlp maximizing z ;
  ms=single_tankNz1.modelstat; ss=single_tankNz1.solvestat;
  Display h.l, h.m, qout.l, qout.m, z.l, z.m; 
  execute_unload 'C:\\Users\\user\\Documents\\bjonesmile_project\DynamicSystem-CSTR-bio-alcoholic-Process\\tank1sol.gdx',qout,h ; 
  '''

def get_model_optBlkMinSV(fid,blk_len):
    return f'''

  Sets
       m      discretize of time horizon ;
  Parameters
       A      bottom area of tank    /5/
       h0     initial value for stata var h
       blk_len    block length
       vertex(m)
       FId         flexibility index  /{fid}/
$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load m h0 blk_len vertex
$gdxin

  Variables
       qout(m)     flow rate of water out of tank controlled by valve
       z           object function
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
       uncertain(m)
       qout1(m)
       obj;
    ;
  eq(m)$(ord(m) lt blk_len) ..   A*(h(m+1)-h(m)) =e=  1/2*(theta(m+1)-qout(m+1)+theta(m)-qout(m)) ;
  uncertain(m) ..            theta(m) =e= (0.5+0.5*FId*vertex(m)) ;
  ineq1(m) ..                h(m) =l= 10 ;
  ineq2(m) ..                h(m) =g= 1 ;
  ineq3(m) ..                qout(m) =l= 0.7 ;
  ineq4(m) ..                qout(m) =g= 0 ;

  qout1(m)$(ord(m) lt blk_len) ..    qout(m+1) =e= qout(m) ;

  h.fx('1') = h0;
  obj .. z =e= h['{blk_len}'];
  Model single_tankNz1 /all/ ;
  Scalar ms 'model status', ss 'solve status'
  Solve single_tankNz1 using minlp minimizing z ;
  ms=single_tankNz1.modelstat; ss=single_tankNz1.solvestat;
  Display h.l, h.m, qout.l, qout.m, z.l, z.m; 
  execute_unload 'C:\\Users\\user\\Documents\\bjonesmile_project\DynamicSystem-CSTR-bio-alcoholic-Process\\tank1sol.gdx',qout,h ; 
  '''

def get_model_optFId_Nz2():
    return '''

  Sets
       m      discretize of time horizon ;
  Parameters
       A      bottom area of tank    /5/
       h0     initial value for stata var h
       vertex(m)

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load m h0 vertex
$gdxin

  Variables
       FId         flexibility index
       qout(m)     flow rate of water out of tank controlled by valve
       z           object function
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
       uncertain(m)
       qout1(m)
       qout2(m)
       obj;
    ;
  eq(m)$(ord(m) lt 800) ..   A*(h(m+1)-h(m)) =e=  1/2*(theta(m+1)-qout(m+1)+theta(m)-qout(m)) ;
  uncertain(m) ..            theta(m) =e= (0.5+0.5*FId*vertex(m)) ;
  ineq1(m) ..                h(m) =l= 10 ;
  ineq2(m) ..                h(m) =g= 1 ;
  ineq3(m) ..                qout(m) =l= 0.7 ;
  ineq4(m) ..                qout(m) =g= 0 ;

  qout1(m)$(ord(m) lt 400) ..    qout(m+1) =e= qout(m) ;
  qout2(m)$((ord(m) gt 400) and (ord(m) lt 800)) ..    qout(m+1) =e= qout(m) ;

  h.fx('1') = h0;
  obj .. z =e= FId;
  Model single_tankNz1 /all/ ;
  Scalar ms 'model status', ss 'solve status'
  Solve single_tankNz1 using minlp maximizing z ;
  ms=single_tankNz1.modelstat; ss=single_tankNz1.solvestat;
  Display h.l, h.m, qout.l, qout.m, z.l, z.m; 
  execute_unload 'C:\\Users\\user\\Documents\\bjonesmile_project\DynamicSystem-CSTR-bio-alcoholic-Process\\tank1sol.gdx',qout,h ; 
  '''

def get_model_optFId_Nz3():
    return '''

  Sets
       m      discretize of time horizon ;
  Parameters
       A      bottom area of tank    /5/
       h0     initial value for stata var h
       vertex(m)

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load m h0 vertex
$gdxin

  Variables
       FId         flexibility index
       qout(m)     flow rate of water out of tank controlled by valve
       z           object function
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
       uncertain(m)
       qout1(m)
       qout2(m)
       qout3(m)
       obj;
    ;
  eq(m)$(ord(m) lt 800) ..   A*(h(m+1)-h(m)) =e=  1/2*(theta(m+1)-qout(m+1)+theta(m)-qout(m)) ;
  uncertain(m) ..            theta(m) =e= (0.5+0.5*FId*vertex(m)) ;
  ineq1(m) ..                h(m) =l= 10 ;
  ineq2(m) ..                h(m) =g= 1 ;
  ineq3(m) ..                qout(m) =l= 0.7 ;
  ineq4(m) ..                qout(m) =g= 0 ;

  qout1(m)$(ord(m) lt 266) ..    qout(m+1) =e= qout(m) ;
  qout2(m)$((ord(m) gt 266) and (ord(m) lt 532)) ..    qout(m+1) =e= qout(m) ;
  qout3(m)$((ord(m) gt 532) and (ord(m) lt 800)) ..    qout(m+1) =e= qout(m) ;

  h.fx('1') = h0;
  obj .. z =e= FId;
  Model single_tankNz1 /all/ ;
  Scalar ms 'model status', ss 'solve status'
  Solve single_tankNz1 using minlp maximizing z ;
  ms=single_tankNz1.modelstat; ss=single_tankNz1.solvestat;
  Display h.l, h.m, qout.l, qout.m, z.l, z.m; 
  execute_unload 'C:\\Users\\user\\Documents\\bjonesmile_project\DynamicSystem-CSTR-bio-alcoholic-Process\\tank1sol.gdx',qout,h ; 
  '''

def genVertexList(v_num,blk_len,num) :
    print("create VertexList")
    VertexList = []
    VertexList.append([])
    for i in range(v_num):
        if i == 0:
            original = list(np.linspace(1,blk_len,num=num,endpoint=True))
            original = [int(v) for v in original]
            for i in original:
                VertexList.append([i])
        else:
            for x in itertools.combinations_with_replacement(original, i+1):
                if len(list(x)) == len(set(x)):
                    VertexList.append(list(x))
    print(VertexList)
    return VertexList, len(VertexList)

def genVertexList_byInput(inputVertex,n):
    v_range = 10
    input_len = len(inputVertex)
    #v_range_set = np.empty((v_len,num),dtype= np.float)
    v_range_set = None
    for v in inputVertex :
        if v_range_set is None :
            v_range_set = np.linspace(v-v_range,v+v_range,num=n+1,dtype=np.int)
        else :
            temp_set = np.linspace(v-v_range,v+v_range,num=n+1,dtype=np.int)
            v_range_set = np.vstack((v_range_set,temp_set))
    vertexList = []
    vertexList.append([])
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
            vertexList = newVertexList
    print(vertexList)
    return vertexList  

if __name__ == "__main__":
    clear_gmsfile.clearfile()
    if len(sys.argv) > 1:
        ws = GamsWorkspace(working_directory = os.getcwd(),system_directory = sys.argv[1])
    else:
        ws = GamsWorkspace(working_directory = os.getcwd())
    
    Nz = 1
    n = 0
    time_len = 800 // Nz
    vertex_set, vertex_setNum = genVertexList(v_num=1,blk_len=200,num=15)
    #vertex_set.clear()
    #vertex_set = genVertexList_byInput(inputVertex=[122,376,620],n=10)
    vertex_setNum = len(vertex_set)
    print(vertex_setNum)
    direct = -1
    init_h0 = 5.0
    input()

    db = ws.add_database()

    time = np.linspace(1,time_len,time_len,dtype= np.int)
    m = db.add_set("m", 1, "discretize of time horizon")
    for t in time:
        m.add_record(str(int(t)))

    blk_len = db.add_parameter("blk_len", 0, "discretize time length of Block")
    blk_len.add_record().value = time_len

    h0 = db.add_parameter("h0", 0, "last end state var h")
    print(init_h0)
    h0.add_record().value = init_h0

    opt = ws.add_options()
    opt.defines["gdxincname"] = db.name
    opt.all_model_types = "sbb"

    vertex = db.add_parameter("vertex", 1, "list of direction of each time point in time horizon")

    #test whole model FId opt
    i = 0
    vertex_FId = []
    for v in vertex_set :
        block_vertex = v
        v_len = len(block_vertex)
        print(f"block {n} vertex: {block_vertex}")
        print(f"block length: {time_len}")
        print(f"vertex length: {v_len}")
        print(f"block start direction: {direct}")
        vertex = db.get_parameter("vertex")
        vertex.clear()

        shift = 0
        direct_current = direct
        for i in range(1,time_len+1):
            if shift == v_len :
                vertex.add_record(str(i)).value = direct_current
                continue
            if(i >= block_vertex[shift]):
                direct_current = -direct_current
                shift += 1
            else :
                pass
            vertex.add_record(str(i)).value = direct_current

        #modelFId = ws.add_job_from_string(get_model_optFId_Nz3())
        modelFId = ws.add_job_from_file("singletankNz3.gms")
        modelFId.run(opt,databases = db)
        FId = modelFId.out_db["z"].last_record().level
        print(FId)
        ms = modelFId.out_db["ms"].find_record().value
        ss = modelFId.out_db["ss"].find_record().value
        if ms > 2 or ss > 1:
            print("No solution test FId FAIL!")
            exit()
        vertex_FId.append(FId)

    i = 0
    minFId = 1.0
    cVertex = None
    for i in range(len(vertex_FId)):
        print(f"vertex {vertex_set[i]} : FId[{vertex_FId[i]}]")
        if vertex_FId[i] < minFId :
            cVertex = vertex_set[i]
            minFId = vertex_FId[i]

    print("critical vertex:",cVertex)
    print("min FId:",minFId)
    exit()