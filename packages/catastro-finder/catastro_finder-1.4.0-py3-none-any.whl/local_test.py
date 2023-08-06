from catastro_finder import CatastroFinder

provincia = CatastroFinder().get_provincias()[30]
print(provincia)
municipio = CatastroFinder().get_municipios(29)[66]
print(municipio)
via = CatastroFinder().get_vias(29,900,"cristo")[0]
print(via)
inmueble = CatastroFinder().search_inmueble(via,"91",provincia,municipio,tipur="U",pest="urbana")
print(inmueble[0])
cp = CatastroFinder().get_cp(29,900,inmueble[0]['RefC'])
print(cp)
lat, lon = CatastroFinder().get_lat_lon(inmueble[0]['RefC'])
print(lat,lon)