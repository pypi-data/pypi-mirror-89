import numpy as np
from astropy.io import fits, ascii
from astropy.table import Table
from scipy.interpolate import interp1d


class interp1d_picklable:
    """ class wrapper for piecewise linear function
    Otherwise, there a problems pickling this function
    to save MCMC results.
    
    Taken from:
    https://stackoverflow.com/questions/32883491/pickling-scipy-interp1d-spline
    """
    def __init__(self, xi, yi, **kwargs):
        self.xi = xi
        self.yi = yi
        self.args = kwargs
        self.f = interp1d(xi, yi, **kwargs)

    def __call__(self, xnew):
        return self.f(xnew)

    def __getstate__(self):
        return self.xi, self.yi, self.args

    def __setstate__(self, state):
        self.f = interp1d(state[0], state[1], **state[2])
        

class kic1255Model:
    """ A Kepler LC model from the Kepler Short cadence data
    
    """
    def __init__(self):
        self.name = "Kepler LC Model from Kepler SC data. Assuming x is in orbital phase"
        self.pnames = [r'A','B','C']
        self.formula = "(A * f(x) + 1.0) * (1.0 + B + C * x)"
        
        self.kepFile = 'tser_data/reference_dat/avg_bin_kep.fits'
        self.kepDat = Table.read(self.kepFile)
        
        self.finterp = interp1d_picklable(self.kepDat['BINMID'],self.kepDat['YBIN'] - 1.0,
                                          bounds_error=False,fill_value=0.0)
        self.ndim = len(self.pnames)
    
    def evaluate(self,x,inputP):
        """ Evaluates the SC model with an interpolating function 
        
        Parameters
        -----------
        x: np.array
            The input phase 
        p: np.array or list
            the parameter array
            p[0] = Amplitude
            p[1] = linear baseline
        """
        p = np.array(inputP)
        return (p[0] * self.finterp(x) + 1.0) * (1.0 + p[1] + p[2] * x)
    
    
    def lnprior(self,inputP):
        """ Prior likelihood """
        
        p = np.array(inputP)
        finiteCheck = np.isfinite(inputP)
        
        if np.all(finiteCheck):
            return 0
        else:
            return -np.inf