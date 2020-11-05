import pandas as pd
import numpy as np
data = pd.read_csv("federalelections.csv", thousands=',',
                   header=None, index_col=0, names=('pop', 'ec'))

# Random simulation, based on real data from the 2016 US presidential election
results = []
for i in range(25000):
    data.loc[:, 'support'] = np.random.uniform(size=data.shape[0])
    voters = (data['pop'] * data['support']).sum() / data['pop'].sum()
    won_popular = int(voters > 0.5)
    won_college = int(data[data['support'] > 0.5]['ec'].sum()
                      / data['ec'].sum() > 0.5)
    results.append((voters, won_popular, won_college))

results = pd.DataFrame(results)
results.columns = 'votes', 'popular vote', 'electoral college'
results['votes'] *= 100
grouper = results.groupby(pd.cut(results['votes'], 100))

# Pplot the results
grouper.mean().set_index('votes').plot(style='-o', ms=5, lw=0.5)
plt.ylabel('Probability of X winning')
plt.xlabel('% of votes cast for X')
plt.title("Electoral college makes election outcomes unpredictable")
plt.tight_layout()
plt.savefig("college.png")
plt.show()
