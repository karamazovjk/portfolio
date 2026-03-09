# Desempenho Acadêmico e Comportamento Estudantil

**Área:** Educação · Análise Exploratória de Dados · Dados Abertos  
**Ferramentas:** Python (pandas, NumPy, Matplotlib, Seaborn) · SQL  
**Fontes de dados:** Kaggle (dataset global) · UFABC / INEP (dados abertos)  
**Status:** 🔄 Em desenvolvimento

---

## Sobre o projeto

Este projeto parte de uma pergunta simples com uma resposta mais complexa do que parece:
**o que realmente impacta o desempenho acadêmico de um estudante?**

A análise é estruturada em dois eixos complementares:

1. **Dataset global (Kaggle):** 200 mil registros com variáveis comportamentais — horas de sono, uso de redes sociais, streaming, saúde mental, frequência e nota no exame. Permite identificar padrões comportamentais associados ao desempenho.

2. **Dados reais da UFABC (dados abertos):** indicadores institucionais de evasão, perfil discente e desempenho acadêmico da própria universidade onde este projeto foi desenvolvido. Permite contrastar os padrões globais com uma realidade local conhecida de perto.

A motivação é pessoal e acadêmica: a UFABC tem um histórico documentado de evasão elevada — chegou a 46% nas primeiras turmas — e entender os fatores associados a isso é relevante tanto institucionalmente quanto para quem vive esse ambiente.

> 🇧🇷 Assim como os demais projetos deste portfólio, a documentação está em português por escolha deliberada de clareza e precisão técnica neste momento da formação.

---

## Perguntas norteadoras

### Sobre o comportamento individual (dataset Kaggle)
- Estudantes que dormem menos têm notas significativamente mais baixas?
- Qual variável comportamental tem maior correlação com desempenho — sono, redes sociais ou nível de estresse?
- Existe um "perfil de risco" identificável combinando múltiplos fatores?
- Os padrões variam por faixa etária ou nível educacional dos pais?

### Sobre o contexto institucional (dados UFABC / INEP)
- Como a taxa de evasão da UFABC evoluiu ao longo dos anos?
- Existem diferenças de evasão entre cursos ou turnos?
- Qual o perfil socioeconômico dos estudantes que evaderam vs. os que concluíram?
- O modelo de ciclos da UFABC (BC&T → curso específico) impacta os indicadores de conclusão?

### Integrando as duas perspectivas
- Os fatores comportamentais identificados globalmente têm correspondência nos indicadores institucionais da UFABC?
- O que os dados sugerem sobre políticas de permanência e apoio estudantil?

---

## Fontes de dados

| Fonte | Descrição | Acesso |
|-------|-----------|--------|
| [Kaggle — Student Academic Performance](https://www.kaggle.com/datasets/riteshswami08/student-academic-performance-and-behavioral-factor) | 200k registros com variáveis comportamentais e nota | Gratuito (login Kaggle) |
| [UFABC — Perfil Discente de Graduação](https://propladi.ufabc.edu.br/informacoes-institucionais/perfil-discente-gaduacao) | Microdados anuais do perfil dos estudantes, formato ODS | Aberto |
| [UFABC — Estatísticas Institucionais](https://dados.ufabc.edu.br/estatisticas) | Indicadores quantitativos de estrutura e desenvolvimento | Aberto (ODS) |
| [INEP — Censo da Educação Superior](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior) | Microdados nacionais filtráveis por instituição | Aberto |
| [Base dos Dados](https://basedosdados.org) | Censo da Educação Superior já tratado, acessível via Python/SQL | Gratuito (login Google) |

---

## Estrutura planejada do projeto

```
projeto-03-desempenho-academico/
├── README.md
├── data/
│   ├── raw/                  ← dados originais sem modificação
│   └── processed/            ← dados tratados prontos para análise
├── notebooks/
│   ├── 01_limpeza.ipynb      ← carregamento e tratamento dos dados
│   ├── 02_eda_global.ipynb   ← análise exploratória do dataset Kaggle
│   ├── 03_eda_ufabc.ipynb    ← análise dos dados institucionais da UFABC
│   └── 04_conclusoes.ipynb   ← síntese e comparação entre as perspectivas
└── queries/
    └── analises.sql          ← consultas SQL usadas na análise
```

---

## Metodologia prevista

1. **Coleta e limpeza** — download dos datasets, tratamento de nulos, padronização de tipos e categorias
2. **EDA dataset global** — distribuições, correlações, segmentações por perfil
3. **EDA dados UFABC/INEP** — evolução temporal da evasão, comparação entre cursos, perfil socioeconômico
4. **Análise comparativa** — o que os padrões globais dizem sobre o contexto local?
5. **Visualizações** — gráficos claros e interpretados, não apenas gerados

---

## Contexto: a evasão na UFABC

A UFABC adota um modelo curricular em dois ciclos — o estudante ingressa pelo BC&T (Bacharelado em Ciência e Tecnologia) ou BCS (Bacharelado em Ciências e Humanidades) e depois escolhe o curso de formação específica. Esse modelo foi criado justamente para reduzir a evasão causada pela escolha precoce de carreira.

Mesmo assim, a evasão histórica permaneceu alta. Entender se fatores comportamentais (sono, carga de trabalho, saúde mental) contribuem para esse quadro — e em que medida — é a pergunta central desta segunda parte da análise.

---

## Próximos passos

- [ ] Download e inspeção inicial do dataset Kaggle
- [ ] Coleta dos dados do Perfil Discente (Propladi/UFABC) e do Censo INEP
- [ ] Notebook de limpeza e padronização
- [ ] EDA exploratória do dataset global
- [ ] EDA dos dados institucionais da UFABC
- [ ] Síntese comparativa e visualizações finais
