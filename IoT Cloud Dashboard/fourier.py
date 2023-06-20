import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
"""# Sample data
x_axis = np.array(
    [-0.02352, -0.02352, -0.02352, -0.26362, -0.19992, -0.19992, -0.05586, 0.01176, 0.01176, -0.0588, -0.12936,
     -0.12936, -0.18816, -0.18816, -0.20286, -0.19698, -0.19698, -0.08036, 0.05096, 0.05096, -0.02744, -0.08918,
     -0.08918, -0.04214, -0.02058, -0.02058, 0.00196, 0.02548, 0.02548, -0.00098, -0.01372, -0.01372, 0.00588, 0.00588,
     -0.06076, -0.10486, -0.10486, -0.06272, -0.19502, -0.19502, -0.19404, -0.0784, -0.0784, -0.0245, 0.01372, 0.01372,
     -0.07056, -0.09702, -0.09702, -0.00784, 0.04704, 0.04704, -0.00392, -0.11662, -0.11662, -0.2205, -0.2205, -0.2303,
     -0.24794, -0.24794, -0.11662, 0.00882, 0.00882, -0.08526, -0.12936, -0.12936, -0.02254, 0.06566, 0.06566, 0.10682,
     0.11368, 0.11368, 0.00196, -0.07546, -0.07546, -0.03626, -0.03626, -0.03038, -0.12936, -0.12936, -0.16268,
     -0.21658, -0.21658, -0.26656, -0.21462, -0.21462, -0.12642, -0.07252, -0.07252, -0.18718, -0.2156, -0.2156,
     0.00098, 0.0637, 0.0637, -0.0343, -0.05488, -0.05488, -0.01372, -0.01372, -0.0196, -0.05978, -0.05978, -0.06664,
     -0.19796, -0.19796, -0.25872, -0.15974, -0.15974, 0.05194, 0.1519, 0.1519, -0.01862, -0.08624, -0.08624, 0.03528,
     0.07938, 0.07938, -0.06468, -0.06468, -0.18326, -0.23912, -0.23912, -0.2009, -0.18326, -0.18326, -0.16268,
     -0.10192, -0.10192, -0.04802, -0.02352, -0.02352, -0.01078, 0.03234, 0.03234, 0.09114, 0.08036, 0.08036, -0.05194,
     -0.11368, -0.11368, -0.04116, -0.04116, 0.06958, 0.03234, 0.03234, -0.07448, -0.11172, -0.11172, -0.0147, 0.0441,
     0.0441, 0.00686, -0.0098, -0.0098, -0.0049, -0.0147, -0.0147, 0.05586, 0.1274, 0.1274, 0.00784, 0.00784, -0.17444,
     -0.13328, -0.13328, 0.02646, -0.09016, -0.09016, -0.2205, -0.19306, -0.19306, -0.00098, 0.10094, 0.10094, 0.07252,
     0.0588, 0.0588, -0.01078, -0.0441, -0.0441, 0.01666, 0.01666, -0.01764, -0.08526, -0.08526, -0.02744, -0.11564,
     -0.11564, -0.1813, -0.13622, -0.13622, 0.01274, 0.11956, 0.11956, -0.08428, -0.21756, -0.21756, -0.08918,
     0.00882])  # Replace ellipsis with the full array"""

dataframe = pd.read_csv('dataset_vib_aws.csv')
x_axis = np.array(dataframe['x'])
dataframe.to_csv('dataset_vib_aws.csv', encoding='utf-8', index=False)

print(x_axis)
# Perform Fourier transforms
x_freq = np.fft.fft(x_axis)
#y_freq = np.fft.fft(y_axis)
#z_freq = np.fft.fft(z_axis)

# Calculate the frequencies corresponding to the Fourier transforms
num_samples = len(x_axis)
sampling_freq = 1 / (50 * 1e-6)  # Measure_Period_us converted to Hz
freq_axis = np.fft.fftfreq(num_samples, d=1 / sampling_freq)

# Print the frequency and magnitude components
for freq, x_magnitude in zip(freq_axis, x_freq):
    print(f"Frequency: {freq} Hz")
    print(f"X-axis Vibration Magnitude: {np.abs(x_magnitude)}")
    #(f"Y-axis Magnitude: {np.abs(y_magnitude)}")
    #print(f"Z-axis Magnitude: {np.abs(z_magnitude)}")
    print()

# Plot the Fourier transform results
plt.figure(figsize=(8, 4))

# X-axis Fourier Transform
plt.plot(abs(freq_axis), np.abs(x_freq))
plt.title('X-axis Fourier Transform')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
"""

# Y-axis Fourier Transform
plt.subplot(132)
plt.plot(abs(freq_axis), np.abs(y_freq))
plt.title('Y-axis Fourier Transform')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')

# Z-axis Fourier Transform
plt.subplot(133)

plt.plot(abs(freq_axis), np.abs(z_freq))
plt.title('Z-axis Fourier Transform')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')

plt.tight_layout()"""
plt.show()
