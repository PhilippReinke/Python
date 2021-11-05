import numpy as np
import matplotlib.pyplot as plt

### Parameter
f = lambda x : x*np.sin(10*np.pi*x) + 2 # on intervall [-1,2]
popSize 			= 50
probMutation  		= 0.5 				# Anteil der Mutationen
intensityMutation 	= 0.1 				# Stärke der Mutation (also bit-switches)
probCrossOver 		= 0.2				# Anteil der Kreuzungen (Rest bleibt unverändert)
numBit		  		= 24				# muss gerade sein
numBitHalf	  		= numBit//2
numGenerations		= 100

### Startpopulation
pop = np.random.randint(2, size=(popSize, numBit))

### Evolution
for gen in range(0, numGenerations):

	# kreuzen (also Nachkommen erzeugen)
	crossOverIndices = np.random.randint( popSize, size=(int(probCrossOver*popSize), 2) )

	for a,b in crossOverIndices:
		child = np.concatenate( (pop[a][:numBitHalf], pop[b][numBitHalf:numBit]) )
		pop = np.append(pop, [child], axis=0)

	# Mutationen
	mutationIndices = np.random.randint( popSize, size=int(probMutation*popSize) )

	for ele in mutationIndices:
		idx = np.random.randint( numBit, size=int(intensityMutation*numBit) )
		for ele1 in idx:
			pop[ele][ele1] = 1 - pop[ele][ele1]

	# Selektion (eliminiere die schlechtesten)
	numRemove  = int(probCrossOver*popSize)
	popDecimal = []
	for ele in pop:
		temp = int("".join(ele.astype(str)), 2)
		popDecimal.append(temp/2**numBit * 3 - 1)
	popDecimal = np.array(popDecimal)

	idxSorted = np.argpartition(f(popDecimal), numRemove)
	
	# ignoriere die kleinsten Werte
	pop 	   = pop[idxSorted][numRemove:]
	popDecimal = popDecimal[idxSorted][numRemove:]

	# Plots speichern
	if (gen+1)%5 == 0:
		x = np.linspace(-1, 2, num=150)
		plt.plot(x, f(x), color="b")
		plt.scatter(popDecimal, f(popDecimal), color="r")
		plt.savefig("images/" + str(gen+1) + ".jpg")
		plt.clf()

	# Fortschritt anzeigen
	if (gen+1)%10 == 0:
		print("Fortschritt %i / %i" % (gen+1, numGenerations))

### zeige letztes Resultat
x = np.linspace(-1, 2, num=100)
plt.plot(x, f(x), color="b")
plt.scatter(popDecimal, f(popDecimal), color="r")
plt.show()