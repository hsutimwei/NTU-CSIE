import matplotlib.pyplot as plt

x = [1,2,3,4,5]

y1 = [10.4,11.2,11.6,12.0,12.4]
a1, = plt.plot(x,y1,'r-.*',label='rogue-1-f1')


y2 = [1.9,3.0,3.2,3.4,3.6]
a2, = plt.plot(x, y2, 'g-.*',label='rogue-2-f1')

y3 = [9.8,10.5,11.1,11.5,11.8]
a3, = plt.plot(x,y3,'b-.*',label='rogue-L-f1')

plt.xlabel("steps")
plt.ylabel("f1-score*100")
plt.show()