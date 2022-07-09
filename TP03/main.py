# Percorre o AFD
def AFD(palavra, maquina, estadoInicial, contadorPosPalavara = 0):
  estadoAtual = estadoInicial
  while (len(palavra) > contadorPosPalavara):

      if palavra[contadorPosPalavara] in maquina[estadoAtual].keys():
        estadoAtual =  maquina[estadoAtual][palavra[contadorPosPalavara]]
        contadorPosPalavara += 1
      else:
        break
  
  return estadoAtual


def AP(palavra, maquina, estadoInicial, contadorPosPalavara = 0):
  estadoAtual = estadoInicial
  stack = []
  tam_stack = len(stack)
 #{'pri': {'a': [('pri', '\\', 'Y')], 'b': [('seg', 'Y', '\\')]}, 'seg': {'b': [('seg', 'Y', '\\')]}}
  while (len(palavra) > contadorPosPalavara):
      add = 1
      nenhuma_tran = True
      if (palavra[contadorPosPalavara] in maquina[estadoAtual].keys()):
        configs =  maquina[estadoAtual][palavra[contadorPosPalavara]]
        configs.append(-1)
        if("\\" in maquina[estadoAtual].keys()):
          configs.extend(maquina[estadoAtual]["\\"])
      elif("\\" in maquina[estadoAtual]):
        configs = maquina[estadoAtual]["\\"]
      else:
        break
      
      
      #desempilhar
      for config in configs: 
        if(config == -1):
          add = 0
          continue
        if(config[1] == "\\"):
          nenhuma_tran = False
          break
        elif(len(stack) > 0 and config[1] == stack[-1]):
          nenhuma_tran = False
          stack.pop()
          break

      if(nenhuma_tran):
        break

      #empilhar
      if(config[2] != "\\"):
        stack.extend(list(config[2][::-1]))
      estadoAtual = config[0]
      contadorPosPalavara += add

  if(len(stack) > 0 and contadorPosPalavara >= len(palavra)):
    while(True):
      nenhuma_tran = False
      if("\\" in maquina[estadoAtual].keys()):
        configs = maquina[estadoAtual]["\\"]
      else: 
        break

      for config in configs: 
        if(config[1] == "\\"):
          nenhuma_tran = False
          break
        elif(len(stack) > 0 and config[1] == stack[-1]):
          nenhuma_tran = False
          stack.pop()
          break

      if(nenhuma_tran):
        break
      
      if(config[2] != "\\"):
        stack.extend(list(config[2][::-1]))
      estadoAtual = config[0]
      contadorPosPalavara += add

  return estadoAtual, len(stack), contadorPosPalavara

# Confere que se o estado em que encerrou a computação é final
def VerificarReconhecimento(palavra, maquina, estadoInicial, estadoFinal):
  '''
    Confere que se o estado em que encerrou a computação é final
  '''
  
  contadorPalavra = 0
  estadoParado = AFD(palavra, maquina, estadoInicial, contadorPalavra)

  if estadoParado in estadoFinal:
    print("OK")
  else:
    print("X")

def VerificarReconhecimento_ap(palavra, maquina, estadoInicial, estadoFinal):
  ''' 
    confere se o estado é final e a pilha é vazia (tipo de reconhecimento utilizado)
  '''

  contadorPalavra = 0
  estadoParado, pilha, contadorPalavraParada = AP(palavra, maquina, estadoInicial, contadorPalavra)
  
  #print(estadoParado)
  #print(pilha)
  if estadoParado in estadoFinal and pilha == 0 and contadorPalavraParada >= len(palavra):
    print("OK")
  else:
    print("X")

def read_file(filename: str):
  ''' 
    # Lê o arquivo de entrada e retorna as informações necessárias para computar um AFD
  '''

  afd = {}
  initials = []
  finals = []
  tests = []

  with open(filename, "r") as file1:
    lines = file1.readlines()
    
    count = 0

    line = lines[1]
    for i in line[3:].replace("\n", "").split(" "):
        afd[i] = {}
    
    input_symbols = lines[2][3:].replace("\n", "")    

    line = lines[3]
    for i in line[3:].replace("\n", "").split(" "):
        initials.append(i)

    line = lines[4]
    for i in line[3:].replace("\n", "").split(" "):
        finals.append(i)

    for i in range(5, len(lines)):
        if(lines[i].replace("\n", "") == "---"):
            tests_init = i + 1
            break

        split_transitions = lines[i].replace("\n", "").split(" | ")
        
        #<<<<<<<<<<<<<<< AQUI >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        origem_destino = split_transitions[0].split(" -> ")
        simbolos = split_transitions[1].split(" ")

        for j in simbolos:
           
            afd[origem_destino[0]][j] = origem_destino[1]
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    for line in lines[tests_init:]:
        tests.append(line.replace("\n", ""))

  return afd, input_symbols, initials, finals, tests

def read_file_ap(filename: str):
  afd = {}
  initials = []
  finals = []
  tests = []

  with open(filename, "r") as file1:
    lines = file1.readlines()
    
    count = 0
    # Strips the newline character
    line = lines[1]
    for i in line[3:].replace("\n", "").split(" "):
        afd[i] = {}

    input_symbols = lines[2][3:].replace("\n", "")
    
    pushdown_symbols = lines[3][3:].replace("\n", "")

    line = lines[4]
    for i in line[3:].replace("\n", "").split(" "):
        initials.append(i)

    line = lines[5]
    for i in line[3:].replace("\n", "").split(" "):
        finals.append(i)


    for i in range(6, len(lines)):
        if(lines[i].replace("\n", "") == "---"):
            tests_init = i + 1
            break

        split_transitions = lines[i].replace("\n", "").split(" | ")
        
        origem_destino = split_transitions[0].split(" -> ")
        simbolos = split_transitions[1].split(" ")
        
        for j in simbolos:
            stack_info = j.split(",")[1]
            if(j[0] in afd[origem_destino[0]].keys()):
              afd[origem_destino[0]][j[0]].append((origem_destino[1], stack_info.split("/")[0], stack_info.split("/")[1]))
            else:
              afd[origem_destino[0]][j[0]] = [(origem_destino[1], stack_info.split("/")[0], stack_info.split("/")[1])]
    
    for line in lines[tests_init:]:
        tests.append(line.replace("\n", ""))

  ''' print(afd)
  print(initials)
  print(finals)
  print(tests) '''

  return afd, initials, finals, tests, pushdown_symbols

def tipo_automato(filename):
  with open(filename, "r") as file1:
        lines = file1.readlines()
  return lines[0].replace("\n", "")


def Execucao_AFD(filename):
    machine, simbolos_entrada, i, F, casos_teste = read_file(filename)
    for teste in casos_teste:
      #print(list(map(int, teste)))
      estadoInicial = i[0]
      estadoFinal = F
      VerificarReconhecimento(list(teste), machine, estadoInicial, estadoFinal)

def Execucao_AP(filename):
    ap, initials, finals, tests, pushdown_symbols = read_file_ap(filename)
    #print(ap)
    for teste in tests:
      #print(list(map(int, teste)))
      estadoInicial = initials[0]
      estadoFinal = finals
      VerificarReconhecimento_ap(list(teste), ap, estadoInicial, estadoFinal)




def main():
    print('|---------------------------------------------------------------|')
    print('|                      Trabalho Prático 3                       |')
    print('|                              -                                |')
    print('|              Fundamentos da Teoria da Computação              |')
    print('|---------------------------------------------------------------|')
    print()
    print("Digite o nome do arquivo de entrada:")
    arquivoEntrada = input(f">>")

    automato = tipo_automato(arquivoEntrada)
    if(automato == "@AF"):
      Execucao_AFD(arquivoEntrada)
    elif(automato == "@AP"):
      Execucao_AP(arquivoEntrada)



main()