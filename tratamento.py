#%%
import pandas as pd
import numpy as np

df_2019 = pd.read_csv('./data/pib_2019.csv', encoding='latin-1')
df_atualizado = pd.read_excel('./data/data.xlsx')
#df_regiao = pd.read_csv('./data/Lista_Estados_Brasil_Versao_CSV.csv', encoding='latin-1')
# %%
df_atualizado_ = df_atualizado.iloc[1:28,:]
#df_atualizado_ = df_atualizado_.query('Territorialidades != "Distrito Federal"')

#%%
df_atualizado_2019 = df_atualizado_[['Territorialidades', 
                                    'Renda per capita 2019', 
                                    '% de extremamente pobres 2019', 
                                    'População total 2019', 
                                    'IDHM Educação 2019', 
                                    'IDHM Longevidade 2019',
                                    'IDHM Ajustado à Desigualdade 2019']]

df_atualizado_2020 = df_atualizado_[['Territorialidades', 
                                    'Renda per capita 2020', 
                                    '% de extremamente pobres 2020', 
                                    'População total 2020', 
                                    'IDHM Educação 2020', 
                                    'IDHM Longevidade 2020',
                                    'IDHM Ajustado à Desigualdade 2020']]

df_atualizado_2021 = df_atualizado_[['Territorialidades', 
                                    'Renda per capita 2021', 
                                    '% de extremamente pobres 2021', 
                                    'População total 2021', 
                                    'IDHM Educação 2021', 
                                    'IDHM Longevidade 2021',
                                    'IDHM Ajustado à Desigualdade 2021']]
#%%
import re
def corrige_colunas(col_name):
    new_col_name = re.sub(" \d+", " ", col_name)
    return new_col_name[0:(len(col_name)-1)].replace(' ', '_').lower()

# %%

df_atualizado_2019.columns = [corrige_colunas(col) for col in df_atualizado_2019.columns]
df_atualizado_2020.columns = [corrige_colunas(col) for col in df_atualizado_2020.columns]
df_atualizado_2021.columns = [corrige_colunas(col) for col in df_atualizado_2021.columns]

# %%

df_atualizado_2019 = df_atualizado_2019.merge(df_2019[['Region', 'Area', 'State']], left_on='territorialidade', right_on="State", how='left')
df_atualizado_2020 = df_atualizado_2020.merge(df_2019[['Region', 'Area', 'State']], left_on='territorialidade', right_on="State", how='left')
df_atualizado_2021 = df_atualizado_2021.merge(df_2019[['Region', 'Area', 'State']], left_on='territorialidade', right_on="State", how='left')

# %%

df_final = df_atualizado_2019.append(df_atualizado_2020, ignore_index = True)
df_final = df_final.append(df_atualizado_2021, ignore_index = True)

# %%

df_final.to_csv('data_modelagem.csv')