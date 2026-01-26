# Louisa Rawles -- NFL ML

## Purpose
I created this project to ingest NFL data via their API and load it into a relational database system for
analytics via tree-based ML classifiers.

---

## System Architecture
- Data Sources: NFL Next Gen Stats APIs (JSON)
- Ingestion: Python API-specific scrapers with shared factory logic
- Processing: NFLDataClasses, NFLLoaders, and encapsulation methods to parse, normalize, and encapsulate data
- Storage: SQLite relational database
- Analytics Frameworks: NumPy, Pandas, Matplotlib
- Modeling: Tree-based classifier trained with Gini and Entropy
- Visualization: Decision-tree plot, QB passing-zone heatmaps (NFLDataVis)

---

## Technologies & Tools
- Python - Primary programming language
- Sqlite3 - Database driver
- Matplotlib, NumPy, Pandas - Analytics
- Scikit-learn - Decision tree
- Requests - RESTful API integration

---

## Progress
### Current Update
I completed an end-to-end game statistic pipeline that ingests game data and loads it into a structured GameStats table
via Python files in the NFLScrapers/GameCenter directory and the database driver. The decision tree file within the root
directory trains a classifier with 500+ inputs and outputs well-informed game outcome predictions based on statistical analysis.
### Coming Phases
I will now enter phases to predict individual player performance, so that I can determine team metrics.

---

## Authors
- **Louisa Rawles** - [https://github.com/louisarawles](https://github.com/louisarawles)
