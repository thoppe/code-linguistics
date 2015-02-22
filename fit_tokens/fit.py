import numpy as np
import sqlite3

language = "javascript"
f_conn = "db_tokens/{}.db".format(language)
conn = sqlite3.connect(f_conn)

cmd_grab = '''SELECT count FROM tokens'''
COUNTS = np.array([x for (x,) in conn.execute(cmd_grab)])
FREQ = COUNTS
FREQ = np.sort(FREQ)[::-1]

import pylab as plt
plt.loglog(FREQ,'o',lw=0,alpha=.75)
plt.show()

