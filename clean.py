import pandas as pd
cd= pd.read_csv("crop.csv", low_memory=False)
cd_1 = cd.loc[:, ['SiteID', 'Location']]
Tri_dict = {188 : 'AURN Bristol Centre',
203 : 'Brislington Depot',
206 : 'Rupert Street',
209 : 'IKEA M32',
213 : 'Old Market',
215 : 'Parson Street School',
228 : 'Temple Meads Station',
270 : 'Wells Road',
271 : 'Trailer Portway P&R',
375 : 'Newfoundland Road Police Station',
395 : "Shiner's Garage",
452 : 'AURN St Pauls',
447 : 'Bath Road',
459 : 'Cheltenham Road \\ Station Road',
463 : 'Fishponds Road',
481 : 'CREATE Centre Roof',
500 : 'Temple Way',
501 : 'Colston Avenue',
672 : 'Marlborough Street'}
# Loop through each row in the DataFrame
mismatch_index = []
for index, row in cd_1.iterrows():
    
    # Get the SiteID and Location values for the current row
    site_id = row['SiteID']
    location = row['Location']
    
    # Check if the SiteID matches the corresponding Location value in the Tri_dict dictionary
    if Tri_dict.get(site_id, None) != location:
        print(f"Mismatch detected: SiteID={site_id} and Location={location}")
        mismatch_index.append(index)
        clean_cd = cd.drop(index=mismatch_index)
        clean_cd.to_csv("clean.csv", index=False)
