#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-

# Aelius Brazilian Portuguese POS-Tagger and Corpus Annotation Tool
#
# Copyright (C) 2010-2011 Leonel F. de Alencar
# Author: Leonel F. de Alencar <leonel.de.alencar@ufc.br>
#          
# URL: <http://sourceforge.net/projects/aelius/>
# For license information, see LICENSE.TXT
#
# $Id: ProcessaNomesProprios.py $

#from cPickle import dump 11042011
import string, nltk

exemplos=["– Luzia pediu a Deus e a Ávila para que lhe ajudassem a sair de Sobral .",
 "Deus ajudou Luzia .",
 "... Sobral era uma cidade intelectual .",
 "... Cidade intelectual , Sobral tinha muitos poetas .",
 "Município intelectual , Sobral tinha muitos poetas ",
"Fortaleza era uma cidade provinciana .", # também é minusculizada, embora seja nome próprio
 "Ávila ajudou Luzia .",
 "... Cansada , Luzia logo dormiu .",
 "Ávida por sossego , Luzia deixou a cidade .",
 "Ótimo !",
"Bom",
"... – Bom",
"?",
"! ? ? –",
""]

# sinais de pontuação que podem
# ocorrer no início das sentenças;
# pressupõe-se que no texto ocorre apenas
# Unicode 2013 EN DASH e reticências como sinais
# de pontuação além dos definidos em string.punctuation
pontuacao="–...%s" % string.punctuation



# palavras com inicial maiúscula em 
# posição não inicial
dicionario=nltk.defaultdict(int)

def extrai_palavra_inicial(sentenca):
	'''Extrai índice da palavra que se encontra no início de uma sentença
dada, sob a forma de uma lista de tokens, com cada sinal de pontuação, tal como
definido na variável global pontuacao,representando um token. 
Caso iniciada por sinal de pontuação, esse é ignorado.
'''
	comprimento=len(sentenca)
	if comprimento < 1:
		return -1
	

	else:
		inicio=0
		indice=0
		condicao=True
		
		while condicao and comprimento > indice:
			# print sentenca
			# print len(sentenca), indice 
			if sentenca[indice] in pontuacao: # pressupõe entrada toquenizada
				inicio+=1
			else:
				condicao=False
				return inicio
			indice+=1
	return -1

def armazena_palavras_maiusculas(sentenca):
	inicio=extrai_palavra_inicial(sentenca)
	if inicio >= 0:		
		for palavra in sentenca[inicio+1:]:
			p=palavra.decode("utf-8")
			if len(p) > 0 and p[0].isupper(): #aqui 14092010
				dicionario[palavra]+=1
	#f=open("dicionario_maiusculas.pkl","wb") # isso é mesmo necessário? 11042011: não!
	#dump(dicionario,f,-1)
	#f.close()
            
def minusculiza_nao_nomes_proprios(lista_de_sentencas):
	for sent in lista_de_sentencas:
		if len(sent) > 0:
			armazena_palavras_maiusculas(sent)
	for sent in lista_de_sentencas:
		if len(sent) > 0:
			inicio=extrai_palavra_inicial(sent)
			if inicio >=0 and dicionario[sent[inicio]] == 0:
            # print "Início da sentença:%s" % sent[inicio]
				palavra=sent[inicio]
				palavra=palavra.decode("utf-8").lower()
				sent[inicio]=  palavra.encode("utf-8")
				
	# print dicionario
	return lista_de_sentencas
            
def maiusculiza_inicio_de_sentenca(sentenca):
	inicio=extrai_palavra_inicial(sentenca)
	if inicio >= 0:
		palavra=sentenca[inicio]
		# print palavra
		palavra=palavra.decode("utf-8")
		palavra="%s%s" % (palavra[0].upper(),palavra[1:])
		sentenca[inicio]=palavra.encode("utf-8")
		# print "Início da sentença:%s" % sentenca[inicio]
	return sentenca # como o argumento da função é uma lista, esta é
# alterada pela função, tornando-se desnecessário retorná-la; talvez fosse 
# mais elegante criar uma nova lista 

def separa_palavras_de_etiquetas(lista_de_tuplas):
	lista_de_palavras=[w for w,t in lista_de_tuplas]
	lista_de_etiquetas=[t for w,t in lista_de_tuplas]
	return lista_de_palavras,lista_de_etiquetas

def pprint(lista_de_sentencas):
	for sent in lista_de_sentencas:
		for p in sent:
			print p,
		print

def main():
    lista_de_sentencas=[]
    for sent in exemplos:
	    lista_de_sentencas.append(sent.split())
    for sent in lista_de_sentencas:
        armazena_palavras_maiusculas(sent)
    #print dicionario
    lista_de_sentencas=minusculiza_nao_nomes_proprios(lista_de_sentencas)
    pprint(lista_de_sentencas)
    for i in range(len(lista_de_sentencas)):
	    lista_de_sentencas[i]=maiusculiza_inicio_de_sentenca(lista_de_sentencas[i])
    pprint(lista_de_sentencas)
 
if __name__ == '__main__':
    main()
