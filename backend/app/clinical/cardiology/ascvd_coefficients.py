from dataclasses import dataclass
from typing import Dict, Any, Tuple

@dataclass
class PCEParams:
    S0: float
    mean_lp: float
    betas: Dict[str, float]


_PCE_CONSTANTS: Dict[Tuple[str, str], PCEParams] = {
    ("female", "white"): PCEParams(
        S0=0.9665,
        mean_lp=-29.18,
        betas={
            "ln_age": -29.799,
            "ln_age_sq": 4.884,
            "ln_tc": 13.540,
            "ln_age*ln_tc": -3.114,
            "ln_hdl": -13.578,
            "ln_age*ln_hdl": 3.149,
            "ln_sbp_trt": 2.019,
            "ln_sbp_untrt": 1.957,
            "smoker": 7.574,
            "ln_age*smoker": -1.665,
            "diabetes": 0.661,
        },
    ),
    ("female", "black"): PCEParams(
        S0=0.9533,
        mean_lp=86.61,
        betas={
            "ln_age": 17.114,
            "ln_tc": 0.940,
            "ln_hdl": -18.920,
            "ln_age*ln_hdl": 4.475,
            "ln_sbp_trt": 29.291,
            "ln_age*ln_sbp_trt": -6.432,
            "ln_sbp_untrt": 27.820,
            "ln_age*ln_sbp_untrt": -6.087,
            "smoker": 0.691,
            "diabetes": 0.874,
        },
    ),
    ("male", "white"): PCEParams(
        S0=0.9144,
        mean_lp=61.18,
        betas={
            "ln_age": 12.344,
            "ln_tc": 11.853,
            "ln_age*ln_tc": -2.664,
            "ln_hdl": -7.990,
            "ln_age*ln_hdl": 1.769,
            "ln_sbp_trt": 1.797,
            "ln_sbp_untrt": 1.764,
            "smoker": 7.837,
            "ln_age*smoker": -1.795,
            "diabetes": 0.658,
        },
    ),
    ("male", "black"): PCEParams(
        S0=0.8954,
        mean_lp=19.54,
        betas={
            "ln_age": 2.469,
            "ln_tc": 0.302,
            "ln_hdl": -0.307,
            "ln_sbp_trt": 1.916,
            "ln_sbp_untrt": 1.809,
            "smoker": 0.549,
            "diabetes": 0.645,
        },
    ),
}
