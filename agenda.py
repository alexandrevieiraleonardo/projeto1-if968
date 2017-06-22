import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

def printCores(texto, cor) :
  print(cor + texto + RESET)
  
def prioridadeValida(pri):
  if len(pri) == 3:
    return (pri[1].isalpha() and pri[0] == '(' and pri[2] == ')')
  else:
    return False

def horaValida(horaMin) :
  return ((len(horaMin) == 4  and horaMin.isnumeric())and(0 <= int(horaMin[2:])<= 59 and 0 <= int(horaMin[:2])<= 23))

def projetoValido(proj):
  return (proj[0] == '+' and len(proj)>=2)

def contextoValido(cont):
  return (cont[0] == '@'and len(cont)>=2)

def dataValida(data):
  meses = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
  if len(data) == 8 and data.isnumeric():
    mes = int(data[:4][2:])
    return (1<=mes<=12 and 1<=int(data[:2])<=meses[mes])
  else:
    return False

def adicionar(descricao, extras):
    # não é possível adicionar uma atividade que não possui descrição.
    if descricao  == '' :
      descricao = input("Digite descrição:")
    listaAtividade = ['','','','','',''] #inicia uma lista nula
    listaAtividade.pop(3)
    listaAtividade.insert(3,descricao)  #add a desscricao na posicao 3
    for item in extras:   #add os componentes em suas posicoes
        if dataValida(item):
            listaAtividade.pop(0)
            listaAtividade.insert(0,item)
        if horaValida(item):
            listaAtividade.pop(1)
            listaAtividade.insert(1,item)
        if len(item) == 1:
            listaAtividade.pop(2)
            listaAtividade.insert(2,'(' + item + ')')
        if contextoValido(item):
            listaAtividade.pop(4)
            listaAtividade.insert(4,item)
        if projetoValido(item):
            listaAtividade.pop(5)
            listaAtividade.insert(5,item)      
    novaAtividade = ' '.join(listaAtividade)  # converte a lista pra string
    #print(novaAtividade)
  # Escreve no TODO_FILE.
    try:
      fp = open(TODO_FILE, 'a')
      fp.write(novaAtividade + "\n")
      fp.close()
    except IOError as err:
      print("Não foi possível escrever para o arquivo " + TODO_FILE)
      print(err)
      return False

    return True 

# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []
  #linhas = linhas.splitlines()
  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
    l = l.rstrip('\n')
    tokens = l.split() # quebra o string em palavras
    for item in tokens: # valida palavra por palavra e atribui a suas respectivas strings
      if prioridadeValida(item):
        pri = item
      elif contextoValido(item):
        contexto = item
      elif projetoValido(item):
        projeto = item
      elif dataValida(item):
        data = item
      elif horaValida(item):
        hora = item
      else:
        desc = desc + item + ' '
      tokens.insert(tokens.index(item),'')  
      tokens.remove(item)   #elimina o token ja computado
    itens.append((desc, (data, hora, pri, contexto, projeto)))
  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém.


def listar(): #
    print('\n\n----------Lista de Tarefas-------------')
    # Ler o TODO_FILE.
    try:
      fp = open(TODO_FILE, 'r')
      i = 0
      linhas = fp.readlines() #le todas as linhas
      itens = organizar(linhas) # transforma em uma lista de tuplas
      for i in range(len(itens)):
        itens[i] = itens[i] + tuple(str(i)) #add a posicao da linha no arquivo, no fim de cada tupla
        i = i+1
      itens_ordenados = ordenarPorPrioridade(itens) # ordena a lista de tuplas
      for item in itens_ordenados:
          pr = item[1][2]
          print(item[2] + ' ',end='')
          if (pr=='(A)'or pr=='(B)'or pr=='(C)'or pr=='(D)'): #prioridades de A-D ficam vermelhas
            printCores(linhas[int(item[2])],RED)
          else:
            printCores(linhas[int(item[2])],BLUE) # o resto fica azul
      fp.close()
    except IOError as err:
      print("Não foi possível ler o arquivo" + TODO_FILE)
      print(err)
      return False
    print('---------------------------------------\n\n')
def ordenarPorDataHora(itens):
  
  return itens
   
def ordenarPorPrioridade(itens):
  itens = sorted(itens,key=lambda item:item[1][2])#ordena, porem os sem prioridades ficam em primeiro
  ordenados = []
  inicio = -1
  i=0
  for item in itens:
    if(item[1][2] == '' and inicio == -1):  #verifica o indice em que os elementos sem prioridade comecam
      inicio = i
    if(item[1][2] == '' and inicio != -1): #verifica o indice em que os elementos sem prioridade terminam
      fim = i
    i = i + 1
  for i in range(fim+1,len(itens)): #add os itens com prioridade no inicio da lista ordenados
    ordenados.append(itens[i])
  for i in range(inicio,fim+1): #add os itens SEM prioridade no inicio da lista ordenados
    ordenados.append(itens[i])
  return ordenados

def fazer(num):
  # Ler o TODO_FILE e remover a linha procurada das linhas do arquivo
    try:
      fp = open(TODO_FILE, 'r')
      linhas = fp.readlines()
      linha_feita = linhas[num] #supondo que a ordem é a de escrita
      linhas.remove(linha_feita)
      fp.close()
    except IOError as err:
      print("Não foi possível ler o arquivo" + TODO_FILE)
      print(err)
      return False
    
  # Ler o ARCHIVE_FILE e add a linha procurada no final do arquivo
    try:
      fp = open(ARCHIVE_FILE, 'a')
      fp.write(linha_feita)
      fp.close()
    except IOError as err:
      print("Não foi possível ler o arquivo" + ARCHIVE_FILE)
      print(err)
      return False
    
    # Atualizar TODO_FILE, com a linha procurada removida
    try:
      fp = open(TODO_FILE, 'w')
      fp.write(''.join(linhas))
      fp.close()
    except IOError as err:
      print("Não foi possível ler o arquivo" + TODO_FILE)
      print(err)
      return False
    return num

def remover(num):
  # Ler o TODO_FILE e remover a linha procurada das linhas do arquivo
    try:
      fp = open(TODO_FILE, 'r+')
      linhas = fp.readlines()
      linha_remover = linhas[num] #supondo que a ordem é a de escrita
      linhas.remove(linha_remover)
      fp.close()
    except IOError as err:
      print("Não foi possível ler o arquivo" + TODO_FILE)
      print(err)
      return False
  # Atualizar TODO_FILE , com a linha procurada removida
    try:
      fp = open(TODO_FILE, 'w')
      fp.write(''.join(linhas))
      fp.close()
    except IOError as err:
      print("Não foi possível ler o arquivo" + TODO_FILE)
      print(err)
      return False
    return num
  
def priorizar(num, prioridade):
    # Ler o TODO_FILE , procurar a linha[num] e mudar o trecho da string referente a prioridade
    try:
      fp = open(TODO_FILE, 'r')
      linhas = fp.readlines()
      linha_modificar = linhas[num] #supondo que a ordem é a de escrita
      inicio = linha_modificar.find('(')
      fim = linha_modificar.find(')') #encontrando o trecho referente a  prioridade
      linha_modificada = linha_modificar[:inicio+1] + prioridade + linha_modificar[fim:]
      linhas[num] = linha_modificada
      fp.close()
    except IOError as err:
      print("Não foi possível ler o arquivo" + TODO_FILE)
      print(err)
      return False
    # Atualizar TODO_FILE, com a prioridade da linha procurada alterada
    try:
      fp = open(TODO_FILE, 'w')
      fp.write(''.join(linhas))
      fp.close()
    except IOError as err:
      print("Não foi possível ler o arquivo" + TODO_FILE)
      print(err)
      return False
    return num
  
def processarComandos(comandos) :
  comandos.pop(0)
  if comandos[0] == ADICIONAR:
    comandos.pop(0) 
    desc = ''
    extras = []
    for item in comandos:
      if((dataValida(item) or projetoValido(item) or horaValida(item)) or (len(item) == 1 or contextoValido(item))):
        extras.append(item)
      else: 
        desc = desc + ' ' + item
    adicionar(desc,extras)
  elif comandos[0] == LISTAR:
    listar()
  elif comandos[0] == REMOVER:
    remover( int(comandos[1]))
  elif comandos[0] == FAZER:
    fazer(int(comandos[1])) 
  elif comandos[0] == PRIORIZAR:
    priorizar(int(comandos[1]),comandos[2])
  else :
    print("Comando inválido.")

processarComandos(sys.argv)
