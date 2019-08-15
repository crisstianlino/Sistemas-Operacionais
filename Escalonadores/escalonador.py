import sys
import csv
from operator import itemgetter


#Equipe:
#Antonio Victor
#Caio Rodrigues
#Cristian Lino
#
#
#
#Comando para execução: python escalonador.py Arquivo.csv Algoritmo saida=numero quantum=numero
#OBS: Utilizar o comando completo mesmo que o não seja necessário o quantum(No caso pode-se colocar qualquer valor no campo numero). Seguir estritamente esse formato.
#
#Exemplo: python escalonador.py processos.csv rr saida=1 quantum=10


class escalonador:

	def __init__(self,caminho,algoritmo,tipoSaida,quantum):
		self.caminho = caminho
		self.processos = []
		self.processos = self.lerArquivo(caminho)
		self.algoritmo = algoritmo
		self.tipoSaida = int(tipoSaida[6])
		self.quantum = int(quantum[8:])
		self.quantidadeProcessos = len(self.processos)
		self.tempoProcessamento = 0
		self.mediaTempoEspera = 0
		self.mediaTempoTurnaround = 0
		self.mediaThroughput = 0
		self.tempoContexto = 0
		self.tempoResposta = 0

	def lerArquivo(self,caminho):
		lista = []
		with open(caminho,'r') as csvfile:
			reader = csv.reader(csvfile)
			aux = []
			for linha in reader:
				aux = linha
				aux[0] = int(aux[0])
				aux[2] = int(aux[2])
				aux[3] = int(aux[3])
				lista.append(aux)
		return lista

	#Ordenar os processos em relação ao tempo de Chegada.

	def ordenarProcessosFCFS(self):
		processos_Ordenados = []
		processos_Ordenados = self.processos[:]
		processos_Ordenados = sorted(processos_Ordenados, key=itemgetter(0))
		return processos_Ordenados

	#Ordenar os processos em relação ao tempo de Chegada e ao tamanho do Burst Time.

	def ordernarProcessosSJF(self):
		processos_Ordenados = []
		processos_Ordenados = self.processos[:]
		processos_Ordenados = sorted(processos_Ordenados, key=itemgetter(0,2))
		return processos_Ordenados

	#Ordenar os processos em relação ao tempo de Chegada e ao prioridade do processo.

	def ordernarProcessosPriority(self):
		processos_Ordenados = []
		processos_Ordenados = self.processos[:]
		processos_Ordenados = sorted(processos_Ordenados, key=itemgetter(0,3))
		return processos_Ordenados

	#Escolhe qual o proximo processo a ser executado

	def prox(self,processos):
		for i in range(len(processos)):
			if(processos[i][0] <= self.tempoProcessamento):
				return processos[i]
				
	#Retorna o menor burst da lista de processos até o momento		
	
	def menor_burst(self,lista):
		menor = 0
		for i in range(len(lista)):
			if(lista[i][0] <= self.tempoProcessamento and lista[i][2] < lista[menor][2]):
				menor = i
		return menor
	
	#Retorna o indice da lista que tem maior prioridade(menor valor numerico) até o momento
	
	def menor_priority(self,lista):
		menor = 0
		for i in range(len(lista)):
			if(lista[i][0] <= self.tempoProcessamento and lista[i][3] < lista[menor][3]):
				menor = i
		return menor
		
	#Posiciona o processo no "final" da fila. Função necessária para o algoritmo RR
		
	def posicionar(self,processo,processos_Ordenados):
		posicao = 0
		for i in range(len(processos_Ordenados)):
			if(processos_Ordenados[i][0] <= self.tempoProcessamento):
				posicao = i+1
		lista = []
		if(posicao == 0):
			lista.append(processo[:])
			for j in range(len(processos_Ordenados)):
				lista.append(processos_Ordenados[j][:])
		else:
			for k in range(posicao):
				lista.append(processos_Ordenados[k][:])
			lista.append(processo[:])
			for l in range(len(processos_Ordenados)-posicao):
				lista.append(processos_Ordenados[posicao][:])
				posicao += 1
		return lista
				
			
	#Retorna o tempo de espera de um processo em específico
		
	def tempoEspera(self,gantt,processo):
		aux = []
		for i in range(len(gantt)):
			if(gantt[i][1] == processo[1]):
				aux.append(gantt[i][:])
		soma = aux[0][0] - processo[0]
		for j in range(len(aux)-1):
			soma += aux[j+1][0] - aux[j][4]
		return soma
		
	def tempoDeResposta(self,gantt,processo):
		aux = []
		for i in range(len(gantt)):
			if(gantt[i][1] == processo[1]):
				aux.append(gantt[i][:])
		return aux[0][0] - processo[0]
				
			

	

	def fcfs(self):
		processos_Ordenados = []
		processos_Ordenados = self.ordenarProcessosFCFS()
		if(self.tipoSaida == 1):
			for i in range(self.quantidadeProcessos):
				self.mediaTempoEspera += self.tempoProcessamento - processos_Ordenados[i][0] 	# Calculo do tempo de espera dos processos
				self.tempoResposta += self.tempoProcessamento - processos_Ordenados[i][0]	 	# Calculo do tempo de resposta(intervalo da chegada até o inicio do processo)
				self.tempoProcessamento += processos_Ordenados[i][2]						 	# Calculo do tempo de Processamento
				self.mediaTempoTurnaround += self.tempoProcessamento - processos_Ordenados[i][0]# Calculo do tempo de Turnaround(que é o tempo transcorrido desde o momento em que o software entra e o instante em que termina sua execução)

			# Imprimir o tipo de Saida 1
			self.imprimirTipo1(sys.argv[2],self.tempoProcessamento 													# Tempo de Processamento
										,((self.tempoProcessamento - self.tempoContexto)/self.tempoProcessamento)	# Utilização da CPU
										,(self.quantidadeProcessos/self.tempoProcessamento)							# Média do Throughput
										,(self.mediaTempoTurnaround/self.quantidadeProcessos)						# Média do Tempo Turnaround
										,(self.mediaTempoEspera/self.quantidadeProcessos)							# Média do tempo de Espera
										,(self.tempoResposta/self.quantidadeProcessos)								# Média de tempo de Resposta
										,self.tempoContexto															# Tempo da troca de Contexto
										,self.quantidadeProcessos)													# Quantidade de Processos executados
		else:

			for i in range(self.quantidadeProcessos):
				self.tempoProcessamento += processos_Ordenados[i][2]							#Calculo do Tempo de Processamento
				#Imprimir o tipo de Saida 2
				self.imprimirTipo2(processos_Ordenados[i][1],self.tempoProcessamento)			#Id do Processo/Tempo de Processamento


	def sjf(self):
		processos_Ordenados = []
		processos_Ordenados = self.ordernarProcessosSJF()
		#Escolher o primeiro processo a ser executado
		prox_Processos =  []
		prox_Processos.append(processos_Ordenados[0])
		if(self.tipoSaida == 1):
			for i in range(self.quantidadeProcessos):
				self.mediaTempoEspera += self.tempoProcessamento - prox_Processos[0][0]
				self.tempoResposta += self.tempoProcessamento - prox_Processos[0][0]
				self.tempoProcessamento += prox_Processos[0][2]
				self.mediaTempoTurnaround += self.tempoProcessamento - prox_Processos[0][0]
				#Deletar o processos das listas
				del prox_Processos[0]
				del processos_Ordenados[0]
				#Reogarnizar a lista de acordo com o burst time
				processos_Ordenados = sorted(processos_Ordenados, key=itemgetter(2))
				#Adicionar ao prox_Processos o processo com o menor burst time e que já entrou depois da execução do primeiro
				prox_Processos.append(self.prox(processos_Ordenados))
			self.imprimirTipo1(sys.argv[2],self.tempoProcessamento
											,((self.tempoProcessamento - self.tempoContexto)/self.tempoProcessamento)
											,(self.quantidadeProcessos/self.tempoProcessamento)
											,(self.mediaTempoTurnaround/self.quantidadeProcessos)
											,(self.mediaTempoEspera/self.quantidadeProcessos)
											,(self.tempoResposta/self.quantidadeProcessos)
											,self.tempoContexto
											,self.quantidadeProcessos)
		else:
			for i in range(self.quantidadeProcessos):
				self.tempoProcessamento += prox_Processos[0][2]
				self.imprimirTipo2(prox_Processos[0][1],self.tempoProcessamento)
				del prox_Processos[0]
				del processos_Ordenados[0]
				processos_Ordenados = sorted(processos_Ordenados, key=itemgetter(2))
				prox_Processos.append(self.prox(processos_Ordenados))


	def sjfp(self):
		processos_Ordenados = self.ordernarProcessosSJF() #Lista ordenada em relação ao tempo de chegada e burst time
		if(self.tipoSaida == 1):
			troca = 0
			gantt = [] # Derivação do gráfico de gantt de escalonamento em uma lista
			while len(processos_Ordenados) > 0:						
				indice = self.menor_burst(processos_Ordenados)#Verifica quem tem o menor burst no tempo de processamento atual
				if(indice != troca):#Aqui indica que um novo processo com burst time menor foi detectado								
					gantt.append(processos_Ordenados[troca][:])		#Salvamos a informação do ultimo processo que esteve na CPU
					gantt[-1].append(self.tempoProcessamento)		#e adicionamos a informação de quando ele terminou					
				processos_Ordenados[indice][2] -= 1			#Cada repetição do laço significa 1 unidade de CPU, logo é reduzida apenas
				self.tempoProcessamento += 1				#uma unidade de burst time do processo e adicionado uma unidade de processamento
				if(processos_Ordenados[indice][2] == 0):			#Caso o burst time do processo finalize, salvamos sua informação e
					gantt.append(processos_Ordenados[indice][:])	#deletamos da lista de processo e, logo após, é procurado outro processo
					gantt[-1].append(self.tempoProcessamento)		#na lista														
					del processos_Ordenados[indice]					#
					indice = self.menor_burst(processos_Ordenados)	#
				troca = indice	#troca guarda o indice do ultimo processo executado
			self.processos = self.lerArquivo(self.caminho)												
			processos_Ordenados = self.ordenarProcessosFCFS()
			for i in range(len(gantt) - 1):					#Nesses 2 laços são feitas alterações na lista gantt
				gantt[i+1][0] = gantt[i][4]					#para uso no calculo das estatisticas
			for j in range(len(gantt)):						#O tempo de chegada é alterado para o tempo em que o processo chegou na CPU, pois
				gantt[j][2] = gantt[j][4] - gantt[j][0]		#o processo poderia ter sido trocado de contexto				
			for k in range(len(processos_Ordenados)):#Para cada processo da lista, é calculado suas estatisticas							
				espera = self.tempoEspera(gantt,processos_Ordenados[k])			
				self.mediaTempoEspera += espera									
				self.mediaTempoTurnaround = self.mediaTempoTurnaround + espera + processos_Ordenados[k][2]
				self.tempoResposta += self.tempoDeResposta(gantt,processos_Ordenados[k])
			self.imprimirTipo1(self.algoritmo,self.tempoProcessamento
											,((self.tempoProcessamento - self.tempoContexto)/self.tempoProcessamento)
											,(self.quantidadeProcessos/self.tempoProcessamento)
											,(self.mediaTempoTurnaround/self.quantidadeProcessos)
											,(self.mediaTempoEspera/self.quantidadeProcessos)
											,(self.tempoResposta/self.quantidadeProcessos)
											,self.tempoContexto
											,self.quantidadeProcessos)
			
		else:
			troca = 0
			while len(processos_Ordenados) > 0:
				indice = self.menor_burst(processos_Ordenados)
				if(indice != troca):
					self.imprimirTipo2(processos_Ordenados[troca][1],self.tempoProcessamento)
				processos_Ordenados[indice][2] -= 1
				self.tempoProcessamento += 1
				if(processos_Ordenados[indice][2] == 0):
					self.imprimirTipo2(processos_Ordenados[indice][1],self.tempoProcessamento)
					del processos_Ordenados[indice]
					indice = self.menor_burst(processos_Ordenados)	
				troca = indice
					
				



	def priority(self):
		processos_Ordenados = self.ordernarProcessosPriority()
		#Escolher o primeiro processo a ser executado
		prox_Processos =  []
		prox_Processos.append(processos_Ordenados[0])
		if(self.tipoSaida == 1):
			for i in range(self.quantidadeProcessos):
				self.mediaTempoEspera += self.tempoProcessamento - prox_Processos[0][0]
				self.tempoResposta += self.tempoProcessamento - prox_Processos[0][0]
				self.tempoProcessamento += prox_Processos[0][2]
				self.mediaTempoTurnaround += self.tempoProcessamento - prox_Processos[0][0]
				#Deletar o processos das listas
				del prox_Processos[0]
				del processos_Ordenados[0]
				#Reogarnizar a lista de acordo com a prioridade
				processos_Ordenados = sorted(processos_Ordenados, key=itemgetter(3))
				#Adicionar ao prox_Processos o processo com o menor prioridade e que já entrou depois da execução do primeiro
				prox_Processos.append(self.prox(processos_Ordenados))
			self.imprimirTipo1(sys.argv[2],self.tempoProcessamento
											,((self.tempoProcessamento - self.tempoContexto)/self.tempoProcessamento)
											,(self.quantidadeProcessos/self.tempoProcessamento)
											,(self.mediaTempoTurnaround/self.quantidadeProcessos)
											,(self.mediaTempoEspera/self.quantidadeProcessos)
											,(self.tempoResposta/self.quantidadeProcessos)
											,self.tempoContexto
											,self.quantidadeProcessos)
		else:
			for i in range(self.quantidadeProcessos):
				self.tempoProcessamento += prox_Processos[0][2]
				self.imprimirTipo2(prox_Processos[0][1],self.tempoProcessamento)
				del prox_Processos[0]
				del processos_Ordenados[0]
				processos_Ordenados = sorted(processos_Ordenados, key=itemgetter(3))
				prox_Processos.append(self.prox(processos_Ordenados))
	
	def priorityp(self):#Algoritmo identico ao SJFP, com exceção na busca do processo, que é pela prioridade.
		processos_Ordenados = self.ordernarProcessosPriority()
		if(self.tipoSaida == 1):
			troca = 0
			gantt = []
			while len(processos_Ordenados) > 0:						
				indice = self.menor_priority(processos_Ordenados)		
				if(indice != troca):																
					gantt.append(processos_Ordenados[troca][:])
					gantt[-1].append(self.tempoProcessamento)							
				processos_Ordenados[indice][2] -= 1					
				self.tempoProcessamento += 1						
				if(processos_Ordenados[indice][2] == 0):			
					gantt.append(processos_Ordenados[indice][:])
					gantt[-1].append(self.tempoProcessamento)																
					del processos_Ordenados[indice]					
					indice = self.menor_priority(processos_Ordenados)	
				troca = indice
			self.processos = self.lerArquivo(self.caminho)												
			processos_Ordenados = self.ordenarProcessosFCFS()
			for i in range(len(gantt) - 1):					
				gantt[i+1][0] = gantt[i][4]					
			for j in range(len(gantt)):						
				gantt[j][2] = gantt[j][4] - gantt[j][0]						
			for k in range(len(processos_Ordenados)):							
				espera = self.tempoEspera(gantt,processos_Ordenados[k])			
				self.mediaTempoEspera += espera									
				self.mediaTempoTurnaround = self.mediaTempoTurnaround + espera + processos_Ordenados[k][2]
				self.tempoResposta += self.tempoDeResposta(gantt,processos_Ordenados[k])
			self.imprimirTipo1(self.algoritmo,self.tempoProcessamento
											,((self.tempoProcessamento - self.tempoContexto)/self.tempoProcessamento)
											,(self.quantidadeProcessos/self.tempoProcessamento)
											,(self.mediaTempoTurnaround/self.quantidadeProcessos)
											,(self.mediaTempoEspera/self.quantidadeProcessos)
											,(self.tempoResposta/self.quantidadeProcessos)
											,self.tempoContexto
											,self.quantidadeProcessos)
			
		else:
			troca = 0
			while len(processos_Ordenados) > 0:
				indice = self.menor_priority(processos_Ordenados)
				if(indice != troca):
					self.imprimirTipo2(processos_Ordenados[troca][1],self.tempoProcessamento)
				processos_Ordenados[indice][2] -= 1
				self.tempoProcessamento += 1
				if(processos_Ordenados[indice][2] == 0):
					self.imprimirTipo2(processos_Ordenados[indice][1],self.tempoProcessamento)
					del processos_Ordenados[indice]
					indice = self.menor_priority(processos_Ordenados)	
				troca = indice


	def rr(self):
		processos_Ordenados = self.ordenarProcessosFCFS()#Lista ordenada em relação ao tempo de chegada | Essa lista funcionará como uma fila
		if(self.tipoSaida == 1):
			gantt = []# Derivação do gráfico de gantt de escalonamento em uma lista
			while len(processos_Ordenados) > 0:
				if(processos_Ordenados[0][2] > self.quantum):#Aqui indica que o processo não vai finalizar em um quantum
					processos_Ordenados[0][2] -= self.quantum    #O burst time do processo é reduzido em relação ao quantum e 
					self.tempoProcessamento += self.quantum      #o tempo de processamento é adicionado em relação ao quantum
					gantt.append(processos_Ordenados[0][:])	 #Adicionamos a informação desse quantum na lista de gantt
					gantt[-1].append(self.tempoProcessamento)
					aux = processos_Ordenados[0][:]#Guardamos o processo nessa variavel auxiliar para reposiciona-lo em uma nova lista
					del processos_Ordenados[0]#O processo é deletado da lista para voltar ao final da "fila"
					processos_Ordenados = self.posicionar(aux,processos_Ordenados) #Nova lista produzida onde o primeiro elemento é o proximo processo a ser executado				
				else:
					self.tempoProcessamento += processos_Ordenados[0][2]
					gantt.append(processos_Ordenados[0][:])
					gantt[-1].append(self.tempoProcessamento)
					del processos_Ordenados[0]
			self.processos = self.lerArquivo(self.caminho)												
			processos_Ordenados = self.ordenarProcessosFCFS()
			for i in range(len(gantt) - 1):					
				gantt[i+1][0] = gantt[i][4]					
			for j in range(len(gantt)):						
				gantt[j][2] = gantt[j][4] - gantt[j][0]						
			for k in range(len(processos_Ordenados)):							
				espera = self.tempoEspera(gantt,processos_Ordenados[k])			
				self.mediaTempoEspera += espera									
				self.mediaTempoTurnaround = self.mediaTempoTurnaround + espera + processos_Ordenados[k][2]
				self.tempoResposta += self.tempoDeResposta(gantt,processos_Ordenados[k])
			self.imprimirTipo1(self.algoritmo,self.tempoProcessamento
											,((self.tempoProcessamento - self.tempoContexto)/self.tempoProcessamento)
											,(self.quantidadeProcessos/self.tempoProcessamento)
											,(self.mediaTempoTurnaround/self.quantidadeProcessos)
											,(self.mediaTempoEspera/self.quantidadeProcessos)
											,(self.tempoResposta/self.quantidadeProcessos)
											,self.tempoContexto
											,self.quantidadeProcessos)
		
		else:
			while len(processos_Ordenados) > 0:
				if(processos_Ordenados[0][2] > self.quantum):
					processos_Ordenados[0][2] -= self.quantum
					self.tempoProcessamento += self.quantum
					self.imprimirTipo2(processos_Ordenados[0][1],self.tempoProcessamento)
					aux = processos_Ordenados[0][:]
					del processos_Ordenados[0]
					processos_Ordenados = self.posicionar(aux,processos_Ordenados)				
				else:
					self.tempoProcessamento += processos_Ordenados[0][2]
					self.imprimirTipo2(processos_Ordenados[0][1],self.tempoProcessamento)
					del processos_Ordenados[0]



	def imprimirTipo1(self,tipoAlgoritmo,tempoProcessamento,utilizaçãoCPU,mediaThroughput,mediaTempoTurnaround,mediaTempoEspera,tempoResposta,tempoContexto,quantidadeProcessos):
		print("\nAlgoritmo " + tipoAlgoritmo)
		print("Tempo de Processamento: {}".format(tempoProcessamento))
		print("Percentual da Utilização da CPU: {}".format(utilizaçãoCPU*100))
		print("Media Throughput dos processos: {}".format(mediaThroughput))
		print("Média Turnaround dos processos: {}".format(mediaTempoTurnaround))
		print("Média Tempo de espera dos processos: {}".format(mediaTempoEspera))
		print("Média do Tempo de Resposta dos processos: {}".format(tempoResposta))
		print("Média de Troca de contextos: {}".format(tempoContexto))
		print("Número de Procesos executados: {}\n".format(quantidadeProcessos))

	def imprimirTipo2(self, pid, tempoProcessamento):
		print("Id do processo: {}".format(pid))
		print("Tempo de Processamento: {}".format(tempoProcessamento))
		
	def main(self):
		if(self.algoritmo == "fcfs" or self.algoritmo == "FCFS"):
			self.fcfs()
		elif (self.algoritmo == "sjf" or self.algoritmo == "SJF"):
			self.sjf()
		elif (self.algoritmo == "sjfp" or self.algoritmo == "SJFP"):
			self.sjfp()
		elif (self.algoritmo == "priority" or self.algoritmo == "PRIORITY"):
			self.priority()
		elif (self.algoritmo == "priorityp" or self.algoritmo == "PRIORITYP"):
			self.priorityp()
		elif (self.algoritmo == "rr" or self.algoritmo == "RR"):
			self.rr()


escala = escalonador(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
escala.main()

