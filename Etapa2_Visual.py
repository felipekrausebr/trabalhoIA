import random
import tkinter as tk


class AgenteBaseadoEmModelo:
    def __init__(self, tamanho_grid, obstaculos):
        self.tamanho = tamanho_grid
        self.linha = random.randint(0, tamanho_grid - 1)
        self.coluna = random.randint(0, tamanho_grid - 1)

        self.visitados = set()
        self.obstaculos = set(obstaculos)

    def posicao(self):
        return self.linha, self.coluna

    def atualizar_memoria(self):
        self.visitados.add(self.posicao())

    def acoes_validas(self):
        movimentos = []

        direcoes = {
            "N": (-1, 0),
            "S": (1, 0),
            "L": (0, 1),
            "O": (0, -1),
        }

        for acao, (dl, dc) in direcoes.items():
            nl = self.linha + dl
            nc = self.coluna + dc

            if 0 <= nl < self.tamanho and 0 <= nc < self.tamanho:
                if (nl, nc) not in self.obstaculos:
                    movimentos.append((acao, nl, nc))

        return movimentos

    def decidir(self):
        self.atualizar_memoria()

        movimentos = self.acoes_validas()

        # Priorizar células NÃO visitadas
        nao_visitados = [m for m in movimentos if (m[1], m[2]) not in self.visitados]

        if nao_visitados:
            return random.choice(nao_visitados)

        # Se tudo já foi visitado, escolhe qualquer válido
        return random.choice(movimentos) if movimentos else None

    def mover(self, movimento):
        if movimento:
            _, nl, nc = movimento
            self.linha = nl
            self.coluna = nc


class Simulacao:
    def __init__(self, tamanho=10, atraso=400):
        self.tamanho = tamanho
        self.atraso = atraso

        # Obstáculos fixos (pode ajustar)
        self.obstaculos = self.gerar_obstaculos()

        self.agente = AgenteBaseadoEmModelo(tamanho, self.obstaculos)

        self.passos = 0
        self.executando = True

        self.janela = tk.Tk()
        self.janela.title("Etapa 2 - Agente com Modelo")

        self.canvas = tk.Canvas(
            self.janela,
            width=tamanho * 50,
            height=tamanho * 50,
            bg="white"
        )
        self.canvas.pack()

        self.label = tk.Label(self.janela, font=("Arial", 12))
        self.label.pack()

        self.loop()

    def gerar_obstaculos(self):
        obstaculos = set()

        for _ in range(20):  # quantidade de obstáculos
            obstaculos.add((random.randint(0, 9), random.randint(0, 9)))

        return obstaculos

    def desenhar(self):
        self.canvas.delete("all")

        for i in range(self.tamanho):
            for j in range(self.tamanho):

                cor = "white"

                if (i, j) in self.obstaculos:
                    cor = "blue"

                elif (i, j) in self.agente.visitados:
                    cor = "#d3d3d3"

                x1 = j * 50
                y1 = i * 50
                x2 = x1 + 50
                y2 = y1 + 50

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="black")

        # desenhar agente
        l, c = self.agente.posicao()

        self.canvas.create_oval(
            c * 50 + 10,
            l * 50 + 10,
            c * 50 + 40,
            l * 50 + 40,
            fill="red"
        )

    def atualizar(self):
        movimento = self.agente.decidir()
        self.agente.mover(movimento)
        self.passos += 1

    def loop(self):
        if self.executando:
            self.atualizar()
            self.desenhar()

            self.label.config(
                text=f"Passos: {self.passos} | Visitados: {len(self.agente.visitados)}"
            )

        self.janela.after(self.atraso, self.loop)

    def executar(self):
        self.janela.mainloop()


if __name__ == "__main__":
    sim = Simulacao()
    sim.executar()