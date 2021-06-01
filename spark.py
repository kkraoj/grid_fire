# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 07:16:23 2021

@author: kkrao
"""

import os
import pandas as pd
import numpy as np
import gdal
import seaborn as sns
import matplotlib.pyplot as plt

def get_value(filename, mx, my, band = 1):
    ds = gdal.Open(filename)
    gt = ds.GetGeoTransform()
    data = ds.GetRasterBand(band).ReadAsArray().astype(np.float32)
    px = ((mx - gt[0]) / gt[1]).astype(int) #x pixel
    py = ((my - gt[3]) / gt[5]).astype(int) #y pixel
    return data[py,px]


dir_data = r"D:/Krishna/projects/grid_fire/data"
lfmcDir =  r"D:\Krishna\projects\vwc_from_radar\data\map\dynamic_maps\lfmc"


#%% load and cleanup

# df =pd.read_excel(os.path.join(dir_data, "PGE_Fire Incident Data 2014-2019.xlsx"))
# df.head()
# df.columns
# df.shape

# cols = [x for x in df.columns if "Unnamed" not in x]

# df = df[cols]
# df = df.iloc[1:]

# df.columns = df.iloc[0]
# df = df.iloc[1:]


# df.columns = ["Utility Name"]+list(df.columns)[1:-1]+["Notes"]  

# df = df.loc[df["Utility Name"]=="PG&E"]
# df["Size"].unique()
# df.groupby("Size").Size.count().plot.bar()

# df.FireDate = pd.to_datetime(df["FireDate"])
# df["lfmc"]=np.nan

# for index, row in df.iterrows():
#     # if index<17580:
#         # continue
#     print("[INFO] Index = %d"%index)
#     # row = gdf.loc[15720]
#     date = row.FireDate
    
#     if date.day>=15:
#         day = 15
#     else:
#         day=1
#     lfmcDate = "%04d-%02d-%02d"%(date.year, date.month, \
#                                day)
    
#     lfmcFile = os.path.join(lfmcDir, "lfmc_map_%s.tif"%lfmcDate)
    
#     try:
#         lfmc = get_value(lfmcFile, np.array(row.Longitude), np.array(row.Latitude))
#     except:
#         print("[INFO] LFMC patch requested is out of bounds")
#         continue
#     df.loc[index,"lfmc"]=lfmc
#     # break

# df.to_excel(os.path.join(dir_data, "PGE_Fire Incident Data 2014-2019 Cleaned.xlsx"))

#%% add salo data
# df = pd.read_excel(os.path.join(dir_data, "PGE_Fire Incident Data 2014-2019 Cleaned.xlsx"))

# df['canopyHeight']=np.nan
# df['canopyBulkDensity']=np.nan

# filename = os.path.join(dir_data, "cfo","canopyHeight","canopyHeight2020CAProjected.tif")
# df['canopyHeight']=get_value(filename, df["Longitude"], df["Latitude"])

# filename = os.path.join(dir_data, "cfo","canopyBulkDensity","canopyBulkDensity2020CAProjected.tif")
# df['canopyBulkDensity']=get_value(filename, df["Longitude"], df["Latitude"])

# df.to_excel(os.path.join(dir_data, "PGE_Fire Incident Data 2014-2019 Cleaned.xlsx"))

#%% investigation
df = pd.read_excel(os.path.join(dir_data, "PGE_Fire Incident Data 2014-2019 Cleaned.xlsx"), index_col = 0)
# df = df.loc[df.lfmc>0].copy()

# df.groupby("Land Use at Origin").Size.count().plot.bar()


df["sparkOrFire"] = "Spark"

fires = ['.26 - 9.99 Acres','100 - 299 Acres','10 - 99 Acres','> 5000 Acres',\
         '1000 - 4999 Acres', '300 - 999 Acres','0.25 - 10 Acres',\
             '10 - 100 Acres','100+ Acres']
    
df.loc[df.Size.isin(fires),"sparkOrFire"] = "Fire"
df = df.loc[df.canopyHeight>=3].copy() ## Only tall trees
df = df.loc[df.lfmc>=0].copy() ## only valid LFMC
# df = df.loc[df['Type']=="Overhead"]
df.groupby("sparkOrFire").sparkOrFire.count()


fig, axs = plt.subplots(1, 4,figsize = (1.5*4,3), sharey= True)

ax = axs[0]
sns.boxplot(x="sparkOrFire", y="lfmc", data=df,ax=ax, fliersize = 0,color="darkorange")

ax.set_ylabel("Live fuel moisture content (%)")
ax.set_xlabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
# ax.set_ylim(0,200)
# ax.set_yticks(np.linspace(0,200,6))
ax.set_title("Overall (n=%d)"%df.shape[0],fontsize = 10)
print(df.shape)

ax = axs[1]
sub = df.loc[df["Land Use at Origin"].isin(["Rural","RURAL"])].copy()
sns.boxplot(x="sparkOrFire", y="lfmc", data=sub,ax=ax, fliersize = 0,color = "darkgoldenrod")
ax.set_ylabel("")
ax.set_xlabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_title("Rural (n=%d)"%sub.shape[0],fontsize = 10)
print(sub.shape)

ax = axs[2]

sub = df.loc[df["Land Use at Origin"].isin(["Conifer Fires","ardwood Fore", "dwood Wood"])].copy()
sns.boxplot(x="sparkOrFire", y="lfmc", data=sub,ax=ax, fliersize = 0,color = "darkgreen")
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_title("Forest (n=%d)"%sub.shape[0],fontsize = 10)

ax = axs[3]
sub = df.loc[df["Land Use at Origin"].isin(["Herbaceous", "Shrub"])].copy()
sns.boxplot(x="sparkOrFire", y="lfmc", data=sub,ax=ax, fliersize = 0, color= "limegreen")
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_title("Herbaceous (n=%d)"%sub.shape[0],fontsize = 10)
print(sub.shape)

fig.text(0.5,-0.05,"Fire size",ha = "center")

#%% canopy height

fig, axs = plt.subplots(1, 4,figsize = (1.5*4,3), sharey= True)

ax = axs[0]
sns.boxplot(x="sparkOrFire", y="canopyHeight", data=df,ax=ax, fliersize = 0,color="darkorange")

ax.set_ylabel("Canopy height (m)")
ax.set_xlabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_ylim(0,30)
ax.set_yticks(np.linspace(0,30,3))
ax.set_title("Overall (n=%d)"%df.shape[0],fontsize = 10)
print(df.shape)

ax = axs[1]
sub = df.loc[df["Land Use at Origin"].isin(["Rural","RURAL"])].copy()
sns.boxplot(x="sparkOrFire", y="canopyHeight", data=sub,ax=ax, fliersize = 0,color = "darkgoldenrod")
ax.set_ylabel("")
ax.set_xlabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_title("Rural (n=%d)"%sub.shape[0],fontsize = 10)
print(sub.shape)

ax = axs[2]

sub = df.loc[df["Land Use at Origin"].isin(["Conifer Fires","ardwood Fore", "dwood Wood"])].copy()
sns.boxplot(x="sparkOrFire", y="canopyHeight", data=sub,ax=ax, fliersize = 0,color = "darkgreen")
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_title("Forest (n=%d)"%sub.shape[0],fontsize = 10)

ax = axs[3]
sub = df.loc[df["Land Use at Origin"].isin(["Herbaceous", "Shrub"])].copy()
sns.boxplot(x="sparkOrFire", y="canopyHeight", data=sub,ax=ax, fliersize = 0, color= "limegreen")
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_title("Herbaceous (n=%d)"%sub.shape[0],fontsize = 10)
print(sub.shape)

fig.text(0.5,-0.05,"Fire size",ha = "center")

#%% Bulk density
fig, axs = plt.subplots(1, 4,figsize = (1.5*4,3), sharey= True)

ax = axs[0]
sns.boxplot(x="sparkOrFire", y="canopyBulkDensity", data=df,ax=ax, fliersize = 0,color="darkorange")

ax.set_ylabel("Canopy bulk density (kg.m$^{-3}$)")
ax.set_xlabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_ylim(0,15)
ax.set_yticks(np.linspace(0,15,4))
ax.set_title("Overall (n=%d)"%df.shape[0],fontsize = 10)
print(df.shape)

ax = axs[1]
sub = df.loc[df["Land Use at Origin"].isin(["Rural","RURAL"])].copy()
sns.boxplot(x="sparkOrFire", y="canopyBulkDensity", data=sub,ax=ax, fliersize = 0,color = "darkgoldenrod")
ax.set_ylabel("")
ax.set_xlabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_title("Rural (n=%d)"%sub.shape[0],fontsize = 10)
print(sub.shape)

ax = axs[2]

sub = df.loc[df["Land Use at Origin"].isin(["Conifer Fires","ardwood Fore", "dwood Wood"])].copy()
sns.boxplot(x="sparkOrFire", y="canopyBulkDensity", data=sub,ax=ax, fliersize = 0,color = "darkgreen")
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_title("Forest (n=%d)"%sub.shape[0],fontsize = 10)

ax = axs[3]
sub = df.loc[df["Land Use at Origin"].isin(["Herbaceous", "Shrub"])].copy()
sns.boxplot(x="sparkOrFire", y="canopyBulkDensity", data=sub,ax=ax, fliersize = 0, color= "limegreen")
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xticklabels(["<0.25\nacres","$\geq$0.25\nacres"])
ax.set_title("Herbaceous (n=%d)"%sub.shape[0],fontsize = 10)
print(sub.shape)

fig.text(0.5,-0.05,"Fire size",ha = "center")