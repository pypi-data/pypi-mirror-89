import numpy as np
import pandas as pd
import os

from svolfit import svolfit
    
dt=1.0/252.0
FILE='test_path.csv'
SERIES='asset'

dir_name = os.path.dirname(__file__)
file_path = os.path.join(dir_name, 'data', FILE)

#TODO: need to test that test data file exists...
series=pd.read_csv(file_path)
series=series[SERIES].to_numpy()
#print(series)

#TODO: test vpath as well.

models=['template','Heston','Heston','Heston','Bates','Bates','Bates','H32','B32','GARCHdiff','GARCHjdiff']
methods=['tree','tree','treeX2','grid','tree','treeX2','grid','grid','grid','grid','grid']

#for cc in range(0,len(models)):
#    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
#    print(pars)
#    print(junk)

def compare(testpars,pars):

    passed=True    
    for x in testpars:
        if( x in pars ):
            if( np.abs(testpars[x]-pars[x]) > 1.0e-10):
                passed = False
        else:
            passed = False

    return passed

def test_template():
    cc=0
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert not pars

def test_1():
    cc=1
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    testpars={'mu': -0.020125986627865067, 'theta': 0.004601872378995704, 'rho': -0.13995295241931954, 'alpha': 1.639070454809888, 'eta': 0.05483430121799801, 'q': 5.017155496202451, 'v0': 0.0050442224177215155, 'vT': 0.008524577734159055}
    assert compare(testpars,pars)

def test_2():
    cc=2
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    testpars={'mu': -0.019896024073659497, 'theta': 0.004564439415462577, 'rho': -0.13798540905020365, 'alpha': 1.630201398330046, 'eta': 0.054824502665627176, 'q': 4.951186694066523, 'v0': 0.005033519352794092, 'vT': 0.008577665008225781}
    assert compare(testpars,pars)

def test_3():
    cc=3
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    testpars={'mu': -0.019921258455721153, 'theta': 0.004669753765629827, 'rho': -0.14176784130257092, 'alpha': 1.4949754093539167, 'eta': 0.05308689025093166, 'q': 4.954313154029384, 'v0': 0.004503015079507199, 'vT': 0.008728921538737035}
    assert compare(testpars,pars)

def test_4():
    cc=4
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    testpars={'mu': -0.015172712676648383, 'theta': 0.004595329670686874, 'rho': -0.2916246495684411, 'alpha': 1.2642592750263475, 'eta': 0.04739771704327333, 'jumpintensity': 0.5958076459063104, 'jumpmean': -0.012117487676897139, 'jumpvolatility': 0.002000000000000002, 'q': 5.172112579810689, 'v0': 0.004661113895238095, 'vT': 0.008776627873960349}
    assert compare(testpars,pars)

def test_5():
    cc=5
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    testpars={'mu': -0.01489674797645721, 'theta': 0.004565259038688452, 'rho': -0.2931867405108989, 'alpha': 1.255140674802936, 'eta': 0.047309612837556456, 'jumpintensity': 1.195230120005545, 'jumpmean': -0.012115467408280026, 'jumpvolatility': 0.0020000001457076877, 'q': 5.12022489091278, 'v0': 0.004648349434012367, 'vT': 0.00887126749566859}
    assert compare(testpars,pars)

def test_6():
    cc=6
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    testpars={'mu': -0.021223302514863245, 'theta': 0.004482003774902545, 'rho': -0.39497808062417156, 'alpha': 0.9342193366483296, 'eta': 0.041363525790708344, 'jumpintensity': 9.975891380138686, 'jumpmean': -1.5305156697570884e-05, 'jumpvolatility': 0.005328729806358738, 'q': 4.894586011861112, 'v0': 0.003671292959578983, 'vT': 0.00873514531761896}
    assert compare(testpars,pars)

def test_7():
    cc=7
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    testpars={'mu': -0.01902204745297676, 'theta': 0.0036534952797811784, 'rho': -0.05572309682325205, 'alpha': 1.6050788714494955, 'eta': 0.051343264376896285, 'q': 4.449056994794761, 'v0': 0.005424198899706855, 'vT': 0.008588314924535852}
    assert compare(testpars,pars)

def test_8():
    cc=8
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    testpars={'mu': -0.014561306023665965, 'theta': 0.003643956709640766, 'rho': -0.21350257254278232, 'alpha': 1.3197642991121314, 'eta': 0.04539342298541184, 'jumpintensity': 0.6326380331108526, 'jumpmean': -0.011924932545179876, 'jumpvolatility': 0.0021, 'q': 4.6678158563500585, 'v0': 0.004364565679458361, 'vT': 0.009627718410569914}
    assert compare(testpars,pars)

def test_9():
    cc=9
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    testpars={'mu': -0.020295321449618944, 'theta': 0.004415223179282759, 'rho': -0.10315528230245756, 'alpha': 2.00778594959696, 'eta': 0.9726750509279738, 'q': 4.244356488123494, 'v0': 0.004317649475517201, 'vT': 0.008609745008684565}
    assert compare(testpars,pars)

def test_10():
    cc=10
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    testpars={'mu': -0.05269338432198227, 'theta': 0.0042144333986774635, 'rho': -0.12633187082249647, 'alpha': 1.9999617087435282, 'eta': 0.9842645006499546, 'jumpintensity': 9.95493420454033, 'jumpmean': 0.0032247544993619912, 'jumpvolatility': 0.002000000000000035, 'q': 4.12883980434238, 'v0': 0.0040186832575974975, 'vT': 0.008816731938380916}
    assert compare(testpars,pars)
