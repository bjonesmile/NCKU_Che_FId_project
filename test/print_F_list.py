import numpy as np
import sys
import os

time_length = 240
Nz = 80
F_step = time_length//Nz

if time_length%Nz == 0:
    F_list = np.arange(F_step,time_length,F_step)
    F_list = np.append(F_list,[time_length])
else:
    F_list = np.linspace(F_step,time_length,num = Nz,endpoint=True,dtype=np.int)
    F_list[-1] = time_length
print(len(F_list))
print(F_list)


with open("gamsfile_F_equation_of_Nz"+str(Nz)+".txt",'w') as F_file :
    i = 0
    for j in range(1,Nz+1):
        F_file.write(f"Fin{j}(m)\n")
    F_file.write('\n')
    for j in range(1,Nz+1):
        F_file.write(f"Fout{j}(m)\n")
    F_file.write('\n')

    i = 0
    last_F = None
    for F in F_list :
        if i == 0:
            F_file.write(f"Fin{i+1}(m)$(ord(m) lt {F})..Fin(m)=e=Fin(m+1);\n")
        else:
            F_file.write(f"Fin{i+1}(m)$((ord(m) gt {last_F}) and (ord(m) lt {F}))..Fin(m)=e=Fin(m+1);\n")
        i += 1
        last_F = F

    F_file.write('\n')

    i = 0
    last_F = None
    for F in F_list :
        if i == 0:
            F_file.write(f"Fout{i+1}(m)$(ord(m) lt {F})..Fout(m)=e=Fout(m+1);\n")
        else:
            F_file.write(f"Fout{i+1}(m)$((ord(m) gt {last_F}) and (ord(m) lt {F}))..Fout(m)=e=Fout(m+1);\n")
        i += 1
        last_F = F