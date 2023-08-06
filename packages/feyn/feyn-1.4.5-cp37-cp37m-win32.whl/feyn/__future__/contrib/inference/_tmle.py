
import numpy as np


class TMLE:
    """Calculates the Targeted Maximum Likelihood for some data
       and feyn.Graph exposure and outcome models.
    """

    def __init__(self, data, outcome_graph, exposure_graph, alpha=0.05, continuous_bound=5.e-6) -> None:
        """Initialize the TMLE class

        Arguments:
            data {dict(str, np.array) or pd.DataFrame} -- dataset to calculate TMLE
            outcome_graph {feyn.Graph} -- model for the outcome variable
            exposure_graph {feyn.Graph} -- model for the exposure variable

        Keyword Arguments:
            alpha {float} -- significance of confidence interval (default: {0.05})
            continuous_bound {float} -- significance of bounded
            variables to the (0., 1.) interval (default: {0.0005})
        """

        self.data = data

        if all(hasattr(outcome_graph, attr) for attr in ['target', 'predict']):
            self.outcome_graph = outcome_graph
            self.outcome = outcome_graph.target
        else:
            raise AttributeError("The outcome graph should have the attributes 'target' and 'predict'!")

        if all(hasattr(exposure_graph, attr) for attr in ['target', 'predict', 'features']):
            self.exposure_graph = exposure_graph
            self.exposure = exposure_graph.target
            self.confounders = exposure_graph.features
        else:
            raise AttributeError("The exposure graph should have the attributes 'target', 'features' and 'predict'!")

        # Bounding
        self.outcome_min = data[self.outcome].min()
        self.outcome_max = data[self.outcome].max()

        # Inference measures
        self.bound = continuous_bound
        self.alpha = alpha

        self.delta = None
        self.ate = None
        self.ate_se = None
        self.ate_ci = None

        # Needed to "expose" the following items for testing stuff:
        # 1. Predictions
        self._OA1 = None
        self._OA1 = None
        self._O_actual = None

        self._pi_1 = None
        self._pi_0 = None
        self._HA1 = None
        self._HA0 = None
        self._HA = None

        # 2. Bounded things
        self._bounded_outcome = None
        self._bounded_O_actual = None
        ###

    def _get_outcome_predictions(self):
        # Predicting outcomes for treatment = 1 only
        df_A1 = self.data.copy()
        df_A1[self.exposure] = np.ones(df_A1[self.exposure].shape[0])
        OA1 = self.outcome_graph.predict(df_A1)

        # Predicting outcomes for treatment = 0 only
        df_A0 = self.data.copy()
        df_A0[self.exposure] = np.zeros(df_A0[self.exposure].shape[0])
        OA0 = self.outcome_graph.predict(df_A0)

        # Predicting outcomes for original dataset
        O_actual = self.outcome_graph.predict(self.data)

        return OA1, OA0, O_actual

    def _exposure_probability(self):
        pi_1 = self.exposure_graph.predict(self.data)
        pi_0 = 1 - pi_1
        return pi_1, pi_0

    def _predefined_covariates(self, pi_1, pi_0):
        # Check for probability values outside of (0, 1)!
        if np.any(pi_1 <= 0) or np.any(pi_1 > 1.) or np.any(pi_0 <= 0) or np.any(pi_0 > 1):
            raise ValueError("Probability values outside the (0, 1] interval!")
        else:
            # Calculate H_a: if A = 1 then 1 / prob else -1 / prob
            HA = self.data[self.exposure] * (1 / pi_1) - (1 - self.data[self.exposure]) * (1. / pi_0)

            HA1 = np.where(HA > 0, HA, 0)
            HA0 = np.where(HA < 0, HA, 0)

        return HA1, HA0, HA

    # Bounding according to TMLE and making sure no values are equal to 0 or 1
    def _unit_bounding(self, y):
        y_star = (y - self.outcome_min) / (self.outcome_max - self.outcome_min)  # line
        y_star = np.where(y_star < self.bound, self.bound, y_star)
        y_star = np.where(y_star > 1 - self.bound, 1 - self.bound, y_star)
        return y_star

    def _unit_unbounding(self, ystar):
        y = ystar * (self.outcome_max - self.outcome_min) + self.outcome_min
        return y

    @staticmethod
    def _logit(p):
        y = np.log(np.divide(p, 1. - p))
        return y

    @staticmethod
    def _inv_logit(p):
        y = 1 / (1 + np.exp(-p))
        return y

    def fit(self):
        """Calculates the Average Treatment Effect (ATE), standard errors
           and confidence intervals.
        """

        import statsmodels.api as sm

        OA1, OA0, O_actual = self._get_outcome_predictions()

        pi_1, pi_0 = self._exposure_probability()

        HA1, HA0, HA = self._predefined_covariates(pi_1, pi_0)

        bounded_outcome = self._unit_bounding(self.data[self.outcome])

        # Dirty
        self._OA1 = OA1
        self._OA0 = OA0
        self._O_actual = O_actual

        self._pi_1 = pi_1
        self._pi_0 = pi_0
        self._HA1 = HA1
        self._HA0 = HA0
        self._HA = HA
        ###

        # Generalized linear model
        bounded_O_actual = self._unit_bounding(O_actual)

        # Dirty
        self._bounded_outcome = bounded_outcome
        self._bounded_O_actual = bounded_O_actual
        ###

        f = sm.families.family.Binomial()

        # try except
        try:
            log = sm.GLM(bounded_outcome,
                         np.column_stack([HA1, HA0]),
                         offset=self._logit(bounded_O_actual),
                         family=f, missing='drop').fit()
        except Exception as inst:
            print('Error in the Generalized Linear Model from statsmodels: "%s".' % inst)
            raise

        self.delta = log.params

        bounded_OA1 = self._unit_bounding(OA1)
        bounded_OA0 = self._unit_bounding(OA0)
        bounded_OA = bounded_OA1 * self.data[self.exposure] + bounded_OA0 * (1 - self.data[self.exposure])

        updated_bounded_OA1 = self._inv_logit(self._logit(bounded_OA1) + self.delta[0] * HA1)
        updated_bounded_OA0 = self._inv_logit(self._logit(bounded_OA0) + self.delta[1] * HA0)

        updated_bounded_OA = log.predict(np.column_stack((HA1, HA0)), offset=self._logit(bounded_OA))

        updated_OA1 = self._unit_unbounding(updated_bounded_OA1)
        updated_OA0 = self._unit_unbounding(updated_bounded_OA0)
        updated_OA = self._unit_unbounding(updated_bounded_OA)

        self.ate = np.nanmean(updated_OA1 - updated_OA0)

        # Step 6) Calculating Psi
        zalpha = 1.96

        # ic = updated_OA1 - updated_OA0 - ate
        unbounded_outcome = self._unit_unbounding(bounded_outcome)

        ic = HA * (unbounded_outcome - updated_OA) + (updated_OA1 - updated_OA0) - self.ate
        seIC = np.sqrt(np.nanvar(ic, ddof=1) / self.data[self.exposure].shape[0])
        self.ate_se = seIC
        self.ate_ci = [self.ate - zalpha * seIC, self.ate + zalpha * seIC]

    def summary(self):

        from IPython.display import display

        print('======================================================================')
        print('                       TMLE w. QLattice                 ')
        print('======================================================================')
        print('Targeted Maximum Likelihood applied with QLattice graphs.\n')
        print('Average Treatment Effect: ', round(float(self.ate), 3))
        print(str(round(100 * (1 - self.alpha), 1)) + '% two-sided CI: (' +
        str(round(self.ate_ci[0], 3)), ',',
        str(round(self.ate_ci[1], 3)) + ')')
        print('\n======================================================================')
        print('                       Outcome model')
        print('======================================================================')

        display(self.outcome_graph)

        print('======================================================================')
        print('                       Exposure model')
        print('======================================================================')

        display(self.exposure_graph)
        print('======================================================================\n')
