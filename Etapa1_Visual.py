import random
import tkinter as tk


class AgenteReativoSimples:
    def __init__(self, tamanho_grid):
        self.tamanho_grid = tamanho_grid
        self.linha = random.randint(0, tamanho_grid - 1)
        self.coluna = random.randint(0, tamanho_grid - 1)

    def perceber_acoes_validas(self):
        acoes_validas = []

        if self.linha > 0:
            acoes_validas.append("N")
        if self.linha < self.tamanho_grid - 1:
            acoes_validas.append("S")
        if self.coluna < self.tamanho_grid - 1:
            acoes_validas.append("L")
        if self.coluna > 0:
            acoes_validas.append("O")

        return acoes_validas

    def decidir_movimento(self):
        return random.choice(self.perceber_acoes_validas())

    def mover(self, acao):
        if acao == "N":
            self.linha -= 1
        elif acao == "S":
            self.linha += 1
        elif acao == "L":
            self.coluna += 1
        elif acao == "O":
            self.coluna -= 1

    def posicao(self):
        return self.linha, self.coluna


class SimulacaoGrid:
    def __init__(self, tamanho_grid=10, tamanho_celula=60, atraso_ms=500, max_passos=200):
        self.tamanho_grid = tamanho_grid
        self.tamanho_celula = tamanho_celula
        self.atraso_ms = atraso_ms
        self.max_passos = max_passos

        self.agente = AgenteReativoSimples(tamanho_grid)
        self.fronteiras_alcancadas = set()
        self.passo_atual = 0
        self.executando = False
        self.job = None
        self.trilha = []

        self.janela = tk.Tk()
        self.janela.title("Etapa 1 - Agente Reativo Simples")

        largura = tamanho_grid * tamanho_celula
        altura = tamanho_grid * tamanho_celula

        self.label_info = tk.Label(self.janela, text="", font=("Arial", 12), justify="left")
        self.label_info.pack(pady=10)

        self.canvas = tk.Canvas(self.janela, width=largura, height=altura, bg="white")
        self.canvas.pack()

        frame = tk.Frame(self.janela)
        frame.pack(pady=10)

        tk.Button(frame, text="Iniciar", width=12, command=self.iniciar).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Pausar", width=12, command=self.pausar).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Passo", width=12, command=self.executar_um_passo_manual).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Reiniciar", width=12, command=self.reiniciar).grid(row=0, column=3, padx=5)

        self.verificar_fronteiras()
        self.atualizar_tela()

    def verificar_fronteiras(self):
        linha, coluna = self.agente.posicao()

        if linha == 0:
            self.fronteiras_alcancadas.add("NORTE")
        if linha == self.tamanho_grid - 1:
            self.fronteiras_alcancadas.add("SUL")
        if coluna == 0:
            self.fronteiras_alcancadas.add("OESTE")
        if coluna == self.tamanho_grid - 1:
            self.fronteiras_alcancadas.add("LESTE")

    def colorir_celula(self, linha, coluna, cor):
        x1 = coluna * self.tamanho_celula
        y1 = linha * self.tamanho_celula
        x2 = x1 + self.tamanho_celula
        y2 = y1 + self.tamanho_celula
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=cor)

    def desenhar_grid(self):
        self.canvas.delete("all")

        for i in range(self.tamanho_grid):
            for j in range(self.tamanho_grid):
                cor = "white"

                if i == 0 or i == self.tamanho_grid - 1 or j == 0 or j == self.tamanho_grid - 1:
                    cor = "#e8f4ff"

                if (i, j) in self.trilha:
                    cor = "#d9d9d9"

                self.colorir_celula(i, j, cor)

        linha, coluna = self.agente.posicao()

        x1 = coluna * self.tamanho_celula + 10
        y1 = linha * self.tamanho_celula + 10
        x2 = (coluna + 1) * self.tamanho_celula - 10
        y2 = (linha + 1) * self.tamanho_celula - 10

        self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="black")
        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="R", fill="white", font=("Arial", 14, "bold"))

    def atualizar_tela(self, acao="---"):
        self.desenhar_grid()
        linha, coluna = self.agente.posicao()

        texto = (
            f"Passo: {self.passo_atual}\n"
            f"Posição atual: ({linha}, {coluna})\n"
            f"Última ação: {acao}\n"
            f"Fronteiras alcançadas: "
            f"{', '.join(sorted(self.fronteiras_alcancadas)) if self.fronteiras_alcancadas else 'Nenhuma'}"
        )
        self.label_info.config(text=texto)

    def terminou(self):
        return len(self.fronteiras_alcancadas) == 4 or self.passo_atual >= self.max_passos

    def executar_logica_passo(self):
        if self.terminou():
            return "FIM"

        self.trilha.append(self.agente.posicao())

        acao = self.agente.decidir_movimento()
        self.agente.mover(acao)
        self.passo_atual += 1
        self.verificar_fronteiras()
        self.atualizar_tela(acao)

        print(f"Passo {self.passo_atual}: ação={acao}, posição={self.agente.posicao()}")

        return acao

    def loop_automatico(self):
        if not self.executando:
            return

        resultado = self.executar_logica_passo()

        if resultado == "FIM":
            self.executando = False
            if len(self.fronteiras_alcancadas) == 4:
                self.label_info.config(text=self.label_info.cget("text") + "\n\nObjetivo concluído.")
            else:
                self.label_info.config(text=self.label_info.cget("text") + "\n\nLimite de passos atingido.")
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
            resultado = self.executar_logica_passo()
            if resultado == "FIM":
                if len(self.fronteiras_alcancadas) == 4:
                    self.label_info.config(text=self.label_info.cget("text") + "\n\nObjetivo concluído.")
                else:
                    self.label_info.config(text=self.label_info.cget("text") + "\n\nLimite de passos atingido.")

    def reiniciar(self):
        self.pausar()
        self.agente = AgenteReativoSimples(self.tamanho_grid)
        self.fronteiras_alcancadas = set()
        self.passo_atual = 0
        self.trilha = []
        self.verificar_fronteiras()
        self.atualizar_tela()

    def executar(self):
        self.iniciar()
        self.janela.mainloop()


if __name__ == "__main__":
    simulacao = SimulacaoGrid(
        tamanho_grid=10,
        tamanho_celula=60,
        atraso_ms=500,
        max_passos=500
    )
    simulacao.executar()