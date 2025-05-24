import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def lire_csv(filename: str) -> pd.DataFrame | None:
    """Pour commencer, on commence par créer une fonction qui va lire un fichier csv et renvoyer un
    dataframe, prêt à être utilisé dans streamlit pour être affiché.
    En cas de fichier introuvable, on lève une exception nommée FileNotFoundError
    :param filename: le nom du fichier que l'on souhaite lire
    :return: Si le nom du fichier spécifié existe, la fonction retourne le dataframe du fichier csv. 
    Si le nom du fichier spécifié n'existe pas, la fonction ne retourne rien (None) et on met un message d'erreur dans streamlit"""

    try:
        data = pd.read_csv(filename)
        return data
    except Exception as e:
        st.error(f"Fichier introuvable : {filename}")
        return None
    

def charge_totale(dataframe : pd.DataFrame) -> float:
    """Cette simple fonction sert à calculer la charge moyenne de la colonne PJM_Load_MW
    :param dataframe: le dataframe auquel applique à la colonne PJM_Load_MW la méthode mean (ne prend pas en compte les NaN)
    :return: retourne le résultat du calcul charge moyenne MW"""

    charge_totale_MW = dataframe["PJM_Load_MW"].sum()

    return charge_totale_MW
    

def charge_moyenne(dataframe : pd.DataFrame) -> float:
    """Cette simple fonction sert à calculer la charge moyenne de la colonne PJM_Load_MW
    :param dataframe: le dataframe auquel applique à la colonne PJM_Load_MW la méthode mean (ne prend pas en compte les NaN)
    :return: retourne le résultat du calcul charge moyenne MW"""

    charge_moyenne_MW = dataframe["PJM_Load_MW"].mean()

    return charge_moyenne_MW


def charge_maximale(dataframe : pd.DataFrame) -> float:
    """Cette simple fonction sert à calculer la charge moyenne de la colonne PJM_Load_MW
    :param dataframe: le dataframe auquel applique à la colonne PJM_Load_MW la méthode mean (ne prend pas en compte les NaN)
    :return: retourne le résultat du calcul charge moyenne MW"""

    charge_maximale_MW = dataframe["PJM_Load_MW"].max()

    return charge_maximale_MW


def charge_minimale(dataframe : pd.DataFrame) -> float:
    """Cette simple fonction sert à calculer la charge moyenne de la colonne PJM_Load_MW
    :param dataframe: le dataframe auquel applique à la colonne PJM_Load_MW la méthode mean (ne prend pas en compte les NaN)
    :return: retourne le résultat du calcul charge moyenne MW"""

    charge_minimale_MW = dataframe["PJM_Load_MW"].max()

    return charge_minimale_MW




st.title("Dashboard consommation électrique")
df = lire_csv("PJM_Load_hourly.csv") 

total = charge_totale(df)
moyenne = charge_moyenne(df)
pic = charge_maximale(df)
creux = charge_minimale(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("⚡ Charge totale", f"{total:,.0f} MW")
col2.metric("⚡ Charge moyenne", f"{moyenne:,.0f} MW")
col3.metric("⚡ Pic sur la période", f"{total:,.0f} MW")
col3.metric("⚡ Creux sur la période", f"{moyenne:,.0f} MW")




st.dataframe(df, use_container_width=True) 



