import os
import PyPDF2
import re

DATA_FOLDER = "./data"
TICKETS_FOLDER = "./tickets-balcony-sides"
EXTENSION = ".pdf"

def read_processed_data(file_name):
  data = {}
  path = os.path.join(DATA_FOLDER, file_name)
  with open(path, "r") as file:
    lines = file.readlines()
    for line in lines:
      clean_line = line.strip()
      row, seat, guest = clean_line.split(",")
      if not data.get(row):
        data[row] = {}
      data[row][seat] = guest
  return data

def convert_lodge(lodge):
  match lodge:
    case "I":
      return "1"
    case "II":
      return "2"
    case "III":
      return "3"
    case "IV":
      return "4"
    case "V":
      return "5"
    case "VI":
      return "6"

try:
  balcony_left = read_processed_data("processed_balcony_left.csv")
  balcony_right = read_processed_data("processed_balcony_right.csv")

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

      lodge_matches = re.findall(r"lóže\s*(\S+).", text)
      side_matches = re.findall(r"STRANA\s*(\S+)", text)
      seat_matches = re.findall(r"SEDADLO\s*(\d+)", text)

      lodge = convert_lodge(lodge_matches[0]) if lodge_matches else "0"
      side = side_matches[0] if side_matches else None
      seat = seat_matches[0] if seat_matches else None
      
      if side == "vlevo":
        guest = balcony_left[lodge][seat]
      elif side == "vpravo":
        guest = balcony_right[lodge][seat]

    os.rename(
      os.path.join(TICKETS_FOLDER, file_name),
      os.path.join(
        TICKETS_FOLDER, 
        f"21. 12. Rybova mse" +
        (f"_balkon_{side}_1_{seat}" if lodge == "0" else f"_loze_{lodge}_{side}_{seat}") +
        f" {guest}{EXTENSION}"
      )
    )
except Exception as e:
  print(f"The following error has occured: {e}")
