import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from scipy import stats as st
import pandas as pd

def confidence_interval_t(data, confidence=0.95):
    data_array = 1.0 * np.array(data)
    degree_of_freedom = len(data_array) - 1
    sample_mean, sample_standard_error = np.mean(data_array), st.sem(data_array)
    t = st.t.ppf((1 + confidence) / 2., degree_of_freedom)
    margin_of_error = sample_standard_error * t
    Confidence_Interval = 1.0 * np.array([sample_mean - margin_of_error, sample_mean + margin_of_error])
    return sample_mean, Confidence_Interval, margin_of_error

sent_packets_vector = np.array([[200],[400],[600],[800],[1000]])
sent_packets_array = np.repeat(sent_packets_vector, 10, axis=1)

Packet_received_100_filename = 'Packet_received_100.csv'
Packet_received_200_filename = 'Packet_received_200.csv'
Packet_received_300_filename = 'Packet_received_300.csv'
Packet_received_400_filename = 'Packet_received_400.csv'
Packet_received_500_filename = 'Packet_received_500.csv'
Packet_received_filename = [Packet_received_100_filename, Packet_received_200_filename, Packet_received_300_filename,
                            Packet_received_400_filename, Packet_received_500_filename]
no_simulation_runs = 10
number_of_aircraft = ['100', '200', '300', '400', '500']
no_elements_variable_values = len(number_of_aircraft)

received_packets_array = np.empty(shape=[no_elements_variable_values, no_simulation_runs])
row_index = 0
for file in Packet_received_filename:
    Packet_received_dataframe = pd.read_csv(file)
    Packet_received_row = Packet_received_dataframe[(Packet_received_dataframe.type == 'scalar')].value.to_numpy()
    received_packets_array[row_index] = Packet_received_row
    row_index += 1

sample_mean, Confidence_Interval_array, margin_of_error = confidence_interval_t(received_packets_array[0], confidence=0.95)
sample_mean_received_array = 1.0 * np.array(sample_mean)
margin_of_error_received_array = 1.0 * np.array(margin_of_error)

for row in range(1, no_elements_variable_values):
    sample_mean, confidence_Interval, margin_of_error = confidence_interval_t(received_packets_array[row], confidence=0.95)
    sample_mean_received_array = np.append(sample_mean_received_array, sample_mean)
    margin_of_error_received_array = np.append(margin_of_error_received_array, margin_of_error)
##########################################################
# Received Packets
##########################################################


x_data = number_of_aircraft
y_data = sample_mean_received_array
margin_of_error = margin_of_error_received_array

x_pos = np.arange(len(x_data))
width=0.0
x_pos1 = [x - width for x in x_pos]
x_pos2 = [x + width for x in x_pos]

fig, ax = plt.subplots()
ax.errorbar(x_pos1, sample_mean_received_array,
            yerr=margin_of_error,
            fmt='o',
            ecolor='dimgrey',
            color='black',
            elinewidth=1,
            markersize=3,
            capsize=4,
            capthick=1,
            label='Received packets'
            )

ax.errorbar(x_pos2, sent_packets_vector,
            fmt='s',
            ecolor='dimgrey',
            color='black',
            elinewidth=1,
            markersize=3,
            capsize=4,
            capthick=1,
            label='Sent packets'
            )
ax.legend()
ax.set_xlabel('Number of packets', fontname='Helvetica', fontsize=10)  # , fontweight='bold'
ax.set_ylabel('Number of aircraft', fontname='Helvetica', fontsize=10)  # , fontweight='bold'
ax.set_xticks(x_pos)
ax.set_xticklabels(x_data)
ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=3, color='black', labelsize=8)
ax.tick_params(which='minor', length=2, color='black')
ax.grid(True, ls=(0, (1, 8)), c='black', linewidth=0.5)  # , linewidth=0.5
ax.xaxis.grid(ls=(0, (1, 5)))
ax.grid(which='minor', ls=(0, (1, 10)), c='black', alpha=0.7, linewidth=0.5)
# Save the figure and show
plt.tight_layout()
plt.savefig('received_packets_vs_no_of_aircraft.pdf', format='pdf', dpi=1200)
plt.show()
