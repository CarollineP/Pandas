import pandas as pd
import os
from datetime import datetime

# Nome do arquivo CSV para armazenar os registros
csv_file = "registro_ponto.csv"

# Criar o arquivo CSV se não existir
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["TagID", "Nome", "CPF", "Entrada", "Saída", "Tempo Permanência"])
    df.to_csv(csv_file, index=False)

# Função para registrar entrada e saída
def registrar_ponto(tag_id, nome, cpf):
    # Carregar os dados do CSV
    df = pd.read_csv(csv_file)

    # Verifica se a pessoa já tem entrada registrada sem saída
    mask = (df["TagID"] == tag_id) & (df["Saída"].isna())

    if mask.any():
        # Registra saída e calcula tempo de permanência
        df.loc[mask, "Saída"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df["Tempo Permanência"] = pd.to_datetime(df["Saída"]) - pd.to_datetime(df["Entrada"])
        print(f"{nome} saiu. Tempo de permanência: {df.loc[mask, 'Tempo Permanência'].values[0]}")
    else:
        # Registra entrada
        novo_registro = pd.DataFrame([{
            "TagID": tag_id,
            "Nome": nome,
            "CPF": cpf,
            "Entrada": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Saída": None,
            "Tempo Permanência": None
        }])
        df = pd.concat([df, novo_registro], ignore_index=True)
        print(f"{nome} entrou às {novo_registro['Entrada'].values[0]}")

    # Salva no CSV
    df.to_csv(csv_file, index=False)

    # Exibir tabela formatada no terminal do VS Code
    print("\nTabela de Registros:\n")
    print(df.fillna("-"))  # Preencher NaN com "-"

# Simulação de leituras (substitua pelo código do seu RFID)
registrar_ponto("123456", "João Silva", "123.456.789-00")
registrar_ponto("987654", "Maria Souza", "987.654.321-00")
registrar_ponto("123456", "João Silva", "123.456.789-00")  # Passagem para saída
