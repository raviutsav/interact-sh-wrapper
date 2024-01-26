import pandas as pd

def empty_file(file_path):
    """
    This function erases the content of file.

    Args:
        file_path (string): path to reach the file.

    Returns:
        Void
    """
    try:
        open(file_path, 'w').close()
    except Exception as e:
        print(f"Not able to locate/write to file: {e}")


def read_and_store_data(file_path, interaction_data):
    """
    This function read and store the data extracted from the file into dataframe

    Args:
        file_path (string): path of the file which is containing data.

    Returns:
        Void
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.replace('\x00','')
                line = line[:-1]
                data_in_list = line.split(' ')

                link = data_in_list[0][1:-1]
                datestamp = data_in_list[-2]
                timestamp = data_in_list[-1]

                new_data = {'datetime': pd.to_datetime(datestamp + " " + timestamp), 'value': ' '.join(data_in_list[1:])}
                interaction_data[link] = interaction_data[link].append(new_data, ignore_index=True)

    except  Exception as e:
        print(f"An error occured: {e}")

    empty_file(file_path)

def query_data(start_time, end_time, df):
    """
    This function filters the dataframe according to given data and time stamp limit.

    Args:
        start_time (Pandas: datetime): Start date and time from which we want data.
        end_time (Pandas: datetime): End date and time till which we want data.
        df (Pandas: DataFrame): DataFrame which is storing the data.

    Returns:
        (Pandas: DataFrame): DataFrame obtained after filtering according to given parameters.
    """
    mask = (df['datetime'] >= start_time) & (df['datetime'] <= end_time)
    result = df[mask]
    return result
