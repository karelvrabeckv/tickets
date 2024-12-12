import os
import PyPDF2
import re

DATA_FOLDER = "./data"
TICKETS_FOLDER = "./tickets"
EXTENSION = ".pdf"

def read_processed_data(file_name):
  data = {}
  path = os.path.join(DATA_FOLDER, file_name)
  with open(path, "r") as file:
    lines = file.readlines()
    for line in lines:
      clean_line = line.strip()
      row, seat, name = clean_line.split(",")
      if not data.get(row):
        data[row] = {}
      data[row][seat] = name
  return data

try:
  seats = read_processed_data("processed_seats.csv")
  tables = read_processed_data("processed_tables.csv")

  for file_name in os.listdir(TICKETS_FOLDER):
    if not file_name.endswith(EXTENSION):
      raise Exception("Invalid extension")

    path = os.path.join(TICKETS_FOLDER, file_name)
    with open(path, "rb") as file:
      reader = PyPDF2.PdfReader(file)
      if len(reader.pages) == 0:
        raise Exception("No pages in PDF file")

      page = reader.pages[0]
      text = page.extract_text()
      words = text.split()
      
      date_matches = re.findall(r"(\d+)\.\s*(\d+)\.", text)
      table_matches = re.findall(r"Stůl\s*(\d+)", text)
      row_matches = re.findall(r"Řada\s*(\d+)", text)
      seat_matches = re.findall(r"Místo\s*(\d+)", text)
 
      date = f"{date_matches[0][0]}. {date_matches[0][1]}."
      name = "".join(words[0:3])

      table = table_matches[0] if table_matches else None
      row = row_matches[0] if row_matches else None
      seat = seat_matches[0] if seat_matches else None
      guest = tables[table][seat] if table else seats[row][seat]

    os.rename(
      os.path.join(TICKETS_FOLDER, file_name),
      os.path.join(
        TICKETS_FOLDER, 
        f"{date} {name}_" +
        (f"stul_{table}" if table else f"{row}") +
        f"_{seat} {guest}{EXTENSION}"
      )
    )
except Exception as e:
  print(f"The following error has occured: {e}")
