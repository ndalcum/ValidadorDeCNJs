#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import warnings
import datetime as dt
from datetime import date


# In[ ]:


##################################
# DEIXA APENAS NÚMEROS NA STRING #
##################################

def tira_carac_nao_numericos(numero_cnj):
    '''
    Retira todos os caracteres diferentes de digitos e retorna uma string apenas com numeros.
    
    Parâmetros
    --------
    numero_cnj : str
        Numero de processo CNJ sem formatacao.
    
    Saída
    --------
    cnj_digits: str
        String somente com os numeros do processo CNJ. 
    '''

    cnj_digits = ''
    
    try:
        for digit in numero_cnj:    
            if digit.isdigit():
                cnj_digits += str(digit)
    except:
        pass

    return cnj_digits


# In[ ]:


##############################################
# ADICIONA ZEROS À ESQUERDA DE UMA SEQUÊNCIA #
##############################################

def adiciona_zeros_a_esq(cnj_ou_campo, num_caract=20):
    '''
    Adiciona zeros ate que o número atinja o numero de caracteres desejado.
    
    Parametros
    --------
    cnj_ou_campo : str
        Número CNJ ou do campo a ser formatado.
    num_caract=20 : int (opt)
        Número de caracteres do comprimento do campo ou do numero CNJ (usualmente 20).
    
    Saida
    --------
    cnj_digits: str
        String com o numero acrescido dos zeros a esquerda. 
    '''

    return tira_carac_nao_numericos(cnj).zfill(20)


# In[ ]:


##############################################
# DEVOLVE O PADRÃO CNJ, COM PONTOS E TRAÇOS  #
##############################################

def normaliza_cnj(cnj):
    '''
    Inclui  os caracteres nao numericos e retorna uma string no formato CNJ.
    
    Parametros
    --------
    cnj : str
        Numero de processo CNJ com 20 digitos numericos.
    
    Saida
    --------
    cnj_normalizado: str
        String ja formatada no padrao CNJ com 25 digitos (nnnnnnn-dv.aaaa.j.tr.oooo). 
    '''
    
    cnj_normalizado = ''
    
    if (len(cnj) == 20) and (cnj == tira_carac_nao_numericos(cnj)):
        cnj_d = identifica_campos_cnj(cnj)
        caracteres_nao_numericos = ['-', '.', '.', '.', '.']
        
        count = 0 
        
        
        while count < 6:
            cnj_normalizado = cnj_normalizado + list(cnj_d.values())[count]
            if count < 5:
                cnj_normalizado += caracteres_nao_numericos[count]
            count+=1
            
        return cnj_normalizado
    
    else:
        pass


# In[ ]:


###########################################################
# VERIFICA SE O Nª NA POSIÇÃO DO ANO É VÁLIDO (após 1970) #
###########################################################

def ano_eh_valido(cnj):
    '''
    Checa se o valor na posicao do ano eh apos 1970.
    
    Parametros
    ----------
    cnj_apenas_numeros : str
        String contendo apenas numeros.
        
    Saida
    ----------
    True se a posicao do ano retornar um numero entre 1970 e o ano atual.
    False se a posicao do ano retornar um numero diferente do intervalo possivel.
    '''
    cnj = str(tira_carac_nao_numericos(cnj))
    cnj_d = identifica_campos_cnj(cnj)
    
    return int(cnj_d['ano']) in range(1970, date.today().year)


# In[ ]:


#################################################
# IDENTIFICA E SEPARA OS 6 CAMPOS DO PADRÃO CNJ #
#################################################

def identifica_campos_cnj(cnj):
    '''
    Identifica os campos do numero de processo no formato CNJ e retorna um dicionario de campos.
    
    Parametros
    ----------
    cnj : str (obr)
        String contendo apenas números.
        
    Saida
    ----------
    cnj_d : dict
        Dicionario contendo os campos do numero CNJ:
        numero (7 dígitos) - numeracao crescente de acordo com a ordem de distribuicao do processo;
        dv (2 dígitos) - digito verificador do processo;
        ano (4 dígitos) - ano de distribuicao do processo;
        justica (1 dígito) - codigo identificador da justica onde o processo tramita;
        tribunal (2 dígitos) - codigo identificador do tribunal regional onde o processo tramita;
        origem (4 dígitos) - codigo da comarca/cidade em que o processo tramita.
    '''
    
    cnj = tira_carac_nao_numericos(cnj)
    
    try:    
        cnj_d = {
            'numero': cnj[0:7],
            'dv': cnj[7:9],
            'ano': cnj[9:13],
            'just': cnj[13],
            'tribunal': cnj[14:16],
            'origem': cnj[16:]
        }
        
    except:
        cnj_d = {
            'numero': cnj,
            'dv': '',
            'ano': '',
            'just': '',
            'tribunal': '',
            'origem': ''
        }

    return cnj_d


# In[ ]:


#############################################
# VERIFICA SE O DÍGITO VERIFICADOR É VÁLIDO #
#############################################

def dv_eh_valido(cnj):
    '''
    Parametros:
    --------
    cnj: str
    
    Saida
    --------
    True se o resultado da operacao eh igual a 1.
    False se o resultado da operacao eh diferente de 1.
    '''
    
    cnj = str(tira_carac_nao_numericos(cnj))
    cnj_d = identifica_campos_cnj(cnj)
    
    r = int(str(int(cnj_d['numero'])%97) + str(cnj_d['ano'] + cnj_d['just'] + cnj_d['tribunal']))%97
    r = int(str(r) + cnj_d['origem'] + cnj_d['dv'])%97
    
    return r == 1


# In[ ]:


#############################################
# VERIFICA SE O DÍGITO VERIFICADOR É VÁLIDO #
#############################################

def justica_eh_valida(cnj, justicas_possiveis=[4, 5, 8]):
    '''
    Checa se o processo tramita na Justica Federal, Trabalhista ou Civel.
    
    Parâmetros
    ----------
    cnj_apenas_numeros : str
        String contendo apenas numeros.
    justicas_possiveis : list
        Lista contendo possibilidades de dígitos para a justiça. Por padrão aceita:
            - 4: Justiça Federal
            - 5: Justiça do Trabalho
            - 8: Justiça Comum (Cível e Criminal)
        
    Saida
    ----------
    True se a posicao da justica retornar 4 (JF), 5 (JT) ou 8 (JC).
    False se a posicao do ano retornar um numero diferente do intervalo possivel.
    '''
    
    cnj = str(tira_carac_nao_numericos(cnj))
    cnj_d = identifica_campos_cnj(cnj)
    
    return int(cnj_d['just']) in justicas_possiveis


# In[ ]:


######################################
# SEPARA CAMPO A CAMPO NO PADRÃO CNJ #
######################################

def normaliza_campos_cnj(cnj_d):
    '''
    Acrescenta zeros à esquerda em cada campodo numero de processo no formato CNJ e retorna um dicionario de campos.
    
    Parametros
    ----------
    cnj : str (obr)
        String contendo apenas números.
        
    Saida
    ----------
    cnj_d : dict
        Dicionario contendo os campos do numero CNJ preenchidos com zeros à esquerda de acordo com :
        numero (7 dígitos) - numeracao crescente de acordo com a ordem de distribuicao do processo;
        dv (2 dígitos) - digito verificador do processo;
        ano (4 dígitos) - ano de distribuicao do processo;
        justica (1 dígito) - codigo identificador da justica onde o processo tramita;
        tribunal (2 dígitos) - codigo identificador do tribunal regional onde o processo tramita;
        origem (4 dígitos) - codigo da comarca/cidade em que o processo tramita.
    '''
    
    cnj_d['numero'] = cnj_d['numero'].zfill(7)
    cnj_d['dv'] = cnj_d['dv'].zfill(2)
    cnj_d['ano'] = cnj_d['ano'].zfill(4)
    cnj_d['just'] = cnj_d['just'].zfill(1)
    cnj_d['tribunal'] = cnj_d['tribunal'].zfill(2)
    cnj_d['origem'] = cnj_d['origem'].zfill(4)

    return cnj_d


# In[ ]:


#######################################################################
# VERIFICA SE O CNJ DE ENTRADA JÁ ESTAVA NO PADRÃO OU SE FOI ALTERADO #
#######################################################################

def cnj_foi_alterado(cnj, cnj_normalizado):
    '''
    Identifica se o cnj original foi mantido ou se precisou ser normalizado para encaixar-se no padrão.
    
    Parametros
    ----------
    cnj : str (obr)
        String original.
        
    cnj_normalizado: str (obr)
        String de cnj final, após todos os tratamentos
        
    Saida
    ----------
    resultado : bool
        True se forem diferentes
        False se forem iguais
    '''
    return cnj != cnj_normalizado


# In[ ]:


#######################################################################################################
# VERIFICA SE O CNJ É VÁLIDO E RETORNA VERIFICAÇÃO, CNJ INICIAL, CNJ NORMALIZADO E SE HOUVE ALTERAÇÃO #
#######################################################################################################

def cnj_eh_valido(cnj):
    
    # garante que a entrada tem apenas numeros e sera interpretada como string
    cnj_apenas_numeros = str(tira_carac_nao_numericos(cnj))
    
    
    try:
        # testa se a entrada tem o comprimento padrão do cnj (20 caracteres)
        if len(cnj_apenas_numeros) == 20:

            # verifica se o dv é válido
            if dv_eh_valido(cnj_apenas_numeros):

                # se for, retorna True e o cnj normalizado
                return dv_eh_valido(cnj_apenas_numeros), cnj, normaliza_cnj(cnj_apenas_numeros)

            else:
                # se não for, retorna falso e o cnj original
                return dv_eh_valido(cnj_apenas_numeros), cnj, normaliza_cnj(cnj_apenas_numeros)

        # se tem menos de 20 digitos
        else:

            #primeiro tenta split nos campos para colocar 20 digitos com os zeros distribuídos

            cnj_d = identifica_campos_cnj(cnj)
            cnj_campos = cnj.replace('-', '.').split('.')

            count = 0

            for key in cnj_d.keys():
                try:
                    cnj_d[key] = cnj_campos[count]
                    count+=1
                except:
                    return False, cnj, normaliza_cnj(cnj_apenas_numeros)

            cnj_d = normaliza_campos_cnj(cnj_d)
            cnj_apenas_numeros = ''.join(cnj_d.values())

            # verifica se o dv é válido
            if dv_eh_valido(cnj_apenas_numeros) and justica_eh_valida(cnj_apenas_numeros) and ano_eh_valido(cnj_apenas_numeros):

                # se for, retorna True e o cnj normalizado

                return dv_eh_valido(cnj_apenas_numeros), cnj, normaliza_cnj(cnj_apenas_numeros)

            else:

                # se nao for, como no caso de não ter pontos e traços, acrescenta zeros na frente
                cnj_apenas_numeros_20_digitos = adiciona_zeros_a_esq(cnj)

                # verifica se o dv agora eh valido 
                if dv_eh_valido(cnj_apenas_numeros_20_digitos):

                    # se for, retorna True e o cnj normalizado
                    return dv_eh_valido(cnj_apenas_numeros_20_digitos), cnj, normaliza_cnj(cnj_apenas_numeros_20_digitos)

                else:

                    # se não for, tenta verificar outras posições para os zeros faltantes 
                    cnj_d = identifica_campos_cnj(cnj_apenas_numeros)
                    cnj_d['origem'] = cnj_d['origem'].zfill(4)

                    count = 1
                    comp_original = len(cnj_apenas_numeros)

                    while (count < (len(cnj_apenas_numeros) - 6)):
                        cnj_d['numero'] = cnj_apenas_numeros[:count].zfill(7)
                        cnj_d['dv'] = cnj_apenas_numeros[count:count+2].zfill(2)
                        cnj_d['ano'] = cnj_apenas_numeros[count+2:count+6].zfill(4)
                        cnj_d['just'] = cnj_apenas_numeros[count+6:count+7].zfill(1)
                        cnj_d['tribunal'] = cnj_apenas_numeros[count+7:count+9].zfill(2)
                        cnj_d['origem'] = cnj_apenas_numeros[count+9:count+13].zfill(4)

                        cnj_possivel = ''.join([campo for campo in cnj_d.values()])

                        # se for, retorna True e o cnj normalizado
                        if dv_eh_valido(cnj_possivel) and justica_eh_valida(cnj_possivel) and ano_eh_valido(cnj_possivel):
                            return dv_eh_valido(cnj_apenas_numeros), cnj, normaliza_cnj(cnj_apenas_numeros)

                        # se não for, tenta uma nova posição até encerrar todas as possibilidades
                        count+=1

                        # se sair do loop sem solução, retorna False e o cnj original
                        return dv_eh_valido(cnj_apenas_numeros), cnj, normaliza_cnj(cnj_apenas_numeros)
    except:
        pass


# In[ ]:


######################
# PROGRAMA PRINCIPAL #
######################

try:
    cliente = input('Digite o nome do cliente: ')
    cnjs = pd.DataFrame(pd.read_csv('cnjs.csv'))
    cnjs = list(cnjs.iloc[:, 0])
    resultado = [cnj_eh_valido(cnj) for cnj in cnjs]
    resultado = pd.DataFrame(resultado, columns=['é cnj', 'de', 'para'])
    resultado['foi alterado?'] = resultado['de'] != resultado['para']
    nome_arquivo = cliente + "_" + str(resultado.shape[0]) + '_cnjs_normalizados.xlsx'
    resultado.to_excel(nome_arquivo)
    print(f'\n\nARQUIVO \"{nome_arquivo}\" GERADO COM SUCESSO!')
except:
    print("\n\nERRO\n\nVerifique:\n1. se a entrada se chama \"cnjs\" e possui extensão .csv;\n" +
          "2. se este arquivo tem apenas uma coluna com o título 'cnjs' na célula A1.\n" +
          "\n-- FECHE TODOS OS ARQUIVOS E TENTE NOVAMENTE --")

