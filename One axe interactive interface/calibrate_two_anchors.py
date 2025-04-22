import math

h = 21 * 1e-3

def make_calibration(base_distance_to_anchor1, calibration_distance_to_anchor1, base_distance_to_anchor2, calibration_distance_to_anchor2):


    n_anchor1 = calculate_attenuation_rate(base_amplitude_to_anchor1, calibration_amplitude_to_anchor1,
                                           base_distance_to_anchor1, calibration_distance_to_anchor1)
    n_anchor2 = calculate_attenuation_rate(base_amplitude_to_anchor2, calibration_amplitude_to_anchor2,
                                           base_distance_to_anchor2, calibration_distance_to_anchor2)