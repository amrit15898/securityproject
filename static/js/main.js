var map = new ol.Map({
    target: 'map',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM()
      }),
      new ol.layer.Tile({
        source: new ol.source.TileWMS({
          url: 'http://localhost:8080/geoserver/osm_north/wms',
          params: {'LAYERS': 'osm_north:my_osm', 'TILED': true},
          serverType: 'geoserver',
          // Countries have transparency, so do not fade tiles:
          transition: 0
        })
      }) 
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([76.791019, 30.740393]),
      zoom: 6
    })
  });

map.on("click",function (e){
    console.log("clcked at")
    console.log(e)
})