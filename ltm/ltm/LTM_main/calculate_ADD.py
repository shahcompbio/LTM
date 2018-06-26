
import numpy as np
import math


def calculate_ADD(seq1, seq2):
    n11=0
    n10=0
    n01=0
    n00=0
    
    for i in range(len(seq1)):
        if seq1[i]==seq2[i]:
            if str(seq1[i])=='1':
                n11+=1
            else:
                n00+=1
        if seq1[i]!=seq2[i]:
            if str(seq1[i])=='0':
                n01+=1
            else:
                n10+=1
                
    num = (n11+n10)*(n11+n01)
    # in case of no common mutation, choosing a very small number for n11, effectively increases the distance to infinity
    if n11>0:
        denum = math.pow(n11, 2)
    else:
        denum = 1e-8
        
    d_ADD=math.log(num/float(denum))
    return d_ADD
    
    
if __name__=='__main__':
    seq1='101010111110101'
    seq2='001010000000101'
    print calculate_ADD(seq1, seq2)
    
    
    