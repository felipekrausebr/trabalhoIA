import random
import heapq
import tkinter as tk


class AgenteBaseadoEmUtilidade:
    def __init__(self, tamanho, inicio, objetivo, grade_custos):
        self.tamanho = tamanho
        self.inicio = inicio
        self.objetivo = objetivo
        self.grade_custos = grade_custos

        self.posicao_atual = inicio
        self.caminho_planejado = []
        self.caminho_percorrido = [inicio]
        self.custo_total = 0

    def dentro_do_grid(self, linha, coluna):
        return 0 <= linha < self.tamanho and 0 <= coluna < self.tamanho

    def vizinhos_validos(self, posicao):
        linha, coluna = posicao
        candidatos = [
            (linha - 1, coluna),  # Norte
            (linha + 1, coluna),  # Sul
            (linha, coluna - 1),  # Oeste
            (linha, coluna + 1),  # Leste
        ]

        validos = []
        for l, c in candidatos:
            if self.dentro_do_grid(l, c):
                validos.append((l, c))
        return validos

    def buscar_menor_caminho_dijkstra(self):
        fila = []
        heapq.heappush(fila, (0, self.inicio))

        distancias = {self.inicio: 0}
        pai = {}
        visitados = set()

        while fila:
            custo_atual, atual = heapq.heappop(fila)

            if atual in visitados:
                continue

            visitados.add(atual)

            if atual == self.objetivo:
                break

            for vizinho in self.vizinhos_validos(atual):
                custo_entrada = self.grade_custos[vizinho[0]][vizinho[1]]
                novo_custo = custo_atual + custo_entrada

                if vizinho not in distancias or novo_custo < distancias[vizinho]:
                    distancias[vizinho] = novo_custo
                    pai[vizinho] = atual
                    heapq.heappush(fila, (novo_custo, vizinho))

        if self.objetivo not in distancias:
            return [], None

        caminho = []
        atual = self.objetivo

        while atual != self.inicio:
            caminho.append(atual)
            atual = pai[atual]

        caminho.append(self.inicio)
        caminho.reverse()

        return caminho, distancias[self.objetivo]

    def planejar(self):
        self.caminho_planejado, custo = self.buscar_menor_caminho_dijkstra()
        self.custo_total_planejado = custo if custo is not None else 0

    def mover_um_passo(self):
        if not self.caminho_planejado:
            return False

        if self.posicao_atual == self.objetivo:
            return False

        indice_atual = self.caminho_planejado.index(self.posicao_atual)

        if indice_atual + 1 < len(self.caminho_planejado):
            proxima = self.caminho_planejado[indice_atual + 1]
            self.posicao_atual = proxima
            self.caminho_percorrido.append(proxima)
            self.custo_total += self.grade_custos[proxima[0]][proxima[1]]
            return True

        return False

    def chegou_ao_objetivo(self):
        return self.posicao_atual == self.objetivo


class SimulacaoEtapa4:
    def __init__(self, tamanho=10, tamanho_celula=55, atraso_ms=500):
        self.tamanho = tamanho
        self.tamanho_celula = tamanho_celula
        self.atraso_ms = atraso_ms

        self.grade_custos = self.gerar_grade_custos()
        self.inicio, self.objetivo = self.sortear_inicio_objetivo()

        self.agente = AgenteBaseadoEmUtilidade(
            tamanho=self.tamanho,
            inicio=self.inicio,
            objetivo=self.objetivo,
            grade_custos=self.grade_custos
        )
        self.agente.planejar()

        self.passo_atual = 0
        self.executando = False
        self.job = None

        self.janela = tk.Tk()
        self.janela.title("Etapa 4 - Agente Baseado em Utilidade")
        self.janela.geometry("1080x720")
        self.janela.configure(bg="#f2f2f2")

        largura = self.tamanho * self.tamanho_celula
        altura = self.tamanho * self.tamanho_celula

        self.frame_principal = tk.Frame(self.janela, bg="#f2f2f2")
        self.frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        self.frame_info = tk.Frame(self.frame_principal, bg="#f2f2f2")
        self.frame_info.grid(row=0, column=0, sticky="n", padx=(0, 25))

        self.label_info = tk.Label(
            self.frame_info,
            text="",
            font=("Arial", 12),
            justify="left",
            anchor="nw",
            bg="#f2f2f2"
        )
        self.label_info.pack(anchor="nw")

        self.frame_legenda = tk.Frame(self.frame_info, bg="#f2f2f2")
        self.frame_legenda.pack(anchor="nw", pady=15)

        tk.Label(self.frame_legenda, text="Legenda de custos", font=("Arial", 11, "bold"), bg="#f2f2f2").pack(anchor="w")
        tk.Label(self.frame_legenda, text="Verde = custo 1", bg="#f2f2f2").pack(anchor="w")
        tk.Label(self.frame_legenda, text="Amarelo = custo 2", bg="#f2f2f2").pack(anchor="w")
        tk.Label(self.frame_legenda, text="Vermelho = custo 3", bg="#f2f2f2").pack(anchor="w")

        self.frame_botoes = tk.Frame(self.frame_info, bg="#f2f2f2")
        self.frame_botoes.pack(anchor="nw", pady=20)

        tk.Button(self.frame_botoes, text="Iniciar", width=14, command=self.iniciar).grid(row=0, column=0, pady=5)
        tk.Button(self.frame_botoes, text="Pausar", width=14, command=self.pausar).grid(row=1, column=0, pady=5)
        tk.Button(self.frame_botoes, text="Passo", width=14, command=self.executar_um_passo_manual).grid(row=2, column=0, pady=5)
        tk.Button(self.frame_botoes, text="Reiniciar", width=14, command=self.reiniciar).grid(row=3, column=0, pady=5)

        self.frame_grid = tk.Frame(self.frame_principal, bg="#f2f2f2")
        self.frame_grid.grid(row=0, column=1, sticky="n")

        self.canvas = tk.Canvas(
            self.frame_grid,
            width=largura,
            height=altura,
            bg="white",
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.canvas.pack()

        self.atualizar_tela()

    def gerar_grade_custos(self):
        # distribuição simples de terrenos:
        # maioria custo 1, alguns custo 2, poucos custo 3
        grade = []
        for _ in range(self.tamanho):
            linha = []
            for _ in range(self.tamanho):
                valor = random.choices([1, 2, 3], weights=[65, 25, 10])[0]
                linha.append(valor)
            grade.append(linha)
        return grade

    def sortear_inicio_objetivo(self):
        livres = [(i, j) for i in range(self.tamanho) for j in range(self.tamanho)]
        inicio = random.choice(livres)
        objetivo = random.choice(livres)

        while objetivo == inicio:
            objetivo = random.choice(livres)

        return inicio, objetivo

    def cor_por_custo(self, custo):
        if custo == 1:
            return "#8ee28e"
        if custo == 2:
            return "#f4e66a"
        return "#ef5350"

    def colorir_celula(self, linha, coluna, cor):
        x1 = coluna * self.tamanho_celula
        y1 = linha * self.tamanho_celula
        x2 = x1 + self.tamanho_celula
        y2 = y1 + self.tamanho_celula
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=cor)

    def desenhar_grid(self):
        self.canvas.delete("all")

        caminho_set = set(self.agente.caminho_planejado)
        percorrido_set = set(self.agente.caminho_percorrido)

        for i in range(self.tamanho):
            for j in range(self.tamanho):
                pos = (i, j)
                custo = self.grade_custos[i][j]
                cor = self.cor_por_custo(custo)

                if pos in caminho_set:
                    cor = "#9fd3ff"
                if pos in percorrido_set:
                    cor = "#90caf9"

                if pos == self.inicio:
                    cor = "#fff3cd"
                if pos == self.objetivo:
                    cor = "#f8d7da"

                self.colorir_celula(i, j, cor)

                x_centro = j * self.tamanho_celula + self.tamanho_celula / 2
                y_centro = i * self.tamanho_celula + self.tamanho_celula / 2

                if pos == self.inicio:
                    self.canvas.create_text(x_centro, y_centro, text="I", font=("Arial", 16, "bold"))
                elif pos == self.objetivo:
                    self.canvas.create_text(x_centro, y_centro, text="F", font=("Arial", 16, "bold"))
                else:
                    self.canvas.create_text(x_centro, y_centro, text=str(custo), font=("Arial", 10))

        linha, coluna = self.agente.posicao_atual
        x1 = coluna * self.tamanho_celula + 10
        y1 = linha * self.tamanho_celula + 10
        x2 = (coluna + 1) * self.tamanho_celula - 10
        y2 = (linha + 1) * self.tamanho_celula - 10

        self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="black")
        self.canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text="R",
            fill="white",
            font=("Arial", 14, "bold")
        )

    def atualizar_tela(self):
        self.desenhar_grid()

        caminho_existe = len(self.agente.caminho_planejado) > 0

        texto = (
            f"Início: {self.inicio}\n"
            f"Objetivo: {self.objetivo}\n"
            f"Posição atual: {self.agente.posicao_atual}\n"
            f"Passo atual: {self.passo_atual}\n"
            f"Caminho encontrado: {'Sim' if caminho_existe else 'Não'}\n"
            f"Tamanho do caminho: {max(0, len(self.agente.caminho_planejado) - 1)}\n"
            f"Custo acumulado percorrido: {self.agente.custo_total}\n"
            f"Custo total planejado: {self.agente.custo_total_planejado}"
        )

        if self.agente.chegou_ao_objetivo():
            texto += "\n\nObjetivo alcançado com menor custo."

        self.label_info.config(text=texto)

    def executar_logica_passo(self):
        if not self.agente.caminho_planejado:
            self.atualizar_tela()
            return "SEM_CAMINHO"

        if self.agente.chegou_ao_objetivo():
            self.atualizar_tela()
            return "FIM"

        moveu = self.agente.mover_um_passo()

        if moveu:
            self.passo_atual += 1

        self.atualizar_tela()

        if self.agente.chegou_ao_objetivo():
            return "FIM"

        return "CONTINUA"

    def loop_automatico(self):
        if not self.executando:
            return

        resultado = self.executar_logica_passo()

        if resultado in ["FIM", "SEM_CAMINHO"]:
            self.executando = False
            return

        self.job = self.janela.after(self.atraso_ms, self.loop_automatico)

    def iniciar(self):
        if not self.executando:
            self.executando = True
            self.loop_automatico()

    def pausar(self):
        self.executando = False
        if self.job is not None:
            self.janela.after_cancel(self.job)
            self.job = None

    def executar_um_passo_manual(self):
        if not self.executando:
            self.executar_logica_passo()

    def reiniciar(self):
        self.pausar()

        self.grade_custos = self.gerar_grade_custos()
        self.inicio, self.objetivo = self.sortear_inicio_objetivo()

        self.agente = AgenteBaseadoEmUtilidade(
            tamanho=self.tamanho,
            inicio=self.inicio,
            objetivo=self.objetivo,
            grade_custos=self.grade_custos
        )
        self.agente.planejar()

        self.passo_atual = 0
        self.atualizar_tela()

    def executar(self):
        self.iniciar()
        self.janela.mainloop()


if __name__ == "__main__":
    simulacao = SimulacaoEtapa4(
        tamanho=10,
        tamanho_celula=55,
        atraso_ms=500
    )
    simulacao.executar()