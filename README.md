# Trabalho 2 - Inteligencia Aritificial

----------------------------------------------
Informações do Projeto

Disciplina: Inteligência Artificial 

Aluno: Felipe Grein Krause

----------------------------------------------

# Descrição Geral

Este projeto tem como objetivo implementar e analisar diferentes tipologias de agentes inteligentes em um ambiente representado por um grid bidimensional (n × n).

Ao longo do desenvolvimento, foram implementadas quatro versões progressivas de agentes, cada uma incorporando níveis crescentes de sofisticação em termos de:

percepção do ambiente
representação interna
tomada de decisão

O estudo permite observar como a evolução da arquitetura do agente impacta seu comportamento e desempenho.

# Ambiente

O ambiente é modelado como um grid 10 × 10, onde:

cada célula representa uma posição possível do agente
o agente pode se mover apenas nas direções:
Norte (N)
Sul (S)
Leste (L)
Oeste (O)
não são permitidos movimentos diagonais

Dependendo da etapa, o ambiente pode conter:

células vazias
obstáculos estáticos
custos associados às células

# Etapa 1 – Agente Reativo Simples
