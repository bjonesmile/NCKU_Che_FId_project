from gams import *
import sys
import os
import numpy as np
import itertools
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

  Solve single_tankNz1 using minlp {optStateVardirection} z ;

  Display h.l, h.m, qout.l, qout.m, z.l, z.m; 
  execute_unload 'C:\\Users\\user\\Documents\\bjonesmile_project\DynamicSystem-CSTR-bio-alcoholic-Process\\tank1sol.gdx',qout,h ; 
  '''


def get_model_blk_init_text():
    return '''

  Sets
       m      discretize of time horizon ;
  Parameters
       A      bottom area of tank    /5/
       blk_len    discretize time length of Block 
       h0     initial value for stata var h
       vertex(m)

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load m blk_len h0 vertex
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
  
  
  '''
def get_model_BlkFIdtext():
    return '''
  obj .. z =e= FId;

  h.fx('1') = h0;
  Model single_tankNz1 /all/ ;
  Solve single_tankNz1 using minlp maximizing z ;
  Display h.l, h.m, qout.l, qout.m, z.l, z.m; 
  execute_unload 'C:\\Users\\user\\Documents\\bjonesmile_project\DynamicSystem-CSTR-bio-alcoholic-Process\\tank1sol.gdx',qout,h ; 
  '''

def genVertexList(v_num,blk_len,num) :
    print("create VertexList")
    VertexList = []
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
    print(len(VertexList))
    return VertexList, len(VertexList)

def genVertexList_byInput(inputVertex,n):
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

if __name__ == "__main__":
    clear_gmsfile.clearfile()
    if len(sys.argv) > 1:
        ws = GamsWorkspace(working_directory = os.getcwd(),system_directory = sys.argv[1])
    else:
        ws = GamsWorkspace(working_directory = os.getcwd())
    
    Nz = 1
    n = 0
    time_len = 800 // Nz
    vertex_set = genVertexList_byInput(inputVertex=[185,554],n=5)
    direct = -1
    init_h0 = 5.0
    #print(vertex_set)
    input()
    exit()

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

    blkFId = 0.4
    target_value = 10.0-1.0

    vertex = db.add_parameter("vertex", 1, "list of direction of each time point in time horizon")

    timer = timer.MyTimer()
    target_set = []
    tensity_set = []
    for v in vertex_set :
        block_vertex = v
        v_len = len(block_vertex)
        print(f"block {n} vertex: {block_vertex}")
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
        print(db.get_parameter("vertex").get_number_records())
        
        Blk_max = ws.add_job_from_string(get_model_optBlkkStateVar(fid= blkFId,opt_d= 1, blk_len= time_len))
        Blk_max.run(opt,output=sys.stdout,databases = db)
        max_stateVar = Blk_max.out_db["z"].last_record().level
        print(f"Block[{n+1}] max state : {max_stateVar}")
        Blk_min = ws.add_job_from_string(get_model_optBlkkStateVar(fid= blkFId,opt_d= -1, blk_len= time_len))
        Blk_min.run(opt,output=sys.stdout,databases = db)
        min_stateVar = Blk_min.out_db["z"].last_record().level
        print(f"Block[{n+1}] min state : {min_stateVar}")
        target = max_stateVar - min_stateVar
        if target <= 0:
            target = 0
            print(v)
            tensity_set.append(v)
            input()
        print(f"target function value {target}")
        target_set.append(target)
    
    critical_vertex = None
    critical_value = 10.0-1.0
    for i in range(len(target_set)):
        if target_set[i] < critical_value :
            critical_value = target_set[i] 
            critical_vertex = vertex_set[i]

    print(f"critical vertex: {critical_vertex}")
    print(f"critical value: {critical_value}")
    print(tensity_set)
    timer.getTime(kind="process")
    timer.getTime(kind="real")