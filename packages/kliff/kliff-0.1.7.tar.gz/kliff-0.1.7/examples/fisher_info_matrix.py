from kliff.dataset import DataSet
from kliff.fisher import Fisher
from kliff.kimcalculator import KIMCalculator
from kliff.modelparameters import ModelParameters

# KIM model parameters
model = "Three_Body_Stillinger_Weber_Si__MO_405512056662_004"
params = ModelParameters(model)
fname = "../tests/input/Si_SW_init_guess.txt"
params.read(fname)

# training set
tset = DataSet()
tset.read("../tests/training_set/Si_T300_4")
configs = tset.get_configurations()

# calculator
calc = KIMCalculator(model)
calc.create(configs)

# Fisher
fisher = Fisher(params, calc)
fim, fim_std = fisher.compute()

print("Fisher information:")
print(fim)
print("Stdandard deviation of Fisher information:")
print(fim_std)
