# Predicció de Resultats de Tennis

Aquest projecte implementa un sistema de predicció de resultats de partits de tennis utilitzant diferents models de machine learning.

## Arxius Principals

### data_cleaner.ipynb

Arxiu principal per a la preparació i neteja de les dades. Aquest notebook conté tot el procés de:

- Càlcul de característiques històriques: Head-to-Head (H2H), victòries i derrotes totals
- Càlcul de mètriques específiques per superfície: WinRate acumulat, forma recent (últims 10 partits), dies de descans
- Implementació del sistema Elo (global i per superfície)
- Generació de noves columnes amb característiques diferencials entre jugadors
- Exportació de datasets nets i preparats per a l'entrenament de models

**Sortida**: Genera el fitxer `wimbeldon_dataset_all_surfaces_v2.csv` amb totes les característiques calculades.

### programa_final.ipynb

Arxiu principal per realitzar les prediccions del torneig utilitzant **XGBoost**. Aquest és el model principal del projecte.

Aquest notebook inclou:

- Model XGBoost amb validació temporal i calibratge isotònic
- Optimització d'hiperparàmetres (especialment `n_estimators`)
- Prediccions per ronda del torneig de Wimbledon 2025
- Reentrenament incremental després de cada ronda
- Anàlisi d'importància de característiques amb SHAP
- Avaluació completa amb mètriques d'accuracy i Brier Score

**Característiques**: Utilitza el sistema Elo avançat, característiques diferencials i calibratge de probabilitats.

### programa_final_LR.ipynb

Arxiu alternatiu per realitzar prediccions utilitzant **Regressió Logística**. Aquest model serveix com a comparació i baseline respecte al model principal amb XGBoost.

Aquest notebook inclou:

- Model de Regressió Logística amb validació temporal i calibratge isotònic
- Optimització del paràmetre de regularització `C`
- Prediccions per ronda del torneig de Wimbledon 2025
- Reentrenament incremental després de cada ronda
- Anàlisi d'importància de característiques a través dels coeficients
- Avaluació completa amb mètriques d'accuracy i Brier Score

**Ús**: Utilitzar com a referència per comparar rendiment amb el model principal. La Regressió Logística és més simple i interpretable, però generalment té un rendiment inferior a XGBoost.

## Estructura del Treball

1. **Preparació de dades** (`data_cleaner.ipynb`): Neteja i generació de característiques
2. **Entrenament i predicció principal** (`programa_final.ipynb`): Model XGBoost (recomanat)
3. **Comparació alternativa** (`programa_final_LR.ipynb`): Model de Regressió Logística

## Requisits

Les llibreries principals utilitzades són:
- pandas
- numpy
- xgboost
- scikit-learn
- shap (per al model XGBoost)

## Dataset

El dataset final generat (`wimbeldon_dataset_all_surfaces_v2.csv`) conté totes les característiques necessàries per entrenar els models, incloent:
- Head-to-Head històric
- Estadístiques globals i per superfície
- Sistema Elo (global i per superfície)
- Característiques diferencials entre jugadors

## Dades Primitives

Tota la informació primitiva del projecte es troba a la carpeta `data`. Aquesta carpeta conté:

- **Dades de partits històrics**: Informació sobre partits de tennis de diferents temporades i tornejos
- **Diccionaris de dades**: Documentació sobre l'estructura i el significat de les columnes
- **Dades consolidades**: Fitxers merge que combinen informació de múltiples fonts
- **Dades per any**: Dades organitzades per temporades (2000-2025)

Aquesta informació primitiva és processada pel notebook `data_cleaner.ipynb` per generar el dataset final amb totes les característiques calculades.

## Resultats

Tota la informació sobre els resultats de les prediccions i les comparacions amb els resultats reals està continguda al fitxer Excel `ResultatWimbeldon.xlsx`. Aquest fitxer inclou:

- Resultats reals dels partits del torneig de Wimbledon 2025
- Prediccions generades pels models
- Comparatives entre diferents models
- Anàlisi de rendiment i precisió de les prediccions
