# Tempo de tela, estresse e sono: uma análise exploratória de dados

**Área:** Saúde digital · Comportamento · Bem-estar  
**Ferramentas:** Python (Pandas, NumPy, Matplotlib) · SQL · Power BI *(em desenvolvimento)*  
**Status:** 🔄 Em desenvolvimento

---

## Objetivo

Investigar se o aumento do uso diário de smartphones está associado a maiores níveis de estresse percebido e menor duração do sono. O foco está em identificar **correlações e padrões nos dados** — não em estabelecer relações causais.

**Perguntas norteadoras:**
- Usuários com mais horas de tela dormem menos?
- Maior tempo de tela está associado a níveis de estresse mais altos?
- Esses padrões variam por ocupação, faixa etária ou sistema operacional?

---

## Sobre o dataset

- **Fonte:** Dataset público disponível no Kaggle
- **Volume:** 50.000 registros de usuários
- **Variáveis principais:** tempo de tela diário (h), duração do sono (h), nível de estresse (0–10), produtividade (0–10), ocupação, faixa etária, sistema operacional

---

## Estrutura do projeto

```
projeto-01-tempo-de-tela/
├── README.md                        ← este arquivo
├── dataset.ipynb                    ← carregamento e limpeza dos dados
├── exploration data analysis.ipynb  ← análise exploratória e visualizações
└── queries.sql                      ← consultas SQL usadas na análise ⚠️ (a extrair do notebook)
```

> ⚠️ **Nota:** as queries SQL ainda estão incorporadas no notebook de análise. A extração para um arquivo `.sql` separado está pendente.

---

## Metodologia

1. **Carregamento e limpeza dos dados** — tratamento de valores ausentes e outliers
2. **Análise Exploratória de Dados (EDA)** — distribuições, médias, comparações por grupo
3. **Análise de correlação** — entre tempo de tela, sono, estresse e produtividade
4. **Consultas SQL** — agregações e detecção de padrões por segmento
5. **Visualização e dashboard** — Power BI *(em desenvolvimento)*

---

## Principais resultados

| Métrica | Valor |
|---|---|
| Usuários analisados | 50.000 |
| Idade média | 39,0 anos |
| Uso médio diário de tela | 6,5 h |
| Duração média do sono | 6,5 h |
| Usuários que dormem menos de 7h | 59,0% |
| Nível médio de estresse | 5,5 / 10 |
| Produtividade média | 5,5 / 10 |
| Correlação sono × produtividade | 0,003 |
| Correlação estresse × produtividade | 0,010 |

### Tabelas de Visualização

<img width="805" height="260" alt="PDU" src="https://github.com/user-attachments/assets/244c5a09-c3f2-4d21-b578-b0888ca847b9" />
<img width="732" height="260" alt="IUS" src="https://github.com/user-attachments/assets/bc5513d1-c89f-4e5c-b57b-4e628ecbe0ad" />



### Interpretação

As correlações encontradas entre sono e produtividade (0,003) e entre estresse e produtividade (0,010) são **próximas de zero**, indicando ausência de relação linear expressiva neste dataset. Isso não significa que essas variáveis não se relacionam na realidade — mas sim que, nos dados analisados, essa relação não aparece de forma linear e direta.

Outros achados relevantes:
- O tempo médio de uso (~6,5 h/dia) é consistente entre diferentes ocupações, sugerindo um padrão de consumo digital generalizado
- A distribuição entre Android e iOS é equilibrada, sem diferença notável nos padrões de uso
- O comportamento digital entre dias de semana e fins de semana não apresenta variação expressiva

### Limitações
- Dataset sintético/público: os dados podem não refletir comportamentos reais com fidelidade
- Correlação linear não captura relações mais complexas entre as variáveis
- Ausência de dados longitudinais: não é possível avaliar mudanças ao longo do tempo

---

## Próximos passos

- [ ] Extrair queries SQL para arquivo `.sql` separado
- [ ] Finalizar dashboard no Power BI
- [ ] Adicionar visualizações mais detalhadas por faixa etária e ocupação
- [ ] Explorar análises não-lineares entre as variáveis

---
