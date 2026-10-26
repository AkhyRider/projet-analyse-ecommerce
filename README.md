# 🛒 Analyse E-Commerce Olist — Projet Data Analysis

![Python](https://img.shields.io/badge/Python-3.14.4-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-3.0.2-150458?logo=pandas)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![Status](https://img.shields.io/badge/Status-En%20cours-yellow)

> **Projet académique** — Analyse exploratoire du dataset public Olist (E-Commerce brésilien, 2016-2018).  
> Réalisé dans le cadre d'un cours d'analyse de données avec Pandas, Matplotlib et Seaborn.

---

## 🎯 Questions Métier

| # | Question | Méthode |
|---|----------|---------|
| 1 | Quelles **catégories de produits** génèrent le plus de CA ? | `groupby` + `pivot_table` |
| 2 | Comment évolue le **CA mensuel** entre 2016 et 2018 ? | Analyse temporelle, `resample` |
| 3 | Quel est l'impact du **délai de livraison** sur la satisfaction client ? | Corrélation, boxplot |
| 4 | Quels **États brésiliens** sont les plus dynamiques ? | Agrégation géographique |

---

## 📁 Structure du Projet

```
projet-analyse-ecommerce/
├── data/
│   ├── raw/                          # Fichiers CSV Olist bruts
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   └── product_category_name_translation.csv
│   └── master_clean.csv              # Table jointe et nettoyée (généré)
│
├── notebooks/
│   ├── 01_nettoyage.ipynb            # Nettoyage, jointures, feature engineering
│   └── 02_analyse.ipynb              # Exploration, visualisations, réponses
│
├── outputs/
│   └── figures/                      # Graphiques exportés en PNG
│       ├── fig1_top10_categories_ca.png
│       ├── fig2_ca_mensuel.png
│       ├── fig3_delai_satisfaction.png
│       ├── fig4_boxplot_delai_notes.png
│       └── fig5_performance_etats.png
│
├── requirements.txt                  # Dépendances Python exactes
└── README.md                         # Ce fichier
```

---

## 🚀 Installation & Démarrage

### 1. Cloner le dépôt

```bash
git clone https://github.com/AkhyRider/projet-analyse-ecommerce.git
cd projet-analyse-ecommerce
```

### 2. Créer l'environnement virtuel

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Accéder aux données

Le dataset Olist est disponible gratuitement sur Kaggle :

🔗 **[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**

**Étapes :**
1. Créez un compte Kaggle (gratuit)
2. Téléchargez tous les fichiers CSV du dataset
3. Placez-les dans le dossier `data/raw/`

### 5. Lancer les notebooks

```bash
jupyter notebook
# ou
jupyter lab
```

Exécutez les notebooks **dans l'ordre** :
1. `01_nettoyage.ipynb` → génère `data/master_clean.csv`
2. `02_analyse.ipynb` → génère les graphiques dans `outputs/figures/`

> ⚠️ **Important** : Cliquez sur *Kernel → Restart & Run All* pour vérifier que chaque notebook s'exécute de bout en bout sans erreur.

---

## 📊 Aperçu des Visualisations

### Évolution du CA mensuel
![CA mensuel](outputs/figures/fig2_ca_mensuel.png)

### Top 10 catégories par CA
![Top catégories](outputs/figures/fig1_top10_categories_ca.png)

### Impact du délai de livraison sur la satisfaction
![Délai vs Satisfaction](outputs/figures/fig3_delai_satisfaction.png)

### Performance géographique par État
![Performance États](outputs/figures/fig5_performance_etats.png)

---

## 🔑 Résultats Clés

| Indicateur | Valeur |
|------------|--------|
| Commandes analysées | ~96 000 (livrées) |
| Période | Oct. 2016 — Août 2018 |
| CA total estimé | R$ 13,5M+ |
| Panier moyen | ~R$ 140 |
| Note de satisfaction moyenne | 4.07 / 5 |
| Catégorie #1 | health_beauty |
| État #1 | São Paulo (SP, ~40% du CA) |

---

## 🚧 Limites de l'Analyse

1. **Période limitée** : Seulement ~22 mois, insuffisant pour valider les saisonnalités sur plusieurs cycles.
2. **Pas de données de retours** : L'insatisfaction liée aux retours produits n'est pas capturée.
3. **Causalité délai/satisfaction** : La corrélation observée ne prouve pas la causalité.
4. **Biais géographique** : Surreprésentation de SP qui peut masquer des dynamiques régionales.
5. **Inflation non corrigée** : Les montants CA ne sont pas déflatés.

---

## 👨‍💻 Auteur

**AkhyRider** — [GitHub Profile](https://github.com/AkhyRider)

---

## 📄 Licence

Dataset : © Olist — Usage éducatif sous licence CC BY-NC-SA 4.0  
Code : MIT License
