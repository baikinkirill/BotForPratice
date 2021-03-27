podmishkaPomidora=int(input())

maxJopaIn21=0
maxAGAGAGA3=0
maxOGOGO7=0
maxPizdec=0

for i in range(0,podmishkaPomidora):
  e=int(input())
  if(e%21==0 and e>maxJopaIn21):
    maxJopaIn21=e
  elif(e%7==0 and e>maxOGOGO7 and e%21!=0): maxOGOGO7=e
  elif(e%3==0 and e>maxAGAGAGA3 and e%21!=0): maxAGAGAGA3=e
  elif(e>=maxPizdec): maxPizdec=e

if((maxJopaIn21*maxPizdec>=maxOGOGO7*maxAGAGAGA3) and (maxJopaIn21 > 0) and (maxPizdec>0)):
  print(maxJopaIn21*maxPizdec)
elif((maxJopaIn21*maxPizdec<maxOGOGO7*maxAGAGAGA3) and (maxOGOGO7*maxAGAGAGA3 > 0)):
  print(maxOGOGO7*maxAGAGAGA3)
else: print("Нет такого!")