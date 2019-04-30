import numpy as np
import time

##########################################################
# Runtime complexity (RC) notation: <p(n),q(n)>, where
# p(n) = runtime complexity of preprocessing
# q(n) = runtime complexity of querying
##########################################################

REPEAT = 1000

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

def test(func,n=100) :
    pts = []
    qts = []
    for i in range(2,n) :
        _, pt, qt = func(i)
        pts.append(pt)
        qts.append(qt)
        if i % 10 == 0 :
            print("[INFO] : Finished testing with N = %d." % (i))

    return pts, qts

if __name__ == "__main__" :
    # _, pt, qt = naive(200)
    # print("[Naive] Preprocessing = %.8f seconds, Query = %.8f" % (pt/REPEAT,qt/REPEAT))
    pts, qts = test(naive)
    print(pts)
    print(qts)
