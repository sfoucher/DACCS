import ee
import folium
import datetime


ee.Initialize()

class eeMapHack(object):
    def __init__(self,center=[0, 0],zoom=3):
        self._map = folium.Map(location=center,zoom_start=zoom)
        return

    def addToMap(self,img,vizParams,name):
         map_id = ee.Image(img.visualize(**vizParams)).getMapId()
         tile_url_template = "https://earthengine.googleapis.com/map/{mapid}/{{z}}/{{x}}/{{y}}?token={token}"
         mapurl = tile_url_template.format(**map_id)
         folium.WmsTileLayer(mapurl,layers=name).add_to(self._map)

         return

    def addLayerControl(self):
         self._map.add_child(folium.map.LayerControl())
         return


# initialize map object
eeMap = eeMapHack(center=[45,-71],zoom=5)
## Filter to only include images intersecting Colorado or Utah.
polygon = ee.Geometry.Polygon([[[-86.53922211333486, 66.4065189106996],
          [-86.53922211333486, 44.815840394531605],
          [-67.46353851958486, 44.815840394531605],
          [-67.46353851958486, 66.4065189106996]]])
# Filter the LE7 collection to a single date.
collection = (ee.ImageCollection('COPERNICUS/S2')
          .filterDate(datetime.datetime(2019, 6, 1),
                      datetime.datetime(2019, 9, 30))
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))
            .filterBounds(polygon))
#print(collection.getInfo())

#### Make list of image IDs
l8_id = []
for f in collection.getInfo()['features']:
  image_id = f['id']
  
  l8_id.append(image_id)
print(l8_id)
print(len(l8_id))
image = collection.mosaic().select('B4', 'B3', 'B2').multiply(0.0001)
vis = {
    'min': 0,
    'max': 0.3
}
eeMap.addToMap(image, vis, 'Land')

# Add and stretch the water.  Once where the elevation is masked,
# and again where the elevation is zero.
#elev = ee.Image('srtm90_v4')
#mask1 = elev.mask().eq(0).And(image.mask())
#mask2 = elev.eq(0).And(image.mask())

#eeMap.addToMap(image.mask(mask1), {'gain': 6.0, 'bias': -200}, 'Water: Masked')
#eeMap.addToMap(image.mask(mask2), {'gain': 6.0, 'bias': -200}, 'Water: Elev 0')

# add layer control to map
eeMap.addLayerControl()

outHtml = 'map.html' # temporary file path, change if needed
eeMap._map.save(outHtml)

