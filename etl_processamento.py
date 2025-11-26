import pandas as pd
import os
import re  #<- Biblioteca de Expressões Regulares


def processar_dados():
    print("🔄 Iniciando processamento com REGEX...")

    # Primeiro passo: Carregar o arquivo .csv original
    nome_arquivo_entrada = 'GSE113690_Autism_16S_rRNA_OTU_assignment_and_abundance.csv'
    nome_arquivo_saida = 'dados_limpos_microbiota.csv'

    if not os.path.exists(nome_arquivo_entrada):
        print(f"❌ Erro: '{nome_arquivo_entrada}' não encontrado.")
        return

    #Leitura do arquivo CSV
    df = pd.read_csv(nome_arquivo_entrada)
    print(f"📂 Arquivo original lido: {len(df)} linhas.")

    print("🧬 Extraindo taxonomia...")

    #Segundo passo: Separar os metadados da Taxonomia
    def extrair_taxonomia_regex(tax_str):
        tax_str = str(tax_str)
        dados = {'Phylum': 'Não Identificado', 'Genus': 'Não Identificado'}

        #O Regex abaixo procura: "letra p ou g", seguido de "__", seguido de "qualquer coisa que não seja ;"
        #Isso ignora se tem underline antes (_p__) ou não (p__)

        #Busca FILO (p__)
        match_phylum = re.search(r'[p]__([^;]+)', tax_str)
        if match_phylum:
            valor = match_phylum.group(1).strip()
            # Limpa se vier escrito 'norank' ou estiver vazio
            if valor and 'norank' not in valor:
                dados['Phylum'] = valor

        #Busca GÊNERO (g__)
        match_genus = re.search(r'[g]__([^;]+)', tax_str)
        if match_genus:
            valor = match_genus.group(1).strip()
            if valor and 'norank' not in valor:
                dados['Genus'] = valor

        return pd.Series(dados)

    #Terceiro passo: Aplicar a função
    df_tax = df['taxonomy'].apply(extrair_taxonomia_regex)
    df = pd.concat([df, df_tax], axis=1)

    #Para teste: Mostra o que ele encontrou na primeira linha
    exemplo = df['Phylum'].iloc[0]
    print(f"📝 Teste de Extração (Linha 1): '{exemplo}'")

    #Verifica se o exemplo saiu como "Não identificado" ou "Outros", pois tive problema de extração anteriormente com isso.
    if exemplo == 'Não Identificado' or exemplo == 'Outros':
        print("⚠️ ALERTA: A extração falhou! Verifique o formato da coluna taxonomy.")
    else:
        print("✅ SUCESSO: Taxonomia extraída corretamente!")

    #Melt (Transformação)
    print("📊 Reorganizando tabela...")
    cols_meta = ['OTU', 'taxonomy', 'Phylum', 'Genus']
    cols_amostra = [c for c in df.columns if c not in cols_meta]

    df_long = df.melt(id_vars=['Phylum', 'Genus'],
                      value_vars=cols_amostra,
                      var_name='Sample_ID',
                      value_name='Abundance')

    #Classificação dos Grupos
    df_long['Group'] = df_long['Sample_ID'].apply(lambda x: 'TEA' if str(x).startswith('A') else 'Controle')

    #Remove zeros e salva
    df_final = df_long[df_long['Abundance'] > 0]
    df_final.to_csv(nome_arquivo_saida, index=False)
    print(f"💾 Arquivo salvo: {nome_arquivo_saida}")


if __name__ == '__main__':
    processar_dados()