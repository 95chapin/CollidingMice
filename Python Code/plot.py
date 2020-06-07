import numpy as np
import matplotlib.pyplot as plt
from mice import readParam
import re


# def find_str(s, char):
#     index = 0

#     if char in s:
#         c = char[0]
#         for ch in s:
#             if ch == c:
#                 if s[index:index+len(char)] == char:
#                     return index

#             index += 1

#     return -1

# w1, b1 = readParam("fc1")
# w2, b2 = readParam("fc2")
# w3, b3 = readParam("fc3")

filename = "avgScore.txt"
s = []
key1 = "Average score[: ]"
with open(filename, 'r') as f:
    w = f.readlines()
    
with open("avg.txt",'+a') as f:
    for x in w:
        loc = re.findall('\d*\.?\d+',x)
        if len(loc) != 0 :
            f.write(loc[1] + "\n")
            s.append(float(loc[1])) 
        
# fig = plt.figure()
# plt.plot(np.arange(len(w1)), w1)
# plt.plot(np.arange(len(w2)), w2)
# plt.plot(np.arange(len(w3)), w3)
# plt.ylabel('Weight Value')
# plt.xlabel('Episode #')
# plt.show()

# fig2 = plt.figure()
# plt.plot(np.arange(len(b1)), b1)
# plt.plot(np.arange(len(b2)), b2)
# plt.plot(np.arange(len(b3)), b3)
# plt.ylabel('Bias Value')
# plt.xlabel('Episode #')
# plt.show()
# print(len(b1))

# fig3 = plt.figure()
# plt.plot(np.arange(len(s)), s)
# plt.ylabel('Avg Score')
# plt.xlabel('Episode #')