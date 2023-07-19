import pandas as pd
import numpy as np
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder

def to_onehot(base: pd.DataFrame, cat_columns: np.array):
    """
    Esta função:
        - Transforma as colunas informadas em dummies one hot (sem excluir uma classe), ou seja, uma coluna para cada categoria.
    Dados de entrada:
                    - base: Dataframe (base de dados).
                    - cat_columns: Lista dos nomes das variáveis categóricas que serão transformadas em dummies.
    Dados de saída:
                    - DataFrame com as variáveis preparados para a modelagem.
    """
    
    one_hot_enc = make_column_transformer(
    (OneHotEncoder(handle_unknown = 'ignore'),
    cat_columns),
    
    remainder='passthrough')
    
    dados = one_hot_enc.fit_transform(base)
    base_onehot = pd.DataFrame(dados, columns=one_hot_enc.get_feature_names_out())
    
    return base_onehot

def to_dummies(cat_columns: np.array, covariaveis_data: pd.DataFrame, le):
    """
    Esta função:
        - Transforma as colunas informadas em dummie, ou seja, uma coluna para cada categoria.
        - Busca excluir a categoria menos informativa, aquela que contém Misto, Outro ou Não informado.   
    Dados de entrada:
                    - cat_columns: Lista dos nomes das variáveis categóricas que serão transformadas em dummies.
                    - covariaveis_data: DataFrame que contém todas as variáveis listadas em cat_columns.
                    - le: LabelEncoder função do Scikit Learn que transforma as variáveis em dummies.
    Dados de saída:
                    - DataFrame com as variáveis preparados para a modelagem.
    """
    for col in cat_columns:
        n = len(covariaveis_data[col].unique())
        if (n > 2):
            dummies = pd.get_dummies(covariaveis_data[col])
            if 'Não informado' in dummies.columns or 'Outro' in dummies.columns or 'Outros' in dummies.columns or 'Misto' in dummies.columns:
                for categorias_vazias in ['Não informado', 'Outro', 'Outros', 'Misto']:
                    indice = np.where(dummies.columns == categorias_vazias)
                    print(dummies.columns[indice])
                    if np.array(indice).size != 0:
                        dummies = dummies.drop(dummies.columns[indice], axis=1)
                        break
            else:
                dummies = dummies.drop(dummies.columns[0], axis=1)
            covariaveis_data[dummies.columns] = dummies
            covariaveis_data.drop(col, axis=1, inplace=True) 
        else:
            le.fit(covariaveis_data[col])
            covariaveis_data[col] = le.transform(covariaveis_data[col])
    return covariaveis_data

    