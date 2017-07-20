#!/home/vossj/suncat/bin/python

#SBATCH -p iric
#SBATCH --job-name=opt.py
#SBATCH --output=myjob.out
#SBATCH --error=myjob.err
#SBATCH --time=2:00:00                                 #default is 20 hours
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=END,FAIL                            #get emailed about job BEGIN, END, or FAIL
#SBATCH --mail-user=allegralatimer@gmail.com
#SBATCH --ntasks-per-node=16                            #task to run per node; each node has 16 cores

from catmap import ReactionModel
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
from catmap import analyze

def custom_fig(fig, title, save_name):
    for j, ax in enumerate(fig.axes):
        if j == 0:
            ax.set_ylabel(descriptor_labels[1],size = 25,fontproperties=font)
            ax.set_xlabel(descriptor_labels[0],size = 25,fontproperties=font)
            ax.set_title(title,size = 25,fontproperties=font)
            #ax.set_xticklabels([300,400,500,600,700,800],size=15)
            #ax.set_yticklabels([' ',-8,-7,-6,-5,-4,-3,-2,-1,0],size=15)
    fig.savefig(save_name)
    return

font0=FontProperties()
font = font0.copy()
font.set_style('italic')
font.set_weight('bold')
#font.set_size('32')


#change to reflect your descriptors
descriptor_labels = ['$\Delta E(C^*)/eV$', '$\Delta E(O^*)/eV$']
adjust_kwargs = {'left':0.2,'right':0.8,'bottom':0.2}

###### Run MKM ########
mkm_file = 'mechanism.mkm'
#mkm_file = 'mechanism.log'
model = ReactionModel(setup_file=mkm_file)
model.output_variables += ['rate','production_rate','rate_control', 'free_energy', 'electronic_energy','forward_rate_constant','reverse_rate_constant','carbon_selectivity','coverage']
model.run()

##### Model Analysis ######
vm = analyze.VectorMap(model)

vm.plot_variable = 'rate' #tell the model which output to plot
vm.log_scale = True #rates should be plotted on a log-scale
vm.min = 1e-25 #minimum rate to plot
vm.max = 1e3 #maximum rate to plot
fig = vm.plot(save='rate.pdf') #draw the plot and save it as "rate.pdf"

vm.plot_variable = 'coverage' #tell the model which output to plot
vm.log_scale = True #rates should be plotted on a log-scale
vm.min = 1e-5 #minimum rate to plot
vm.max = 1 #maximum rate to plot
fig = vm.plot(save='coverage.pdf') #draw the plot and save it as "coverage.pdf"

vm.production_rate_map = model.production_rate_map #attach map
vm.threshold = 1e-30 #do not plot rates below this
vm.plot_variable = 'production_rate'
vm.descriptor_labels = ['', '']
vm.subplots_adjust_kwargs = adjust_kwargs 
vm.plot(save='pretty_production_rate.pdf')

#example of how to plot TOF for one product
vm.plot_variable = 'production_rate'
vm.log_scale = True
vm.min = 1e-25
vm.max = 1e0
vm.include_labels = ['CO_g']
vm.subplots_adjust_kwargs = adjust_kwargs 
fig = vm.plot(save='CO_g.pdf')
custom_fig(fig, '$\mathbf{CO TOF}$','CO_tof.pdf')

#example of how to plot selectivity to a product
vm.plot_variable = 'carbon_selectivity'
vm.log_scale = True
vm.min = 1e-5
vm.max = 1
vm.include_labels = ['CO_g']
vm.subplots_adjust_kwargs = adjust_kwargs 
fig = vm.plot(save='CO_sel.pdf')
custom_fig(fig, '$\mathbf{CO Selectivity}$','CO_sel.pdf')

#example of how to plot coverage of a single adsorbate
vm.plot_variable = 'coverage'
vm.log_scale = True
vm.min = 1e-2
vm.max = 0.5

vm.include_labels = ['C_s']
vm.subplots_adjust_kwargs = adjust_kwargs 
fig = vm.plot(save='C_s.pdf')
custom_fig(fig, '$\mathbf{C_{s} Coverage}$','C_s.pdf')

vm.include_labels = ['O_s']
vm.subplots_adjust_kwargs = adjust_kwargs 
fig = vm.plot(save='O_s.pdf')
custom_fig(fig, '$\mathbf{O_{s} Coverage}$','O_s.pdf')


