import math
import random
import time


# Available capacitor bank steps in kVAR
CAPACITOR_STEPS = [5, 5, 10, 10, 20]

# Desired power factor
TARGET_PF = 0.95


def read_system_data():
    """
    Simulate electrical system measurements.

    In a real system, replace these values with measurements
    from appropriate voltage/current/power-factor sensors.
    """

    voltage = random.uniform(225, 235)
    current = random.uniform(10, 30)
    power_factor = random.uniform(0.65, 0.90)

    return voltage, current, power_factor


def calculate_real_power(voltage, current, power_factor):
    """Calculate approximate single-phase real power in kW."""
    power = voltage * current * power_factor
    return power / 1000


def calculate_required_kvar(power_kw, present_pf, target_pf):
    """
    Calculate capacitor reactive power required for
    improving power factor.
    """

    if present_pf >= target_pf:
        return 0

    theta1 = math.acos(present_pf)
    theta2 = math.acos(target_pf)

    kvar = power_kw * (
        math.tan(theta1) - math.tan(theta2)
    )

    return max(0, kvar)


def select_capacitor_steps(required_kvar):
    """
    Select available capacitor steps without exceeding
    the required kVAR as much as possible.
    """

    selected = []
    remaining = required_kvar

    for step in CAPACITOR_STEPS:
        if step <= remaining:
            selected.append(step)
            remaining -= step

    return selected


def calculate_corrected_pf(power_kw, capacitor_kvar):
    """Calculate approximate corrected power factor."""

    if power_kw <= 0:
        return 1.0

    reactive_power = power_kw * math.tan(
        math.acos(0.80)
    )

    corrected_reactive_power = reactive_power - capacitor_kvar

    if corrected_reactive_power <= 0:
        return 1.0

    apparent_power = math.sqrt(
        power_kw ** 2 + corrected_reactive_power ** 2
    )

    return power_kw / apparent_power


def main():

    print("=" * 60)
    print("       AUTOMATIC POWER FACTOR CORRECTION SYSTEM")
    print("=" * 60)

    try:

        while True:

            voltage, current, present_pf = read_system_data()

            power_kw = calculate_real_power(
                voltage,
                current,
                present_pf
            )

            required_kvar = calculate_required_kvar(
                power_kw,
                present_pf,
                TARGET_PF
            )

            selected_steps = select_capacitor_steps(
                required_kvar
            )

            installed_kvar = sum(selected_steps)

            corrected_pf = calculate_corrected_pf(
                power_kw,
                installed_kvar
            )

            print("\n----------------------------------------")
            print(f"Voltage             : {voltage:.2f} V")
            print(f"Current             : {current:.2f} A")
            print(f"Real Power          : {power_kw:.2f} kW")
            print(f"Present Power Factor: {present_pf:.3f}")
            print(f"Target Power Factor : {TARGET_PF:.3f}")
            print(f"Required Capacitor  : {required_kvar:.2f} kVAR")
            print(f"Selected Steps      : {selected_steps}")
            print(f"Installed Capacitor : {installed_kvar} kVAR")
            print(f"Corrected PF        : {corrected_pf:.3f}")

            if present_pf < TARGET_PF:
                print("APFC Status         : Capacitor bank ON")
            else:
                print("APFC Status         : Capacitor bank OFF")

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nAPFC system stopped.")


if __name__ == "__main__":
    main()
