import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei importieren und Spalten umbenennen:
df = pd.read_csv('2024-02-22 Data Bewerbungsaufgabe.csv', sep=';', header=0)
df.columns = ['wkt_geom', 'Energiequelle', 'Leistung in kW']

# Spalte 'A' aus dem DataFrame entfernen:
df.drop(columns=['wkt_geom'])

# DataFrame nach Energiequellen sortieren:
df.sort_values(by='Energiequelle', inplace=True)

# Leistung für Einträge mit 'Yes' auf 600 kW festlegen:
df.loc[df['Leistung in kW'] == 'Yes', 'Leistung in kW'] = 600

# Einträge ohne Leistung oder mit anderem Inhalt löschen:
df = df[df['Leistung in kW'].apply(lambda x: str(x).isdigit())]

# Einträge basierend auf ihren Energiequellen in separate DataFrames aufteilen:
energiequellen_dfs = {}
for energiequelle, group in df.groupby('Energiequelle'):
    energiequellen_dfs[energiequelle] = group.copy()

# Leistung der Energiequelle 'gas' plotten und als Bild speichern:
gas_df = energiequellen_dfs.get('gas')
if gas_df is not None:
    gas_df['Leistung in kW'] = gas_df['Leistung in kW'].astype(int)
    gas_df_grouped = gas_df.groupby('Leistung in kW').size()
    # Anpassung der Plot-Eigenschaften:
    gas_df_grouped.plot(kind='bar', color='cadetblue')
    plt.xlabel('Leistung in kW', fontsize=14)
    plt.ylabel('Anzahl der Einträge', fontsize=14)
    plt.title('Leistung der Energiequelle "gas"', fontsize=16)
    plt.gcf().set_size_inches(10, 7)
    plt.savefig('gas_leistung_plot.png', dpi=300)
    plt.show()
else:
    print('Die Energiequelle "gas" ist nicht im DataFrame enthalten.')
