import numpy as np
import os, time

##########################################################
# Runtime complexity (RC) notation: <p(n),q(n)>, where
# p(n) = runtime complexity of preprocessing
# q(n) = runtime complexity of querying
##########################################################

REPEAT = 1000

# No preprocessing, baseline RMQ
# RC: <O(1),O(n)>
def simple(n) :

    # generate random array of integers
    A = np.arange(n)
    np.random.shuffle(A)

    # create random queries
    queries = []
    for i in range(REPEAT) :
        ns = np.random.randint(n,size=2)
        queries.append(np.sort(ns))

    # repeat counter
    t = REPEAT

    # start timing (query, no preprocessing time)
    start = time.time()
    
    while t > 0 :

        # execute query
        qi, qj = queries[t-1]
        answer = A[qi]
        for i in range(qi+1,(qj+1),1) :
            if A[i] < answer :
                answer = A[i]

        t -= 1

    # stop timing (query)
    end = time.time()

    return answer, 0.0, float(end-start)


# Complete preprocessing, trivial RMQ
# RC: <O(n^2),O(1)>
def naive(n) :

    # generate random array of integers
    A = np.arange(n)
    np.random.shuffle(A)

    # create random queries
    queries = []
    for i in range(REPEAT) :
        ns = np.random.randint(n,size=2)
        queries.append(np.sort(ns))

    # repeat counter
    t = REPEAT
    t1 = REPEAT

    # start timing (preprocessing)
    start = time.time()

    while t > 0 :

        # use dynamic programming to construct the table
        B = np.zeros(n*n).astype(int).reshape(n,n)
        for i in range(n) :
            B[i,i] = A[i]
        for k in range(1,n,1) :
            for i in range(n-k) :
                B[i,i+k] = min(B[i,i+k-1],B[i+1,i+k])
        t -= 1
    
    # stop timing (preprocessing)
    end = time.time()

    while t1 > 0 :

        # execute query
        qi, qj = queries[t1-1]
        answer = B[qi,qj]
        t1 -= 1

    # stop timing (query)
    end1 = time.time()

    return answer, float(end-start), float(end1-end)

# Block-level preprocessing, improved RMQ
# RC: <O(n),O(n^(0.5))>
def block(n) :

    # generate random array of integers
    A = np.arange(n)
    np.random.shuffle(A)

    # create random queries
    queries = []
    for i in range(REPEAT) :
        ns = np.random.randint(n,size=2)
        queries.append(np.sort(ns))

    # repeat counter
    t = REPEAT
    t1 = REPEAT

    # start timing (preprocessing)
    start = time.time()

    while t > 0 :

        # choose block size = n^(0.5)
        b = int(np.sqrt(n))
        num_blocks = int(np.ceil(n/b))
        
        # use dynamic programming to construct the table
        B = np.zeros(num_blocks).astype(int)
        for i in range(num_blocks) :
            B[i] = A[i*b]
            for j in range(i*b+1,(i+1)*b) :
                if j >= n :
                    break
                if A[j] < B[i] :
                    B[i] = A[j]
        t -= 1

    # stop timing (preprocessing)
    end = time.time()

    while t1 > 0 :

        # execute query
        qi, qj = queries[t1-1]
        bi = int(qi/b)
        bj = int(qj/b)
        min_iblock = A[qi]
        min_jblock = A[qj]
        for i in range(qi,min((bi+1)*b,n)) :
            if A[i] < min_iblock :
                min_iblock = A[i]
        for i in range(qj,min((bj+1)*b,n)) :
            if A[i] < min_jblock :
                min_jblock = A[i]
        answer = min(min_iblock,min_jblock)
        for i in range(bi+1,bj) :
            if B[i] < answer :
                answer = B[i]

        t1 -= 1

    # stop timing (query)
    end1 = time.time()

    return answer, float(end-start), float(end1-end)

def test(func,name,n=100) :
    pts = []
    qts = []
    for i in range(2,n) :
        _, pt, qt = func(i)
        pts.append(pt)
        qts.append(qt)
        if i % 10 == 0 :
            print("[INFO] %s : Finished testing with N = %d." % (name,i))

    return pts, qts

if __name__ == "__main__" :

    # test simple
    pts, qts = test(simple,"Simple",n=200)
    np.savetxt("rmq_simple.csv", np.array([pts,qts]), delimiter=',', fmt='%.16f')
    os.system("tr , '\n' < rmq_simple.csv > tmp; mv tmp rmq_simple.csv")

    # test naive 
    pts, qts = test(naive,"Naive",n=100)
    np.savetxt("rmq_naive.csv", np.array([pts,qts]), delimiter=',', fmt='%.16f')
    os.system("tr , '\n' < rmq_naive.csv > tmp; mv tmp rmq_naive.csv")

    # test block 
    pts, qts = test(block,"Block",n=200)
    np.savetxt("rmq_block.csv", np.array([pts,qts]), delimiter=',', fmt='%.16f')
    os.system("tr , '\n' < rmq_block.csv > tmp; mv tmp rmq_block.csv")

