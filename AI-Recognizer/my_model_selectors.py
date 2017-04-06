import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold

import asl_utils


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def bic(self, model, n_components):
        """Bayesian information criterion for the current model on the input X.

        Parameters
        ----------
        X : array of shape (n_samples, n_dimensions)

        Returns
        -------
        bic: float
            The lower the better.
        """
        log_l = model.score(self.X, self.lengths)
        # p = m^2 +2mf-1
        p = n_components ** 2 + 2 * n_components * model.n_features - 1
        # BIC = -2 * logL + p * logN
        return -2 * log_l + p * np.log(len(self.X))

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        best_result = float("inf")
        best_model = None
        for i in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(i)
                # gmm = mixture.GaussianMixture(n_components=i, covariance_type='diag')
                # gmm.fit(self.X)
                # bic = gmm.bic(self.X)
                bic = self.bic(self, model, i)  # after review formula attached in the code I was just using lib before
                if bic < best_result:
                    best_result = bic
                    best_model = model
            except:
                if best_model is None:
                    best_model = self.base_model(self.min_n_components)
                continue

        return best_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)  *  SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        best_result = float("-inf")
        best_model = None
        for i in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(i)
                log_p_i = model.score(self.X, self.lengths)
                sum_log_p_not_i = []
                for word in self.hwords:
                    if word == self.this_word:
                        continue
                    x, x_length = self.hwords[word]
                    sum_log_p_not_i.append(model.score(x, x_length))
                current_result = log_p_i - (sum(sum_log_p_not_i) / len(sum_log_p_not_i))
                if current_result > best_result:
                    best_result = current_result
                    best_model = model
            except:
                if best_model is None:
                    best_model = self.base_model(self.min_n_components)
                continue

        return best_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        best_result = float("-inf")
        best_model = None
        for i in range(self.min_n_components, self.max_n_components + 1):
            try:
                split_method = KFold(n_splits=2)
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    results = []
                    self.X, self.lengths = asl_utils.combine_sequences(cv_train_idx, self.sequences)
                    test_x, test_lengths = asl_utils.combine_sequences(cv_test_idx, self.sequences)
                    model = self.base_model(i)
                    results.append(model.score(test_x, test_lengths))
                    average = sum(results) / float(len(results))
                    if average > best_result:
                        best_result = average
                        best_model = model
            except:
                if best_model is None:
                    best_model = self.base_model(self.min_n_components)
        return best_model
