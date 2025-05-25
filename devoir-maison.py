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


def conversion_en_date(df : pd.DataFrame, colonnedate : str = "Datetime", format_date : str="%Y-%m-%d %H:%M:%S") -> pd.DataFrame : 
    """Cette fonction a pour objectif de transformer la colonne datetime de notre fichier csv qui est à l'origine une chaine 
    de caractère en date réelle pour pouvoir ensuite l'utiliser dans un graphique matplotlib
    :param df: on prend le dataframe d'origine 
    :param colonnedate: la colonne du csv à convertir qui est égale à datetime qui est l'intitulé de la colonne où se trouvent les dates et les heures
    :param format_date: format de la date et des heures. %Y correspond aux années %m correspond aux mois %d correspond aux jours 
    %H correspond aux heures %M correspond aux minutes
    :return: retourne le nouveau dataframe avec la colonne convertie"""

    df_conversion = df.copy()

    df_conversion[colonnedate] = pd.to_datetime(df_conversion[colonnedate],format=format_date)

    return df_conversion


def tracer_vue_ensemble(df: pd.DataFrame,title: str = "Vue d'ensemble de la charge PJM en MW de 1998 à 2001", xlabel : str = "Date", ylabel : str = "MW") -> None:
    """Fonction pour tracer le graphique matplotlib de la vue d'ensemble de la charge PJM en MW de 1998 à 2001
    :param y: on met le MW
    :param title: titre du graphique 
    :param xlabel: libellé de l'axe x 
    :param ylabel: libellé de l'axe y
    :return: ici la fonction ne retourne rien (None)"""

    plt.figure(figsize=(8, 4))                 
    plt.plot(df["Datetime"], df["PJM_Load_MW"], lw=0.4)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(alpha=.3)
    plt.tight_layout()


def filtrer_par_date(df : pd.DataFrame, debut, fin) -> pd.DataFrame : 
    """L'objectif de cette fonction est de créer un nouveau dataframe qui filtre les dates en fonction des bornes de début et de fin
    :param: on prend le dataframe d'origine
    :param: la variable début qui contient la date à laquelle commence le datset
    :param: la variable fin qui contient la dernière date du dataset"""

    debut= pd.to_datetime(debut).date()
    fin = pd.to_datetime(fin).date()

    mask = (df["Datetime"].dt.date >= debut) & (df["Datetime"].dt.date <= fin)
    selection = df[mask].sort_values("Datetime") 

    return selection


def ajouter_colonne_saison(df : pd.DataFrame, saisons_selectionnees: list[str]) -> pd.DataFrame : 
    """L'objectif de cette fonction est de créer un nouveau dataframe qui va venir filtrer sur une liste de saisons. Cela permettra par la suite à l'appel de cette fonction
    de pouvoir se rendre compte des changements au niveau de la charge en fonction de la saisonnalité choisie. 
    :param df: on prend le dataframe d'origine 
    :return: retourne le nouveau dataframe filtré"""

    saison = {12:"Hiver", 1:"Hiver", 2:"Hiver",
              3:"Printemps", 4:"Printemps", 5:"Printemps",
              6:"Eté", 7:"Eté", 8:"Eté",
              9:"Automne", 10:"Automne", 11:"Automne"}
    
    df = df.copy()
    df["saison"] = df["Datetime"].dt.month.map(saison)
    mask = df["saison"].isin(saisons_selectionnees)     
    
    return df[mask].sort_values("Datetime")



def energie_journaliere(
    dataframe: pd.DataFrame,
    frequence: str = "D",                     # "D", "W" ou "M"
    colonnecharge: str = "PJM_Load_MW"
) -> pd.DataFrame:
    """
    Agrège l'énergie (somme des MW) sur la fréquence demandée.
    Retourne toujours un DataFrame avec deux colonnes :
        • 'date'          : début de la période
        • 'energie_MWh'   : somme des MW (≈ MWh)

    frequence :
        "D" → jour       (pas supplémentaire)
        "W" → semaine    (dimanche comme fin de semaine)
        "M" → mois       (fin de mois)
    """
    # ── 1) on part d'une copie pour ne pas toucher au DF original
    df = dataframe.copy()

    # ── 2) convertir en datetime si besoin puis créer 'date'
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df["date"] = df["Datetime"].dt.date       # YYYY-MM-DD (objet date)

    # ── 3) somme quotidienne (toujours nécessaire)
    daily = (
        df.groupby("date", as_index=False)[colonnecharge]
          .sum()
          .rename(columns={colonnecharge: "PJM_Load_MW"})
    )

    # ── 4) si "D" on s'arrête là
    if frequence == "D":
        return daily

    # ── 5) sinon on ré-agrège en semaine ou mois
    daily["date"] = pd.to_datetime(daily["date"])   # pour Grouper
    rule = "W-SUN" if frequence == "W" else "M"

    agg = (
        daily.groupby(pd.Grouper(key="date", freq=rule), as_index=False)
             ["PJM_Load_MW"].sum()
    )

    return agg


def tracer_energie_journaliere(df: pd.DataFrame, col: str = "PJM_Load_MW", title: str = "Énergie journalière (Σ 24 h)", xlabel: str = "Date",ylabel: str = "MWh") -> None:
    # 1) s’assurer que 'date' est bien un datetime64
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # 2) largeur de figure proportionnelle au nombre de barres
    fig_w = max(8, 0.04 * len(df))          # 0.04 → 1 pouce ≈ 2.5 cm pour 25 barres
    plt.figure(figsize=(fig_w, 4))

    # 3) bar-chart
    plt.bar(df["date"], df[col], width=0.8)

    # 4) titres & axes
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis="y", alpha=.3)








st.title("Dashboard consommation électrique")
df = lire_csv("PJM_Load_hourly.csv") 

df = conversion_en_date(df,colonnedate="Datetime",format_date="%Y-%m-%d %H:%M:%S")


st.title("Principaux indicateurs")
total = charge_totale(df)
moyenne = charge_moyenne(df)
pic = charge_maximale(df)
creux = charge_minimale(df)

col1, col2= st.columns(2)
col1.metric("⚡ Charge totale", f"{total:,.0f} MW")
col2.metric("⚡ Charge moyenne", f"{moyenne:,.0f} MW")
col3, col4 = st.columns(2)
col3.metric("⚡ Pic sur la période", f"{total:,.0f} MW")
col3.metric("⚡ Creux sur la période", f"{moyenne:,.0f} MW")


st.sidebar.title("Paramètres temporels")
min_day = df["Datetime"].min().date()
max_day = df["Datetime"].max().date()

debut = st.sidebar.date_input("Début", value=min_day, min_value=min_day, max_value=max_day)
fin   = st.sidebar.date_input("Fin", value=max_day, min_value=min_day, max_value=max_day) 
df_date = filtrer_par_date(df, debut, fin)


choix = st.sidebar.multiselect(
    "Saison(s) à afficher",
    ["Hiver", "Printemps", "Eté", "Automne"],
    default=["Hiver", "Printemps", "Eté", "Automne"]
)

df_filtre = ajouter_colonne_saison(df_date, choix)


st.title("Charge horaire PJM – vue d’ensemble")
tracer_vue_ensemble(df_filtre,title=f"PJM — {debut} → {fin}")  
st.pyplot(plt)  

daily_energy = energie_journaliere(df_filtre)

show_daily = st.sidebar.toggle("Afficher l’énergie journalière", value=False)

 # 1) granularité
label_freq = st.sidebar.radio(
        "Granularité du graphe",
        [("Jour", "D"), ("Semaine", "W"), ("Mois", "M")],
        horizontal=True,
        format_func=lambda x: x[0]
    )
freq = label_freq[1]                   # "D", "W" ou "M"

    # 2) calcule / ré-agrège en fonction du choix
daily_energy = energie_journaliere(df_filtre, frequence=freq)

    # 4) tracé toujours en barres
st.title(f"Énergie {label_freq[0].lower()} (Σ 24 h)")
tracer_energie_journaliere(
        daily_energy,
        col="PJM_Load_MW",                         # <— bon nom de colonne
        title=f"Énergie – {label_freq[0].lower()}"
    )
st.pyplot(plt)



st.title("Jeu de données d'origine")
st.dataframe(df, use_container_width=True)
