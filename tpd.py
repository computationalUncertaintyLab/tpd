#mcandrew

import numpy as np
import pandas as pd

class tpd(object):
    def __init__(self,list_minModMax=None, list_pcts=None, list_probs = [0.025,0.50,0.975]):
        self.list_pcts  = list_pcts
        self.list_probs = list_probs
        
        if list_minModMax is not None:
            self.mi, self.mod, self.mx = list_minModMax
        elif list_pcts is not None:
            self.mob = self.computeParamsFromQuantiles()
            self.mi, self.mod, self.mx = self.mob['x']

    def computeParamsFromQuantiles(self):
        from scipy.optimize import minimize
        def error(miModMx):
            proposal = tpd(miModMx)
            e = 0.
            for xval,prob in zip(self.list_pcts,self.list_probs):
                e+=(proposal.cdf(xval) - prob)**2
            return e
        return minimize( error, np.array(self.list_pcts).reshape(-1,) )

    def pdf(self,x):
        """ 
        this is the pdf for a triangular probability density.
        This function inputs an x value (x) and returns the corresponding density value 
        """
        mi,mod,mx = self.mi,self.mod,self.mx
        if mi==mod==mx:
            mi-=0.1
            mx+=0.1
        if x < mi or x>mod:
            return 0.
        elif x>=mi and x<mx:
            return 2*(x-mi)/( (mod-mi)*(mx-mi) )
        elif x==mx:
            return 2/(mod-mi)
        elif x > mx and x <= mod:
            return 2*(mod-x)/ ( (mod-mi)*(mod-mx) )

    def cdf(self,x):
        """ 
        This is the cdf for a triangular probability density.
        This function inputs an x value (x) and returns the corresponding probability less than x
        """
        mi,mod,mx = self.mi,self.mod,self.mx
        if x<= mi:
            return 0
        elif x>=mi and x<=mod:
            return ((x-mi)**2)/( (mx-mi)*(mod-mi) )
        elif x > mod and x <= mx:
            return 1 - ((mx-x)**2)/( (mx-mi)*(mx-mod) )
        elif x>=mx:
            return 1.


if __name__ == "__main__":

    TPD_withParams = tpd( list_minModMax = [10,50,90] )
    
    TPD_estimate = tpd( list_pcts = [18.95,50,81] )
    
    

    
