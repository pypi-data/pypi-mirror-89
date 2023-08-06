
from svolfit.models.Heston import Heston_grid,Heston_tree,Heston_treeX2
from svolfit.models.Bates import Bates_grid,Bates_tree,Bates_treeX2
from svolfit.models.H32 import H32_grid,H32_tree,H32_treeX2
from svolfit.models.B32 import B32_grid,B32_tree,B32_treeX2
from svolfit.models.GARCHdiff import GARCHdiff_grid,GARCHdiff_tree,GARCHdiff_treeX2
from svolfit.models.GARCHjdiff import GARCHjdiff_grid,GARCHjdiff_tree,GARCHjdiff_treeX2
from svolfit.models.template import template

def model_create(series, dt, model, method):

#    print(model,method)
    if( model == 'Heston' ):
        if( method == 'tree' ):
            modelobj = Heston_tree(series,dt, model, method)
        elif( method == 'treeX2' ):
            modelobj = Heston_treeX2(series,dt, model, method)
        elif( method == 'grid' ):
            modelobj = Heston_grid(series,dt, model, method)
        else:
            print('unknown method')
    elif( model == 'Bates' ):
        if( method == 'tree' ):
            modelobj = Bates_tree(series,dt, model, method)
        elif( method == 'treeX2' ):
            modelobj = Bates_treeX2(series,dt, model, method)
        elif( method == 'grid' ):
            modelobj = Bates_grid(series,dt, model, method)
        else:
            print('unknown')
    elif( model == 'H32' ):
#        if( method == 'tree' ):
#            modelobj = H32_tree(series,dt, model, method)
#        elif( method == 'treeX2' ):
#            modelobj = H32_treeX2(series,dt, model, method)
        if( method == 'grid' ):
            modelobj = H32_grid(series,dt, model, method)
        else:
            print('unknown')
    elif( model == 'B32' ):
#        if( method == 'tree' ):
#            modelobj = B32_tree(series,dt, model, method)
#        elif( method == 'treeX2' ):
#            modelobj = B32_treeX2(series,dt, model, method)
        if( method == 'grid' ):
            modelobj = B32_grid(series,dt, model, method)
        else:
            print('unknown')
    elif( model == 'GARCHdiff' ):
#        if( method == 'tree' ):
#            modelobj = GARCHdiff_tree(series,dt, model, method)
#        elif( method == 'treeX2' ):
#            modelobj = GARCHdiff_treeX2(series,dt, model, method)
        if( method == 'grid' ):
            modelobj = GARCHdiff_grid(series,dt, model, method)
        else:
            print('unknown')
    elif( model == 'GARCHjdiff' ):
#        if( method == 'tree' ):
#            modelobj = GARCHjdiff_tree(series,dt, model, method)
#        elif( method == 'treeX2' ):
#            modelobj = GARCHjdiff_treeX2(series,dt, model, method)
        if( method == 'grid' ):
            modelobj = GARCHjdiff_grid(series,dt, model, method)
        else:
            print('unknown')
    else:
        modelobj = template(series,dt, model, method)
        print('Unsupported model: '+model+' and method: '+method)

    return modelobj
