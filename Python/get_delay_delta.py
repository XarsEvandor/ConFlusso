def get_delay_frequencies(csv_filepath):
    """
    Reads a CSV file with a specific format (Roll, AccelX, AccelY, AccelZ, GyroX, GyroY, GyroZ)
    and returns the frequencies of each unique non-zero delay between two consecutive Rolls.

    :param csv_filepath: Path to the CSV file.
    :return: A dictionary with delays as keys and their frequencies as values.
    """
    import pandas as pd

    # Load the CSV file
    df = pd.read_csv(csv_filepath)
    
    # Convert Roll from microseconds to milliseconds by truncating
    df['Roll'] = df['Roll'] // 1000

    # Calculate the time difference between consecutive data points
    df['delta'] = df['Roll'].diff()

    # Filter out zero delays and calculate the frequency of each non-zero delay
    delay_frequencies = df['delta'][df['delta']
                                        > 0].value_counts().sort_index()

    return delay_frequencies.to_dict()


# Example usage
# Replace with your actual CSV file path
csv_filepath = 'orientation_data.csv'
delay_frequencies = get_delay_frequencies(csv_filepath)
print("Delay Frequencies:", delay_frequencies)
