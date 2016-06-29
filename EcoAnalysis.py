
"""
Privacy EcoSystem

ANALYSIS

Vincent Marmion 
Version 1
Created 11_8_14
"""
#---------------------------------------------------------------
#-------------------ANALYSIS--------------------------------
#---------------------------------------------------------------
def analysis():
	population = []
	numOrgs = []
	totalWealth = []
	totalAccounts = []
	marketGaps = []

	m1 = []
	m2 = []
	m3 = []
	m4 = []
	m5 = []
	m6 = []

	for year in ECONOMY:
		population.append(year[0])
		numOrgs.append(year[1])
		totalWealth.append(year[2])
		totalAccounts.append(year[3])
		marketGaps.append(year[4])
	for market in marketGaps:
		m1.append(market[0])
		m2.append(market[1])
		m3.append(market[2])
		m4.append(market[3])
		m5.append(market[4])
		m6.append(market[5])
	marketGapsHistory = [m1,m2,m3,m4,m5,m6]


	plots(population,numOrgs,totalWealth, totalAccounts, marketGapsHistory)

def plots(population,numOrgs,totalWealth, totalAccounts, marketGapsHistory):

	fig1 = plt.figure(num=None, figsize=(11, 8), dpi=80, facecolor='w', edgecolor='k')
	title = "----------       ECONOMY        ----------"+"\nRUNS: "+ str(NUMRUNS)+"\n"
	fig1.suptitle(title)
	
	plt.subplot(311)
	plt.plot(totalWealth , "r:", lw = 2.0, label="Wealth")
	plt.ylabel("TOTAL WEALTH \n")
	plt.legend(bbox_to_anchor=(0.95, 0.9), loc=2, title = "Wealth", borderaxespad=0.)

	plt.subplot(312)
	plt.plot(totalAccounts, "k:", lw = 2.0, label= "Accounts")
	plt.ylabel("TOTAL ACCOUNTS \n")
	#plt.axis([0,NUMRUNS,-0.05,])
	plt.legend(bbox_to_anchor=(0.95, 0.9), loc=2, title = "Accounts", borderaxespad=0.)

	plt.subplot(313)
	plt.plot(marketGapsHistory[0], lw = 2.0, label= REMITS[0])
	plt.plot(marketGapsHistory[1], lw = 2.0, label= REMITS[1])
	plt.plot(marketGapsHistory[2], lw = 2.0, label= REMITS[2])
	plt.plot(marketGapsHistory[3], lw = 2.0, label= REMITS[3])
	plt.plot(marketGapsHistory[4], lw = 2.0, label= REMITS[4])
	plt.plot(marketGapsHistory[5], lw = 2.0, label= REMITS[5])
	plt.ylabel("MARKETS \n")
	#plt.axis([0,NUMRUNS,-0.05,])
	plt.legend(bbox_to_anchor=(0.95, 0.9), loc=2, title = "Accounts", borderaxespad=0.)
	plt.show()