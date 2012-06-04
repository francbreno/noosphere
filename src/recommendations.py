#Código disponibilizado no livro Programming Collective Intelligence


# Lista de avaliacoes
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just my Luck': 3.0, 
	'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
	'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just my Luck': 1.5, 
	'Superman Returns': 5.0, 'You, Me and Dupree': 3.5, 'The Night Listener': 3.0},
	'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 
	'The Night Listener': 4.0},
	'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just my Luck': 3.0, 
	'Superman Returns': 4.0, 'You, Me and Dupree': 2.5, 'The Night Listener': 4.5},
	'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just my Luck': 2.0, 
	'Superman Returns': 3.0, 'You, Me and Dupree': 2.0, 'The Night Listener': 3.0},
	'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
	'Superman Returns': 5.0, 'You, Me and Dupree': 3.5, 'The Night Listener': 3.0},
	'Toby': {'Snakes on a Plane': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 1.0}}

from math import sqrt


# Calcula similaridade utilizando distancia euleriana
def sim_distance(prefs, person1, person2):

	si = {}
	for item in prefs[person1]:
		for item in prefs[person2]:
			si[item] = 1

	if len(si) == 0 : return 0;

	sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
				for item in prefs[person1] if item in prefs[person2]])

	return 1 / (1 + sqrt(sum_of_squares)) # No livro foi omitida a chamada a sqrt

# calcula similaridade utilizando escala de correlacao de Pearson
def sim_pearson(prefs, person1, person2):

	si = {}
	
	for item in prefs[person1]:
		if item in prefs[person2]: si[item] = 1

	n = len(si)

	if n == 0 : return 0;

	sum1 = sum([prefs[person1][it] for it in si])
	sum2 = sum([prefs[person2][it] for it in si])

	sum1Sq = sum([pow(prefs[person1][it], 2) for it in si])
	sum2Sq = sum([pow(prefs[person2][it], 2) for it in si])

	pSum = sum([prefs[person1][it] * prefs[person2][it] for it in si])

	num = pSum - (sum1 * sum2 / n)
	den = sqrt((sum1Sq - pow(sum1, 2)/n) * (sum2Sq - pow(sum2, 2)/n))

	if den == 0: return 0

	r = num / den

	return r

# retorna uma lista de avaliacoes ordenadas por similatidade
def top_matches(prefs, person, n=5, similarity=sim_distance):
	
	scores = [(similarity(prefs, person, other), other)
		for other in prefs if other != person]

	scores.sort();
	scores.reverse();
	return scores[0:n]


# retorna uma lista de recomendacoes para um pessoa a partir de uma lista de preferencias
def getRecommendations(prefs, person, similarity=sim_pearson):
	
	totals = {}
	simSums = {}

	for other in prefs:

		if other == person: continue

		sim = similarity(prefs, person, other)

		if sim <= 0: continue

		for item in prefs[other]:
			
			# apenas nao avaliados por person			
			if item not in prefs[person] or prefs[person][item] == 0:

				totals.setdefault(item, 0)
				totals[item] += prefs[other][item] * sim
				
				simSums.setdefault(item, 0)
				simSums[item] += sim

	# Nomaliza a lista
	rankings = [(total / simSums[item], item) for item, total in totals.items()]
	
	rankings.sort()
	rankings.reverse()
	
	return rankings

# inverte os avaliadores pelos itens avaliados e retorna um novo dicionario
def transformPrefs(prefs):
	
	result = {}

	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item, {})
			result[item][person] = prefs[person][item]

	return result 
	
