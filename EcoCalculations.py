
"""
Privacy EcoSystem

CALCULATIONS

Vincent Marmion 
Version 1
Created 11_8_14
"""

#-------------------CALCULATIONS--------------------------------
#---------------------------------------------------------------


def calc_org_wealth():
	for org in ORGANISATIONS:
		if org.status == ACTIVE:
			org.wealth = (org.size * REVENUE[org.policy])

def calc_economy_wealth():
	Economy.totalWealth = 0
	for org in ORGANISATIONS:
		if org.status == ACTIVE:
			Economy.totalWealth += org.wealth
	return 0

def calc_economy_accounts():
	total = 0
	for org in ORGANISATIONS:
		if org.status == ACTIVE:
			total += org.size 
	
	maxAccounts = Economy.population * Economy.numOrgs
	accountRatio = maxAccounts/total
	Economy.totalAccounts = accountRatio
	return 0

def calc_economy_marketGap():
	Economy.marketGaps = [0,0,0,0,0,0]
	Economy.RATIOmarketGaps = [0,0,0,0,0,0]
	for person in PEOPLE:
		if person.status == ACTIVE:
			for remit in xrange(6):
				Economy.marketGaps[remit] += person.desires[remit]
	for remit in xrange(len(REMITS)):
		Economy.RATIOmarketGaps[remit] = desires[remit]/Economy.population
	return 0