import csv
import os
import shutil

import matplotlib.pyplot as plt
import requests

# Constants
medicamento1 = os.getenv('med1')
medicamento2 = os.getenv('med2')
output_dir = "./output"
data_dir = "./data"


def download_csv(filename, file_url):

  # Create the output directory if it doesn't exist
  os.makedirs(data_dir, exist_ok=True)

  # Send a GET request to the file URL
  dosis = requests.get(
      f'https://drive.google.com/uc?id={os.getenv(file_url)}&export=download')

  # Check if the request was successful
  if dosis.status_code == 200:
    # Save the content of the response (file) to a local file in the output directory
    file_path = os.path.join(data_dir, filename)
    with open(file_path, 'wb') as f:
      f.write(dosis.content)
    print(f"File {filename} downloaded successfully to the 'output' folder.")
  else:
    print(f"Failed to download {filename}.")


def procesar_medicamento(filepath):

  # Listas para almacenar los datos
  fechas = []
  dosis = []

  # Leer el archivo CSV
  with open(filepath, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
      fecha = f"{row['Mes']} {row['Dia']}"  # Concatenamos mes y día
      fechas.append(fecha)
      dosis.append(float(row['Dosis']))

  return fechas, dosis


# Remove downloaded files
def remove_folder(folder):
  try:
    # Remove the folder and its contents
    shutil.rmtree(folder)
    print(f"Folder {folder} and its contents removed successfully.")
  except Exception as e:
    print(f"An error occurred while removing folder {folder}: {e}")


def plot_data(fecha1, dosis1, fecha2, dosis2):
  # Crear el gráfico
  fig, ax1 = plt.subplots(figsize=(10, 6))  # Tamaño de la figura
  ax2 = ax1.twinx()  # Crear un segundo eje y

  # Plotear los datos del medicamento 1 en el primer eje y (izquierda)
  ax1.plot(fecha1,
           dosis1,
           marker='',
           linestyle='-',
           color='blue',
           label=medicamento1)
  ax1.set_ylabel(f'Dosis de {medicamento1} [mg]', color='blue')

  # Plotear los datos del medicamento 2 en el segundo eje y (derecha)
  ax2.plot(fecha2,
           dosis2,
           marker='',
           linestyle='--',
           color='purple',
           label=medicamento2)
  ax2.set_ylabel(f'Dosis de {medicamento2} [mg]', color='purple')

  # Añadir etiquetas y título
  plt.title('Dosis de Medicamentos de Octubre a Marzo')
  plt.xlabel('Fecha [Mes]')

  # Añadir leyendas
  lines1, labels1 = ax1.get_legend_handles_labels()
  lines2, labels2 = ax2.get_legend_handles_labels()
  ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

  # Ajustar las etiquetas del eje x
  n = 7
  ax1.set_xticks(range(0, len(fecha1), n))
  ax1.set_xticklabels(fecha1[::n], rotation=45)

  # Mostrar la gráfica
  plt.grid(True)  # Habilitar cuadrícula
  plt.tight_layout()  # Ajustar diseño
  plt.savefig("./output/plot.png")  # Guardar la gráfica en un archivo


# Set filenames
med1_file = f'dosis_{medicamento1}.csv'
med2_file = f'dosis_{medicamento2}.csv'

# Descargar archivos
download_csv(med1_file, medicamento1)
download_csv(med2_file, medicamento2)

# Procesar datos
fecha1, dosis1 = procesar_medicamento(f'./{data_dir}/{med1_file}')
fecha2, dosis2 = procesar_medicamento(f'./{data_dir}/{med2_file}')

# Plot data
plot_data(fecha1, dosis1, fecha2, dosis2)

# Remove folder
remove_folder(data_dir)
