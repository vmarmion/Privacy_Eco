from __future__ import division
from decimal import *
import math
import sys
import scipy
import matplotlib.pyplot as plt
from random import *


"""
Privacy EcoSystem

Vincent Marmion 
Version 1
Created 11_8_14

Scenarios
1: Bad Opaque -> irregular information leak to consumers: Expect Jumpy
2: Bad Transparent -> Gradaula information leak: Expect Boiling Frogs
3: Good Transparent -> No Selling: Expect Poor Economics
4:
"""

"""
CONSTRUCTS ------------------------------------------------------------------
"""

"""---------------------ORGANISATIONS--------

Organisations = 6 types
Social 		[Phone 		(prevention), Social Network 	(Promotion)]

Commecial 	[Utility 	(prevention), Discounts			(promotion)]

Information [Newspaper 	(prevention), Magazine			(promotion)]

Orgs Have:
PrivacyPolicy: 	Good and Transparent
				Good and Opaque
				Bad and Transparent
				Bad and Opaque

Orgs Can:
		Take Information
			Good 	[up to 2 Primary Attributes] [1 Secondary Attributes]
			Bad		[up to 2 Primary Attributes] [up to 5 Secondary Attributes]	
		Advertise

		Spawn
		Collapse
"""
"""----------------------USERS----------------

Users = 2 types (prevention or promotion focus)

Users Can:
	on first use: decisde to check PrivacyPolicy
	Leave an org at any time
	Join Alternatives
	Die/ReGenerate

Users Have:
	Liklihood they will check PrivacyPolicy [type of Org/Reg Focus]
	Liklihood they will leave an Org [Popularity of Alternatives/ Num of Alternatives/ News]
	Liklihood they will join an Org [Popularity or Org/Recognition]
Users are:
	Born with:
		Knowledge from parents
		Network of friends, established randomly (or from accounts??)
		No set of accounts
"""





"""----------------------EVENTS----------------
Events:
		Org Specific Hack
		News Story

----------------------INFORMATION------------

Attributes 	: Primary Identifiyers, fingerprint, name, email, retina
			: Seondary Identifiyers, preferences, audit logs, personlity traits


"""
#------------------------------CLASSES---------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
ECONOMIES = []

REG_FOCUS = ["PREVENTION","PROMOTION"]
PREVENTION = 0
PROMOTION = 1
STATUS = ["ACTIVE","NONACTIVE"]
ACTIVE = 0
NONACTIVE = 1

OPENNESS = 0
PROTECTION = 1

LEFT = 0
JOINED = 1
SWITCHED = 2

SOCIAL_PREVENTION = 0
COMMERCE_PROVENTION =1
NEWS_PREVENTION = 2
SOCIAL_PROMOTION = 3
COMMERCE_PROMOTION = 4
NEWS_PROMOTION = 5

REMITS = ["SOCIAL(Prevention)  ", "COMMERCE(Prevention)", "NEWS(Prevention)  ", "SOCIAL(Promotion)", "COMMERCE(Promotion)", "NEWS(Promotion)" ]
POLICIES = ["RESPECT_CLEAR ", "RESPECT_OPAQUE" ,"EXPLOIT_OPAQUE", "EXPLOIT_CLEAR"]

POLICY_ATTRACTION = [1.0, 0.5, 0.5, 0.25]
POLICY_REVENUE = [0.1,0.1,0.2, 0.2]

NUM_ECOS = 4
MAX_POPULATION = 1000
MAX_ORGS = 10
MAX_TIMESTEPS = 1000
MAX_YEARS = 100

DEBUG = 0

class Economy_CLASS:

	def __init__(self, ecoID):
		
		self.ecoID = ecoID
		
		self.economyYears = []
		self.timespan = [0, 0]
		self.date = [0,0]
		
		self.PEOPLE = []
		self.population = 0
		self.populationIDMarker = 0

		self.ORGANISATIONS = []
		self.numOrgs = 0
		self.orgIDMarker = 0
		
		self.yearlyEcoWealth = 0.0
		self.yearlyAccountTotal = 0.0
		
		self.marketGaps = [0,0,0,0,0,0]
		self.RATIOmarketGaps = [0,0,0,0,0,0]
		
		self.lastEvent = ""
		self.peopleActions = [0,0,0] #leave, join ,switch

	def displayEconomy(self):
		ecoInfo = "Eco:%s Y%s :T%s" % (self.ecoID, self.date[0], self.date[1])
		popInfo = "Pop[N%s, E%s]" % (self.population, self.populationIDMarker)
		orgInfo = "Org[N%s, E%s]" % (self.numOrgs, self.orgIDMarker)
		wealthInfo = "W%.2f" % self.yearlyEcoWealth
		accountInfo = "Ac%.2f" % self.yearlyAccountTotal
		marketGapInfo = "MG %.2f %.2f %.2f %.2f %.2f %.2f" % (self.RATIOmarketGaps[SOCIAL_PREVENTION], self.RATIOmarketGaps[COMMERCE_PROVENTION],self.RATIOmarketGaps[NEWS_PREVENTION],self.RATIOmarketGaps[SOCIAL_PROMOTION],self.RATIOmarketGaps[COMMERCE_PROMOTION],self.RATIOmarketGaps[NEWS_PROMOTION])
		actionInfo = "Ac[L:%s J:%s S:%s]" % (self.peopleActions[LEFT], self.peopleActions[JOINED], self.peopleActions[SWITCHED])
		eventInfo = "Ev_%s" % self.lastEvent
		print ecoInfo,popInfo,orgInfo,wealthInfo,accountInfo,marketGapInfo,accountInfo,actionInfo,eventInfo
	
	def displayOrgs(self, status):
		for org in self.ORGANISATIONS:
			if org.status == status:
				org.display()

	def displayPeople(self, status):
		for person in self.PEOPLE:
			if person.status == status:
				person.display()

class Organisation_CLASS:
	
	def __init__(self, orgID):
		self.orgID = orgID
		self.remit = 0
		self.policyDimension = 0
		self.policy = [0.0, 0.0]
		self.size = 0
		self.wealth = 0
		self.popularity = 0
		self.status = ACTIVE

	def display(self):
		print "ORG:", self.orgID, '%.2f' % self.popularity,"STATUS", self.status, "Remit:", self.remit, REMITS[self.remit],"Policy:",self.policy,"Size:", self.size, "Wealth:", self.wealth

class Person_CLASS:
	'Common base class for all People'
	def __init__(self, personID):
		self.personID = personID
		self.regFocus = 0.0
		self.focusBias = 0
		self.accounts = []
		self.desires = [1,1,1,1,1,1]
		self.status = ACTIVE
		self.age = 0
				

	def display(self):
   		print "PERSON ID:", self.personID, "Status:", STATUS[self.status], "Focus:", REG_FOCUS[self.focusBias],'%.2f' % self.regFocus, "Accounts", self.accounts, "Seeking:", self.desires


#-------------------INITIATE-----------------------------------
#---------------------------------------------------------------
def initiate_economies():
	for ecoID in xrange(NUM_ECOS):
		Economy = Economy_CLASS(ecoID)
		Economy.timespan = [MAX_YEARS, MAX_TIMESTEPS]
		ECONOMIES.append(Economy)
	if DEBUG == 1:
		print "Method: initiate_economy"
		print "SAME?", len(ECONOMIES), NUM_ECOS
	return 0

def initiate_organisations(Economy):
	#creates a random set of new organisations
	numOrgs = returnRandomInt(1,MAX_ORGS)
	for ID in xrange(numOrgs):
		remit = returnRandomInt(0,5)
		create_org(ID,remit, Economy)
	if DEBUG == 1: 
		print "initiate_organisations:"
		print "SAME?", Economy.numOrgs, Economy.orgIDMarker, len(Economy.ORGANISATIONS) 
	return 0


def create_org(orgID, remit, Economy):
	org = Organisation_CLASS(orgID)
	org.remit = remit
	org.wealth = returnRandomReal()*1000
	setPolicy(org)
	Economy.ORGANISATIONS.append(org)
	Economy.numOrgs += 1
	Economy.orgIDMarker += 1
	if DEBUG == 1:
		print "--------------" 
		print "create_org:", orgID, REMITS[remit]
		org.display()
		print "SAME?", Economy.orgIDMarker, len(Economy.ORGANISATIONS) 
	return 0

def orgPopularity(org, Economy):
	org.popularity = ((org.size+org.wealth)/Economy.population)

def setPolicy(org):
	openness = returnRandomReal()
	protection = returnRandomReal()
	policyDimension = 0
	org.policy = [openness, protection]
	if openness > 0.5: #open
		if protection > 0.5: #Respect
			policyDimension = 0 #open_respect
		else:
			policyDimension = 1 #open_exploit
	else:
		if protection > 0.5:
			policyDimension = 2 #closed_respect
		else:
			policyDimension = 3 #closed_exploit
	org.policyDimension = policyDimension

	return 0

def initiate_population(Economy):
	#creates the initial population
	population = returnRandomInt(1,MAX_POPULATION)
	for personID in xrange(population):
		create_person(personID, Economy)
	for org in Economy.ORGANISATIONS:
		orgPopularity(org, Economy)
	if DEBUG == 1: 
		print "initiate_population"
		print "SAME?",population, Economy.population, Economy.populationIDMarker, len(Economy.PEOPLE)

	return 0

def create_person(personID, Economy):
	person = Person_CLASS(personID)
	initiate_regFocus(person)
	Economy.PEOPLE.append(person)
	Economy.population += 1
	Economy.populationIDMarker += 1
	if DEBUG == 1: 
		print "----------------"
		print "create_person", personID, REG_FOCUS[person.focusBias]#, len(person.connections)
		person.display()
	return 0

def initiate_regFocus(person):
	focus = returnRandomReal()
	if focus >= 0.5:
		person.focusBias = PROMOTION
	person.regFocus = focus
	if DEBUG == 1: print "initiate_regFocus"
	return 0


#-------------------FUNCTIONS-----------------------------------
#---------------------------------------------------------------

def returnRandomReal():
	num = uniform(0,1)
	return num

def returnRandomInt(start, stop):
	num = randint(start, stop)
	return num


#-------------------CALCULATIONS--------------------------------
#---------------------------------------------------------------
def calc_org_wealth(Economy):
	for org in Economy.ORGANISATIONS:
		if org.status == ACTIVE:
			org.wealth = (org.size * POLICY_REVENUE[org.policyDimension])
	if DEBUG == 1: print "calc_org_wealth"
	return 0

def calc_economy_wealth(Economy):
	yearlyEcoWealth = 0
	for org in Economy.ORGANISATIONS:
		if org.status == ACTIVE:
			yearlyEcoWealth += org.wealth
	Economy.yearlyEcoWealth = yearlyEcoWealth
	if DEBUG == 1: print "calc_economy_wealth"
	return 0

def calc_economy_accounts(Economy):
	yearlyAccountTotal = 0
	for org in Economy.ORGANISATIONS:
		if org.status == ACTIVE:
			yearlyAccountTotal += org.size 
	Economy.yearlyAccountTotal = (yearlyAccountTotal/(Economy.population * Economy.numOrgs))
	if DEBUG == 1: print "calc_economy_accounts"
	return 0

def calc_economy_marketGap(Economy):
	Economy.marketGaps = [0,0,0,0,0,0]
	Economy.RATIOmarketGaps = [0,0,0,0,0,0]
	for remit in xrange(len(REMITS)):
		for person in Economy.PEOPLE:
			if person.status == ACTIVE:
				Economy.marketGaps[remit] += person.desires[remit]
		Economy.RATIOmarketGaps[remit] = Economy.marketGaps[remit]/Economy.population
	if DEBUG == 1: print "calc_economy_marketGap"
	return 0

#---------------------------------------------------------------
#-------------------ORGANISATION EVENT--------------------------
#---------------------------------------------------------------

def newOrg(Economy):
	desiredRemit = returnRandomInt(0,(len(REMITS)-1))
	marketDesire = Economy.RATIOmarketGaps[desiredRemit]
	dice = returnRandomReal() 
	if marketDesire >= dice:
		org = create_org(Economy.orgIDMarker, desiredRemit, Economy)		
		Economy.lastEvent = "ORG CREATRED"
	else:
		Economy.lastEvent = "ORG NO FUNDS"
	if DEBUG == 1: print "newOrg"
	return 0

def killOrg(Economy):
	org = Economy.ORGANISATIONS[returnRandomInt(0, Economy.orgIDMarker-1)]
	if org.status == ACTIVE:

		dice1 = returnRandomReal()
		dice2 = returnRandomReal()

		if  org.popularity < dice1:
			if Economy.RATIOmarketGaps[org.remit] < dice2:
				org.status = NONACTIVE
				Economy.numOrgs -= 1
				Economy.lastEvent = "ORG FAILED"
				for person in Economy.PEOPLE:
					#remove this org from accounts, recalc desire
					for account in person.accounts:
						if account == org.orgID:
							person.accounts.remove(account)
							person.desires[org.remit] = 1
			else:
				Economy.lastEvent = "ORG DESIRED"
		else:
			 Economy.lastEvent = "ORG POPULAR"	
	if DEBUG == 1: print "killOrg"
	return 0

#---------------------------------------------------------------
#-------------------PERSON EVENT--------------------------
#---------------------------------------------------------------


def ageing(Economy):
	for person in Economy.PEOPLE:
		if person.status == ACTIVE:
			person.age +=1
	if DEBUG == 1: print "aging"
	return 0

def dying(person):
	for person in PEOPLE:
		if person.status == ACTIVE:
			dice = returnRandomInt(0,100)
			age = person.age
			if dice > 99.5:
				if DEBUG == 1: print "death",age
	if DEBUG == 1: print "dying"
	return 0



def leavingOrg(person, Economy):
	action = "LEFT ORG"
	num_accounts = len(person.accounts)	
	if num_accounts != 0:
		ID = person.accounts[returnRandomInt(0,num_accounts-1)]
		org = Economy.ORGANISATIONS[ID]
		stay_chance = org.policy[0] * org.policy[1] * person.regFocus
		if org.popularity < returnRandomReal()/4:
			if stay_chance < returnRandomReal()/4:
				Economy.peopleActions[0] += 1
				leftOrg(person, org, Economy)
			else: action = "NO LEAVE: popular"
		else: action = "NO LEAVE: desired" 
	else: action = "NO LEAVE: No accounts"

	if DEBUG == 1: 
		print "--------------------Method: leavingOrg()--------------------"
		print action
	return 0

def switchOrg(person, Economy):
	action = "SWITCHED ORG"
	num_accounts = len(person.accounts)	
	if num_accounts != 0: 
		if Economy.numOrgs > 1:
			orgID = person.accounts[returnRandomInt(0,num_accounts-1)]
			org = Economy.ORGANISATIONS[orgID]		
			alternativeOrg = Economy.ORGANISATIONS[returnRandomInt(0, (len(Economy.ORGANISATIONS)-1))]
			if alternativeOrg.status == ACTIVE:
				if org.orgID != alternativeOrg.orgID:
					if org.remit == alternativeOrg.remit:
						stay_chance = org.policy[0] * org.policy[1] * org.popularity * person.regFocus
						switch_chance = alternativeOrg.policy[0] * alternativeOrg.policy[1] * alternativeOrg.popularity * person.regFocus
						if stay_chance < switch_chance:
							Economy.peopleActions[2] += 1
							leftOrg(person, org, Economy)
							joinedOrg(person, alternativeOrg, Economy)
							#raw_input("Press Enter to continue...")
						else: action = "NO SWITCH: chance"
					else: action = "NO SWITCH: ORGS not the same remit"
				else: action = "NO SWITCH: the same organisations"
			else: action = "NO SWITCH: NONACTIVE org"
		else: action = "NO SWITCH: dead economy"
	else: action = "NO SWITCH: No Accounts"
	if DEBUG == 1: 
		print "--------------------Method: switchOrg()--------------------"
		print action
	return 0


def joiningOrg(person, Economy):
	action = "JOINED ORG"
	org = Economy.ORGANISATIONS[returnRandomInt(0,(len(Economy.ORGANISATIONS)-1))]
	if org.status == ACTIVE:
		if person.desires[org.remit] == 1:
			join_chance = (org.policy[0] * org.policy[1] * person.regFocus)
			#need adverts
			if org.popularity > returnRandomReal():
				if join_chance < returnRandomReal():
					Economy.peopleActions[1] += 1
					joinedOrg(person, org, Economy)
				
				else: action = "NO JOIN: chance"
			else: action = "NO JOIN: popularity"
		else: action = "NO JOIN: different remits"
	else: action = "NO JOIN: non active org"
	if DEBUG == 1: 
		print "--------------------Method: joiningOrg()--------------------"
		print action
	return 0

def leftOrg(person, org, Economy):
	if DEBUG == 1: 
		print "--------------------Method: leftOrg()--------------------"
		person.display()
		org.display()
	person.accounts.remove(org.orgID)
	person.desires[org.remit] = 1
	org.size -=1
	orgPopularity(org, Economy)
	if DEBUG == 1: 
		person.display()
		org.display()
	return 0


	

def joinedOrg(person, org, Economy):
	if DEBUG == 0: 
		print "--------------------Method: joinedOrg()--------------------"
		person.display()
		org.display()
	person.accounts.append(org.orgID)
	person.desires[org.remit] = 0
	org.size += 1
	orgPopularity(org, Economy)
	if DEBUG == 1: 
		person.display()
		org.display()
	return 0

#---------------------------------------------------------------
#-------------------PERSON EVENT END--------------------------
#---------------------------------------------------------------

def orgEvent(Economy):
	dice = returnRandomInt(0,1)
	if 	dice == 0:	
		newOrg(Economy)		
	else: 	
		killOrg(Economy)	
	return 0

def personEvent(Economy):
	for person in Economy.PEOPLE:
		dice = returnRandomInt(0,3)
		if dice == 0:
			leavingOrg(person, Economy)		
		elif dice == 1:
			joiningOrg(person, Economy)	
		elif dice == 2:
			switchOrg(person, Economy)
	return 0

def update_economy_status(Economy):
	calc_org_wealth(Economy)
	calc_economy_accounts(Economy)
	calc_economy_wealth(Economy)
	calc_economy_marketGap(Economy)
	thisEconomy = [Economy.population, Economy.numOrgs, Economy.yearlyEcoWealth, Economy.yearlyAccountTotal, Economy.marketGaps, Economy.date]
	Economy.economyYears.append(thisEconomy)
	
	if DEBUG == 1: print "update_economy_status"
	return 0

def displayAllEconomies():
	for eco in ECONOMIES:
		eco.displayEconomy()
	return 0

def play():
	initiate_economies()
	displayAllEconomies()
	for ecoID in xrange(NUM_ECOS):
		Economy = ECONOMIES[ecoID]
		initiate_organisations(Economy)
		initiate_population(Economy)
		YEARS, TIMESTEPS = Economy.timespan
		for year in xrange(YEARS):
			Economy.peopleActions = [0,0,0]			
			for time in xrange(TIMESTEPS):
				Economy.date = [year, time]
				personEvent(Economy)
			#ageing()
			orgEvent(Economy)
			update_economy_status(Economy)
			Economy.displayEconomy()			
		if DEBUG == 1: 
			Economy.displayOrgs(ACTIVE)
			Economy.displayPeople(ACTIVE)
	displayAllEconomies()
	#analysis()
	return 0
		
	

	

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
	title = "----------       ECONOMY        ----------"+"\nRUNS: "+ str(YEARS)+"\n"
	fig1.suptitle(title)
	
	plt.subplot(311)
	plt.plot(totalWealth , "r:", lw = 2.0, label="Wealth")
	plt.ylabel("TOTAL WEALTH \n")
	plt.legend(bbox_to_anchor=(0.95, 0.9), loc=2, title = "Wealth", borderaxespad=0.)

	plt.subplot(312)
	plt.plot(totalAccounts, "k:", lw = 2.0, label= "Accounts")
	plt.ylabel("TOTAL ACCOUNTS \n")
	#plt.axis([0,YEARS,-0.05,])
	plt.legend(bbox_to_anchor=(0.95, 0.9), loc=2, title = "Accounts", borderaxespad=0.)

	plt.subplot(313)
	plt.plot(marketGapsHistory[0], lw = 2.0, label= REMITS[0])
	plt.plot(marketGapsHistory[1], lw = 2.0, label= REMITS[1])
	plt.plot(marketGapsHistory[2], lw = 2.0, label= REMITS[2])
	plt.plot(marketGapsHistory[3], lw = 2.0, label= REMITS[3])
	plt.plot(marketGapsHistory[4], lw = 2.0, label= REMITS[4])
	plt.plot(marketGapsHistory[5], lw = 2.0, label= REMITS[5])
	plt.ylabel("MARKETS \n")
	#plt.axis([0,YEARS,-0.05,])
	plt.legend(bbox_to_anchor=(0.95, 0.9), loc=2, title = "Accounts", borderaxespad=0.)
	plt.show()




play()





