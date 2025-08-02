# from src.executables.executable import executable



# executable()



import pynasafirms


client = pynasafirms.NasaFirms(map_key="93f4e7690a9c14e23a4e8d0004c6e0be")

print(client.get_area_modis_nrt("INR", 1))
