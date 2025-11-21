import pandas as pd
import numpy as np

def processar_dados():
    print("Iniciando processamento de dados...")

    #Primeiro passo: Carregar o arquivo .csv original
    nome_arquivo = "GSE113690_Autism_16S_rRNA_OTU_assignment_and_abundance.csv"

    try:
        df = pd.read_csv(nome_arquivo)
        print(f"Arquivo {nome_arquivo} carregado com sucesso!")
    except FileNotFoundError:
        print(f"Erro. Arquivo {nome_arquivo} não encontrado.")
        return

    #Segundo passo: Separar os metadados da Taxonomia
    print("Extraindo taxonomia...")

    def extrair_taxonomia(tax_str):
        partes = str(tax_str).split(';')
        dados = {'Phylum': 'Outros', 'Genus': 'Outros'}
        for parte in partes:
            parte = parte.strip()
            if parte.startswith('p__'):
                dados['Phylum'] = parte.split('__')[1]
                #Limpeza extra caso esteja vazio ou "norank"
                if not dados['Phylum'] or dados['Phylum'] == 'norank':
                    dados['Phylum'] = 'Não identificado'
            if parte.startswith('g__'):
                dados['Genus'] = parte.split('__')[1]
                if not dados['Genus'] or dados['Genus'] == 'norank':
                    dados['Genus'] = 'Não identificado'
        return pd.Series(dados)

    df_tax = df['taxonomy'].apply(extrair_taxonomia)
    df = pd.concat([df, df_tax], axis = 1)

    #Terceiro passo: Transformar de Wide para LONG (Melt)
    print(f"Reorganizando a tabela (Pivot/Melt)...")

    colunas_metadados = ['OTU', 'taxonomy', 'Phylum', 'Genus']
    #Pega todas as colunas que não são metadados (ou seja, amostras A1, A2, B1...)
    colunas_amostras = [c for c in df.columns if c not in colunas_metadados]

    df_long = df.melt(id_vars = ['Phylum', 'Genus'], value_vars = colunas_amostras, var_name = 'Sample_ID', value_name = 'Abundance')

    #Quarto passo: Criar a coluna de Grupo
    #A = TEA (Autismo), B Controle (Neurotípico)
    df_long['Group'] = df_long['Sample_ID'].apply(lambda x: 'TEA' if str(x).startswith('A') else 'Controle')

    #Quinto e último passo: Realizar a limpeza final. Remover amostras com abundância 0 para deixar o arquivo mais leve e rápido
    df_final = df_long[df_long['Abundance'] > 0]

    print(f"Salvando arquivo final com {len(df_final)} linhas...")
    df_final.to_csv('dados_limpos_microbiota.csv', index = False)
    print(f"Sucesso!!! Arquivo 'dados_limpos_microbiota.csv' criado!")

if __name__ == '__main__':
    processar_dados()