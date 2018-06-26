import numpy as np
import math


def comb_list(seq, k):
    "returns a list of all k-combinations of the elements of sequence seq"
    n=len(seq)
    if not 0<=k<=n:
        raise Exception,"0<=k<=len(seq) is not true"
    v=[]   #list of combinations

    def f(x,y,a):
        if x==k:
            #we have taken enough elements, reject all remaining elements
            v.append(a)
            return
        if y==n-k:
            #we have rejected enough elements, take all remaining elements
            a.extend(seq[x+y:])
            v.append(a)
            return
        if (x<k):
            #take element seq[x+y]
            h=a+[seq[x+y]]
            f(x+1,y,h)
        if (y<n-k):
            #don't take element seq[x+y]
            f(x,y+1,a)            
    f(0,0,[])
    #print len(v)
    return v

def calculate_distance(seq1,seq2,alphabets_list):
    # assume we have n alphabets
    
    # calculating J
    J = np.zeros((len(alphabets_list),len(alphabets_list))) 
    for i in range(len(seq1)):
        s1=seq1[i]
        s2=seq2[i]
        s1_index= alphabets_list.index(s1)
        s2_index= alphabets_list.index(s2)
        J[s1_index][s2_index]+=1
    
    # Calculating D1, and D2
    D1=np.zeros((len(alphabets_list),len(alphabets_list))) 
    D2=np.zeros((len(alphabets_list),len(alphabets_list))) 
    for i in range(len(alphabets_list)):
        # D1
        
        for i in range(len(alphabets_list)):
            tmp_d1=0
            tmp_d2=0
            for j in range(len(alphabets_list)):
                tmp_d1 += J[i,j]
                tmp_d2 += J[j,i]
            D1[i,i]=tmp_d1
            D2[i,i]=tmp_d2
            
    # calculating the distance numpy.linalg.det
    
    # negative value for det(J) means more dissimilarities than similarities between the two sequences
    # cannot take log of negative or zero values so will lower bound at one (will yield maximum possible distance)
    numerator = max(np.linalg.det(J),1)
    d1 = max(np.linalg.det(D1),1)
    d2 = max(np.linalg.det(D2),1)
    denominator = math.sqrt(d1)*math.sqrt(d2)
    d = -math.log(numerator/float(denominator))
    return d
    
def dist_md(s1,s2,alphabets_list):
    J=np.zeros(len(s1),len(s2))
    for i in range(len(s1)):
        n1=s1[i]
        n2=s2[i]
        s1_index=alphabets_list.index(s1)
        s2_index=alphabets_list.index(s2)
        J[S1_index][S2_index]+=1
        
    D1=np.zeros((len(alphabets_list)),len(alphabets_list))
    D2=np.zeros((len(alphabets_list)),len(alphabets_list))
    for i in range(len(alphabets_list)):
        tmp_d1=0
        tmp_d2=0
        for j in range(len(alphabets_list)):
            tmp_d1+=J[i,j]
            tmp_d2+=J[j,i]
        D1[i,i]=tmp_d1
        D2[i,i]=tmp_d2
        
    num = max(np.linalg.det(J),1)
    denom = math.sqrt(d1)*math.sqrt(d2)
    d = -math.log(num/float(denom))
    return d

def dist_d2_norm(d1,d2,infile_path):
    infile=open(infile_path)
    for line in infile:
        tmp=line.strip().split('\t')
        if int(tmp[0]) > int(tmp[4]):
            d1[i,j]=i*2+1
            d2[j,i]=j*3-1




if __name__=='__main__':
    seq1='TCTTTCCTCCTTCCTCCCTTTCTCTTCCTCC'
    seq2='CCTCCCCTCTCTCCCCCTTCTCTCTCCTTCT'
    alphabets_list=['T','C']
    d = calculate_distance(seq1,seq2,alphabets_list)
    print d
    
    