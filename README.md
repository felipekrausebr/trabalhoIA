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

### PEAS

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

## Etapa 2 – Agente Reativo Baseado em Modelo

### Descrição

Nesta etapa, o agente passa a manter um estado interno, armazenando informações sobre o ambiente já explorado.

Ele registra:

- células visitadas
- posições de obstáculos

---

### Objetivo

Explorar o ambiente visitando o maior número possível de células, evitando repetições e obstáculos.

---

### Características

- memória das posições visitadas
- identificação de obstáculos
- exploração mais eficiente
- decisões baseadas em percepção + memória

---

### PEAS

- **Performance:** maximizar cobertura do grid
- **Environment:** grid com obstáculos estáticos
- **Actuators:** movimentos N, S, L, O
- **Sensors:** posição atual + memória interna

---

### Espaço de Estados

- **Estado:** posição atual + mapa interno + células visitadas
- **Estado inicial:** posição aleatória
- **Ações:** movimentos válidos
- **Transição:** deslocamento para célula livre
- **Objetivo:** explorar o máximo possível do grid

---

### Melhorias em relação à Etapa 1

- evita revisitar células
- desvia de obstáculos
- melhora eficiência da exploração

---

## Etapa 3 – Agente Baseado em Objetivos

### Descrição

Nesta etapa, o agente passa a atuar com base em um objetivo explícito:

- sair de uma posição inicial
- alcançar uma posição final

---

### Objetivo

Encontrar um caminho válido do início ao destino.

---

### Características

- existência de estado objetivo
- uso de planejamento
- ambiente com obstáculos
- busca por solução viável

---

### Algoritmo utilizado

Foi utilizado o algoritmo:

**BFS (Busca em Largura)**

Justificativa:

- garante encontrar um caminho válido
- encontra o menor caminho em número de passos
- adequado para ambientes sem custo diferenciado

---

### PEAS

- **Performance:** alcançar o destino
- **Environment:** grid com obstáculos
- **Actuators:** movimentos N, S, L, O
- **Sensors:** posição atual + posição objetivo + mapa

---

### Espaço de Estados

- **Estado:** posição atual
- **Estado inicial:** posição inicial aleatória
- **Ações:** movimentos válidos
- **Transição:** deslocamento no grid
- **Objetivo:** atingir posição final
- **Estratégia:** BFS

---

### Evolução

- comportamento orientado a metas
- introdução de planejamento
- solução deixa de ser aleatória

---

## Etapa 4 – Agente Baseado em Utilidade

### Descrição

Nesta etapa, o agente passa a considerar não apenas alcançar o objetivo, mas também qualidade da solução, medida pelo custo total.

Cada célula do grid possui um custo associado, representando diferentes tipos de terreno.

---

### Objetivo

Encontrar o caminho de menor custo total entre o início e o destino.

---

### Características

- ambiente com custos
- avaliação de múltiplos caminhos
- otimização da solução
- decisão baseada em utilidade

---

### Algoritmo utilizado

**Dijkstra**

Justificativa:

- encontra o caminho de menor custo
- adequado para grafos com pesos positivos
- considera custo acumulado

### PEAS

- **Performance:** minimizar custo total
- **Environment:** grid com custos
- **Actuators:** movimentos N, S, L, O
- **Sensors:** posição atual + custos + objetivo

---

### Espaço de Estados

- **Estado:** posição atual
- **Estado inicial:** posição inicial definida
- **Ações:** movimentos válidos
- **Transição:** movimento com custo associado
- **Objetivo:** alcançar destino com menor custo
- **Estratégia:** Dijkstra

---

### Evolução

- escolha entre múltiplas soluções
- otimização do caminho
- análise quantitativa de desempenho
