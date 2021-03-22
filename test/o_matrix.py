import numpy as np
import oapackage

print(800%25)
exit()

run_size = 20
strength = 2
number_of_factors= 10
factor_levels = 2
arrayclass=oapackage.arraydata_t(factor_levels, run_size, strength, number_of_factors)
print(arrayclass)

ll2=[arrayclass.create_root()]
ll2[0].showarraycompact()

test = np.array(ll2[0])
test_T = np.transpose(test)
print(test)
print(test_T)
print(np.dot(test_T,test))

ary = ll2
for i in range(8):
    ary = oapackage.extend_arraylist(ary, arrayclass)
    print(f'extended to {len(ary)} arrays with {i+2} columns')
"""for L in ary :
    array = np.array(L)
    print(array)"""
final_ary = np.array(ary[0],dtype = np.int)
print(final_ary)
print(final_ary.shape)
exit()

list3columns = oapackage.extend_arraylist(ll2, arrayclass)
print('extended to %d arrays with 3 columns' % len(list3columns))
list3columns = oapackage.extend_arraylist(list3columns, arrayclass)
print('extended to %d arrays with 3 columns' % len(list3columns))
result = None
for L in list3columns :
    array = np.array(L)
    print(array)
    input()