import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------------------------------------------------------------
#                                         Fonction de lecture du jeu de données 
# --------------------------------------------------------------------------------------------------------------------------------

def lire_csv(filename: str) -> pd.DataFrame | None :
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


# --------------------------------------------------------------------------------------------------------------------------------
#                                         Fonction de calcul de la charge totale
# --------------------------------------------------------------------------------------------------------------------------------  

def charge_totale(dataframe_total : pd.DataFrame) -> float :
    """L'objectif de cette fonction est de calculer la charge totale sur toute la période de notre jeu de donnée (1998 à 2002)
    :param dataframe_total: le dataframe auquel on applique à la colonne PJM_Load_MW la méthode mean (ne prend pas en compte les NaN)
    :return: retourne le résultat du calcul charge moyenne MW"""

    charge_totale_MW = dataframe_total["PJM_Load_MW"].sum()
    return charge_totale_MW


# --------------------------------------------------------------------------------------------------------------------------------
#                                         Fonction de calcul de la charge moyenne
# --------------------------------------------------------------------------------------------------------------------------------  

def charge_moyenne(dataframe_moy : pd.DataFrame) -> float:
    """L'objectif de cette fonction est de calculer la charge moyenne sur toute la période de notre jeu de donnée (1998 à 2002)
    :param dataframe_moy: le dataframe auquel on applique à la colonne PJM_Load_MW la méthode mean (ne prend pas en compte les NaN)
    :return: retourne le résultat du calcul charge moyenne MW"""

    charge_moyenne_MW = dataframe_moy["PJM_Load_MW"].mean()
    return charge_moyenne_MW


# --------------------------------------------------------------------------------------------------------------------------------
#                                         Fonction de calcul de la charge maximale
# -------------------------------------------------------------------------------------------------------------------------------- 

def charge_maximale(dataframe_pic : pd.DataFrame) -> float:
    """L'objectif de cette fonction est de calculer la charge maximale, en d'autre terme le pic de charge sur toute la période de notre jeu de donnée (1998 à 2002)
    :param dataframe_pic: le dataframe auquel on applique à la colonne PJM_Load_MW la méthode mean (ne prend pas en compte les NaN)
    :return: retourne le résultat du calcul charge moyenne MW"""

    charge_maximale_MW = dataframe_pic["PJM_Load_MW"].max()
    return charge_maximale_MW


# --------------------------------------------------------------------------------------------------------------------------------
#                                         Fonction de calcul de la charge minimale
# -------------------------------------------------------------------------------------------------------------------------------- 

def charge_minimale(dataframe_creux : pd.DataFrame) -> float:
    """L'objectif de cette fonction est de calculer  la charge minimale, en d'autre terme, le creux de charge sur toute la période de notre jeu de donnée (1998 à 2002)
    :param dataframe_creux: le dataframe auquel on applique à la colonne PJM_Load_MW la méthode mean (ne prend pas en compte les NaN)
    :return: retourne le résultat du calcul charge moyenne MW"""

    charge_minimale_MW = dataframe_creux["PJM_Load_MW"].min()
    return charge_minimale_MW


# --------------------------------------------------------------------------------------------------------------------------------
#                                         Fonction de conversion en type Datetime
# -------------------------------------------------------------------------------------------------------------------------------- 

def conversion_en_date(dataframe_a_convertir : pd.DataFrame, format_date : str="%Y-%m-%d %H:%M:%S") -> pd.DataFrame : 
    """Cette fonction a pour objectif de transformer la colonne datetime de notre fichier csv en type datetime pour pouvoir ensuite l'utiliser dans un graphique matplotlib
    :param dataframe_a_convertir: DataFrame d’origine contenant une colonne nommée Datetime dont les valeurs sont des chaînes représentant une date et une heure.
    :param format_date: Spécifie la structure des dates/heures dans la colonne. %Y correspond aux années %m correspond aux mois %d correspond aux jours 
    %H correspond aux heures %M correspond aux minutes
    :return: retourne le nouveau dataframe avec la colonne convertie"""

    #Je ne veux pas modifier directement le dataframe d'origne (dataframe_a_convertir) pour éviter d'altérer les données d'origine, donc je fais une copie du dataframe d'origine.
    df_conversion = dataframe_a_convertir.copy()
    df_conversion["Datetime"] = pd.to_datetime(df_conversion["Datetime"],format=format_date)
    return df_conversion


# --------------------------------------------------------------------------------------------------------------------------------
#                               Fonction de conversion pour préparation de la date en semaine
# -------------------------------------------------------------------------------------------------------------------------------- 

def preparation_date_en_semaine(dataframe_prepa_semaine: pd.DataFrame) -> pd.DataFrame : 
    """L'objectif de la fonction est de convertir df["Datetime"] au type datetime64 et de créer une nouvelle colonne intitulé jour_semaine qui regroupera les jours de la semaine
    :param dataframe_prepa_semaine: DataFrame comprenant obligatoirement Datetime convertible en type datetime
    :return: Le même DataFrame **avec deux garanties : Datetime est bien au type datetime et une colonne jour_semaine a été ajoutée."""
    
    dataframe_prepa_semaine["Datetime"] = pd.to_datetime(df["Datetime"])
    df["jour_semaine"] = dataframe_prepa_semaine["Datetime"].dt.day_name()
    return df


# --------------------------------------------------------------------------------------------------------------------------------
#                               Fonction pour tracer le premier graphique - vue d'ensemble
# -------------------------------------------------------------------------------------------------------------------------------- 

def tracer_vue_ensemble(dataframe_pour_vue_ensemble: pd.DataFrame,title: str = "Vue d'ensemble de la charge PJM en MW de 1998 à 2001", xlabel : str = "Date", ylabel : str = "charge en MW") -> None:
    """L'objectif de cette fonction est de s'occuper de la partie traçage du graphique contenue dans une dataframe qui montre une vue d'ensemble de la charge PJM en MW de 1998 à 2001
    :param dataframe_pour_vue_ensemble: le dataframe devant contenir les informations nécessaire à la construction de notre graphique (ici des dates et la charge en megaWatts)
    :param y: on place sur cette axe y les valeurs de la colonne PJM_Load_MW
    :param title: titre du graphique 
    :param xlabel: libellé de l'axe x, à savoir la date
    :param ylabel: libellé de l'axe y, à savoir la charge en MW
    :return: La fonction ne renvoie rien, elle crée la figure Matplotlib et l’affiche dans l'application streamlit à son appel"""

    plt.figure(figsize=(8, 4))                 
    plt.plot(dataframe_pour_vue_ensemble["Datetime"], dataframe_pour_vue_ensemble["PJM_Load_MW"], lw=0.4) # je rend la ligne plus fine avec line width (lw) car sinon le graphique n'est pas très lisible...
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
   
 

# --------------------------------------------------------------------------------------------------------------------------------
#                     Fonction pour tracer le deuxième graphique - distribution de la charge électrique
# -------------------------------------------------------------------------------------------------------------------------------- 

def tracer_distibution_charge(dataframe_pour_distribution: pd.DataFrame, title : str = "Distribution de la charge électrique horaire (MW)", xlabel : str = "charge en MW", ylabel : str = "Fréquence") -> None : 
    """L'objectif de cette fonction est de s'occuper de la partie traçage du graphique qui montre la distribution de la charge horaire sur la période donnée (possibilité de jouer avec les dates sur streamlit)
    :param dataframe_pour_distribution: le dataframe qui contient toutes les informations nécessaire à la construction de notre graphique ici PJM_Load_MW
    :param title: titre du graphique 
    :param xlabel: libellé de l'axe x, à savoir la charge en MW
    :param ylabel: libellé de l'axe y, à savoir la fréquence à laquelle chaque valeur apparaît dans le jeu de données 
    :return: La fonction ne renvoie rien, elle créée la figure matplotlib et l'affiche dans l'application streamlit à son appel"""

    plt.figure(figsize=(8, 4)) 
    plt.hist(dataframe_pour_distribution["PJM_Load_MW"], bins=80)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


# --------------------------------------------------------------------------------------------------------------------------------
#                                                   Fonction pour filtrer par date
# -------------------------------------------------------------------------------------------------------------------------------- 

def filtrer_par_date(dataframe_filtre_date : pd.DataFrame, debut, fin) -> pd.DataFrame : 
    """L'objectif de cette fonction est de filtrer un dataFrame entre deux dates incluses et renvoie la sous‐partie triéechronologiquement.
    :param dataframe_filtre-date: on prend le dataframe d'origine auquel on va ajouter un masque permettant de dessiner les bornes correspondant à notre jeu de donnée
    :param debut: la variable début qui contient la date à laquelle commence le datset
    :param fin: la variable fin qui contient la dernière date du dataset
    :return: retourne une copie du dataframe `df` restreinte à l’intervalle demandé"""

    debut = pd.to_datetime(debut).date()
    fin = pd.to_datetime(fin).date()

    mask = (dataframe_filtre_date["Datetime"].dt.date >= debut) & (dataframe_filtre_date["Datetime"].dt.date <= fin)
    selection = dataframe_filtre_date[mask].sort_values("Datetime") 

    return selection


# --------------------------------------------------------------------------------------------------------------------------------
#                             Fonction pour ajouter une colonne saison au dataframe
# -------------------------------------------------------------------------------------------------------------------------------- 

def ajouter_colonne_saison(dataframe_saison : pd.DataFrame, saisons_selectionnees: list[str]) -> pd.DataFrame : 
    """L'objectif de cette fonction est d'ajouter une colonne « saison » au dataFrame à partir des mois, puis de conserver uniquement les lignes dont la saison figure dans
    saisons_selectionnees.
    :param dataframe_saison: on prend le dataframe d'origine dont la colonne datetime est utilisée pour pouvoir déterminer la saison
    :param saisons_selectionnees: correspond à la liste des saisons à choisir par l'utilisateur, la casse est importante
    :return: retourne un nouveau dataframe enrichi d'une nouvelle colonne nommée saison et filtrée sur les saisons demandées"""

    saison = {12:"Hiver", 1:"Hiver", 2:"Hiver",
              3:"Printemps", 4:"Printemps", 5:"Printemps",
              6:"Eté", 7:"Eté", 8:"Eté",
              9:"Automne", 10:"Automne", 11:"Automne"}
    
    df = dataframe_saison.copy()
    df["saison"] = df["Datetime"].dt.month.map(saison) 
    mask = df["saison"].isin(saisons_selectionnees)     
    
    return df[mask].sort_values("Datetime")


# --------------------------------------------------------------------------------------------------------------------------------
#                             Fonction détecter un pic en fonction d'un seuil donné
# -------------------------------------------------------------------------------------------------------------------------------- 

def detecter_pic_en_fonction_du_seuil(dataframe_detecter_pic_seuil : pd.DataFrame, seuil_fourni: float) -> pd.DataFrame | None :
    """L'objectif de cette fonction est de sélectionner les pics de charge en MW dont la valeur dépasse un seuil donné. 
    :param dataframe_detecter_pic_seuil: dataFrame contenant une colonne numérique PJM_Load_MW représentant la charge en mégawatts auquel on va appliquer le filtre en fonction du seuil fourni
    :param seuil_fourni: Valeur de seuil choisie par l'utilisateur. Toutes les lignes qui sont supérieure ou égale à ce seuil sont conservées.
    :return: si la valeur de seuol (seuil_fourni) est inférieur ou égal à 0, on ne retourne rien car ce sont des valeurs impossible. 
    Sinon, on renvoit le dataframe filtré, le sous ensemble limitée au charges qui sont supérieure ou égales au seuil choisi par l'utilisateur (seuil_fourni)"""
    if seuil_fourni <= 0 :
        st.warning("Le seuil doit être supérieur à 0")
        return None
    else : 
        pic = dataframe_detecter_pic_seuil[dataframe_detecter_pic_seuil["PJM_Load_MW"] >= seuil_fourni]
        return pic


# --------------------------------------------------------------------------------------------------------------------------------
#                             Fonction tracer les pics dépassant un seuil donné
# -------------------------------------------------------------------------------------------------------------------------------- 

def tracer_pic(dataframe_pour_pic : pd.DataFrame, seuil: float, color: str = "#FF0000",s: int = 20, marker: str = "o") -> None : 
    """L'objectif de cette fonction est d'afficher, sous forme de nuage de points, les pics de charge de la colonne PJM_Load_MW qui dépassent un seuil donné.
    :param df: dataframe utilisé contenant les colonnes datetime et PJM_Load_MW
    :param seuil: La valeur seuil, seuls les enregistrements de la colonne PJM_Load_MW est supérieure ou égale au seuil sont représentés. Si le seuil est inférieur ou égal à 0, la fonction se termine sans rien tracer.
    :param color: paramètre spécifique utilisé dans matplolib scatter pour spécifier la couleur des nuages de points
    :param s: paramètre spécifique utilisé dans matplotlib scatter qui signifie size et désigne la taille des nuages de points
    :param marker: paramètre spécifique utilisé dans matplotlib scatter qui dessine les nuages de points. Ici o, donc les nuages de points seront des o représentés dans le graphique
    :return: La fonction ne renvoie rien, elle trace simplement des nuages de points, ce qui la rend compatible avec un graphique déjà existant"""

    if seuil <= 0 : 
        return None
    
    filtrer_pic = detecter_pic_en_fonction_du_seuil(dataframe_pour_pic, seuil)

    if filtrer_pic is not None and not filtrer_pic.empty : 
        plt.scatter(filtrer_pic["Datetime"], filtrer_pic["PJM_Load_MW"], color = color, s=s , marker = marker)


# --------------------------------------------------------------------------------------------------------------------------------
#                             Fonction pour afficher le top 10 sur le dataset
# -------------------------------------------------------------------------------------------------------------------------------- 

def afficher_top_10(dataframe_top10 : pd.DataFrame, nb_lignes : int=10) -> pd.DataFrame : 
    """L'objectif de cette fonction est de sélectionner les 10 premiers enregistrements présentant la charge la plus élevée.
    :param dataframe_top10: dataFrame contenant la colonne PJM_Load_MW, les autres colonnes sont conservées dans le résultat auquel on applique donc la méthode nlargest pour avoir le top10
    :param nb_lignes: nombre de lignes à extraire
    :return: renvoie un sous ensemble du dataframe limité aux 10 lignes présentant les valeurs les plus fortes."""

    top_10 = dataframe_top10.nlargest(nb_lignes, "PJM_Load_MW")
    return top_10

# --------------------------------------------------------------------------------------------------------------------------------
#                             Fonction pour afficher le low 10 sur le dataset
# -------------------------------------------------------------------------------------------------------------------------------- 

def afficher_low_10(dataframe_low10 : pd.DataFrame, nb_lignes: int=10) -> pd.DataFrame : 
    """L'objectif de cette fonction est de sélectionner les 10 premiers enregistrements présentant la charge la moins élevée.
    :param df: dataFrame contenant la colonne PJM_Load_MW, les autres colonnes sont conservées dans le résultat
    :param n: nombre de lignes à extraire
    :return: renvoie un sous ensemble du dataframe limité aux 10 lignes présentant les valeurs les moins fortes."""

    low_10 = dataframe_low10.nsmallest(nb_lignes, "PJM_Load_MW")
    return low_10





#-----------------------------------------------------------------------------------------------------------------------------------
#                                   Partie Affichage sur l'application streamlit
#-----------------------------------------------------------------------------------------------------------------------------------

# Set the page configuration - recopiée à partir des instructions du DM
st.set_page_config(
page_title="Devoir maison - Master MIMO - 2025",
page_icon=":python:",
layout="wide",
initial_sidebar_state="expanded",
)
st.title("Devoir maison - Master MIMO - 2025")

st.title("Dashboard charge du réseau électrique - Pennsylvania-New Jersey-Maryland Interconnection")
#  Je commence par appeler notre fonction de lecture de notre de jeu de données 
df = lire_csv("PJM_Load_hourly.csv") 

#  Ensuite on appelle notre fonction de conversion de date pour pouvoir faire nos actions d'affichage de graphique
df = conversion_en_date(df,format_date="%Y-%m-%d %H:%M:%S")
df = preparation_date_en_semaine(df)

# J'affiche les principales statistiques du jeu de données : total, moyenne, pic et creux sur la période de notre jeu de donnée
st.title("Principaux indicateurs sur la période (1998 - 2001)")
total = charge_totale(df)
moyenne = charge_moyenne(df)
pic = charge_maximale(df)
creux = charge_minimale(df)

col1, col2 = st.columns(2)
col1.metric("⚡ Charge totale", f"{total:,.0f} MW")
col2.metric("⚡ Charge moyenne", f"{moyenne:,.0f} MW")
col3, col4 = st.columns(2)
col3.metric("⚡ Pic sur la période", f"{pic:,.0f} MW")
col4.metric("⚡ Creux sur la période", f"{creux:,.0f} MW")

# Pour l'intéraction avec l'utilisateur, je choisi de mettre en place une sidebar avec tous les éléments paramétrables 
st.sidebar.title("Paramètres temporels")

# Module de sélection des dates
premiere_date = df["Datetime"].min().date()
derniere_date = df["Datetime"].max().date()
debut = st.sidebar.date_input("Début", value=premiere_date, min_value=premiere_date, max_value=derniere_date)
fin = st.sidebar.date_input("Fin", value=derniere_date, min_value=premiere_date, max_value=derniere_date) 
df_date = filtrer_par_date(df, debut, fin)

# Module de sélection des saisons
choix = st.sidebar.multiselect(
    "Saison(s) à afficher",
    ["Hiver", "Printemps", "Eté", "Automne"],
    default=["Hiver", "Printemps", "Eté", "Automne"]
)

df_filtre = ajouter_colonne_saison(df_date, choix)


st.sidebar.title("Options avancées")
# Module de sélection de sélection du seuil
seuil_fourni = st.sidebar.number_input("Veuillez renseigner le pic recherché")
afficher_pic = st.sidebar.toggle("Afficher les pics", value = False)

# Affichage du graphique avec vue d'ensemble
st.title("Charge – vue d’ensemble")
st.markdown("Ce graphique représente une vue d'ensemble de l'évolution de la charge électrique s'étalant sur toute la durée du jeu de données, donc de 1998 à 2001. Vous pouvez interargir avec le graphique avec la sidebar à gauche de l'écran et choisir une de changer la durée, de jouer avec les saisons, ou encore de définir un seuil de pic.")

tracer_vue_ensemble(df_filtre,title=f"PJM — {debut} → {fin}")  
if afficher_pic :
    tracer_pic(df_filtre, seuil_fourni)

st.pyplot(plt)  

#Affichage du graphique avec distribution de charge 
st.title("Distribution de la charge électrique horaire (MW)")
st.markdown("Ce graphique représente une distribution de la charge électrique horaire. En d'autres termes, ce graphique est capable de montrer la charge électrique horaire normale (celle qu'on retrouve le plus souvent), les pics de production, les creux... C'est un bon complément au premier graphique. Comme pour le premier, il vous est possible d'intérargir avec le graphique avec les élements interactifs de la sidebar. ")
tracer_distibution_charge(df_filtre)
st.pyplot(plt)


# Module de sélection top 1à ou low 10 du tableau
choix_tableau = st.sidebar.radio("Afficher :",["Tout", "Top 10 charge MW", "Low 10 charge MW"])

if choix_tableau == "Top 10 charge MW" :
    df_tableau = afficher_top_10(df_filtre, 10)
elif choix_tableau == "Low 10 charge MW" :
    df_tableau = afficher_low_10(df_filtre, 10)
else :
    df_tableau = df_filtre

# Affichage du jeu de donnée qui prend en compte les paramètres choisis par l'utilisateur
st.title("Jeu de données")
st.markdown("Affichage du jeu de données qui a été utilisé dans le cadre de l'exercice. Ce jeu de donnée a été quelque peu modié avec la possibilité de voir les saisons correspondantes. Il est également possible de faire des petites action comme : 1.afficher le top 10 des charges les plus importantes, 2. Afficher le low 10 des charges les moins importante. ")
st.dataframe(df_tableau, use_container_width=True)

