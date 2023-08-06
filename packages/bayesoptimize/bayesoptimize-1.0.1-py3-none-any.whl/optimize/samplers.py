# Contains the custom Nelder-Mead algorithm
import numpy as np
import copy
import optimize.knowledge
from optimize.optimizers import Sampler
import tqdm
from joblib import Parallel, delayed
import emcee
import time
import corner
import matplotlib.pyplot as plt

class AffInv(Sampler):
    """An class to interface to the emcee affine invariant Ensemble Sampler. In short, affine invariance rescales parameters to be scale-independent, unlike other common samplers such as Metropolis Hastings or Gibbs.
    """
    
    def __init__(self, scorer=None, options=None):
        """Construct the Affine Invariant sampler.

        Args:
            scorer (Likelihood): The Mixed likelihood object.
            options (dict): A dictionary containing any emcee.EnsembleSampler kwargs. Defaults to None.
        """
        super().__init__(scorer=scorer, options=options)
        p0_dict = self.scorer.p0.unpack()
        self.test_pars = copy.deepcopy(self.scorer.p0)
        self.test_pars_vec = np.copy(p0_dict['value'])
        self.p0_vary_inds = np.where(p0_dict["vary"])[0]
        self.init_sampler()
        
    def init_walkers(self, pars=None):
        """Initializes a set of walkers.

        Args:
            pars (Parameters, optional): The starting parameters. Defaults to p0.

        Returns:
            np.ndarray: A set of walkers as a numpy array with shape=(n_walkers, n_parameters_vary)
        """
        
        if pars is None:
            pars = self.scorer.p0
        pars_vary_dict = pars.unpack(vary_only=True)
        n_pars = len(pars)
        n_pars_vary = pars.num_varied()
        search_scales = np.array([par.compute_crude_scale() for par in pars.values() if par.vary])
        walkers = pars_vary_dict['value'] + search_scales * np.random.randn(self.n_walkers, n_pars_vary)
        return walkers
    
    def set_pars(self, pars):
        """Sets the parameters.

        Args:
            pars (Parameters): The parameters to set.
        """
        self.p0 = pars
    
    @property
    def n_walkers(self):
        """Alias for the number of walkers.

        Returns:
            int: The number of walkers.
        """
        return self.sampler.nwalkers
    
    def init_sampler(self):
        """Initializes the emcee.Ensemble sampler.
        """
        n_pars_vary = self.scorer.p0.num_varied()
        n_walkers = 2 * n_pars_vary
        self.sampler = emcee.EnsembleSampler(n_walkers, n_pars_vary, self.compute_score)
        
    def sample(self, pars=None, walkers=None, n_burn_steps=500, n_steps=75_000, rel_tau_thresh=0.01, n_min_steps=1000, n_cores=1, n_taus_thresh=40):
        """Wrapper to perform a burn-in + full MCMC exploration.

        Args:
            pars (Parameters, optional): The starting parameters. Defaults to p0.
            walkers (np.ndarray, optional): The starting walkers. Defaults to calling self.init_walkers(pars).
            n_burn_steps (int, optional): The number of burn in steps. Defaults to 100 * pars.num_varied().
            n_steps (int, optional): The number of mcmc steps to perform in the full phase (post burn-in). Defaults to 50_000 * pars.num_varied().
            rel_tau_thresh (float, optional): The relative change in the auto-correlation time for convergence. This criterion must be met for all walkers. Defaults to 0.01.
            n_min_steps (int, optional): The minimum number of steps to run. Defaults to 1000
            n_threads (int, optional): The number of threads to use. Defaults to 1.

        Returns:
            dict: The sampler result, with keys: flat_chains, autocorrs, steps, pbest, errors, lnL.
        """
        
        self.n_cores = n_cores
        
        # Init pars
        if pars is None and walkers is None:
            walkers = self.init_walkers()
            pars = self.scorer.p0
        elif pars is not None:
            walkers = self.init_walkers(pars)
        
        # Burn in
        if n_burn_steps > 0:
            
            # Run burn in
            print("Running Burn-in MCMC Phase [" + str(n_burn_steps) + "]")
            walkers = self.sampler.run_mcmc(walkers, n_burn_steps, progress=True)
            
            print("Burn in complete ...")
            print("Current Parameters ...")
            
            flat_chains = self.sampler.flatchain
            pars_mcmc = flat_chains[np.nanargmax(self.sampler.flatlnprobability)]
            _pbest = copy.deepcopy(self.scorer.p0)
            _par_vec = np.copy(self.test_pars_vec)
            _par_vec[self.p0_vary_inds] = pars_mcmc
            _pbest.setv(value=_par_vec)
            _pbest.pretty_print()
    
            # Reset
            self.sampler.reset()
    
        # Run full search
    
        # Convergence testing
        autocorrs = []
        old_tau = np.inf

        # Sample up to n_steps
        converged = False
        print("Running Full MCMC Phase ...")
        _trange = tqdm.trange(n_steps, desc="Running Min Steps = " + str(n_min_steps), leave=True)
        for _, sample in zip(_trange, self.sampler.sample(walkers, iterations=n_steps, progress=False)):
            
            # Only check convergence every 100 steps and run at least a minimum number of steps
            if self.sampler.iteration % 200:
                continue

            # Compute the autocorrelation time so far
            # Using tol=0 means that we'll always get an estimate even
            # if it isn't trustworthy
            taus = self.sampler.get_autocorr_time(tol=0)
            med_tau = np.nanmedian(taus)
            autocorrs.append(med_tau)

            # Check convergence:
            # 1. Ensure we've run a sufficient number of autocorrelation time scales
            # 2. Ensure the estimations of the autorr times themselves are settling.
            converged = med_tau * n_taus_thresh < self.sampler.iteration
            rel_tau = np.abs(old_tau - med_tau) / med_tau
            converged &= rel_tau < rel_tau_thresh
            converged &= self.sampler.iteration > n_min_steps
            _trange.set_description("\u03C4 = " + str(round(med_tau, 5)) + " / x" + str(n_taus_thresh) + ", rel change = " + str(round(rel_tau, 5)) + " / " + str(round(rel_tau_thresh, 5)))
            if converged:
                print("Success!")
                break
            
            old_tau = med_tau
            
        # Outputs
        sampler_result = {}
        sampler_result["flat_chains"] = self.sampler.flatchain
        sampler_result["autocorrs"] = np.array(autocorrs)
        sampler_result["steps"] = n_steps
        self.parameter_chain_results(sampler_result)
        sampler_result["lnL"] = self.scorer.compute_logL(sampler_result["pbest"])
        #sampler_result["redchi2"] = self.scorer.compute_reduced_chi2(sampler_result["pbest"])
        return sampler_result
    
    def corner_plot(self, sampler_result):
        """Constructs a corner plot.

        Args:
            sampler_result (dict): The sampler result
            show (bool, optional): Whether or not to show the plot. Defaults to True.

        Returns:
            fig: A matplotlib figure.
        """
        plt.clf()
        pbest_vary_dict = sampler_result["pmed"].unpack(vary_only=True)
        truths = pbest_vary_dict["value"]
        labels = [par.latex_str for par in sampler_result["pbest"].values() if par.vary]
        fig = corner.corner(sampler_result["flat_chains"], labels=labels, truths=truths, show_titles=True)
        return fig
        
    
    def parameter_chain_results(self, sampler_result, percentiles=None):
        """Computes the error bars after sampling.

        Args:
            sampler_result (dict): The sampler result
            percentiles (np.ndarray or list, optional): The percentiles to use for the min, "best" and max. Defaults to [15.9, 50, 84.1].

        Returns:
            dict: A dicionary of with parameter names as keys, and a list of min val, "best val" and the max val.
        """
        
        if percentiles is None:
            percentiles = [15.9, 50, 84.1]
        
        # All acceptance rates
        acc = self.sampler.acceptance_fraction
        
        # Median acceptance rate
        acc_med = np.nanmedian(acc)
        
        # MAD acceptance rate (median absolute deviation)
        acc_mad = np.nanmedian(np.abs(acc - acc_med))
        
        # Good chains
        acceptance_rate_threshold = 0.3
        chain_nsigma_threshold = 3.0
        good_chains = np.where(((np.abs((acc - acc_med) / acc_mad) < chain_nsigma_threshold)| (acc > acceptance_rate_threshold)) \
                                & (np.nansum(self.sampler.lnprobability, axis=1) != -np.inf))
        good_chains = np.reshape(good_chains, np.size(good_chains))
        
        # Extract only good chains
        flat_chains = self.sampler.chain[good_chains, :, :].reshape(np.size(good_chains) * self.sampler.chain.shape[1], self.sampler.chain.shape[2])
        
        # Best pars are those with the highest likelihood. Use the 50th percentile for errors.
        pars_best = self.sampler.chain[1, np.argmax(self.sampler.lnprobability[1, :]), :]
        sampler_result["pbest"] = copy.deepcopy(self.scorer.p0)
        sampler_result["pmed"] = copy.deepcopy(self.scorer.p0)
        par_vec = np.copy(self.test_pars_vec)
        par_vec[self.p0_vary_inds] = pars_best
        sampler_result["pbest"].setv(value=par_vec)
        
        # Errors
        pnames_vary = sampler_result["pbest"].unpack(keys='name', vary_only=True)['name']
        punc = {}
        for i in range(len(pnames_vary)):
            par_quantiles = np.percentile(flat_chains[:, i], percentiles)
            punc[pnames_vary[i]] = np.diff(par_quantiles)
            sampler_result["pmed"][pnames_vary[i]].value = par_quantiles[1]
        
        # Store the errors
        sampler_result["punc"] = punc
        
    def compute_score(self, pars):
        """Wrapper to compute the score, only to be called by the emcee Ensemble Sampler.

        Args:
            pars (np.ndarray): The parameter values.

        Returns:
            float: The log(likelihood)
        """
        self.test_pars_vec[self.p0_vary_inds] = pars
        self.test_pars.setv(value=self.test_pars_vec)
        lnL = self.scorer.compute_logL(self.test_pars)
        return lnL
    
    
# NOT IMPLEMENTED YET
class MultiNest(Sampler):
    pass

# NOT IMPLEMENTED YET
# (Hamiltonian No U-Turn)
class HNUT(Sampler):
    pass