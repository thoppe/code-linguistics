import numpy as np
import pylab as plt
import sqlite3

f_code = 'process_code/db_tokens/python.db'
conn = sqlite3.connect(f_code)

cmd_freq = '''SELECT count FROM tokens LIMIT 100'''
cursor = conn.execute(cmd_freq)
values = np.array([x[0] for x in cursor])

S1 = np.array([np.random.binomial(x,0.5) for x in values])
FREQ = values-S1

RANK = np.argsort(FREQ)+1

#RANK = RANK[idx]
#FREQ = FREQ[idx]

#plt.scatter(RANK, FREQ)
FREQ=sorted(FREQ)[::-1]
#plt.plot(FREQ,'o')
plt.loglog(RANK,FREQ,'o')
plt.show()
