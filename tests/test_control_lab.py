import unittest

from control_lab import (
    BayesianScalarDynamics,
    fit_polynomial_lift,
    residual_controller,
    scalar_lqr_gain,
    simulate_scalar,
)
from control_lab.benchmark import run_model_mismatch_benchmark


class ControlLabTests(unittest.TestCase):
    def test_lqr_stabilizes_simple_scalar_system(self):
        gain = scalar_lqr_gain(1.1, 1.0)
        traj = simulate_scalar(
            a=1.1,
            b=1.0,
            x0=2.0,
            controller=lambda x, t: -gain * x,
            steps=25,
        )
        self.assertLess(abs(traj.states[-1]), 1e-3)

    def test_residual_controller_respects_action_limit(self):
        controller = residual_controller(
            base_gain=1.0,
            residual_policy=lambda x, t: 100.0,
            action_limit=2.0,
        )
        self.assertEqual(controller(1.0, 0), 2.0)

    def test_koopman_inspired_lift_fits_known_nonlinear_dynamics(self):
        samples = []
        for x in (-2.0, -1.0, 0.5, 1.0, 2.0):
            for u in (-0.5, 0.5):
                y = 0.8 * x + 0.1 * x * x + 0.5 * u
                samples.append((x, u, y))
        model = fit_polynomial_lift(samples)
        self.assertAlmostEqual(model.w_x, 0.8, places=5)
        self.assertAlmostEqual(model.w_x2, 0.1, places=5)
        self.assertAlmostEqual(model.w_u, 0.5, places=5)

    def test_bayesian_dynamics_moves_toward_observed_coefficient(self):
        model = BayesianScalarDynamics(
            known_b=1.0,
            noise_variance=0.01,
            mean=0.0,
            variance=10.0,
        )
        for _ in range(20):
            x, u = 2.0, 0.5
            x_next = 1.2 * x + u
            model.update(x=x, u=u, x_next=x_next)
        self.assertAlmostEqual(model.mean, 1.2, places=2)
        self.assertLess(model.variance, 0.01)

    def test_mismatch_benchmark_is_reproducible(self):
        result = run_model_mismatch_benchmark()
        self.assertIn("base_total_cost", result)
        self.assertIn("hybrid_total_cost", result)
        self.assertGreater(result["base_total_cost"], 0.0)


if __name__ == "__main__":
    unittest.main()
