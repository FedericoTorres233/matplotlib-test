import csv
import os
import shutil

import matplotlib.pyplot as plt
import requests

# Constants
med1_name = os.getenv('MED1')
med2_name = os.getenv('MED2')
output_dir = "./output"
data_dir = "./data"
plot_filename = "plot"


def download_csv(filename, file_key):
  """
  This function downloads a file from google drive

  Parameters:
  filename (string): Name of the file to be stored locally.
  file_key (string): Name of the key whose value is a link to the .csv file
  """

  # Create the output directory if it doesn't exist
  os.makedirs(data_dir, exist_ok=True)

  # Send a GET request to the file URL
  file = requests.get(
      f'https://drive.google.com/uc?id={os.getenv(file_key)}&export=download')

  # Check if the request was successful
  if file.status_code == 200:
    # Save the content of the response to a local file in the data directory
    file_path = os.path.join(data_dir, filename)
    with open(file_path, 'wb') as f:
      f.write(file.content)
    print(f"File {filename} downloaded successfully to the 'output' folder.")
  else:
    print(f"Failed to download {filename}.")


def process_medicine(filepath):
  """
  This function processes the .csv files downloaded

  Parameters:
  filename (string): Path of the .csv file to be processed.

  Returns:
  array[string]: The area of the circle.
  array[float]: The area of the circle.
  """

  # Initial arrays
  dates = []
  dose = []

  # Read csv files
  with open(filepath, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
      date = f"{row['Mes']} {row['Dia']}"  # Concatenate month and day
      dates.append(date)
      dose.append(float(row['Dosis']))

  # Return arrays with csv data
  return dates, dose


# Remove downloaded files
def remove_folder(folder):
  try:
    # Remove the folder and its contents
    shutil.rmtree(folder)
    print(f"Folder {folder} and its contents removed successfully.")
  except Exception as e:
    print(f"An error occurred while removing folder {folder}: {e}")


def plot_data(dates1, doses1, dates2, doses2):
  """
  This function plots the data using matplotlib and stores the graph locally.

  Parameters:
  dates1 (array[float]): Array that contains all dates for medicine 1
  doses1 (array[string]): Array that contains the doses for medicine 1 ordered by date
  dates2 (array[float]): Array that contains all dates for medicine 2
  doses1 (array[string]): Array that contains the doses for medicine 2 ordered by date
  """

  fig, ax1 = plt.subplots(figsize=(10, 6))  # Set fig size
  ax2 = ax1.twinx()  # Create a second y-axis

  # Plot the data for medicine 1 on the first y-axis (left)
  ax1.plot(dates1,
           doses1,
           marker='',
           linestyle='-',
           color='green',
           label=med1_name)
  ax1.set_ylabel(f'Dosis de {med1_name} [mg]', color='blue')

  # Plot the data for drug 2 on the second y-axis (right)
  ax2.plot(dates2,
           doses2,
           marker='',
           linestyle='--',
           color='purple',
           label=med2_name)
  ax2.set_ylabel(f'Dosis de {med2_name} [mg]', color='purple')

  # Add labels and title
  plt.title('Dosis de Medicamentos de Octubre a Marzo')
  plt.xlabel('Fecha [Mes]')

  # Add legend
  lines1, labels1 = ax1.get_legend_handles_labels()
  lines2, labels2 = ax2.get_legend_handles_labels()
  ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

  # Adjust x-axis labels
  n = 7
  ax1.set_xticks(range(0, len(dates1), n))
  ax1.set_xticklabels(dates1[::n], rotation=45)

  # Show the graph
  plt.grid(True)  # Enable grid
  plt.tight_layout()  # Adjust layout
  plt.savefig(f"./output/{plot_filename}.png")  # Save graph


# Set filenames
med1_file_local = f'doses_{med1_name}.csv'
med2_file_local = f'doses_{med2_name}.csv'

# Download files
download_csv(med1_file_local, med1_name)
download_csv(med2_file_local, med2_name)

# Process data from csv files
dates1, doses1 = process_medicine(f'./{data_dir}/{med1_file_local}')
dates2, doses2 = process_medicine(f'./{data_dir}/{med2_file_local}')

# Plot all data
plot_data(dates1, doses1, dates2, doses2)

# Remove data folder
remove_folder(data_dir)
