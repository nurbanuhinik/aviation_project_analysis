from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


file = open('stratux_log.txt', 'r')
lines = file.readlines()
file.close()


file = open('stratux_releaselog.txt', 'r')
lines_release = file.readlines()
file.close()

file = open('commit_mean.txt', 'r')
lines_means = file.readlines()
file.close()

dates = []
for line in lines:
    dateString = line.strip().split('\t')[1]
    dates.append(datetime.strptime(dateString, '%Y-%m-%d').timestamp())

release_dates = []
release_ids = []
for line in lines_release:
    data = line.strip().split('\t')
    release_ids.append(data[0])
    release_dates.append(datetime.strptime(data[2], '%Y-%m-%d').timestamp())

i, j = 0, 0

"""
commit_id = []
mean_count = []
for line in lines_means:
    data_commit = line.strip().split('\t')
    commit_id.append(data_commit[0])
    mean_count.append(data_commit[1])
    plt.plot(commit_id, mean_count, 'go')
"""

## iki release arasındaki commit sayisi
commits = {}
for i in range(len(lines)-1, 0, -1):
    j += 1
    id = lines[i].strip().split('\t')[0]
    if id in release_ids:
        commits[id] = j
        j = 0


## iki release arasında gecen gun sayisi
diff = {}               
for i in range(1, len(release_dates)):
    diff[release_ids[i-1]] = (datetime.fromtimestamp(release_dates[i-1]) - datetime.fromtimestamp(release_dates[i])).days
    # diff.append((datetime.fromtimestamp(release_dates[i-1]) - datetime.fromtimestamp(release_dates[i])).days)


for id in release_ids:
    if id in diff and id in commits:
        print(str(id) + '\t' + str(commits[id] / diff[id]))


"""
y_pos = np.arange((str(commits[id]/diff[id])))
release_i = np.arange(len(id))
ax.barh(y_pos,release_i,align='center')
ax.set_yticks(y_pos)
ax.invert_yaxis()
"""

data = mdates.epoch2num(dates)
release_dates = mdates.epoch2num(release_dates)

fig, ax = plt.subplots(1,1)


bin_count = int((datetime.strptime(lines[0].strip().split('\t')[1], '%Y-%m-%d')  - datetime.strptime(lines[len(lines)-1].strip().split('\t')[1], '%Y-%m-%d')).days / 30) 

density, bins, _ = ax.hist(data, bins=bin_count, color='lightblue')
count, _ = np.histogram(data, bins)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))

#d = datetime.strptime('2017-06-17', '%Y-%m-%d').timestamp()

# rect = plt.Rectangle((release_dates[9], 10.0), 20.0, 0.45, color='r')
# plt.gca().add_patch(rect)
i = 0
for a in release_dates:
    rect = plt.Rectangle((a, 7.0 - i), 16.0, 1.45, color='r')
    i += 1
    plt.gca().add_patch(rect)

for x,y,num in zip(bins, density, count):
    if num != 0:
        plt.text(x, y+0.05, '{:.3f}'.format(num/len(lines)), fontsize=7, rotation=0) # x,y,str normalize edilmis commit sayisi(histogramin o araligina denk gelen commit sayisi bolu toplam commit)
plt.show()
