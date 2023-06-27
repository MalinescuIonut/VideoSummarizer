import matplotlib
import matplotlib.pyplot as plt
import numpy as np
  
# Using readlines() 
file1 = open('lista.lis', 'r') 
Lines = file1.readlines() 
file1.close()
numbers=list(map(float, Lines))
numbers.sort()
y = [0]*len(numbers)
x = np.arange(len(numbers))
count = 0
numberAnt="0"
# Strips the newline character 
for number in numbers: 
#    number=line.strip()
    y[count]=float(number)-float(numberAnt)
    x[count]=count
    count=count+1
    numberAnt=number
file1.close() 

fig = plt.figure()
ax = plt.subplot(111)
ax.plot(x, y, label='$y = shot duration')
plt.title('shot length')
ax.legend()
#plt.show()

fig.savefig('lista.png')
