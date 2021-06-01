# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 04:29:08 2020
@author: kkrao
"""

#import arcpy
import os
import glob
import arcpy
from datetime import datetime

arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput=True

dir_data = r"D:/Krishna/projects/grid_fire/data"


files =""
for file in glob.glob(os.path.join(dir_data,"cfo","*CanopyBulkDensity*.tif")):
    files = files+file+";"
#print(files)
#arcpy.env.workspace = os.path.join(dir_data, "cfo","canopyHeight")

##Mosaic several TIFF images to a new TIFF image
print("[INFO] Mosaic started at %s"%datetime.now().strftime("%H:%M:%S"))
arcpy.MosaicToNewRaster_management(files,os.path.join(dir_data, "cfo","canopyBulkDensity"), "canopyBulkDensity2020CA.tif", number_of_bands = 1)

print("[INFO] Mosaic done at %s"%datetime.now().strftime("%H:%M:%S"))