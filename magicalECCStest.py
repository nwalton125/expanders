from magicalECCS import *

#Testcases

#suff_small_sublists
print(len(suff_small_sublists([1,2,3,4,5],3)) == 26)
print(len(suff_small_sublists([], 1)) == 1)

#matmul
A = [[0,0,0],[1,0,1],[0,1,1],[1,1,1]]
v = [1,1,0]
result = [0,1,1,0]
print(matmul_F2(A, v) == result)

#matsolve
k = [0,0,0,0]
result = [[0,0,0]]
print(matsolve_F2(A, k) == result)

A = [[0,0,0,0],[0,1,0,1],[1,1,0,0]]
result = [[0,0,0,0], [0,0,1,0], [1,1,0,1], [1,1,1,1]]
print(kernel_F2(A) == result)

