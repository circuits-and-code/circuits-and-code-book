
import numpy as np
import matplotlib.pyplot as plt
import argparse
from enum import Enum

TITLE = "Buck Converter Plot"

# This simulator does not output correct graphs currently, see buck_dcm.py for a simplified version that isn't a simulator but hopefully looks correct

class BuckConverter3StageModel:
    class Stage(Enum):
        ON = 1
        OFF = 2
        DISCONTINUOUS = 3

    def __init__(
        self,
        Vin,
        duty_cycle,
        L,
        C_output,
        C_parasitic,
        R_output,
        f_sw,
        init_running=False,
    ):
        self.Vin = Vin
        self.duty_cycle = duty_cycle
        self.L = L
        self.C_output = C_output
        self.C_parasitic = C_parasitic
        self.R_output = R_output
        self.f_sw = f_sw
        self.stage = self.Stage.ON

        # States
        self.i_inductor_A = [0]
        self.V_output = [0]
        self.V_sw = [0]

        # outputs
        self.i_in = [0]
        self.i_out = [0]

        if init_running:
            self.V_output = [Vin * duty_cycle] # this statement is incorrect for DCM (and possibly why ur simulator isnt working) -daniel
            # self.V_output = [12] # just experimenting, doesn't seem to help tho 
            self.i_out = [self.V_output[0] / R_output]

            P_output = self.V_output[0] * self.i_out[0]
            self.i_in = [P_output / Vin]
            self.i_inductor_A = [self.i_in[0]]

        self.points_per_cycle = 100

    def rk4_integrate(self, A, B, x, u, dt):
        k1 = A @ x + B @ u
        k2 = A @ (x + 0.5 * dt * k1) + B @ u
        k3 = A @ (x + 0.5 * dt * k2) + B @ u
        k4 = A @ (x + dt * k3) + B @ u

        return x + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    def propogate_on_state(self, dt):
        A = np.array(
            [
                [0, -1 / self.L],
                [1 / self.C_output, -1 / (self.R_output * self.C_output)],
            ]
        )
        B = np.array([[1 / self.L], [0]])

        x = np.array([self.i_inductor_A[-1], self.V_output[-1]]).reshape(2, 1)

        x = self.rk4_integrate(A, B, x, np.array([[self.Vin]]), dt)

        self.i_inductor_A.append(x[0].item())
        self.V_output.append(x[1].item())
        self.i_in.append(x[0].item())
        self.i_out.append(x[1].item() / self.R_output)
        self.V_sw.append(self.Vin)

    def propogate_off_state(self, dt):
        A = np.array(
            [
                [0, -1 / self.L],
                [1 / self.C_output, -1 / (self.R_output * self.C_output)],
            ]
        )
        B = np.array([[-1 / self.L], [0]])

        x = np.array([self.i_inductor_A[-1], self.V_output[-1]]).reshape(2, 1)

        V_diode = 0.0

        x = self.rk4_integrate(A, B, x, np.array([[V_diode]]), dt)

        self.i_inductor_A.append(x[0].item())
        self.V_output.append(x[1].item())
        self.i_in.append(0)
        self.i_out.append(x[1].item() / self.R_output)
        self.V_sw.append(-V_diode)

    def propogate_discontinuous_state(self, dt):
        self.i_inductor_A.append(0.0)  # Clamp inductor current to 0
        self.V_output.append(self.V_output[-1])  # Hold voltage steady
        self.i_in.append(0)
        self.i_out.append(self.V_output[-1] / self.R_output)
        self.V_sw.append(-0.7)  # Diode drop

    def propogate_discontinuous_state_actual(self, dt):
        A = np.array(
            [
                [0, -1 / self.L, -1 / self.L],
                [1 / self.C_output, -1 / (self.R_output * self.C_output), 0],
                [-1 / self.C_parasitic, 0, 0],
            ]
        )
        B = np.array([[1 / self.L], [0], [0]])

        x = np.array([self.i_inductor_A[-1], self.V_output[-1], 0]).reshape(3, 1)

        u = np.array([[0]])

        x = self.rk4_integrate(A, B, x, u, dt)

        self.i_inductor_A.append(x[0].item())
        self.V_output.append(x[1].item())
        self.i_in.append(0)
        self.i_out.append(x[1].item() / self.R_output)
        self.V_sw.append(x[2].item())

    def simulate(self, num_cycles):
        tot_time_s = num_cycles / self.f_sw
        period_per_cycle = 1 / self.f_sw
        dt = period_per_cycle / self.points_per_cycle
        self.time_vec = np.linspace(0, tot_time_s, int(tot_time_s / dt))

        on_time_threshold_in_cycle = self.duty_cycle * period_per_cycle

        for t in self.time_vec:
            if t == self.time_vec[-1]:
                break

            if (t % period_per_cycle) < on_time_threshold_in_cycle:
                self.propogate_on_state(dt)
            else:
                if self.i_inductor_A[-1] > 0.01:
                    self.propogate_off_state(dt)
                else:
                    self.propogate_discontinuous_state(dt)


# stealing these from the warg 12s esc lol
Vin = 50
Vout = 12
L = 220 * 10**-6
C_output = 47 * 3 * 10**-6
R_load = Vout / 0.500
C_parasitic = 10 * 10**-8
f_sw = 100 * 10**3


def plotter():
    buck_converter = BuckConverter3StageModel(
        Vin, Vout / Vin, L, C_output, C_parasitic, R_load, f_sw, init_running=True # Duty cycle != Vout/Vin in DCM. -daniel
    )
    buck_converter.simulate(3)
    # Draw !

    # make the plot - have 5 subplots, one for each state
    plt.figure(figsize=(20, 15))

    plt.subplot(4, 1, 1)
    plt.plot(buck_converter.time_vec, buck_converter.i_in, label="Input Current")
    plt.plot(
        buck_converter.time_vec, buck_converter.i_inductor_A, label="Inductor Current"
    )
    plt.title("Currents")
    plt.legend()
    plt.xlabel("Time (s)")

    plt.subplot(4, 1, 2)
    plt.plot(buck_converter.time_vec, buck_converter.i_out, label="Output Current")
    plt.title("Output Current")
    plt.legend()
    plt.xlabel("Time (s)")

    plt.subplot(4, 1, 3)
    plt.plot(buck_converter.time_vec, buck_converter.V_output, label="Output Voltage")
    plt.title("Output Voltage")
    plt.legend()
    plt.xlabel("Time (s)")

    plt.subplot(4, 1, 4)
    plt.plot(buck_converter.time_vec, buck_converter.V_sw, label="Switch Voltage")
    plt.title("Switch Voltage")
    plt.legend()
    plt.xlabel("Time (s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(f"{TITLE} Plotter")
    parser.add_argument("--output_path", help="Path to save image to")

    args = parser.parse_args()

    plotter()

    if args.output_path is not None:
        plt.savefig(args.output_path)
    else:
        plt.show()
