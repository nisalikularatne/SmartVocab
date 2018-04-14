import json
import operator
from collections import deque

import numpy

from engine.instructor import accuracy_params as params

EWMA_SEED = -0.8
PROBABILITY_FIRST_PROBLEM_CORRECT = 0.25
MAX_HISTORY_KEPT = 20

class LogisticRegressionModel:
    """
    Predicts the probabilty of the next problem being correct using logistic regression.
    """
    def __init__(self, answer_history=None):
        # History of the past answers up to MAX_HISTORY_KEPT
        if answer_history:
            self.answer_history = deque(answer_history)
        else:
            self.answer_history = deque([0 for x in range(20)])

        # This is capped at MAX_HISTORY_KEPT
        self.total_done = len(self.answer_history )

    def update(self, correct):
        # Add a new answer
        self.answer_history.appendleft(1 if correct else 0)
        self.total_done = len(self.answer_history )
        if (self.total_done > MAX_HISTORY_KEPT):
            self.answer_history.pop()
            self.total_done = len(self.answer_history)
        return self.score()

    # 0-based index where 0 is the most recent problem done
    # Todo: make this sliding, so that 0 is the most recent problem done
    def get_answer_at(self, index):
        return self.answer_history[index]

    def __repr__(self):
        return json.dumps(list(self.answer_history))

    # Exponential moving average
    # See http://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
    def exp_moving_avg(self, weight):
        ewma = EWMA_SEED

        for i in reversed(range(self.total_done)):
            ewma = weight * self.get_answer_at(i) + (1 - weight) * ewma

        return ewma

    def streak(self):
        for i in range(self.total_done):
            if not self.get_answer_at(i):
                return i

        return self.total_done

    # Todo: Count the total correct
    def total_correct(self):
        total = sum(1 for x in self.answer_history if x == 1)
        return total

    def predict(self):
        """
        Returns: the probabilty of the next problem correct using logistic regression.
        """
        # We don't try to predict the first problem
        if self.total_done == 0:
            return PROBABILITY_FIRST_PROBLEM_CORRECT
        # Get values for the feature vector X
        ewma_3 = self.exp_moving_avg(0.333)
        ewma_10 = self.exp_moving_avg(0.1)
        current_streak = self.streak()
        log_num_done = math.log(self.total_done)
        log_num_missed = math.log(self.total_done - self.total_correct() + 1)  # log (num_missed + 1)
        percent_correct = float(self.total_correct()) / self.total_done

        weighted_features = [
            (ewma_3, params.EWMA_3),
            (ewma_10, params.EWMA_10),
            (current_streak, params.CURRENT_STREAK),
            (log_num_done, params.LOG_NUM_DONE),
            (log_num_missed, params.LOG_NUM_MISSED),
            (percent_correct, params.PERCENT_CORRECT),
        ]
        X, weight_vector = zip(*weighted_features)  # unzip the list of pairs
        return LogisticRegressionModel.logistic_regression_predict(params.INTERCEPT, weight_vector, X)
    @staticmethod
    def logistic_regression_predict(intercept, weight_vector, X):
        dot_product = numpy.dot(weight_vector, X)
        z = dot_product + intercept
        return 1.0 / (1.0 + math.exp(-z))

    @staticmethod
    def simulate(answer_history):
        model = LogisticRegressionModel()
        model.update(answer_history)
        return model.predict()

    # The minimum number of problems correct in a row to be greater than the given threshold
    @staticmethod
    def min_streak_till_threshold(threshold):
        model = LogisticRegressionModel()

        for i in itertools.count(1):
            model.update(correct=True)

            if model.predict() >= threshold:
                return i

    def score(self):
        return self.predict()

import logging
import itertools
import math

def exponential_fit(X, Y):
    # See http://mathworld.wolfram.com/LeastSquaresFittingExponential.html
    # TODO(david): This just uses the simpler fit given by equations (3) and (4) of
    #     above link. Try equations (9) and (10).
    # TODO(david): Use numpy when supported

    def sqr(x):
        return x * x

    n = len(X)
    sum_x = sum(X)
    sum_log_y = sum(itertools.imap(math.log, Y))
    sum_x_log_y = sum(itertools.imap(lambda x, y: x * math.log(y), X, Y))
    sum_x_sqr = sum(itertools.imap(sqr, X))

    a_num = sum_log_y * sum_x_sqr - sum_x * sum_x_log_y
    b_num = n * sum_x_log_y - sum_x * sum_log_y
    den = n * sum_x_sqr - sqr(sum_x)

    a = float(a_num) / den
    b = float(b_num) / den

    return math.exp(a), b

class InvFnExponentialNormalizer:
    """
    This is basically a function that takes an accuracy prediction (probability
    of next problem correct) and attempts to "evenly" distribute it in [0, 1]
    such that progress bar appears to fill up linearly.

    The current algorithm is as follows:
    Let
        f(n) = probabilty of next problem correct after doing n problems,
        all of which are correct.
    Let
        g(x) = f^(-1)(x)
    that is, the inverse function of f. Since f is discrete but we want g to be
    continuous, unknown values in the domain of g will be approximated by using
    an exponential curve to fit the known values of g. Intuitively, g(x) is a
    function that takes your accuracy and returns how many problems correct in
    a row it would've taken to get to that, as a real number. Thus, our
    progress display function is just
        h(x) = g(x) / g(consts.PROFICIENCY_ACCURACY_THRESHOLD)
    clamped between [0, 1].

    The rationale behind this is that if you don't get any problems wrong, your
    progress bar will increment by about the same amount each time and be full
    right when you're proficient (i.e. reach the required accuracy threshold).

    (Sorry if the explanation is not very clear... best to draw a graph of f(n)
    and g(x) to see for yourself.)

    This is a class because of static initialization of state.
    """

    def __init__(self, accuracy_model, proficiency_threshold):
        X, Y = [], []
        self.proficiency_threshold = proficiency_threshold

        for i in itertools.count(1):
            accuracy_model.update(correct=True)
            probability = accuracy_model.predict()

            X.append(probability)
            Y.append(i)

            if probability >= proficiency_threshold:
                break

        self.A, self.B = exponential_fit(X, Y)
        # normalize the function output so that it outputs 1.0 at the proficency threshold
        self.A /= self.exponential_estimate(proficiency_threshold)

    def exponential_estimate(self, x):
        return self.A * math.exp(self.B * x)

    def normalize(self, p_val):
        def clamp(value, minval, maxval):
            return sorted((minval, value, maxval))[1]

        return clamp(self.exponential_estimate(p_val), 0.0, 1.0)

if __name__ == "__main__":
    a = LogisticRegressionModel()
    a.update(True)
    a.update(True)

    print(a.predict())

    for i in range(21):
        p = i / 20
        if  LogisticRegressionModel.min_streak_till_threshold(p)==1:
            print("{} question need to be answered corrected".format(
                LogisticRegressionModel.min_streak_till_threshold(p)), " to get a score of {}".format(p))
        else:
           print("{} questions need to be answered corrected".format(LogisticRegressionModel.min_streak_till_threshold(p))," to get a score of {}".format(p))
