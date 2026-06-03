# 🩺 Projeto Software com Aprendizagem de Máquina para Predição de Câncer de Pulmão

O **projeto-software-com-aprendizagem-de-maquina** é uma solução completa que engloba desde a análise estatística de dados clínicos até a criação de um software desktop especializado com interface gráfica e inteligência artificial embarcada para apoiar triagens preliminares de risco de câncer de pulmão.

---

## 🚀 Funcionalidades do Ecossistema

- **Pipeline Automatizada:** Identificação automática se o problema é de classificação ou regressão baseada no comportamento do alvo (*target*).
- **Modelo de Alta Performance:** Uso do algoritmo ensemble `VotingClassifier` / `VotingRegressor` unindo múltiplos modelos matemáticos para maximizar o acerto.
- **Interface Gráfica Industrial:** Software responsivo desenhado em modo escuro (*Dark Mode*), com resolução otimizada de `1200x700` estruturado em blocos de exames.
- **Pronto para Produção:** Mecanismo de persistência que gera executáveis (.exe) isolados sem dependência de instalação local de interpretadores Python.

---

## 📂 Arquitetura da Pipeline de Dados e Treinamento

O core intelligence do projeto consiste em uma esteira estruturada em 9 etapas sequenciais:

### 1. Importação de Bibliotecas
Ambiente construído sob o ecossistema científico do Python:
- Manipulação e Álgebra: `pandas`, `numpy`
- Visualização de Dados: `matplotlib`
- Aprendizado de Máquina: `scikit-learn` (modelos preditivos e métricas)

### 2. Carregamento e Seleção de Atributos
Leitura do arquivo `survey_lung_cancer.csv` isolando especificamente 14 variáveis clínicas estruturais fundamentais para correlação diagnóstica.

### 3. Codificação de Variáveis Categóricas (*Encoding*)
Uso de `LabelEncoder` para transformar strings como gêneros (`MALE`/`FEMALE`) e alvos (`YES`/`NO`) em representações matemáticas binárias discretas ($0$ e $1$).

### 4. Análise Estatística de Correlação
Cálculo de Matriz de Correlação de Pearson focado em mensurar o impacto direto de características como `SMOKING`, `AGE` e `CHRONIC DISEASE` em relação ao surgimento da patologia.

### 5. Divisão de Amostragem (*Holdout*)
Segmentação da base histórica em dados de **Treino (80%)** para o aprendizado e dados de **Teste (20%)** para validação estatística, mitigando riscos de *overfitting*.

### 6. Identificação Dinâmica de Escopo
O algoritmo avalia o volume de classes únicas no alvo:
- Se $\le 10$ classes: Configura automaticamente arquitetura de **Classificação** (Métrica: *Accuracy*).
- Se $> 10$ classes: Configura automaticamente arquitetura de **Regressão** (Métrica: *RMSE*).

### 7. Treinamento Baseado em Comitê (*Ensemble*)
Em vez de depender de um único algoritmo, o sistema instancia um modelo baseado em votação, agregando:
- Regressão Logística / Linear
- Árvores de Decisão (*Decision Trees*)
- Florestas Aleatórias (*Random Forest*)
- K-Vizinhos Próximos (*KNN*)

### 8. Persistência de Modelo
Após a validação da melhor acurácia, o comitê treinado é serializado e exportado em formato binário encapsulado como `especialista_em_cancer.pkl`.

---

## 🖥️ O Software Desktop (Interface Gráfica)

O sistema de produção carrega o arquivo serializado e renderiza uma interface de nível corporativo para profissionais da saúde ou pesquisadores.

![especialista](https://github.com/user-attachments/assets/fb635321-39c7-4ace-9ca4-c9a28493a3c2)

### Características da Interface:
1. **Ficha Clínica Digital:** Menus suspensos interativos (*Comboboxes*) que padronizam a entrada dos sintomas impedindo que o usuário digite valores fora do padrão esperado pela inteligência artificial.
2. **Dashboard Otimizado:** Desenvolvido nas dimensões `1200x700`, dividindo as informações visualmente entre dados de hábitos diários e sinais clínicos biológicos observados.
3. **Tratamento de Exceções Activo:** Validações em tempo real para campos vazios ou formatos de idades incorretos, prevenindo que o sistema sofra travamentos abruptos.

---

## 🔄 Fluxo de Operação do Usuário