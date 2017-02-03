from ase.atoms import string2symbols

abinitio_energies = {
"   H2_g    ":[ -32.94192723    ,   [4442.4]    ],
"   CH4_g   ":[ -231.6023858    ,   [3116.9,3112.8,3110.5,3021.9,1544.7, 1542.8, 1330.5, 1327.0, 1317.7]    ],
"   CH3OH_g ":[ -693.8293839    ,   [281.4, 1002.8, 1066.1, 1153.6, 1354.1, 1459.0, 1478.9, 1492.9, 2964.4, 3018.9, 3089.1, 3773.9] ],
"   CH2O_g  ":[ -659.762148 ,   [2900.3, 2851.0, 1765.5, 1508.3, 1238.6, 1162.2]    ],
"   CO_g    ":[ -626.575032 ,   [2152.3]    ],
"   CO2_g   ":[ -1090.80083 ,   [637.5, 1320.3, 2369.4] ],
"   HCOOH_g ":[ -1123.610214    ,   [73.6, 86.0, 113.8, 604.3, 671.2, 1015.5, 1072.9, 1277.7, 1379.6, 1764.4, 3020.0, 3665.6]   ],
"   O2_g    ":[ -922.222    ,   [29.0, 110.7, 1548.9]   ],
"   H2O_g   ":[ -496.2715336    ,   [3848.3, 3737.4, 1616.1]    ],
"   HCOOCH3_g   ":[ -1320.809649    ,   [56.0, 36.1, 77.0, 95.0, 190.0, 338.4, 614.7, 982.5, 996.2, 1083.4, 1146.3, 1210.9, 1385.4, 1453.9, 1478.2, 1485.6, 1782.7, 2920.0, 3020.8, 3082.2, 3135.3]    ],
                        
"   slab_c  ":[ -57281.96866    ,   []  ],
"   slab_b  ":[ -56818.41942    ,   []  ],
"   slab_0b ":[ -56355.18669    ,   []  ],
                        
"   CH3OH_c ":[ -57977.07416    ,   [55.68300000000001, 116.20800000000001, 121.857, 163.821, 200.13600000000002, 319.572, 744.0540000000001, 964.365, 1138.677, 1161.2730000000001, 1430.8110000000001, 1455.0210000000002, 1477.617, 1488.915, 3018.987, 3098.88, 3144.072, 3308.7000000000003]    ],
"   OCH3_c  ":[ -57959.63725    ,   [56.49, 61.332, 144.453, 164.628, 215.469, 558.4440000000001, 1045.065, 1063.6260000000002, 1149.9750000000001, 1400.952, 1436.46, 1442.109, 2942.322, 3002.04, 3039.1620000000003]    ],
"   OCH2_c  ":[ -57942.82011    ,   [86.349, 108.94500000000001, 179.154, 204.978, 271.15200000000004, 376.869, 1145.133, 1241.9730000000002, 1496.178, 1676.139, 2977.023, 3102.1079999999997]   ],
"   O_c ":[ -57744.02674    ,   [170.27700000000002, 270.345, 810.2280000000001]    ],
"   O_b ":[ -57281.96866    ,   [232.41600000000003, 418.026, 439.008]  ],
"   OH_c    ":[ -57761.79054    ,   [178.347, 229.188, 256.62600000000003, 790.0530000000001, 836.859, 3517.7129999999997]  ],
"   OH_b    ":[ -57299.51599    ,   [197.715, 326.83500000000004, 363.15000000000003, 504.375, 836.052, 3735.603]   ],
"   H2O_c   ":[ -57779.39172    ,   [56.49, 153.33, 229.188, 301.818, 587.496, 750.51, 1592.2110000000002, 3573.396, 3738.831]  ],
"   OCHO_c  ":[ -58390.10501    ,   [122.664, 175.92600000000002, 200.94299999999998, 317.151, 328.449, 371.22, 740.826, 1001.487, 1294.428, 1384.005, 1453.407, 3012.5310000000004] ],
"   OCH2O_c ":[ -58405.322  ,   [118.8, 170.9, 185.3, 207.0, 422.1, 441.8, 575.3, 845.8, 902.5, 999.4, 1207.9, 1340.3, 1394.0, 2884.3, 2958.9]  ],
"   O2_c    ":[ -58205.07294    ,   [185.6, 193.0, 324.5, 371.3, 553.2, 926.0]  ],
                        
                        
"   O-O_c   ":[ -58204.75763    ,   [26.5, 209.6, 301.5, 631.9, 739.5]  ],
"   CH3-H-O_c   ":[ -58436.59472    ,   [46.9, 104.1, 113.6, 188.0, 262.2, 396.2, 438.7, 602.2, 636.2, 853.2, 1041.7, 1268.4, 1391.8, 1404.3, 3063.5, 3224.7, 3240.9]   ],
                        
                        
"   CH3O-H-O_c  ":[ -58438.9298 ,   [69.402, 131.541, 145.26, 188.031, 208.20600000000002, 266.31, 365.57099999999997, 588.3030000000001, 678.687, 986.1540000000001, 1123.344, 1144.326, 1180.641, 1450.986, 1465.512, 1471.161, 1543.7910000000002, 2985.9, 3058.53, 3091.617] ],
"   CH3O-H-O_b  ":[ -57976.92562    ,   [89.577, 130.734, 145.26, 240.48600000000002, 252.591, 368.79900000000004, 376.869, 430.131, 607.671, 1000.6800000000001, 1147.5539999999999, 1161.2730000000001, 1323.48, 1450.1789999999999, 1471.161, 1475.1960000000001, 1530.879, 2952.0060000000003, 3037.548, 3081.126]   ],
"   OCH2-H-O_c  ":[ -58420.99138    ,   [111.36600000000001, 154.944, 195.294, 242.907, 313.116, 388.16700000000003, 480.97200000000004, 548.76, 838.4730000000001, 1074.924, 1182.255, 1233.0960000000002, 1312.989, 1350.9180000000001, 1464.7050000000002, 2951.199, 3050.46]   ],
"   OCH2-H-O_b  ":[ -57958.96114    ,   [141.225, 171.89100000000002, 260.661, 318.765, 390.588, 489.84900000000005, 499.533, 591.531, 667.389, 1116.8880000000001, 1174.185, 1209.693, 1275.06, 1315.41, 1473.582, 2932.638, 3045.618]    ],
                        
                        
                        
"   O2CH-H-O_b  ":[ -58404.55945    ,   [56.0, 148.3, 190.9, 220.8, 282.4, 370.2, 378.8, 465.4, 731.9, 900.3, 1114.2, 1207.2, 1302.5, 1731.0]   ],
"   O2C-H-O_b   ":[ -58388.66389    ,   [56.0, 148.3, 190.9, 220.8, 282.4, 370.2, 378.8, 465.4, 731.9, 900.3, 1114.2, 1207.2, 1302.5, 1731.0]   ],
                        
                        
                        
"   O-H-O_b ":[ -57761.19536    ,   [145.26, 217.89, 455.148, 474.516, 624.618, 851.385, 1168.536, 1362.2]  ],
"   OH-H-O_b    ":[ -57779.22008    ,   [196.101, 217.083, 353.466, 401.9, 418.026, 547.95, 629.46, 808.614, 1324.287, 1547.019, 3730.76]   ],
"   OH-H-O_c    ":[ -58241.19688    ,   [169.47, 201.75, 232.41600000000003, 416.41200000000003, 455.148, 611.706, 689.985, 841.701, 1220.9910000000002, 1502.634, 3713.0070000000005] ],

"   CH3OH-_c    ":[ -57975.79716    ,   [55.68300000000001, 116.20800000000001, 121.857, 163.821, 200.13600000000002, 319.572, 744.0540000000001, 964.365, 1138.677, 1161.2730000000001, 1430.8110000000001, 1455.0210000000002, 1477.617, 1488.915, 3018.987, 3098.88, 3144.072, 3308.7000000000003] ],
"   H2O-_c  ":[ -57778.23972    ,   [56.49, 153.33, 229.188, 301.818, 587.496, 750.51, 1592.2110000000002, 3573.396, 3738.831]  ],
"   OCH2-_c ":[ -57941.73111    ,   [86.349, 108.94500000000001, 179.154, 204.978, 271.15200000000004, 376.869, 1145.133, 1241.9730000000002, 1496.178, 1676.139, 2977.023, 3102.1079999999997]   ],

    "   H2O_b   ":[ -57315.54447    ,   [80.3, 151.5, 227.5, 428.5, 454.3, 472.5, 1576.8, 3627.9, 3738.6]   ],
#   "   O-H-OH_b    ":[ no bar  ,       ],
    "   H2O-_b  ":[ -57314.69047    ,   [80.3, 151.5, 227.5, 428.5, 454.3, 472.5, 1576.8, 3627.9, 3738.6]   ],

             }
for key in abinitio_energies.keys():
    new_key = key.strip()
    abinitio_energies[new_key] = abinitio_energies.pop(key)

ref_dict = {}
ref_dict['H'] = 0.5*abinitio_energies['H2_g'][0]
ref_dict['O'] = abinitio_energies['H2O_g'][0] - 2*ref_dict['H']
ref_dict['C'] = abinitio_energies['CH4_g'][0] - 4*ref_dict['H']
ref_dict['c'] = abinitio_energies['slab_c'][0]
ref_dict['b'] = abinitio_energies['slab_b'][0]
ref_dict['o_ads'] = abinitio_energies['O_c'][0]
ref_dict['two_b'] = abinitio_energies['slab_0b'][0]

o_ads = ['CH3-H-O_c']

two_b = ['O-H-H-O_b']

def get_formation_energies(energy_dict,ref_dict):
    formation_energies = {}
    for key in energy_dict.keys(): #iterate through keys
        E0 = energy_dict[key][0] #raw energy
        name,site = key.split('_') #split key into name/site
        if 'slab' not in name: #do not include empty site energy (0)
            if site != 'g':
                if key in o_ads:
                    E0 -= ref_dict['o_ads'] #subtract slab energy if adsorbed
                elif key in two_b:
                    E0 -= ref_dict['two_b'] 
                else:
                    E0 -= ref_dict[site] 

            #remove - from transition-states
            formula = name.replace('-','')
            #print formula
            #get the composition as a list of atomic species
            composition = string2symbols(formula)
            #for each atomic species, subtract off the reference energy
            for atom in composition:
                E0 -= ref_dict[atom]
            #round to 3 decimals since this is the accuracy of DFT
            E0 = round(E0,3)
            formation_energies[key] = E0
    return formation_energies

formation_energies = get_formation_energies(abinitio_energies,ref_dict)

for key in formation_energies:
    print key, formation_energies[key]


def make_input_file(file_name,energy_dict,abinitio_energies):
    #create a header
    header = '\t'.join(['surface_name','site_name',
                        'species_name','formation_energy',
                        'frequencies','reference'])
    lines = [] #list of lines in the output
    for key in energy_dict.keys(): #iterate through keys
        E = energy_dict[key] #raw energy
        name,site = key.split('_') #split key into name/site
        if 'slab' not in name: #do not include empty site energy (0)
            frequency = abinitio_energies[key][1]
            if site == 'g':
                site = 'gas'
                surface = None
            else:
                surface = 'Ru'
            outline = [surface,site,name,E,frequency,'This Work, BEEF-vdw']
            line = '\t'.join([str(w) for w in outline])
            lines.append(line)
    lines.sort() #The file is easier to read if sorted (optional)
    lines = [header] + lines #add header to top
    input_file = '\n'.join(lines) #Join the lines with a line break
    input = open(file_name,'w') #open the file name in write mode
    input.write(input_file) #write the text
    input.close() #close the file
    print 'Successfully created input file'

file_name = 'energies.txt'
make_input_file(file_name,formation_energies,abinitio_energies)

#Test that input is parsed correctly
from catmap.model import ReactionModel
from catmap.parsers import TableParser
rxm = ReactionModel()
#The following lines are normally assigned by the setup_file
#and are thus not usually necessary.
rxm.surface_names = ['Ru']
rxm.adsorbate_names = ('O2','O','CH3OH')
rxm.transition_state_names = ('O-O','H-O-CH3')
rxm.gas_names = ('CH3OH_g','O2_g','CH4_g','H2O_g','H2_g')
rxm.site_names = ('s',)
rxm.species_definitions = {'s':{'site_names':['110c']}}
#Now we initialize a parser instance (also normally done by setup_file)
parser = TableParser(rxm)
parser.input_file = file_name
parser.parse()
#All structured data is stored in species_definitions; thus we can
#check that the parsing was successful by ensuring that all the
#data in the input file was collected in this dictionary.
for key in rxm.species_definitions:
    print key, rxm.species_definitions[key]
