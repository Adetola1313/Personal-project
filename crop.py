import numpy as np
import pandas as pd
import os
## read CSV files
cd= pd.read_csv("air-quality-data-2003-2022.csv", sep =";", low_memory=False)
cd['Date Time'] = pd.to_datetime(cd['Date Time'])
cd_cropped = cd[cd['Date Time'] >= '2010-01-01 00:00:00']
cd_cropped.to_csv("crop.csv", index=False)
print(cd_cropped)
