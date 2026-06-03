import tkinter as tk
from tkinter import messagebox, ttk
import joblib
import pandas as pd
from PIL import Image, ImageTk
import os
import sys

# ==============================================================================
# FUNÇÃO DE SUPORTE PARA PRODUÇÃO (GERAÇÃO DO .EXE)
# ==============================================================================
def resource_path(relative_path):
    """ Retorna o caminho correto para os arquivos (imagens/modelo), 
        funcionando tanto em desenvolvimento quanto dentro do .exe final. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ==============================================================================
# FUNÇÃO PRINCIPAL DE PREDIÇÃO
# ==============================================================================
def predict():
    try:
        gender_map = {"Masculino": 0, "Feminino": 1}
        binary_map = {"Não": 0, "Sim": 1}

        age_text = age_var.get().strip()
        if not age_text:
            raise ValueError("O campo 'Idade' não pode ficar vazio.")
        age_val = int(age_text)

        # Mapeamento exato das colunas na ordem do modelo
        expected_features = [
            'GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY',
            'PEER_PRESSURE', 'CHRONIC DISEASE', 'WHEEZING', 
            'ALCOHOL CONSUMING', 'COUGHING', 'SHORTNESS OF BREATH', 
            'SWALLOWING DIFFICULTY', 'CHEST PAIN'
        ]

        inputs = {
            'GENDER': gender_map[gender_combobox.get()],
            'AGE': age_val,
            'SMOKING': binary_map[smoking_combo.get()],
            'YELLOW_FINGERS': binary_map[yellow_fingers_combo.get()],
            'ANXIETY': binary_map[anxiety_combo.get()],
            'PEER_PRESSURE': binary_map[peer_pressure_combo.get()],
            'CHRONIC DISEASE': binary_map[chronic_disease_combo.get()],
            'WHEEZING': binary_map[wheezing_combo.get()],
            'ALCOHOL CONSUMING': binary_map[alcohol_consuming_combo.get()],
            'COUGHING': binary_map[coughing_combo.get()],
            'SHORTNESS OF BREATH': binary_map[shortness_breath_combo.get()],
            'SWALLOWING DIFFICULTY': binary_map[swallowing_difficulty_combo.get()],
            'CHEST PAIN': binary_map[chest_pain_combo.get()],
        }

        input_df = pd.DataFrame([inputs])[expected_features]
                
        # Carrega o modelo de produção
        model = joblib.load(resource_path('especialista_em_cancer.pkl'))

        # Executa a classificação
        prediction = model.predict(input_df)[0]

        # Tratamento da resposta do modelo (1 = Risco Detectado / 0 = Não Detectado)
        result = "SIM (Risco Detectado)" if prediction == 1 else "NÃO (Risco Não Detectado)"
        
        messagebox.showinfo("Resultado da Análise", f"Resultado do Modelo: {result}\n\nNota: Este é um modelo preditivo de estudo e não substitui diagnósticos médicos.")

    except ValueError as ve:
        messagebox.showerror("Erro de Entrada", f"Por favor, verifique os campos.\n{ve}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")


# ==============================================================================
# CONFIGURAÇÕES DA JANELA PRINCIPAL (DIMENSÕES PERSONALIZADAS 1200x700)
# ==============================================================================
root = tk.Tk()
root.title("Especialista CP - Dashboard Avançado de Predição")
root.geometry("1200x700") 
root.configure(bg="#121214") 
root.resizable(False, False)

# Configurando estilos modernos para os componentes do ttk
style = ttk.Style()
style.theme_use('default')

style.configure('TCombobox', fieldbackground='#202024', background='#202024', foreground='#ffffff', borderwidth=0, arrowcolor='#00f3ff')
style.map('TCombobox', fieldbackground=[('readonly', '#202024')], foreground=[('readonly', '#ffffff')])
style.configure('TEntry', fieldbackground='#202024', foreground='#ffffff', borderwidth=0, relief='flat')

# Ícone do App
try:
    icone = Image.open(resource_path("edson_desenvolvedor.ico"))
    icone_tk = ImageTk.PhotoImage(icone)
    root.iconphoto(False, icone_tk)
except Exception:
    pass

# ==============================================================================
# ESTRUTURA DE LAYOUT (SIDEBAR + MAIN CONTENT)
# ==============================================================================

# 1. Painel Lateral (Sidebar)
sidebar = tk.Frame(root, bg="#1c1c1e", width=280)
sidebar.pack(side="left", fill="y", padx=(0, 2))
sidebar.pack_propagate(False)

sidebar_title = tk.Label(sidebar, text="SISTEMA MED-AI", font=("Segoe UI", 16, "bold"), bg="#1c1c1e", fg="#00f3ff")
sidebar_title.pack(pady=(40, 5))

sidebar_subtitle = tk.Label(sidebar, text="Módulo Pulmonar v2.0", font=("Segoe UI", 9), bg="#1c1c1e", fg="#7c7c8a")
sidebar_subtitle.pack(pady=(0, 40))

status_frame = tk.Frame(sidebar, bg="#202024", padx=15, pady=15)
status_frame.pack(fill="x", padx=20)

status_lbl = tk.Label(status_frame, text="Status do Modelo:", font=("Segoe UI", 10, "bold"), bg="#202024", fg="#e1e1e6")
status_lbl.pack(anchor="w")
status_val = tk.Label(status_frame, text="● PRONTO PARA OPERAR", font=("Segoe UI", 9), bg="#202024", fg="#04d361")
status_val.pack(anchor="w", pady=(5, 0))

# 2. Painel de Conteúdo Principal
main_panel = tk.Frame(root, bg="#121214", padx=30, pady=30)
main_panel.pack(side="right", fill="both", expand=True)

title_label = tk.Label(main_panel, text="Ficha Clínica Digital do Paciente", font=("Segoe UI", 18, "bold"), bg="#121214", fg="#ffffff")
title_label.pack(anchor="w", pady=(0, 5))

subtitle_label = tk.Label(main_panel, text="Preencha os blocos abaixo com as respostas dos exames e anamnese.", font=("Segoe UI", 10), bg="#121214", fg="#7c7c8a")
subtitle_label.pack(anchor="w", pady=(0, 25))

# Container Geral dos Blocos de Entrada
form_container = tk.Frame(main_panel, bg="#121214")
form_container.pack(fill="both", expand=True)

age_var = tk.StringVar()

# Funções auxiliares para criar cartões estruturados no layout expandido
def criar_card_campo(parent, label_text, widget_type="combo", var_reference=None):
    frame_campo = tk.Frame(parent, bg="#1c1c1e", pady=8, padx=10)
    frame_campo.pack(fill="x", pady=5)
    
    lbl = tk.Label(frame_campo, text=label_text, font=("Segoe UI", 10), bg="#1c1c1e", fg="#e1e1e6")
    lbl.pack(side="left")
    
    frame_widget = tk.Frame(frame_campo, bg="#202024", padx=5, pady=2)
    frame_widget.pack(side="right")
    
    if widget_type == "combo":
        cb = ttk.Combobox(frame_widget, width=12, font=("Segoe UI", 10), state="readonly")
        cb.pack()
        return cb
    else:
        entry = ttk.Entry(frame_widget, textvariable=var_reference, width=14, font=("Segoe UI", 10))
        entry.pack()
        return entry

# --- BLOCO 1: DADOS BÁSICOS E HÁBITOS (Esquerda) ---
card_esquerda = tk.LabelFrame(form_container, text=" Dados Demográficos e Hábitos ", font=("Segoe UI", 10, "bold"), bg="#121214", fg="#00f3ff", padx=15, pady=15)
card_esquerda.pack(side="left", fill="both", expand=True, padx=(0, 15))

gender_combobox = criar_card_campo(card_esquerda, "Gênero Biológico:")
gender_combobox['values'] = ("Masculino", "Feminino")
gender_combobox.current(0)

age_entry = criar_card_campo(card_esquerda, "Idade Cronológica:", widget_type="entry", var_reference=age_var)
smoking_combo = criar_card_campo(card_esquerda, "Histórico de Tabagismo:")
alcohol_consuming_combo = criar_card_campo(card_esquerda, "Consumo Frequente de Álcool:")
peer_pressure_combo = criar_card_campo(card_esquerda, "Exposição à Pressão Social:")

# --- BLOCO 2: ANAMNESE E SINTOMAS (Direita) ---
card_direita = tk.LabelFrame(form_container, text=" Sintomas e Condições Clínicas ", font=("Segoe UI", 10, "bold"), bg="#121214", fg="#00f3ff", padx=15, pady=15)
card_direita.pack(side="right", fill="both", expand=True)

yellow_fingers_combo = criar_card_campo(card_direita, "Sinal de Dedos Amarelados:")
anxiety_combo = criar_card_campo(card_direita, "Crises de Ansiedade Relatadas:")
chronic_disease_combo = criar_card_campo(card_direita, "Possui Outra Doença Crônica:")
wheezing_combo = criar_card_campo(card_direita, "Chiado/Sons ao Respirar:")
coughing_combo = criar_card_campo(card_direita, "Crises de Tosse Persistente:")
shortness_breath_combo = criar_card_campo(card_direita, "Falta de Ar (Dispneia):")
swallowing_difficulty_combo = criar_card_campo(card_direita, "Dificuldade de Deglutição:")
chest_pain_combo = criar_card_campo(card_direita, "Dor Torácica Constante:")

# Definindo valores padrão das caixas de seleção
todos_sintomas = [
    smoking_combo, yellow_fingers_combo, anxiety_combo, peer_pressure_combo,
    chronic_disease_combo, wheezing_combo, alcohol_consuming_combo, coughing_combo,
    shortness_breath_combo, swallowing_difficulty_combo, chest_pain_combo
]
for combo in todos_sintomas:
    combo['values'] = ("Não", "Sim")
    combo.current(0)

# ==============================================================================
# ÁREA DE PROMOÇÃO DA PREDIÇÃO (BOTÃO AMPLIADO)
# ==============================================================================
action_frame = tk.Frame(main_panel, bg="#121214", pady=20)
action_frame.pack(fill="x", side="bottom")

predict_button = tk.Button(
    action_frame, 
    text="ANLISAR DADOS E GERAR DIAGNÓSTICO", 
    command=predict,
    font=("Segoe UI", 11, "bold"),
    bg="#00f3ff", 
    fg="#121214",
    activebackground="#00b8c4",
    activeforeground="#121214",
    bd=0,
    cursor="hand2",
    padx=30,
    pady=12
)
predict_button.pack(side="right")

# Imagem Corporativa no Rodapé do Sidebar (Ajustada para o menu lateral)
try:
    img_pil = Image.open(resource_path("edson_desenvolvedor.png"))
    img_pil = img_pil.resize((240, 50), Image.Resampling.LANCZOS)
    imagem_footer = ImageTk.PhotoImage(img_pil)
    
    footer_label = tk.Label(sidebar, image=imagem_footer, bg="#1c1c1e", bd=0, highlightthickness=0)
    footer_label.image = imagem_footer
    footer_label.pack(side="bottom", pady=20)
except Exception:
    fallback_footer = tk.Label(sidebar, text="EDSON DESENVOLVEDOR", font=("Segoe UI", 8, "bold"), bg="#1c1c1e", fg="#4d4d56")
    fallback_footer.pack(side="bottom", pady=20)

root.mainloop()