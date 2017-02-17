from ase.atoms import string2symbols

formation_energies={}
abinitio_energies={}

def make_input_file(file_name,energy_dict,abinitio_energies):
    #create a header
    header = '\t'.join(['surface_name','site_name',
                        'species_name','formation_energy',
                        'frequencies','reference'])
    lines = [] #list of lines in the output
    
    g=open('formatted_energies.txt','r')
    
    for i,line in enumerate(g): #iterate through keys
        if i!=0:
            print i
            #line.strip('')
            print line
            surface,site,name,E,frequency,ref=line.split()
            
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
