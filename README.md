# Trabalho 2 – Inteligência Artificial

## Informações do Projeto
- **Disciplina:** Inteligência Artificial  
- **Aluno:** Felipe Grein Krause  

---

## Descrição Geral

Este projeto tem como objetivo implementar e analisar diferentes **tipologias de agentes inteligentes** em um ambiente representado por um **grid bidimensional (n × n)**.

Ao longo do desenvolvimento, foram construídas **quatro versões progressivas de agentes**, cada uma incorporando níveis crescentes de sofisticação em:

- percepção do ambiente  
- representação interna  
- tomada de decisão  

O estudo permite observar como a evolução da arquitetura dos agentes impacta diretamente seu **comportamento** e **desempenho**.

---

## Ambiente

O ambiente é modelado como um **grid 10 × 10**, onde:

- cada célula representa uma posição possível do agente  
- o agente pode se mover apenas nas direções:
  - **Norte (N)**
  - **Sul (S)**
  - **Leste (L)**
  - **Oeste (O)**
- **movimentos diagonais não são permitidos**

Dependendo da etapa, o ambiente pode conter:

- células vazias  
- obstáculos estáticos  
- custos associados às células  

---

## Etapa 1 – Agente Reativo Simples

### Descrição

Nesta etapa, foi implementado um **agente reativo simples**, cuja tomada de decisão é baseada **exclusivamente na percepção atual do ambiente**.

O agente:

- não possui memória  
- não registra estados anteriores  
- não constrói qualquer representação interna do ambiente  

---

### Objetivo

Alcançar as **quatro fronteiras do grid**:

- Norte  
- Sul  
- Leste  
- Oeste  

utilizando apenas informações do estado atual.

---

### Características

- ausência total de memória  
- sem modelo interno  
- ambiente sem obstáculos  
- comportamento puramente reativo  
- decisões locais e imediatas  

---

### 🧠 PEAS

| Elemento | Descrição |
|----------|-----------|
| **Performance** | alcançar todas as fronteiras do grid |
| **Environment** | grid 10x10 sem obstáculos |
| **Actuators** | movimentos nas direções N, S, L e O |
| **Sensors** | posição atual e limites do grid |

---

### Espaço de Estados

- **Estado:** posição atual do agente `(linha, coluna)`  
- **Estado inicial:** posição aleatória  
- **Ações:** mover nas quatro direções  
- **Transição:** deslocamento para uma célula adjacente válida  
- **Objetivo:** alcançar todas as bordas do grid  

---

### Limitações

- comportamento aleatório  
- pode repetir trajetórias  
- baixa eficiência  
- não aprende  
- não realiza planejamento  

---

## Considerações

A primeira etapa demonstra o funcionamento de um agente com arquitetura extremamente simples, evidenciando as limitações de sistemas que dependem apenas da percepção imediata.

Nas próximas etapas, a introdução de memória, representação interna e critérios mais elaborados de decisão permitirá comparar diferentes níveis de inteligência no mesmo ambiente.

---
