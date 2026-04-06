import random
import tkinter as tk
from collections import deque


class AgenteBaseadoEmObjetivo:
    def __init__(self, tamanho, inicio, objetivo, obstaculos):
        self.tamanho = tamanho
        self.inicio = inicio
        self.objetivo = objetivo
        self.obstaculos = set(obstaculos)

        self.posicao_atual = inicio
        self.caminho_planejado = []
        self.caminho_percorrido = [inicio]

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
            if self.dentro_do_grid(l, c) and (l, c) not in self.obstaculos:
                validos.append((l, c))

        return validos

    def buscar_caminho_bfs(self):
        fila = deque([self.inicio])
        visitados = {self.inicio}
        pai = {}
        encontrou = False

        while fila:
            atual = fila.popleft()

            if atual == self.objetivo:
                encontrou = True
                break

            for vizinho in self.vizinhos_validos(atual):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    pai[vizinho] = atual
                    fila.append(vizinho)

        if not encontrou:
            return []

        caminho = []
        atual = self.objetivo

        while atual != self.inicio:
            caminho.append(atual)
            atual = pai[atual]

        caminho.append(self.inicio)
        caminho.reverse()
        return caminho

    def planejar(self):
        self.caminho_planejado = self.buscar_caminho_bfs()

    def mover_um_passo(self):
        if not self.caminho_planejado:
            return False

        if self.posicao_atual == self.objetivo:
            return False

        indice_atual = self.caminho_planejado.index(self.posicao_atual)

        if indice_atual + 1 < len(self.caminho_planejado):
            self.posicao_atual = self.caminho_planejado[indice_atual + 1]
            self.caminho_percorrido.append(self.posicao_atual)
            return True

        return False

    def chegou_ao_objetivo(self):
        return self.posicao_atual == self.objetivo


class SimulacaoEtapa3:
    def __init__(self, tamanho=10, tamanho_celula=55, atraso_ms=500, usar_obstaculos=True):
        self.tamanho = tamanho
        self.tamanho_celula = tamanho_celula
        self.atraso_ms = atraso_ms
        self.usar_obstaculos = usar_obstaculos

        self.obstaculos = self.gerar_obstaculos() if usar_obstaculos else set()
        self.inicio, self.objetivo = self.sortear_inicio_objetivo()

        self.agente = AgenteBaseadoEmObjetivo(
            tamanho=self.tamanho,
            inicio=self.inicio,
            objetivo=self.objetivo,
            obstaculos=self.obstaculos
        )
        self.agente.planejar()

        self.passo_atual = 0
        self.executando = False
        self.job = None

        self.janela = tk.Tk()
        self.janela.title("Etapa 3 - Agente Baseado em Objetivos")
        self.janela.geometry("980x700")
        self.janela.configure(bg="#f2f2f2")

        largura = self.tamanho * self.tamanho_celula
        altura = self.tamanho * self.tamanho_celula

        # Frame principal
        self.frame_principal = tk.Frame(self.janela, bg="#f2f2f2")
        self.frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        # Painel da esquerda
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

        self.frame_botoes = tk.Frame(self.frame_info, bg="#f2f2f2")
        self.frame_botoes.pack(anchor="nw", pady=20)

        tk.Button(self.frame_botoes, text="Iniciar", width=14, command=self.iniciar).grid(row=0, column=0, pady=5)
        tk.Button(self.frame_botoes, text="Pausar", width=14, command=self.pausar).grid(row=1, column=0, pady=5)
        tk.Button(self.frame_botoes, text="Passo", width=14, command=self.executar_um_passo_manual).grid(row=2, column=0, pady=5)
        tk.Button(self.frame_botoes, text="Reiniciar", width=14, command=self.reiniciar).grid(row=3, column=0, pady=5)

        # Painel da direita
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

    def gerar_obstaculos(self):
        quantidade = 15
        obstaculos = set()

        while len(obstaculos) < quantidade:
            pos = (random.randint(0, self.tamanho - 1), random.randint(0, self.tamanho - 1))
            obstaculos.add(pos)

        return obstaculos

    def sortear_inicio_objetivo(self):
        livres = [
            (i, j)
            for i in range(self.tamanho)
            for j in range(self.tamanho)
            if (i, j) not in self.obstaculos
        ]

        inicio = random.choice(livres)
        objetivo = random.choice(livres)

        while objetivo == inicio:
            objetivo = random.choice(livres)

        return inicio, objetivo

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
                cor = "white"

                if pos in self.obstaculos:
                    cor = "#1f5f9c"
                elif pos in caminho_set:
                    cor = "#d9edf7"
                if pos in percorrido_set:
                    cor = "#c8e6c9"

                if pos == self.inicio:
                    cor = "#fff3cd"
                if pos == self.objetivo:
                    cor = "#f8d7da"

                self.colorir_celula(i, j, cor)

        for i in range(self.tamanho):
            for j in range(self.tamanho):
                x_centro = j * self.tamanho_celula + self.tamanho_celula / 2
                y_centro = i * self.tamanho_celula + self.tamanho_celula / 2

                if (i, j) == self.inicio:
                    self.canvas.create_text(
                        x_centro,
                        y_centro,
                        text="I",
                        font=("Arial", 16, "bold")
                    )
                elif (i, j) == self.objetivo:
                    self.canvas.create_text(
                        x_centro,
                        y_centro,
                        text="F",
                        font=("Arial", 16, "bold")
                    )

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
            f"Obstáculos: {len(self.obstaculos)}\n"
            f"Caminho encontrado: {'Sim' if caminho_existe else 'Não'}\n"
            f"Tamanho do caminho: {max(0, len(self.agente.caminho_planejado) - 1)}"
        )

        if self.agente.chegou_ao_objetivo():
            texto += "\n\nObjetivo alcançado."

        if not caminho_existe:
            texto += "\n\nNenhum caminho válido encontrado."

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

        self.obstaculos = self.gerar_obstaculos() if self.usar_obstaculos else set()
        self.inicio, self.objetivo = self.sortear_inicio_objetivo()

        self.agente = AgenteBaseadoEmObjetivo(
            tamanho=self.tamanho,
            inicio=self.inicio,
            objetivo=self.objetivo,
            obstaculos=self.obstaculos
        )
        self.agente.planejar()

        self.passo_atual = 0
        self.atualizar_tela()

    def executar(self):
        self.iniciar()
        self.janela.mainloop()


if __name__ == "__main__":
    simulacao = SimulacaoEtapa3(
        tamanho=10,
        tamanho_celula=55,
        atraso_ms=500,
        usar_obstaculos=True
    )
    simulacao.executar()