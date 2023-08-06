import shutil

import numpy as np
import pytest

from besos.evaluator import EvaluatorGeneric
from besos.optimizer import rbf_opt
from besos.parameters import Parameter, RangeParameter
from besos.problem import Problem


@pytest.mark.skipif(shutil.which("bonmin") is None, reason="Requires bonmin to run.")
def test_rbfopt():
    """Simple test to make sure RBFOpt can be run properly"""

    def objective_function(x):
        return (x[0] * x[1] - x[2],)

    p1 = Parameter(value_descriptor=RangeParameter(1, 10), name="None_0")
    p2 = Parameter(value_descriptor=RangeParameter(0.1, 0.9), name="None_1")
    p3 = Parameter(value_descriptor=RangeParameter(0, 10), name="None_2")
    param_list = [p1, p2, p3]

    problem = Problem(param_list, 1)

    evaluator = EvaluatorGeneric(objective_function, problem, error_mode="Silent")

    opt = rbf_opt(evaluator, 30)
    value = opt.iloc[0]

    assert (
        np.isclose(value["None_0"], 1.0)
        and np.isclose(value["None_1"], 0.1)
        and np.isclose(value["None_2"], 10)
        and np.isclose(value["outputs_0"], -9.9)
    ), f"Unexpected output: {value}"  # None_1 assert values hardcoded to pass on Debian
