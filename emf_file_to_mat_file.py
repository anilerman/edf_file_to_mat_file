import pyedflib
import scipy.io
import os
import numpy as np
import datetime


def edf_to_mat(edf_file_path, output_directory):
    # Read the EDF file
    f = pyedflib.EdfReader(edf_file_path)
    n = f.signals_in_file

    signal_labels = f.getSignalLabels()
    signals = np.zeros((n, f.getNSamples()[0]))

    for i in np.arange(n):
        signals[i, :] = f.readSignal(i)

    # Convert header datetime to string
    header = f.getHeader()
    for key, value in header.items():
        if isinstance(value, (list, tuple)):
            header[key] = [v.isoformat() if isinstance(v, (np.datetime64, datetime.datetime)) else v for v in value]
        elif isinstance(value, (np.datetime64, datetime.datetime)):
            header[key] = value.isoformat()

    data = {
        'signals': signals,
        'signal_labels': signal_labels,
        'header': header
    }

    f.close()

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Output file name and path
    base_name = os.path.basename(edf_file_path).replace('.edf', '.mat')
    output_file_path = os.path.join(output_directory, base_name)

    # Save the MAT file
    scipy.io.savemat(output_file_path, data)


def main():
    # Argümanlar doğrudan burada tanımlanıyor
    edf_file_path = '/Users/anilerman/edf_file_to_mat_file/S001R01.edf'
    output_directory = '/Users/anilerman/edf_file_to_mat_file/output'  # Çıkış dizininizi buraya yazın

    edf_to_mat(edf_file_path, output_directory)


if __name__ == "__main__":
    main()
