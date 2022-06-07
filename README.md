# ValidadorDeCNJs

Primeiro programa feito inteiramente por mim para um problema prático sem solução até então. Tem por objetivo validar se uma sequência de caracteres representa um número de processo válido, de acordo com o padrão CNJ.

Testa a validade por meio do dígito verificador, número de caracteres, viabilidade do ano de ingresso do processo e da justiça (por padrão, busca apenas processos na Justiça Federal, Justiça Comum e Justiça do Trabalho).

Retorna, em Excel (.xlsx), uma planilha com quatro colunas:
1. 'é cnj': indica se o número é ou não um número de processo no padrão CNJ
2. 'de': transcreve a entrada sem alterações
3. 'para': coloca a entrada no formato CNJ, com pontos, traços, sem espaços e com a quantidade correta de caracteres do padrão.
4. 'foi alterado?': indica se a entrada já estava no padrão correto ou se precisou ser ajustada ao padrão.

A solução é importante para regularizar bases de dados advindas de clientes jurídicos e que não estão de acordo com o padrão, o que dificulta sua união com bases extraídas de crawlers ou outros serviços de captura, devido à alteração da chave primária (número CNJ).
