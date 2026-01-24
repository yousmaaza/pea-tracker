#!/usr/bin/env python3
import pandas as pd
import json

# Charger le fichier Excel
excel_file = '/Users/yousrids/Documents/pea-tracker/PEA_Watchlist_Indicateurs.xlsx'
xls = pd.ExcelFile(excel_file)

print(f"Feuilles disponibles: {xls.sheet_names}")

# Charger la watchlist
watchlist = pd.read_excel(xls, sheet_name='Watchlist')
print(f"\n=== WATCHLIST ({len(watchlist)} entrées) ===")
print(watchlist.to_string())

# Filtrer les tickers actifs
active = watchlist[watchlist['Actif'] == True]
print(f"\n=== TICKERS ACTIFS ({len(active)}) ===")
for idx, row in active.iterrows():
    print(f"  {row['Ticker']}: {row['Nom']} ({row['Marché']}, {row['Secteur']})")

# Sauvegarder les tickers actifs
active_tickers = []
for _, row in active.iterrows():
    active_tickers.append({
        'ticker': row['Ticker'],
        'nom': row['Nom'],
        'marche': row['Marché'],
        'secteur': row['Secteur'],
        'pays': row['Pays']
    })

with open('/Users/yousrids/Documents/pea-tracker/active_tickers.json', 'w') as f:
    json.dump(active_tickers, f, ensure_ascii=False, indent=2)

print(f"\nTickers actifs sauvegardés dans active_tickers.json")
