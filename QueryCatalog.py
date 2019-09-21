import ee

# Initialize the Earth Engine module.
ee.Initialize()

# Print metadata for a DEM dataset.
print(ee.Image('CGIAR/SRTM90_V4').getInfo())