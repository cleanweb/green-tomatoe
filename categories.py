#!/usr/bin/python

categories=(
("People", ("Population","Populationpercentchange","Population in 2000","Personsunderyearsoldpercent","Personsunderyearsoldpercent","Personsyearsoldandoverpercent","Femalepersonspercent")),
("Demographics", ("Whitepersonspercent","Blackpersonspercent","AmericanIndianandAlaskaNativepersonspercent","Asianpersonspercent","NativeHawaiianandOtherPacificIslanderpercent","Personsreportingtwoormoreracespercent","PersonsofHispanicorLatinooriginpercent","WhitepersonsnotHispanicpersons")),
("People origin", ("Livinginsamehouseyearagopctyroldover","Foreignbornpersonspercent","LanguageotherthanEnglishspokenathomepctage","Highschoolgraduatespercentofpersonsage","Bachelorsdegreeorhigherpctofpersonsage","Veterans","Meantraveltimetoworkminutesworkersage")),
("People housing", ("Housingunits","Homeownershiprate","Housingunitsinmultiunitstructurespercent","Medianvalueofowneroccupiedhousingunits")),
("Household",("Households","Personsperhousehold","Percapitamoneyincomeinpastmonthsdollars","Medianhouseholdincome","Personsbelowpovertylevelpercent")),
("Business", ("Privatenonfarmestablishments","Privatenonfarmemployment","Privatenonfarmemploymentpercentchange","Nonemployerestablishments")),
("Business companies", ("Totalnumberoffirms","Blackownedfirmspercent","AmericanIndianandAlaskaNativeownedfirmspercent","Asianownedfirmspercent","NativeHawaiianandOtherPacificIslanderownedfirmspercent","Hispanicownedfirmspercent","Womenownedfirmspercent")),
("Business types", ("Manufacturersshipments","Merchantwholesalersales","Retailsales","Retailsalespercapita","Accommodationandfoodservicessales","Buildingpermits","Federalspending")),
("Geography", ("Landarea","Personspersquaremile","FIPSCode")),
("Energy sources", ("TotalEnergy","Coal","NaturalGas","Petroleum","TotalFossilFuel","NuclearElectricPower","RenewableEnergy")),
("Energy exchanges", ("NetInterstateFlow","NetElectricityImports")),
("Energy usage", ("EndUseResidential","EndUseCommercial","EndUseIndustrial","EndUseTransportation")))

for (name, list) in categories:
	print "##", name
	for category in list:
		print category,
	print "\n"