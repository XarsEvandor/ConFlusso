def get_delay_frequencies(csv_filepath):
    """
    Reads a CSV file with a specific format (Timestamp, AccelX, AccelY, AccelZ, GyroX, GyroY, GyroZ)
    and returns the frequencies of each unique non-zero delay between two consecutive timestamps.

    :param csv_filepath: Path to the CSV file.
    :return: A dictionary with delays as keys and their frequencies as values.
    """
    import pandas as pd

    # Load the CSV file
    df = pd.read_csv(csv_filepath)

    # Calculate the time difference between consecutive data points
    df['Time_Diff'] = df['Timestamp'].diff()

    # Filter out zero delays and calculate the frequency of each non-zero delay
    delay_frequencies = df['Time_Diff'][df['Time_Diff']
                                        > 0].value_counts().sort_index()

    return delay_frequencies.to_dict()


# Example usage
# Replace with your actual CSV file path
csv_filepath = 'accel_gyro_data.csv'
delay_frequencies = get_delay_frequencies(csv_filepath)
print("Delay Frequencies:", delay_frequencies)
