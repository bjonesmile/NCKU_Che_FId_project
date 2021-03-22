from gekko import GEKKO
import numpy as np
import math
import csv
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

xm = np.array([0,1,2,3,4,5])
ym = np.array([0.1,0.2,0.3,0.5,1.0,0.9])

vertex = []
FId = []

with open('solvedDataCase0.csv', newline='') as csvfile:
  rows = csv.DictReader(csvfile)

  for row in rows:
    vertex.append(row['vertex'])
    FId.append(row['FId'])

correction_x = []
vertex_new = []
for v in vertex :
  v = eval(v)
  vertex_new.append(v)
  if len(v) > 1 :
    sum = 0
    for i in v :
      sum += int(i)**2
    sum = v[0]+math.sqrt(sum)
    correction_x.append(sum)
  else :
    correction_x.append(v[0])

vertex = np.array([np.array(xi) for xi in vertex_new])
correction_x = np.array(correction_x).astype(np.float)
print(vertex.shape)
pca = PCA(n_components=1)
pca.fit(vertex)
vertex_pca = pca.transform(vertex)
print("original shape:   ", vertex.shape)
print("transformed shape:", vertex_pca.shape)
#vertex = np.array(vertex).astype(np.int)
FId = np.array(FId).astype(np.float)

pred_ub = np.max(correction_x)
pred_lb = np.min(correction_x)
print(pred_lb,pred_ub)

m = GEKKO()             # create GEKKO model
m.options.IMODE = 2     # solution mode
x = m.Param(value=np.linspace(pred_lb,pred_ub)) # prediction points
y = m.Var()             # prediction results
m.cspline(x, y, correction_x, FId) # cubic spline
m.solve(disp=False)     # solve

pred_vertex = np.array(list(x.value))
pred_FId = np.array(list(y.value))
print("pred vertex number",pred_vertex.size)
print("pred FId number",pred_FId.size)
print(np.min(pred_FId))
v_min = np.argmin(pred_FId)
print(v_min)
print(pred_vertex[v_min])
print(x.value[v_min])

# create plot
"""
plt.plot(correction_x,FId,'bo')
plt.plot(x.value,y.value,'r--',label='cubic spline')
plt.title("Nz1 vertex[v1] v[0,240]")
plt.xlabel("v1")
plt.ylabel("euclidean norm")
plt.legend(loc='best')
plt.show()
"""

X = vertex
X_new = pca.inverse_transform(vertex_pca)
plt.scatter(X[:, 0], X[:, 1], alpha=0.2,label="original vertex point")
plt.scatter(X_new[:, 0], X_new[:, 1], alpha=0.8, label="inverse-trans")
plt.xlabel("v1")
plt.ylabel("v2")
plt.legend(loc='best')
plt.axis('equal')
plt.show()

point_correct = []
i =0 
for point in vertex :
  print(point)
  point = np.reshape(point,(1,2))
  point_pca = pca.transform(point)
  if i == 0 :
    original_point = point_pca
  point_correct.append(abs(point_pca-original_point))
  point_inverse = pca.inverse_transform(point_pca)
  print(point_pca)
  print(point_inverse)
  i += 1
plt.scatter(point_correct,FId)
plt.show()