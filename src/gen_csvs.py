# extract_import_export.py

import pandas as pd
from utils import load_config

def extract_importacao_petroleo():
    config = load_config()
    filepath = f"{config['paths']['data_raw']}/importacoes-exportacoes-b.xlsx"
    
    # Read entire sheet
    df_raw = pd.read_excel(filepath, header=None)
    
    # Find the row where 'Importação de petróleo - 2000-2025 (b)' appears in column B
    occurrences = []
    for idx, value in enumerate(df_raw[1]):
        if str(value).strip() == 'Importação de petróleo - 2000-2025 (b)':
            occurrences.append(idx)
    
    if len(occurrences) < 2:
        raise ValueError("Second occurrence of 'Importação de petróleo - 2000-2025 (b)' not found in column B.")
    
    start_search_row = occurrences[1] + 2  # 3 rows below the second occurrence should be "MÊS"
    
    # Find the row where column B == "MÊS"
    for idx in range(start_search_row, start_search_row + 10):  # Safe range
        #print(df_raw.at[idx, 1])
        if str(df_raw.at[idx, 1]).strip().upper() == "MÊS":
            header_row = idx
            break
    else:
        raise ValueError("'MÊS' row not found.")

    # Find last row ("Total do Ano")
    for idx in range(header_row, header_row + 100):  # search forward
        if str(df_raw.at[idx, 1]).strip().lower() == "total do ano":
            end_row = idx
            break
    else:
        raise ValueError("'Total do Ano' row not found.")

    # Find last column: should be the one with the current year
    current_year = pd.Timestamp.now().year
    last_col = None
    for col in range(2, df_raw.shape[1]):
        val = df_raw.at[header_row, col]
        if str(int(val)).strip() == str(current_year):
            last_col = col
            break
    if last_col is None:
        raise ValueError(f"Column with year {current_year} not found.")

    # Slice the DataFrame
    df_table = df_raw.iloc[header_row:end_row+1, 1:last_col+1]
    df_table.columns = df_table.iloc[0]  # Set headers
    df_table = df_table[1:]  # Drop the header row

    print(df_table)

    # Save as CSV
    output_path = f"{config['paths']['data_processed']}/importacao_petroleo_{current_year}.csv"
    df_table.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved to {output_path}")

def extract_dispendio_importacao_petroleo():
    config = load_config()
    filepath = f"{config['paths']['data_raw']}/importacoes-exportacoes-b.xlsx"
    
    # Read entire sheet
    df_raw = pd.read_excel(filepath, header=None)
    
    # Find the row where 'Dispêndio com a importação de petróleo - 2000-2025 (US$ FOB)' appears in column B
    occurrences = []
    for idx, value in enumerate(df_raw[1]):
        if str(value).strip() == 'Dispêndio com a importação de petróleo - 2000-2025 (US$ FOB)':
            occurrences.append(idx)
    
    if len(occurrences) < 2:
        raise ValueError("Second occurrence of 'Dispêndio com a importação de petróleo - 2000-2025 (US$ FOB)' not found in column B.")
    
    start_search_row = occurrences[1] + 2  # 3 rows below the second occurrence should be "MÊS"
    
    # Find the row where column B == "MÊS"
    for idx in range(start_search_row, start_search_row + 10):  # Safe range
        if str(df_raw.at[idx, 1]).strip().upper() == "MÊS":
            header_row = idx
            break
    else:
        raise ValueError("'MÊS' row not found.")

    # Find last row ("Total do Ano")
    for idx in range(header_row, header_row + 100):  # search forward
        if str(df_raw.at[idx, 1]).strip().lower() == "total do ano":
            end_row = idx
            break
    else:
        raise ValueError("'Total do Ano' row not found.")

    # Find last column: should be the one with the current year
    current_year = pd.Timestamp.now().year
    last_col = None
    for col in range(2, df_raw.shape[1]):
        val = df_raw.at[header_row, col]
        if str(int(val)).strip() == str(current_year):
            last_col = col
            break
    if last_col is None:
        raise ValueError(f"Column with year {current_year} not found.")

    # Slice the DataFrame
    df_table = df_raw.iloc[header_row:end_row+1, 1:last_col+1]
    df_table.columns = df_table.iloc[0]  # Set headers
    df_table = df_table[1:]  # Drop the header row

    # Save as CSV
    output_path = f"{config['paths']['data_processed']}/dispendio_importacao_petroleo_{current_year}.csv"
    df_table.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    extract_importacao_petroleo()
    extract_dispendio_importacao_petroleo()
