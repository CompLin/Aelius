# -*- coding: utf-8 -*-
# Aelius Brazilian Portuguese POS-Tagger and Corpus Annotation Tool
#
# Copyright (C) 2010-2011 Leonel F. de Alencar
# Author: Leonel F. de Alencar <leonel.de.alencar@ufc.br>
#          
# URL: <http://sourceforge.net/projects/aelius/>
# For license information, see LICENSE.TXT

"""Os arquivos de texto e os modelos de que o Aelius necessita devem estar armazenados ou no diretório $HOME/aelius_data ou no diretório especificado na variável de ambiente AELIUS_DATA.
"""
import os

USUARIO=os.path.expanduser("~") # extração do valor de $HOME
CAMINHO=os.path.join(USUARIO,"aelius_data")
AELIUS_DATA=os.environ.get("AELIUS_DATA",CAMINHO)

# as variáveis abaixo iniciadas por __ são baseadas nas variáveis
# análogas do NLTK:

# Copyright (C) 2001-2011 NLTK Project
# Authors: Steven Bird <sb@csse.unimelb.edu.au>
#          Edward Loper <edloper@gradient.cis.upenn.edu>
# URL: <http://nltk.org/>

__versao__ = "0.9.3 sept-01-2011"

__copyright__ = """Copyright (C) 2010-2011 Leonel F. de Alencar

Distributed and Licensed under the Apache License, Version 2.0,
which is included by reference.
"""
__licenca__ = "Apache License, Version 2.0"

__mantenedor__ = "Leonel F. de Alencar"
__email_do_mantenedor__ = "leonel.de.alencar@ufc.br"
__autor__ = __mantenedor__
__email_do_autor__ = __email_do_mantenedor__

__all__=['ProcessaNomesProprios','AnotaCorpus','Avalia','MXPOST','CalculaEstatisticasLexicais','ExpandeContracoes', 'Toqueniza','SimplificaEtiquetas','Chunking']

def carrega(caminho):
    """Assume-se que 'caminho' é definido relativamente à variável AELIUS_DATA.
    """
    return os.path.join(AELIUS_DATA,caminho)
