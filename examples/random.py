<<<<<<< HEAD
def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

A = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

print (split_list(A, wanted_parts=1))
print (split_list(A, wanted_parts=2))
=======
def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

A = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

print (split_list(A, wanted_parts=1))
print (split_list(A, wanted_parts=2))
>>>>>>> 702a546da1e7687c7f6840999a5263ae5a294833
print (split_list(A, wanted_parts=8))