import numpy as np
import itertools

def crtGridVertexList(vertex,v_range,n=3):
    up_limit = 800
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

if __name__ == "__main__":
    vertexList = crtGridVertexList([1,120,795],10,3)
    print(vertexList)
    print(len(vertexList))

    exit()    
