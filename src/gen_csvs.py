# extract_import_export.py

import pandas as pd
import os
from utils import load_config
import unicodedata
import re

def sanitize_filename(text):
    # Remove acentos
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore').decode('utf-8')
    
    # Substituir traços longos por hífens normais
    text = text.replace("–", "-").replace("—", "-")
    
    # Substituir espaços por underline
    text = text.replace(" ", "_")
    
    # Remover todos os caracteres especiais (exceto underscores e hífens)
    text = re.sub(r'[^\w\-]', '', text)
    
    # Evitar múltiplos underscores
    text = re.sub(r'_+', '_', text)
    
    # Remover underscores ou hífens no começo/final
    text = text.strip('_-')
    
    return text.lower()

def extract_table_by_title(title):
    config = load_config()
    filepath = os.path.join(config['paths']['data_raw'], 'importacoes-exportacoes-b.xlsx')
    df_raw = pd.read_excel(filepath, header=None)

    # 1. Encontrar a 2ª ocorrência do título na coluna B
    occurrences = [i for i, v in enumerate(df_raw[1]) if str(v).strip() == title]
    if len(occurrences) < 2:
        raise ValueError(f"Second occurrence of '{title}' not found.")
    title_row = occurrences[1]

    # 2. Encontrar linha do cabeçalho ("MÊS")
    for i in range(title_row + 2, title_row + 10):
        if str(df_raw.at[i, 1]).strip().upper() == "MÊS":
            header_row = i
            break
    else:
        raise ValueError("'MÊS' header row not found.")

    # 3. Encontrar última linha com "Total do Ano"
    for i in range(header_row, header_row + 100):
        if str(df_raw.at[i, 1]).strip().lower() == "total do ano":
            end_row = i
            break
    else:
        raise ValueError("'Total do Ano' row not found.")

    # 4. Encontrar última coluna com o ano atual
    current_year = pd.Timestamp.now().year
    for col in range(2, df_raw.shape[1]):
        val = df_raw.at[header_row, col]
        try:
            if int(val) == current_year:
                last_col = col
                break
        except:
            continue
    else:
        raise ValueError(f"Column with year {current_year} not found.")

    # 5. Pegar a tabela e renomear colunas
    df_table = df_raw.iloc[header_row:end_row+1, 1:last_col+1]
    df_table.columns = df_table.iloc[0]
    df_table = df_table[1:]

    # 6. Salvar em CSV
    safe_name = sanitize_filename(title)
    output_path = os.path.join(config['paths']['data_processed'], f"{safe_name}_{current_year}.csv")
    df_table.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"[✓] Saved: {output_path}")


def extract_table_by_indicator(indicator_title, excel_filename, output_name):
    config = load_config()
    filepath = os.path.join(config['paths']['data_raw'], excel_filename)

    # Leitura do arquivo Excel completo
    df_raw = pd.read_excel(filepath, header=None)

    # Buscar segunda ocorrência do título na coluna B
    occurrences = [i for i, val in enumerate(df_raw[1]) if str(val).strip() == indicator_title]
    if len(occurrences) < 2:
        raise ValueError(f"Second occurrence of '{indicator_title}' not found in column B.")

    start_search_row = occurrences[1] + 2  # MÊS deve estar logo abaixo

    # Encontrar a linha com o cabeçalho "MÊS"
    for idx in range(start_search_row, start_search_row + 10):
        val = str(df_raw.at[idx, 1]).strip().upper()
        if val == "MÊS":
            header_row = idx
            break
    else:
        raise ValueError("'MÊS' row not found after the indicator.")

    # Encontrar a última linha da tabela (linha com "Total do Ano")
    for idx in range(header_row, header_row + 100):
        val = str(df_raw.at[idx, 1]).strip().lower()
        if val == "total do ano":
            end_row = idx
            break
    else:
        raise ValueError("'Total do Ano' row not found after header.")

    # Determinar a última coluna (ano atual)
    current_year = pd.Timestamp.now().year
    last_col = None
    print(range(2, df_raw.shape[1]))
    for col in range(2, df_raw.shape[1]):
        try:
            val = str(int(df_raw.at[header_row, col])).strip()
            if val == str(current_year):
                last_col = col
                break
        except:
            continue
    if last_col is None:
        raise ValueError(f"Could not find column for current year ({current_year}).")

    # Extrair tabela
    df_table = df_raw.iloc[header_row:end_row+1, 1:last_col+1]
    df_table.columns = df_table.iloc[0]
    df_table = df_table[1:]

    # Salvar CSV
    clean_name = sanitize_filename(output_name)
    output_path = os.path.join(config['paths']['data_processed'], f"{clean_name}_{current_year}.csv")
    df_table.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved to {output_path}")


def extract_all():
    titles = [
        "Importação de petróleo - 2000-2025 (b)",
        "Dispêndio com a importação de petróleo - 2000-2025 (US$ FOB)",
        "Exportação de petróleo - 2000-2025 (b)",
        "Receita com a exportação de petróleo - 2000-2025 (US$ FOB)",
        "Importação de etanol anidro - 2012-2025 (b)",
        "Dispêndio com a importação de etanol anidro - 2012-2025 (US$ FOB)",
        "Importação de etanol hidratado - 2012-2025 (b)",
        "Dispêndio com a importação de etanol hidratado - 2012-2025 (US$ FOB)",
        "Exportação de etanol anidro - 2012-2025 (b)",
        "Receita com a exportação de etanol anidro - 2012-2025 (US$ FOB)",
        "Exportação de etanol hidratado - 2012-2025 (b)",
        "Receita com a exportação de etanol hidratado - 2012-2025 (US$ FOB)"
    ]
    for title in titles:
        try:
            extract_table_by_title(title)
        except Exception as e:
            print(f"[X] Failed for '{title}': {e}")

    extract_table_by_indicator(
        indicator_title="Produção nacional de petróleo por Unidade da Federação e localização (terra e mar) - 2000-2025 (b)",
        excel_filename="producao-petroleo-b.xls",
        output_name="producao nacional petroleo"
    )

    extract_table_by_indicator(
        indicator_title="Volume de petróleo refinado por refinaria e origem (nacional e importada) - 2000-2025 (b)",
        excel_filename="processamento-petroleo-b.xls",
        output_name="volume refinado por origem"
    )


if __name__ == "__main__":
    extract_all()
