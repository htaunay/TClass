# encoding: utf8
"""
TODO

@authors: Henrique d'Escragnolle-Taunay
@contact: htaunay@gmail.com
"""

# global dependencies
import unicodedata

# local dependecies
from tclass.util.stemmer.stemmer import Stemmer

class RSLP(Stemmer):
	"""
    This class implements the interface defined in Stemmer for stemming
    words in the portuguese language.
    """

#>------------------------------------------------------------------------------
#> Special Methods

	def __init__(self):
	
		self.__sPlurais = [ 	
        	[ u"ns", 	u"m"],
        	[ u"ões", 	u"ão"],
			[ u"ães", 	u"ão", 	u"mães" ],
			[ u"ais", 	u"al", 	u"cais",u"mais" ],
			[ u"éis", 	u"el"],
			[ u"eis", 	u"el"],
			[ u"óis", 	u"ol"],
			[ u"is", 	u"il", 	u"lápis",u"cais",u"mais",u"crúcis",
			  				   	u"biquínis",u"pois",u"depois",u"dois",u"leis" ],
			[ u"les", 	 u"l"],
			[ u"res", 	 u"r"],
			[ u"s", 	 u"",  	u"aliás",u"pires",u"lápis",u"cais",
			  				   	u"mais",u"mas",u"menos",u"férias",u"fezes",
			  				   	u"pêsames",u"crúcis",u"gás",u"atrás",
			  				   	u"moisés",u"através",u"convés",u"ês",
								u"país",u"após",u"ambas",u"ambos",u"messias"] 
			]

		self.__sFemininos = [	
			[u"ona", 	u"ão", 	u"abandona",u"lona",u"iona",u"cortisona", u"mamona",
								u"monótona",u"maratona",u"acetona",u"detona",u"carona"],
			[u"ora", 	u"or"],
			[u"na", 	u"no", 	u"carona",u"abandona",u"lona",u"iona",u"mamona",
								u"cortisona",u"monótona",u"maratona",u"acetona",
								u"detona",u"guiana",u"campana",u"grana",
								u"caravana",u"banana",u"paisana"],
			[u"inha", 	u"inho",u"rainha",u"linha",u"minha"],
			[u"esa", 	u"ês",	u"mesa",u"obesa",u"princesa",u"turquesa",
								u"ilesa",u"pesa",u"presa",u"framboesa"],
			[u"osa", 	u"oso",	u"mucosa",u"prosa"],
			[u"íaca", 	u"íaco"],
			[u"ica", 	u"ico", u"dica"],
			[u"ada", 	u"ado", u"pitada"],
			[u"ida", 	u"ido", u"vida"],
			[u"ída", 	u"ido", u"recaída",u"saída",u"dúvida"],
			[u"ima", 	u"imo", u"vítima"],
			[u"iva", 	u"ivo", u"saliva",u"oliva"],
			[u"eira", 	u"eiro",u"beira",u"cadeira",u"frigideira",u"bandeira",
								u"feira",u"capoeira",u"barreira",u"fronteira",
								u"besteira",u"poeira"],
			[u"ã", 		u"ão",  u"amanhã",u"arapuã",u"fã",u"divã"]
			]
        					
		self.__sAugmentativos = [
			[u"íssimo", 	u""],
			[u"abilíssimo", 	u""],
			[u"díssimo", 		u""],
			[u"ésimo", 			u""],
			[u"érrimo", 		u""],
			[u"zinho", 			u""],
			[u"quinho", 		u"c"],
			[u"uinho", 			u""],
			[u"adinho", 		u"d"],
			[u"inho", 			u"",	u"caminho",u"cominho"],
			[u"alhão", 			u""],
			[u"uça", 			u""],
			[u"aço", 			u"",	u"antebraço"],
			[u"adão", 			u""],
			[u"ázio", 			u"",	u"topázio"],
			[u"arraz", 			u""],
			[u"arra", 			u""],
			[u"zão", 			u""],
			[u"ão", 			u"", 	u"camarão",u"chimarrão",u"canção",u"coração",
										u"embrião",u"grotão",u"glutão",u"ficção",u"fogão",
										u"feição",u"furacão",u"gamão",u"lampião",u"leão",
										u"macacão",u"nação",u"órfão",u"orgão",u"patrão",
										u"portão",u"quinhão",u"rincão",u"tração",u"verão",
  										u"falcão",u"espião",u"mamão",u"folião",u"cordão",
  										u"aptidão",u"campeão",u"colchão",u"limão",u"leilão",
  										u"melão",u"barão",u"milhão",u"bilhão",u"fusão",
   										u"cristão",u"ilusão",u"capitão",u"estação",u"senão"] 
   			]
 				
		self.__sSubstantivos = [
			[u"encialista", 	u""],
			[u"alista", 		u""],
			[u"agem", 			u"",	u"coragem",u"chantagem",u"vantagem",u"carruagem"],
			[u"iamento", 		u""],
			[u"amento", 		u"",	u"firmamento",u"fundamento",u"departamento"],
			[u"imento", 		u""],
			[u"mento",			u"", 	u"firmamento",u"elemento",u"complemento",
										u"instrumento",u"departamento"],
			[u"alizado", 		u""],
			[u"atizado", 		u""],
			[u"tizado",			u"",	u"alfabetizado"],
			[u"izado", 			u"",	u"organizado",u"pulverizado"],
			[u"ativo", 			u"",	u"pejorativo",u"relativo"],
			[u"tivo", 			u"",	u"relativo"],
			[u"ivo", 			u"",	u"passivo",u"possessivo",u"pejorativo",u"positivo"],
			[u"ado", 			u"",	u"ado"],
			[u"ido", 			u"",	u"cândido",u"consolido",u"rápido",u"decido",
										u"tímido",u"duvido",u"marido"],
			[u"ador", 			u""],
			[u"edor", 			u""],
			[u"idor", 			u"",	u"ouvidor"],
			[u"dor", 			u"",	u"ouvidor"],
			[u"sor", 			u"",	u"acessor"],
			[u"atória", 		u""],
			[u"tor",			u"",	u"benfeitor",u"leitor",u"editor",u"pastor",
										u"produtor",u"promotor",u"consultor"],
			[u"or", 			u"",	u"motor",u"melhor",u"redor",u"rigor",
										u"sensor",u"tambor",u"tumor",u"assessor",
										u"benfeitor",u"pastor",u"terior",u"favor",u"autor"],
			[u"abilidade", 		u""],
			[u"icionista", 		u""],
			[u"cionista", 		u""],
			[u"ionista", 		u""],
			[u"ionar",	 		u""],
			[u"ional", 			u""],
			[u"ência", 			u""],
			[u"ância", 			u"",	u"ambulância"],
			[u"edouro", 		u""],
			[u"queiro", 		u"c"],
			[u"adeiro",			u"",	u"desfiladeiro",],
			[u"eiro", 			u"",	u"desfiladeiro",u"pioneiro",u"mosteiro"],
			[u"uoso", 			u""],
			[u"oso", 			u"",	u"precioso"],
			[u"alizaç", 		u""],
			[u"atizaç", 		u""],
			[u"tizaç", 			u""],
			[u"izaç",	 		u"",	u"organizaç"],
			[u"ismo", 			u""],
			[u"izaç", 			u""],
			[u"aç", 			u"",	u"equaç",u"relaç"],
			[u"iç", 			u"",	u"eleiç"],
			[u"ário", 			u"",	u"voluntário",u"salário",u"aniversário",
										u"diário",u"lionário",u"armário"],
			[u"atório",			u""],
			[u"rio",			u"",	u"voluntário",u"salário",u"aniversário",
										u"diário",u"compulsório",u"lionário",u"próprio",
										u"stério",u"armário"],
			[u"ério", 			u""],
			[u"ès", 			u""],
			[u"eza", 			u""],
			[u"ez", 			u""],
			[u"esco", 			u""],
			[u"ante", 			u"",	u"gigante",u"elefante",u"adiante",u"possante",
										u"instante",u"restaurante"],
			[u"ástico",	 		u"",	u"eclesiástico"],
			[u"alístico", 		u""],
			[u"áutico", 		u""],
			[u"êuico", 			u""],
			[u"ático", 			u""],
			[u"tico",			u"",	u"político",u"eclesiástico",u"diagnostico",u"prático",
										u"doméstico",u"diagnóstico",u"idêntico",u"alopático",
										u"artístico",u"autêntico",u"eclético",u"crítico",u"critico"],
			[u"ico", 			u"",	u"tico",u"público",u"explico"],
			[u"ividade",	 	u""],
			[u"idade", 			u"",	u"autoridade",u"comunidade"],
			[u"oria", 			u"",	u"categoria"],
			[u"encial",	 		u""],
			[u"ista", 			u""],
			[u"auta",			u""],
			[u"quice", 			u"c"],
			[u"ice", 			u"",	u"cúmplice"],
			[u"íaco", 			u""],
			[u"ente", 			u"",	u"freqüente",u"alimente",u"acrescente",u"permanente",
										u"oriente",u"aparente"],
			[u"ense",			u""],
			[u"inal", 			u""],
			[u"ano", 			u""],
			[u"ável", 			u"",	u"afável",u"razoável",u"potável",u"vulnerável"],
			[u"ível", 			u"",	u"possível"],
			[u"vel",			u"",	u"possível",u"vulnerável",u"solúvel"],
			[u"ura", 			u""],
			[u"ural", 			u"",	u"imatura",u"acupuntura",u"costura"],
			[u"ual",			u"",	u"bissexual",u"virtual",u"visual",u"pontual"],
			[u"ial", 			u""],
			[u"al", 			u"",	u"afinal",u"animal",u"estatal",u"bissexual",
										u"desleal",u"fiscal",u"formal",u"pessoal",
										u"liberal",u"postal",u"virtual",u"visual",
										u"pontual",u"sideral",u"sucursal"],
			[u"alismo",			u""],
			[u"ivismo",			u""],
			[u"ismo",			u"",	u"cinismo"]
			]

		self.__sVerbos = [	
			[u"aríamo",		u""],
			[u"ássemo",		u""],
			[u"eríamo",		u""],
			[u"êssemo",		u""],
			[u"iríamo",		u""],
			[u"íssemo",		u""],
			[u"áramo",		u""],
			[u"árei",		u""],
			[u"aremo",		u""],
			[u"ariam",		u""],
			[u"aríei",		u""],
			[u"ássei",		u""],
			[u"assem",		u""],
			[u"ávamo",		u""],
			[u"êramo",		u""],
			[u"eremo",		u""],
			[u"eriam",		u""],
			[u"eríei",		u""],
			[u"êssei",		u""],
			[u"essem",		u""],
			[u"íramo",		u""],
			[u"iremo",		u""],
			[u"iriam",		u""],
			[u"iríei",		u""],
			[u"íssei",		u""],
			[u"issem",		u""],
			[u"ando",		u""],
			[u"endo",		u""],
			[u"indo",		u""],
			[u"ondo",		u""],
			[u"aram",		u""],
			[u"arão",		u""],
			[u"arde",		u""],
			[u"arei",		u""],
			[u"arem",		u""],
			[u"aria",		u""],
			[u"armo",		u""],
			[u"asse",		u""],
			[u"aste",		u""],
			[u"avam",		u"",	u"agravam"],
			[u"ávei",		u""],
			[u"eram",		u""],
			[u"erão",		u"",	u"verão"],
			[u"erde",		u""],
			[u"erei",		u""],
			[u"êrei",		u""],
			[u"erem",		u""],
			[u"eria",		u""],
			[u"ermo",		u""],
			[u"esse",		u""],
			[u"este",		u"",	u"faroeste",u"agreste"],
			[u"íamo",		u""],
			[u"iram",		u""],
			[u"íram",		u""],
			[u"irão",		u""],
			[u"irde",		u""],
			[u"irei",		u"",	u"admirei"],
			[u"irem",		u"",	u"adquirem"],
			[u"iria",		u""],
			[u"irmo",		u""],
			[u"isse",		u""],
			[u"iste",		u""],
			[u"iava",		u"",	u"ampliava"],
			[u"amo",		u""],
			[u"iona",		u""],
			[u"ara",		u"",	u"arara",u"prepara"],
			[u"ará",		u"",	u"alvará"],
			[u"are",		u"",	u"prepare"],
			[u"ava",		u"",	u"agrava"],
			[u"emo",		u""],
			[u"era",		u"",	u"acelera","espera"],
			[u"erá",		u""],
			[u"ere",		u"",	u"espere"],
			[u"iam",		u"",	u"enfiam",u"ampliam",u"elogiam",u"ensaiam"],
			[u"íei",		u""],
			[u"imo",		u"",	u"reprimo",u"intimo",u"íntimo",u"nimo",
									u"queimo",u"ximo"],
			[u"ira",		u"",	u"fronteira",u"sátira"],
			[u"ído",		u""],
			[u"irá",		u""],
			[u"tizar",		u"",	u"alfabetizar"],
			[u"izar",		u"",	u"organizar"],
			[u"itar",		u"",	u"acreditar",u"explicitar",u"estreitar"],
			[u"ire",		u"",	u"adquire"],
			[u"omo",		u""],
			[u"ai",			u""],
			[u"am",			u""],
			[u"ear",		u"",	u"alardear",u"nuclear"],
			[u"ar",			u"",	u"azar",u"bazaar",u"patamar"],
			[u"uei",		u""],
			[u"uía",		u"u"],
			[u"ei",			u""],
			[u"guem",		u"g"],
			[u"guém",		u"g"],
			[u"ém",			u"",	u"além"],
			[u"em",			u"",	u"alem",u"virgem"],
			[u"er",			u"",	u"éter",u"pier"],
			[u"eu",			u"",	u"chapeu"],
			[u"ia",			u"",	u"estória",u"fatia",u"acia",u"praia",u"elogia",
									u"mania",u"lábia",u"aprecia",u"polícia",u"arredia",
									u"cheia",u"ásia"],
			[u"ir",			u"",	u"freir"],
			[u"iu",			u""],
			[u"eou",		u""],
			[u"ou",			u""],
			[u"i",			u""]
			]

		self.__sAdverbos = [ [u"mente", 	u"",	u"experimente"] ]
		
		self.__sVogais = [ 	
			[u"bil",	u"vel"],
			[u"gue",	u"g",	u"gangue",u"jegue"],
			[u"á", 		u""], 
			[u"ê"		u"",	u"bebê"],
			[u"a",		u"",	u"ásia"],
			[u"e",		u""],
			[u"o",		u""]
			]

#>------------------------------------------------------------------------------
#> Public Methods

	def stem(self, word):

		auxWord = word.decode('UTF-8')
		wlength = len(auxWord)

		if auxWord[wlength-1:] == u"s" and len(auxWord) >= 3:
			result, auxWord = self.__applyStem(auxWord, self.__sPlurais)

		if (auxWord[wlength-1:] == u"a" or auxWord[wlength-1:] == u"ã") and len(auxWord) >= 3:
			result, auxWord = self.__applyStem(auxWord, self.__sFemininos)

		result, auxWord = self.__applyStem(auxWord, self.__sAugmentativos)
		result, auxWord = self.__applyStem(auxWord, self.__sAdverbos)

		result, auxWord = self.__applyStem(auxWord, self.__sSubstantivos)
		if not result:
			result, auxWord = self.__applyStem(auxWord, self.__sVerbos)

		if not result and auxWord[wlength-2:] != u"ão":
			result, auxWord = self.__applyStem(auxWord, self.__sVogais)

		if type(auxWord) != str:
			auxWord = unicodedata.normalize('NFKD', auxWord).encode('ascii','ignore')
		
		if len(auxWord) > 2:
			return auxWord
		else:
			return None
        
#>------------------------------------------------------------------------------
#> Private Methods

	def __trySuffixReplace( self, word, rule ):
		
		suffix = rule[0]
		replace = rule[1]
		
		wLength = len(word)
		sLength = len(suffix)
		matchingSuffix = False
		hasException = False
		
		if word[wLength-sLength:] == suffix:
			matchingSuffix = True
			
			if len(rule) > 2: #there are exceptions
				for i in range(len(rule)-2):
					if rule[i+2] == word:
						#TODO necessary?
						word = rule[i+2]
						hasException = True
			
			if hasException == False: #no exceptions
				word = word[:wLength-sLength] + replace

		return matchingSuffix, word
	
	def __applyStem( self, word, dictionary ):
	
		wLength = len(word)
		result = False

		for i in range(len(dictionary)):
			rule = dictionary[i]
			feedback, word = self.__trySuffixReplace( word, rule )
			
			if feedback == True:
				result = True
			
		return result, word
		
