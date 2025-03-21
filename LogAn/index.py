import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def parse_log_file(log_file, log_pattern):
    """Parses a log file based on a given regular expression pattern."""
    log_entries = []
    with open(log_file, 'r') as f:
        for line in f:
            match = re.search(log_pattern, line)
            if match:
                log_entries.append(match.groupdict()) #capture groups to a dictionary.
    return log_entries

def analyze_log_data(log_data):
    """Analyzes the parsed log data using pandas."""
    df = pd.DataFrame(log_data)
    if not df.empty: #handle empty dataframes.
        # Example: Count occurrences of different log levels
        if 'level' in df.columns:
            level_counts = df['level'].value_counts()
            print("Log Level Counts:\n", level_counts)

        # Example: Basic time-based analysis (if timestamps are present)
        if 'timestamp' in df.columns:
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['hour'] = df['timestamp'].dt.hour
                hourly_counts = df['hour'].value_counts().sort_index()
                print("\nHourly Log Counts:\n", hourly_counts)
                return df #returning df for visualization.
            except:
                print("\nTimestamp column exists, but could not be parsed to datetime.")
                return df
        else:
            return df

    else:
        print("No log data to analyze.")
        return None

def visualize_log_data(df):
    """Visualizes the analyzed log data."""
    if df is not None:
        if 'level' in df.columns:
            plt.figure(figsize=(8, 6))
            sns.countplot(x='level', data=df)
            plt.title('Log Level Distribution')
            plt.show()

        if 'hour' in df.columns:
            plt.figure(figsize=(12, 6))
            sns.lineplot(x=df['hour'].value_counts().sort_index().index, y=df['hour'].value_counts().sort_index().values)
            plt.title('Hourly Log Activity')
            plt.xlabel('Hour')
            plt.ylabel('Log Count')
            plt.xticks(range(24))
            plt.grid(True)
            plt.show()

# Example Usage (replace with your log file and pattern):
log_file = 'example.log'  # Replace with your log file name
log_pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<level>\w+) - (?P<message>.*)' #example log pattern.

# Create a dummy log file for testing.
with open(log_file, 'w') as f:
    f.write("2023-10-27 10:00:00 INFO - User logged in\n")
    f.write("2023-10-27 10:15:00 WARNING - Invalid input\n")
    f.write("2023-10-27 11:00:00 ERROR - Database connection failed\n")
    f.write("2023-10-27 12:00:00 INFO - Process completed\n")
    f.write("2023-10-27 12:30:00 INFO - User logged out\n")
    f.write("2023-10-27 13:00:00 WARNING - File not found\n")
    f.write("2023-10-27 13:15:00 ERROR - Memory allocation error\n")
    f.write("2023-10-27 14:00:00 INFO - System restart\n")
    f.write("2023-10-27 14:30:00 INFO - System online\n")

parsed_logs = parse_log_file(log_file, log_pattern)
analyzed_data = analyze_log_data(parsed_logs)
visualize_log_data(analyzed_data)