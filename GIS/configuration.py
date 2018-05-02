from enum import Enum
import math


class Configuration:
    def __init__(self):
        self.number_of_airplanes = 30
        self.simulation_length = 4  # days
        self.plane_speed = 500  # km/h
        self.simulation_tempo = 0.0005  # amount of hours processed in 0.01 seconds

        disabled_countries = []
        disabled_cities = []


        # Case 3 Europe
        self.airports = {'Lisbon': Airport(name='Lisbon', country='Spain', coord_x=50, coord_y=100),
                         'Porto': Airport(name='Porto', country='Spain', coord_x=70, coord_y=260),
                         'Madrid': Airport(name='Madrid', country='Spain', coord_x=300, coord_y=240),
                         'Bilbao': Airport(name='Bilbao', country='Spain', coord_x=300, coord_y=400),
                         'Valencia': Airport(name='Valencia', country='Spain', coord_x=440, coord_y=200),
                         'Algiers': Airport(name='Algiers', country='Algeria', coord_x=500, coord_y=30),
                         'Tunis': Airport(name='Tunis', country='Tunisia', coord_x=950, coord_y=33),
                         'Toulouse': Airport(name='Toulouse', country='France', coord_x=480, coord_y=400),
                         'Bordeaux': Airport(name='Bordeaux', country='France', coord_x=430, coord_y=480),
                         'Nantes': Airport(name='Nantes', country='France', coord_x=400, coord_y=600),
                         'Paris': Airport(name='Paris', country='France', coord_x=500, coord_y=700),
                         'Geneva': Airport(name='Geneva', country='France', coord_x=800, coord_y=550),
                         'London': Airport(name='London', country='Great Britain', coord_x=400, coord_y=800),
                         'Bristol': Airport(name='Bristol', country='Great Britain', coord_x=350, coord_y=830),
                         'Luxembourg City': Airport(name='Luxembourg City', country='Luxembourg', coord_x=700,
                                                    coord_y=750),
                         'Brussels': Airport(name='Brussels', country='Belgium', coord_x=680, coord_y=780),
                         'Antwerp': Airport(name='Antwerp', country='Belgium', coord_x=680, coord_y=820),
                         'Amsterdam': Airport(name='Amsterdam', country='Netherlands', coord_x=720, coord_y=920),
                         'Cologne': Airport(name='Cologne', country='Germany', coord_x=800, coord_y=800),
                         'Frankfurt': Airport(name='Frankfurt', country='Germany', coord_x=850, coord_y=750),
                         'Stuttgart': Airport(name='Stuttgart', country='Germany', coord_x=880, coord_y=680),
                         'Nuremberg': Airport(name='Nuremberg', country='Germany', coord_x=950, coord_y=720),
                         'Berlin': Airport(name='Berlin', country='Germany', coord_x=1050, coord_y=920),
                         'Munich': Airport(name='Munich', country='Germany', coord_x=980, coord_y=670),
                         'Salzburg': Airport(name='Salzburg', country='Austria', coord_x=1020, coord_y=630),
                         'Vienna': Airport(name='Vienna', country='Austria', coord_x=1140, coord_y=640),
                         'Prague': Airport(name='Prague', country='Czech Republic', coord_x=1080, coord_y=780),
                         'Wroclaw': Airport(name='Wroclaw', country='Poland', coord_x=1160, coord_y=810),
                         'Krakow': Airport(name='Krakow', country='Poland', coord_x=1240, coord_y=780),
                         'Warsaw': Airport(name='Warsaw', country='Poland', coord_x=1270, coord_y=920),
                         'Budapest': Airport(name='Budapest', country='Hungary', coord_x=1220, coord_y=610),
                         'Turin': Airport(name='Turin', country='Italy', coord_x=840, coord_y=500),
                         'Milan': Airport(name='Milan', country='Italy', coord_x=890, coord_y=500),
                         'Verona': Airport(name='Verona', country='Italy', coord_x=940, coord_y=500),
                         'Venice': Airport(name='Venice', country='Italy', coord_x=990, coord_y=500),
                         'Bologna': Airport(name='Bologna', country='Italy', coord_x=950, coord_y=460),
                         'Pisa': Airport(name='Pisa', country='Italy', coord_x=910, coord_y=410),
                         'Rome': Airport(name='Rome', country='Italy', coord_x=1000, coord_y=310),
                         'Naples': Airport(name='Naples', country='Italy', coord_x=1070, coord_y=270),
                         'Palermo': Airport(name='Palermo', country='Italy', coord_x=1030, coord_y=150),
                         'Catania': Airport(name='Catania', country='Italy', coord_x=1090, coord_y=130),
                         'Zagreb': Airport(name='Zagreb', country='Croatia', coord_x=1060, coord_y=530),
                         'Split': Airport(name='Split', country='Croatia', coord_x=1070, coord_y=430),
                         'Belgrade': Airport(name='Belgrade', country='Serbia', coord_x=1240, coord_y=490),
                         'Sofia': Airport(name='Sofia', country='Bulgaria', coord_x=1390, coord_y=390),
                         'Thessaloniki': Airport(name='Thessaloniki', country='Greece', coord_x=1370, coord_y=290),
                         'Corfu': Airport(name='Corfu', country='Greece', coord_x=1270, coord_y=250),
                         'Athens': Airport(name='Athens', country='Greece', coord_x=1410, coord_y=190),
                         }

        self.connections = [Connection(beginning=self.airports['Lisbon'], end=self.airports['Porto']),
                            Connection(beginning=self.airports['Lisbon'], end=self.airports['Madrid']),
                            Connection(beginning=self.airports['Lisbon'], end=self.airports['Valencia']),
                            Connection(beginning=self.airports['Lisbon'], end=self.airports['Bilbao']),
                            Connection(beginning=self.airports['Lisbon'], end=self.airports['Algiers']),
                            Connection(beginning=self.airports['Porto'], end=self.airports['Lisbon']),
                            Connection(beginning=self.airports['Madrid'], end=self.airports['Lisbon']),
                            Connection(beginning=self.airports['Valencia'], end=self.airports['Lisbon']),
                            Connection(beginning=self.airports['Bilbao'], end=self.airports['Lisbon']),
                            Connection(beginning=self.airports['Algiers'], end=self.airports['Lisbon']),
                            Connection(beginning=self.airports['Porto'], end=self.airports['Bilbao']),
                            Connection(beginning=self.airports['Porto'], end=self.airports['Madrid']),
                            Connection(beginning=self.airports['Porto'], end=self.airports['Valencia']),
                            Connection(beginning=self.airports['Porto'], end=self.airports['Algiers']),
                            Connection(beginning=self.airports['Bilbao'], end=self.airports['Porto']),
                            Connection(beginning=self.airports['Madrid'], end=self.airports['Porto']),
                            Connection(beginning=self.airports['Valencia'], end=self.airports['Porto']),
                            Connection(beginning=self.airports['Algiers'], end=self.airports['Porto']),
                            Connection(beginning=self.airports['Bilbao'], end=self.airports['Nantes']),
                            Connection(beginning=self.airports['Bilbao'], end=self.airports['Bordeaux']),
                            Connection(beginning=self.airports['Bilbao'], end=self.airports['Toulouse']),
                            Connection(beginning=self.airports['Bilbao'], end=self.airports['Madrid']),
                            Connection(beginning=self.airports['Bilbao'], end=self.airports['Valencia']),
                            Connection(beginning=self.airports['Nantes'], end=self.airports['Bilbao']),
                            Connection(beginning=self.airports['Bordeaux'], end=self.airports['Bilbao']),
                            Connection(beginning=self.airports['Toulouse'], end=self.airports['Bilbao']),
                            Connection(beginning=self.airports['Madrid'], end=self.airports['Bilbao']),
                            Connection(beginning=self.airports['Valencia'], end=self.airports['Bilbao']),
                            Connection(beginning=self.airports['Madrid'], end=self.airports['Bordeaux']),
                            Connection(beginning=self.airports['Madrid'], end=self.airports['Toulouse']),
                            Connection(beginning=self.airports['Madrid'], end=self.airports['Valencia']),
                            Connection(beginning=self.airports['Madrid'], end=self.airports['Algiers']),
                            Connection(beginning=self.airports['Bordeaux'], end=self.airports['Madrid']),
                            Connection(beginning=self.airports['Toulouse'], end=self.airports['Madrid']),
                            Connection(beginning=self.airports['Valencia'], end=self.airports['Madrid']),
                            Connection(beginning=self.airports['Algiers'], end=self.airports['Madrid']),
                            Connection(beginning=self.airports['Valencia'], end=self.airports['Bordeaux']),
                            Connection(beginning=self.airports['Valencia'], end=self.airports['Toulouse']),
                            Connection(beginning=self.airports['Valencia'], end=self.airports['Algiers']),
                            Connection(beginning=self.airports['Valencia'], end=self.airports['Geneva']),
                            Connection(beginning=self.airports['Valencia'], end=self.airports['Pisa']),
                            Connection(beginning=self.airports['Valencia'], end=self.airports['Tunis']),
                            Connection(beginning=self.airports['Bordeaux'], end=self.airports['Valencia']),
                            Connection(beginning=self.airports['Toulouse'], end=self.airports['Valencia']),
                            Connection(beginning=self.airports['Algiers'], end=self.airports['Valencia']),
                            Connection(beginning=self.airports['Geneva'], end=self.airports['Valencia']),
                            Connection(beginning=self.airports['Pisa'], end=self.airports['Valencia']),
                            Connection(beginning=self.airports['Tunis'], end=self.airports['Valencia']),
                            Connection(beginning=self.airports['Algiers'], end=self.airports['Geneva']),
                            Connection(beginning=self.airports['Algiers'], end=self.airports['Pisa']),
                            Connection(beginning=self.airports['Algiers'], end=self.airports['Tunis']),
                            Connection(beginning=self.airports['Geneva'], end=self.airports['Algiers']),
                            Connection(beginning=self.airports['Pisa'], end=self.airports['Algiers']),
                            Connection(beginning=self.airports['Tunis'], end=self.airports['Algiers']),
                            Connection(beginning=self.airports['Nantes'], end=self.airports['Bristol']),
                            Connection(beginning=self.airports['Nantes'], end=self.airports['London']),
                            Connection(beginning=self.airports['Nantes'], end=self.airports['Paris']),
                            Connection(beginning=self.airports['Nantes'], end=self.airports['Geneva']),
                            Connection(beginning=self.airports['Nantes'], end=self.airports['Bordeaux']),
                            Connection(beginning=self.airports['Bristol'], end=self.airports['Nantes']),
                            Connection(beginning=self.airports['London'], end=self.airports['Nantes']),
                            Connection(beginning=self.airports['Paris'], end=self.airports['Nantes']),
                            Connection(beginning=self.airports['Geneva'], end=self.airports['Nantes']),
                            Connection(beginning=self.airports['Bordeaux'], end=self.airports['Nantes']),
                            Connection(beginning=self.airports['Bordeaux'], end=self.airports['Paris']),
                            Connection(beginning=self.airports['Bordeaux'], end=self.airports['Geneva']),
                            Connection(beginning=self.airports['Bordeaux'], end=self.airports['Pisa']),
                            Connection(beginning=self.airports['Bordeaux'], end=self.airports['Toulouse']),
                            Connection(beginning=self.airports['Paris'], end=self.airports['Bordeaux']),
                            Connection(beginning=self.airports['Geneva'], end=self.airports['Bordeaux']),
                            Connection(beginning=self.airports['Pisa'], end=self.airports['Bordeaux']),
                            Connection(beginning=self.airports['Toulouse'], end=self.airports['Bordeaux']),
                            Connection(beginning=self.airports['Toulouse'], end=self.airports['Geneva']),
                            Connection(beginning=self.airports['Toulouse'], end=self.airports['Turin']),
                            Connection(beginning=self.airports['Toulouse'], end=self.airports['Pisa']),
                            Connection(beginning=self.airports['Toulouse'], end=self.airports['Tunis']),
                            Connection(beginning=self.airports['Geneva'], end=self.airports['Toulouse']),
                            Connection(beginning=self.airports['Turin'], end=self.airports['Toulouse']),
                            Connection(beginning=self.airports['Pisa'], end=self.airports['Toulouse']),
                            Connection(beginning=self.airports['Tunis'], end=self.airports['Toulouse']),
                            Connection(beginning=self.airports['Tunis'], end=self.airports['Turin']),
                            Connection(beginning=self.airports['Tunis'], end=self.airports['Pisa']),
                            Connection(beginning=self.airports['Tunis'], end=self.airports['Rome']),
                            Connection(beginning=self.airports['Tunis'], end=self.airports['Palermo']),
                            Connection(beginning=self.airports['Tunis'], end=self.airports['Catania']),
                            Connection(beginning=self.airports['Turin'], end=self.airports['Tunis']),
                            Connection(beginning=self.airports['Pisa'], end=self.airports['Tunis']),
                            Connection(beginning=self.airports['Rome'], end=self.airports['Tunis']),
                            Connection(beginning=self.airports['Palermo'], end=self.airports['Tunis']),
                            Connection(beginning=self.airports['Catania'], end=self.airports['Tunis']),
                            Connection(beginning=self.airports['Bristol'], end=self.airports['London']),
                            Connection(beginning=self.airports['Bristol'], end=self.airports['Amsterdam']),
                            Connection(beginning=self.airports['Bristol'], end=self.airports['Antwerp']),
                            Connection(beginning=self.airports['London'], end=self.airports['Bristol']),
                            Connection(beginning=self.airports['Amsterdam'], end=self.airports['Bristol']),
                            Connection(beginning=self.airports['Antwerp'], end=self.airports['Bristol']),
                            Connection(beginning=self.airports['London'], end=self.airports['Amsterdam']),
                            Connection(beginning=self.airports['London'], end=self.airports['Antwerp']),
                            Connection(beginning=self.airports['London'], end=self.airports['Brussels']),
                            Connection(beginning=self.airports['London'], end=self.airports['Luxembourg City']),
                            Connection(beginning=self.airports['London'], end=self.airports['Paris']),
                            Connection(beginning=self.airports['Amsterdam'], end=self.airports['London']),
                            Connection(beginning=self.airports['Antwerp'], end=self.airports['London']),
                            Connection(beginning=self.airports['Brussels'], end=self.airports['London']),
                            Connection(beginning=self.airports['Luxembourg City'], end=self.airports['London']),
                            Connection(beginning=self.airports['Paris'], end=self.airports['London']),
                            Connection(beginning=self.airports['Paris'], end=self.airports['Amsterdam']),
                            Connection(beginning=self.airports['Paris'], end=self.airports['Antwerp']),
                            Connection(beginning=self.airports['Paris'], end=self.airports['Brussels']),
                            Connection(beginning=self.airports['Paris'], end=self.airports['Luxembourg City']),
                            Connection(beginning=self.airports['Paris'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Paris'], end=self.airports['Geneva']),
                            Connection(beginning=self.airports['Amsterdam'], end=self.airports['Paris']),
                            Connection(beginning=self.airports['Antwerp'], end=self.airports['Paris']),
                            Connection(beginning=self.airports['Brussels'], end=self.airports['Paris']),
                            Connection(beginning=self.airports['Luxembourg City'], end=self.airports['Paris']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Paris']),
                            Connection(beginning=self.airports['Geneva'], end=self.airports['Paris']),
                            Connection(beginning=self.airports['Amsterdam'], end=self.airports['Antwerp']),
                            Connection(beginning=self.airports['Amsterdam'], end=self.airports['Cologne']),
                            Connection(beginning=self.airports['Amsterdam'], end=self.airports['Prague']),
                            Connection(beginning=self.airports['Amsterdam'], end=self.airports['Berlin']),
                            Connection(beginning=self.airports['Antwerp'], end=self.airports['Amsterdam']),
                            Connection(beginning=self.airports['Cologne'], end=self.airports['Amsterdam']),
                            Connection(beginning=self.airports['Prague'], end=self.airports['Amsterdam']),
                            Connection(beginning=self.airports['Berlin'], end=self.airports['Amsterdam']),
                            Connection(beginning=self.airports['Antwerp'], end=self.airports['Brussels']),
                            Connection(beginning=self.airports['Antwerp'], end=self.airports['Cologne']),
                            Connection(beginning=self.airports['Brussels'], end=self.airports['Antwerp']),
                            Connection(beginning=self.airports['Cologne'], end=self.airports['Antwerp']),
                            Connection(beginning=self.airports['Brussels'], end=self.airports['Cologne']),
                            Connection(beginning=self.airports['Brussels'], end=self.airports['Luxembourg City']),
                            Connection(beginning=self.airports['Brussels'], end=self.airports['Frankfurt']),
                            Connection(beginning=self.airports['Cologne'], end=self.airports['Brussels']),
                            Connection(beginning=self.airports['Luxembourg City'], end=self.airports['Brussels']),
                            Connection(beginning=self.airports['Frankfurt'], end=self.airports['Brussels']),
                            Connection(beginning=self.airports['Luxembourg City'], end=self.airports['Cologne']),
                            Connection(beginning=self.airports['Luxembourg City'], end=self.airports['Frankfurt']),
                            Connection(beginning=self.airports['Luxembourg City'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Luxembourg City'], end=self.airports['Geneva']),
                            Connection(beginning=self.airports['Cologne'], end=self.airports['Luxembourg City']),
                            Connection(beginning=self.airports['Frankfurt'], end=self.airports['Luxembourg City']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Luxembourg City']),
                            Connection(beginning=self.airports['Geneva'], end=self.airports['Luxembourg City']),
                            Connection(beginning=self.airports['Cologne'], end=self.airports['Berlin']),
                            Connection(beginning=self.airports['Cologne'], end=self.airports['Prague']),
                            Connection(beginning=self.airports['Cologne'], end=self.airports['Frankfurt']),
                            Connection(beginning=self.airports['Berlin'], end=self.airports['Cologne']),
                            Connection(beginning=self.airports['Prague'], end=self.airports['Cologne']),
                            Connection(beginning=self.airports['Frankfurt'], end=self.airports['Cologne']),
                            Connection(beginning=self.airports['Frankfurt'], end=self.airports['Geneva']),
                            Connection(beginning=self.airports['Frankfurt'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Frankfurt'], end=self.airports['Nuremberg']),
                            Connection(beginning=self.airports['Frankfurt'], end=self.airports['Prague']),
                            Connection(beginning=self.airports['Geneva'], end=self.airports['Frankfurt']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Frankfurt']),
                            Connection(beginning=self.airports['Nuremberg'], end=self.airports['Frankfurt']),
                            Connection(beginning=self.airports['Prague'], end=self.airports['Frankfurt']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Geneva']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Turin']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Milan']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Verona']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Venice']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Zagreb']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Salzburg']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Munich']),
                            Connection(beginning=self.airports['Stuttgart'], end=self.airports['Nuremberg']),
                            Connection(beginning=self.airports['Geneva'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Turin'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Milan'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Verona'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Verona'], end=self.airports['Munich']),
                            Connection(beginning=self.airports['Munich'], end=self.airports['Verona']),
                            Connection(beginning=self.airports['Venice'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Zagreb'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Salzburg'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Munich'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Nuremberg'], end=self.airports['Stuttgart']),
                            Connection(beginning=self.airports['Turin'], end=self.airports['Geneva']),
                            Connection(beginning=self.airports['Turin'], end=self.airports['Milan']),
                            Connection(beginning=self.airports['Turin'], end=self.airports['Pisa']),
                            Connection(beginning=self.airports['Geneva'], end=self.airports['Turin']),
                            Connection(beginning=self.airports['Milan'], end=self.airports['Turin']),
                            Connection(beginning=self.airports['Pisa'], end=self.airports['Turin']),
                            Connection(beginning=self.airports['Pisa'], end=self.airports['Milan']),
                            Connection(beginning=self.airports['Pisa'], end=self.airports['Bologna']),
                            Connection(beginning=self.airports['Pisa'], end=self.airports['Split']),
                            Connection(beginning=self.airports['Pisa'], end=self.airports['Rome']),
                            Connection(beginning=self.airports['Milan'], end=self.airports['Pisa']),
                            Connection(beginning=self.airports['Bologna'], end=self.airports['Pisa']),
                            Connection(beginning=self.airports['Split'], end=self.airports['Pisa']),
                            Connection(beginning=self.airports['Rome'], end=self.airports['Pisa']),
                            Connection(beginning=self.airports['Bologna'], end=self.airports['Milan']),
                            Connection(beginning=self.airports['Bologna'], end=self.airports['Verona']),
                            Connection(beginning=self.airports['Bologna'], end=self.airports['Venice']),
                            Connection(beginning=self.airports['Bologna'], end=self.airports['Split']),
                            Connection(beginning=self.airports['Bologna'], end=self.airports['Naples']),
                            Connection(beginning=self.airports['Bologna'], end=self.airports['Rome']),
                            Connection(beginning=self.airports['Milan'], end=self.airports['Bologna']),
                            Connection(beginning=self.airports['Verona'], end=self.airports['Bologna']),
                            Connection(beginning=self.airports['Venice'], end=self.airports['Bologna']),
                            Connection(beginning=self.airports['Split'], end=self.airports['Bologna']),
                            Connection(beginning=self.airports['Naples'], end=self.airports['Bologna']),
                            Connection(beginning=self.airports['Rome'], end=self.airports['Bologna']),
                            Connection(beginning=self.airports['Milan'], end=self.airports['Verona']),
                            Connection(beginning=self.airports['Verona'], end=self.airports['Milan']),
                            Connection(beginning=self.airports['Venice'], end=self.airports['Verona']),
                            Connection(beginning=self.airports['Venice'], end=self.airports['Munich']),
                            Connection(beginning=self.airports['Venice'], end=self.airports['Salzburg']),
                            Connection(beginning=self.airports['Venice'], end=self.airports['Zagreb']),
                            Connection(beginning=self.airports['Venice'], end=self.airports['Split']),
                            Connection(beginning=self.airports['Venice'], end=self.airports['Naples']),
                            Connection(beginning=self.airports['Venice'], end=self.airports['Rome']),
                            Connection(beginning=self.airports['Verona'], end=self.airports['Venice']),
                            Connection(beginning=self.airports['Munich'], end=self.airports['Venice']),
                            Connection(beginning=self.airports['Salzburg'], end=self.airports['Venice']),
                            Connection(beginning=self.airports['Zagreb'], end=self.airports['Venice']),
                            Connection(beginning=self.airports['Split'], end=self.airports['Venice']),
                            Connection(beginning=self.airports['Naples'], end=self.airports['Venice']),
                            Connection(beginning=self.airports['Rome'], end=self.airports['Venice']),
                            Connection(beginning=self.airports['Rome'], end=self.airports['Split']),
                            Connection(beginning=self.airports['Rome'], end=self.airports['Naples']),
                            Connection(beginning=self.airports['Rome'], end=self.airports['Palermo']),
                            Connection(beginning=self.airports['Split'], end=self.airports['Rome']),
                            Connection(beginning=self.airports['Naples'], end=self.airports['Rome']),
                            Connection(beginning=self.airports['Palermo'], end=self.airports['Rome']),
                            Connection(beginning=self.airports['Palermo'], end=self.airports['Naples']),
                            Connection(beginning=self.airports['Palermo'], end=self.airports['Catania']),
                            Connection(beginning=self.airports['Palermo'], end=self.airports['Corfu']),
                            Connection(beginning=self.airports['Naples'], end=self.airports['Palermo']),
                            Connection(beginning=self.airports['Catania'], end=self.airports['Palermo']),
                            Connection(beginning=self.airports['Corfu'], end=self.airports['Palermo']),
                            Connection(beginning=self.airports['Catania'], end=self.airports['Naples']),
                            Connection(beginning=self.airports['Catania'], end=self.airports['Corfu']),
                            Connection(beginning=self.airports['Catania'], end=self.airports['Athens']),
                            Connection(beginning=self.airports['Naples'], end=self.airports['Catania']),
                            Connection(beginning=self.airports['Corfu'], end=self.airports['Catania']),
                            Connection(beginning=self.airports['Athens'], end=self.airports['Catania']),
                            Connection(beginning=self.airports['Corfu'], end=self.airports['Naples']),
                            Connection(beginning=self.airports['Corfu'], end=self.airports['Split']),
                            Connection(beginning=self.airports['Corfu'], end=self.airports['Belgrade']),
                            Connection(beginning=self.airports['Corfu'], end=self.airports['Sofia']),
                            Connection(beginning=self.airports['Corfu'], end=self.airports['Thessaloniki']),
                            Connection(beginning=self.airports['Corfu'], end=self.airports['Athens']),
                            Connection(beginning=self.airports['Naples'], end=self.airports['Corfu']),
                            Connection(beginning=self.airports['Split'], end=self.airports['Corfu']),
                            Connection(beginning=self.airports['Belgrade'], end=self.airports['Corfu']),
                            Connection(beginning=self.airports['Sofia'], end=self.airports['Corfu']),
                            Connection(beginning=self.airports['Thessaloniki'], end=self.airports['Corfu']),
                            Connection(beginning=self.airports['Athens'], end=self.airports['Corfu']),
                            Connection(beginning=self.airports['Athens'], end=self.airports['Thessaloniki']),
                            Connection(beginning=self.airports['Athens'], end=self.airports['Sofia']),
                            Connection(beginning=self.airports['Thessaloniki'], end=self.airports['Athens']),
                            Connection(beginning=self.airports['Sofia'], end=self.airports['Athens']),
                            Connection(beginning=self.airports['Thessaloniki'], end=self.airports['Split']),
                            Connection(beginning=self.airports['Thessaloniki'], end=self.airports['Belgrade']),
                            Connection(beginning=self.airports['Thessaloniki'], end=self.airports['Sofia']),
                            Connection(beginning=self.airports['Split'], end=self.airports['Thessaloniki']),
                            Connection(beginning=self.airports['Belgrade'], end=self.airports['Thessaloniki']),
                            Connection(beginning=self.airports['Sofia'], end=self.airports['Thessaloniki']),
                            Connection(beginning=self.airports['Sofia'], end=self.airports['Split']),
                            Connection(beginning=self.airports['Sofia'], end=self.airports['Belgrade']),
                            Connection(beginning=self.airports['Sofia'], end=self.airports['Budapest']),
                            Connection(beginning=self.airports['Sofia'], end=self.airports['Krakow']),
                            Connection(beginning=self.airports['Split'], end=self.airports['Sofia']),
                            Connection(beginning=self.airports['Belgrade'], end=self.airports['Sofia']),
                            Connection(beginning=self.airports['Budapest'], end=self.airports['Sofia']),
                            Connection(beginning=self.airports['Krakow'], end=self.airports['Sofia']),
                            Connection(beginning=self.airports['Belgrade'], end=self.airports['Naples']),
                            Connection(beginning=self.airports['Belgrade'], end=self.airports['Split']),
                            Connection(beginning=self.airports['Belgrade'], end=self.airports['Zagreb']),
                            Connection(beginning=self.airports['Belgrade'], end=self.airports['Vienna']),
                            Connection(beginning=self.airports['Belgrade'], end=self.airports['Budapest']),
                            Connection(beginning=self.airports['Naples'], end=self.airports['Belgrade']),
                            Connection(beginning=self.airports['Split'], end=self.airports['Belgrade']),
                            Connection(beginning=self.airports['Zagreb'], end=self.airports['Belgrade']),
                            Connection(beginning=self.airports['Vienna'], end=self.airports['Belgrade']),
                            Connection(beginning=self.airports['Budapest'], end=self.airports['Belgrade']),
                            Connection(beginning=self.airports['Budapest'], end=self.airports['Zagreb']),
                            Connection(beginning=self.airports['Budapest'], end=self.airports['Vienna']),
                            Connection(beginning=self.airports['Budapest'], end=self.airports['Prague']),
                            Connection(beginning=self.airports['Budapest'], end=self.airports['Wroclaw']),
                            Connection(beginning=self.airports['Budapest'], end=self.airports['Krakow']),
                            Connection(beginning=self.airports['Zagreb'], end=self.airports['Budapest']),
                            Connection(beginning=self.airports['Vienna'], end=self.airports['Budapest']),
                            Connection(beginning=self.airports['Prague'], end=self.airports['Budapest']),
                            Connection(beginning=self.airports['Wroclaw'], end=self.airports['Budapest']),
                            Connection(beginning=self.airports['Krakow'], end=self.airports['Budapest']),
                            Connection(beginning=self.airports['Vienna'], end=self.airports['Split']),
                            Connection(beginning=self.airports['Vienna'], end=self.airports['Zagreb']),
                            Connection(beginning=self.airports['Vienna'], end=self.airports['Salzburg']),
                            Connection(beginning=self.airports['Vienna'], end=self.airports['Munich']),
                            Connection(beginning=self.airports['Vienna'], end=self.airports['Nuremberg']),
                            Connection(beginning=self.airports['Vienna'], end=self.airports['Prague']),
                            Connection(beginning=self.airports['Vienna'], end=self.airports['Wroclaw']),
                            Connection(beginning=self.airports['Vienna'], end=self.airports['Krakow']),
                            Connection(beginning=self.airports['Split'], end=self.airports['Vienna']),
                            Connection(beginning=self.airports['Zagreb'], end=self.airports['Vienna']),
                            Connection(beginning=self.airports['Salzburg'], end=self.airports['Vienna']),
                            Connection(beginning=self.airports['Munich'], end=self.airports['Vienna']),
                            Connection(beginning=self.airports['Nuremberg'], end=self.airports['Vienna']),
                            Connection(beginning=self.airports['Prague'], end=self.airports['Vienna']),
                            Connection(beginning=self.airports['Wroclaw'], end=self.airports['Vienna']),
                            Connection(beginning=self.airports['Krakow'], end=self.airports['Vienna']),
                            Connection(beginning=self.airports['Salzburg'], end=self.airports['Zagreb']),
                            Connection(beginning=self.airports['Salzburg'], end=self.airports['Munich']),
                            Connection(beginning=self.airports['Salzburg'], end=self.airports['Prague']),
                            Connection(beginning=self.airports['Zagreb'], end=self.airports['Salzburg']),
                            Connection(beginning=self.airports['Munich'], end=self.airports['Salzburg']),
                            Connection(beginning=self.airports['Prague'], end=self.airports['Salzburg']),
                            Connection(beginning=self.airports['Munich'], end=self.airports['Nuremberg']),
                            Connection(beginning=self.airports['Munich'], end=self.airports['Prague']),
                            Connection(beginning=self.airports['Munich'], end=self.airports['Wroclaw']),
                            Connection(beginning=self.airports['Munich'], end=self.airports['Krakow']),
                            Connection(beginning=self.airports['Nuremberg'], end=self.airports['Munich']),
                            Connection(beginning=self.airports['Prague'], end=self.airports['Munich']),
                            Connection(beginning=self.airports['Wroclaw'], end=self.airports['Munich']),
                            Connection(beginning=self.airports['Krakow'], end=self.airports['Munich']),
                            Connection(beginning=self.airports['Nuremberg'], end=self.airports['Berlin']),
                            Connection(beginning=self.airports['Nuremberg'], end=self.airports['Prague']),
                            Connection(beginning=self.airports['Nuremberg'], end=self.airports['Krakow']),
                            Connection(beginning=self.airports['Berlin'], end=self.airports['Nuremberg']),
                            Connection(beginning=self.airports['Prague'], end=self.airports['Nuremberg']),
                            Connection(beginning=self.airports['Krakow'], end=self.airports['Nuremberg']),
                            Connection(beginning=self.airports['Berlin'], end=self.airports['Prague']),
                            Connection(beginning=self.airports['Berlin'], end=self.airports['Wroclaw']),
                            Connection(beginning=self.airports['Berlin'], end=self.airports['Warsaw']),
                            Connection(beginning=self.airports['Prague'], end=self.airports['Berlin']),
                            Connection(beginning=self.airports['Wroclaw'], end=self.airports['Berlin']),
                            Connection(beginning=self.airports['Warsaw'], end=self.airports['Berlin']),
                            Connection(beginning=self.airports['Wroclaw'], end=self.airports['Prague']),
                            Connection(beginning=self.airports['Wroclaw'], end=self.airports['Warsaw']),
                            Connection(beginning=self.airports['Wroclaw'], end=self.airports['Krakow']),
                            Connection(beginning=self.airports['Prague'], end=self.airports['Wroclaw']),
                            Connection(beginning=self.airports['Warsaw'], end=self.airports['Wroclaw']),
                            Connection(beginning=self.airports['Krakow'], end=self.airports['Wroclaw']),
                            Connection(beginning=self.airports['Krakow'], end=self.airports['Warsaw']),
                            Connection(beginning=self.airports['Warsaw'], end=self.airports['Krakow']),
                            ]

        # Case 2 airport weights test
        # self.airports = {'A': Airport(name='A', country='country_1', coord_x=300, coord_y=300),
        #                  'B': Airport(name='B', country='country_2', coord_x=200, coord_y=300),
        #                  'C': Airport(name='C', country='country_3', coord_x=400, coord_y=300),
        #                  'D': Airport(name='D', country='country_4', coord_x=300, coord_y=200),
        #                  'E': Airport(name='E', country='country_5', coord_x=300, coord_y=400),
        #                  }
        #
        # self.connections = [Connection(beginning=self.airports['A'], end=self.airports['B'], distance=1000),
        #                     Connection(beginning=self.airports['B'], end=self.airports['A'], distance=1000),
        #                     Connection(beginning=self.airports['A'], end=self.airports['C'], distance=2000),
        #                     Connection(beginning=self.airports['C'], end=self.airports['A'], distance=2000),
        #                     Connection(beginning=self.airports['A'], end=self.airports['D'], distance=3000),
        #                     Connection(beginning=self.airports['D'], end=self.airports['A'], distance=3000),
        #                     Connection(beginning=self.airports['A'], end=self.airports['E'], distance=4000),
        #                     Connection(beginning=self.airports['E'], end=self.airports['A'], distance=4000), ]
        # Case 1 first iteration
        # self.airports = {'A': Airport(name='A', country='country_1', coord_x=30, coord_y=30),
        #                  'B': Airport(name='B', country='country_1', coord_x=100, coord_y=100),
        #                  'C': Airport(name='C', country='country_2', coord_x=100, coord_y=200),
        #                  'D': Airport(name='D', country='country_2', coord_x=200, coord_y=300),
        #                  'E': Airport(name='E', country='country_3', coord_x=200, coord_y=400),
        #                  'F': Airport(name='F', country='country_4', coord_x=300, coord_y=100),
        #                  'G': Airport(name='G', country='country_5', coord_x=300, coord_y=200),
        #
        #   }
        #
        # self.connections = [Connection(beginning=self.airports['A'], end=self.airports['B'], distance=7000),
        #                     Connection(beginning=self.airports['B'], end=self.airports['A'], distance=4000),
        #                     Connection(beginning=self.airports['A'], end=self.airports['F'], distance=4000),
        #                     Connection(beginning=self.airports['A'], end=self.airports['D'], distance=5000),
        #                     Connection(beginning=self.airports['B'], end=self.airports['C'], distance=2000),
        #                     Connection(beginning=self.airports['C'], end=self.airports['E'], distance=2500),
        #                     Connection(beginning=self.airports['E'], end=self.airports['G'], distance=5000),
        #                     Connection(beginning=self.airports['G'], end=self.airports['F'], distance=3000),
        #                     Connection(beginning=self.airports['F'], end=self.airports['G'], distance=2500),
        #                     Connection(beginning=self.airports['G'], end=self.airports['B'], distance=3000),
        #                     Connection(beginning=self.airports['D'], end=self.airports['F'], distance=4000),
        #                     Connection(beginning=self.airports['F'], end=self.airports['D'], distance=3000), ]

        # Filtering disabled countries
        for airport in list(self.airports.values()):
            if airport.country in disabled_countries:
                self.airports.pop(airport.name)

        self.connections = [x for x in self.connections if
                            x.beginning.country not in disabled_countries and x.end.country not in disabled_countries]

        # Filtering disables cities
        for airport in list(self.airports.values()):
            if airport.name in disabled_cities:
                self.airports.pop(airport.name)

        self.connections = [x for x in self.connections if
                            x.beginning.name not in disabled_cities and x.end.name not in disabled_cities]

        for connection in self.connections:
            self.airports[connection.beginning.name].outgoing_connections.append(connection)


class AirplaneState(Enum):
    STATIONARY = 1
    IN_FLIGHT = 2


class Airplane:
    def __init__(self, last_landing=None, state=AirplaneState.STATIONARY, distance_traveled=0, connection=None):
        # Name of last landing location
        self.last_landing = last_landing

        # If it's flying or not
        self.state = state

        # How far has it already traveled
        self.distance_traveled = distance_traveled

        # Connection on which the plane is flying
        self.connection = connection

        # Data of which countries has this airplane visited recently
        self.country_history = []

        if last_landing is not None:
            self.country_history.append(last_landing.country)


class Airport:
    def __init__(self, name, country, coord_x=0, coord_y=0, times_visited=0, possible_destinations=None):

        # Name of airport, also it's ID
        self.name = name

        # Country in which this airport is located
        self.country = country

        # One of coordinates used to visualize the aiport
        self.coord_x = coord_x

        # Other coordinate
        self.coord_y = coord_y

        # How many times this airport has been visited (one airplane landed and took off)
        self.times_visited = times_visited

        # List of airports connected to this one
        if possible_destinations is not None:
            self.outgoing_connections = possible_destinations
        else:
            self.outgoing_connections = []


class Connection:
    def __init__(self, beginning, end, distance=None):
        # Order of those 2 objects matters, connection has a direction
        self.beginning = beginning
        self.end = end

        # If None - calculate from coords
        if distance is not None:
            self.distance = distance
        else:
            self.distance = math.sqrt(
                math.pow(end.coord_x - beginning.coord_x, 2) + pow(end.coord_y - beginning.coord_y, 2)) * 1.8

        if beginning.name == 'Paris' and end.name == 'London':
            print(self.distance)
        # Check if any plane is currently on a given connection
        self.is_occupied = False

        # How many times a plane used this connection
        self.times_used = 0
