from lib.langid import langid

def detect(text):
	textLang = langid.classify(text)
	print("textLang", textLang)
	lines = text.splitlines()
	linesCount = len(lines)
	print("linesCount", linesCount)
	langs = {} #langs dict of tottal lines
	for l, line in enumerate(lines):
		lineLang = langid.classify(line)[0]
		if not lineLang[0] in langs:
			langs[lineLang[0]]=[0,0,[]] #new lang item of total score, lines amount, lines positions
		langdata = langs[lineLang[0]]
		#print("langdata", langdata)
		langs[lineLang[0]][0] = langdata[0] + lineLang[1]
		langs[lineLang[0]][1] = langs[lineLang[0]][1] +len(line.split(" "))
		langs[lineLang[0]][2].append(l)
		
	print("lines langs", langs)
	linesLangs = []
	for l in langs:
		linesLangs.append((l,langs[l])) #e.g (language,(total score, lines amount, sentences positions))
	print(linesLangs)
	linesLangs.sort(key=lambda tup: tup[1], reverse=True)
	print(linesLangs)
	return linesLangs

detectLangTest = """***ENGLISH VERSION BELOW***
Per direct te huur, standard plus room bij The Student Hotel Amsterdam
In plaats van 755------> 685 euro (Volgeboekt voor deze prijs!)
*Kamer met 140 cm bed + en suite badkamer op de 9e (laatste verdieping van het hoofdgebouw)
*Oppervlakte +/- 17 m2
*Flat screen, bureau, ruime kledingkast
* Gedeelde keuken met gezellige huisgenoten en voorzien van alle gemakken
* Gratis gebruik maken van verschillende faciliteiten; fitness, studieruimtes, tv-ruimtes, tafeltennis etc.
*Fiets inbegrepen bij de prijs
*Perfecte ligging!! Naast tramhalte, metrostation, bushalte en op 15 min van het centrum.
*Verschillende activiteiten en feesten georganiseerd door het hotel.
Besluit je in december te verhuizen? Dan is een fikse korting bespreekbaar voor de resterende dagen van de maand december!!
Voor meer info:
http://www.thestudenthotel.com/our-locations/tsh-amsterdam
********************************************************************************
A standard plus room for rent at The Student Hotel Amsterdam from the 4th of December 2013.
Instead of 755 ------> 685 euro (FULLY BOOKED fort his price!)
*Room with 140cm double bed + en suite bathroom 9th floor. (TOP FLOOR of the highest building with stunning view!)
*+/- 17 sqm.
*Flat screen, desk, big wardrobe
*Shared kitchen with nice flatmates and all amenities present
* Free usage of several facilities; gym, studyrooms, tv-rooms, ping pong table etc.
*Bike included with the rent!
*Excellent location -tube, -tram, bus stops all next to the hotel.
*15 min to city centre by bike
*Several parties and activities organized by the staff of the hotel.
And if you decide to move in december I'll hook you up with a big discount for the remaining days of december!!
For more info:
http://www.thestudenthotel.com/our-locations/tsh-amsterdam"""

detectLangNlTest = """***ENGLISH VERSION BELOW***
Per direct te huur, standard plus room bij The Student Hotel Amsterdam
In plaats van 755------> 685 euro (Volgeboekt voor deze prijs!)
*Kamer met 140 cm bed + en suite badkamer op de 9e (laatste verdieping van het hoofdgebouw)
*Oppervlakte +/- 17 m2
*Flat screen, bureau, ruime kledingkast
* Gedeelde keuken met gezellige huisgenoten en voorzien van alle gemakken
* Gratis gebruik maken van verschillende faciliteiten; fitness, studieruimtes, tv-ruimtes, tafeltennis etc.
*Fiets inbegrepen bij de prijs
*Perfecte ligging!! Naast tramhalte, metrostation, bushalte en op 15 min van het centrum.
*Verschillende activiteiten en feesten georganiseerd door het hotel.
Besluit je in december te verhuizen? Dan is een fikse korting bespreekbaar voor de resterende dagen van de maand december!!
Voor meer info:
http://www.thestudenthotel.com/our-locations/tsh-amsterdam"""
if __name__=="__main__":
	detect(detectLangTest)