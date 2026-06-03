import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. CARREGAMENTO DOS DADOS
print("Carregando os dados...")
df = pd.read_csv("survey_lung_cancer.csv")

# Limpar espaços em branco extras nos nomes das colunas
df.columns = df.columns.str.strip()

# 2. PRÉ-PROCESSAMENTO (Tratamento de variáveis categóricas)
print("Pré-processando as variáveis...")

# O dataset original costuma usar 2 para SIM e 1 para NÃO em colunas sintomáticas.
# Vamos mapear o GENDER e a meta LUNG_CANCER, e garantir que as outras fiquem em formato 0 e 1.
le_gender = LabelEncoder()
df['GENDER'] = le_gender.fit_transform(df['GENDER']) # MALE/FEMALE -> 1/0

le_target = LabelEncoder()
df['LUNG_CANCER'] = le_target.fit_transform(df['LUNG_CANCER']) # YES/NO -> 1/0

# Se as colunas de sintomas utilizarem 1 e 2, vamos normalizar para 0 and 1
for col in df.columns:
    if col not in ['GENDER', 'AGE', 'LUNG_CANCER']:
        # Se os valores forem [1, 2], transforma o 1 em 0 e o 2 em 1
        if df[col].max() == 2:
            df[col] = df[col].replace({1: 0, 2: 1})

# Separando preditores (X) e o alvo (y)
X = df.drop(columns=['LUNG_CANCER'])
y = df['LUNG_CANCER']

# 3. DIVISÃO EM TREINO E TESTE
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. TREINAMENTO DO MODELO
print("Treinando o modelo Random Forest...")
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# 5. AVALIAÇÃO DO MODELO
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n=== DESEMPENHO DO MODELO ===")
print(f"Acurácia Geral: {accuracy:.2%}")
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred, target_names=le_target.classes_))

# 6. SALVAR O MODELO PARA PRODUÇÃO (EXPORTAÇÃO)
print("\nExportando o modelo e os transformadores para produção...")

# Criamos uma pasta para os artefatos de produção se não existir
os.makedirs("production_model", exist_ok=True)

# Salvamos o modelo treinado
joblib.dump(model, "production_model/lung_cancer_model.pkl")
# Salvamos os encoders para garantir que a entrada em produção seja tratada igual
joblib.dump(le_gender, "production_model/le_gender.pkl")
joblib.dump(le_target, "production_model/le_target.pkl")
# Salvamos a lista de colunas para validação de schema em produção
joblib.dump(list(X.columns), "production_model/model_features.pkl")

print("Sucesso! Todos os arquivos foram salvos na pasta 'production_model/'.")