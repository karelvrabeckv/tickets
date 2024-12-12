import os
import PyPDF2
import re

FOLDER = "./tickets"
EXTENSION = ".pdf"

try:
  for file_name in os.listdir(FOLDER):
    if file_name.endswith(EXTENSION):
      path = os.path.join(FOLDER, file_name)
      with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        date_pattern = r"(\d+)\.\s*(\d+)\."
        row_pattern = r"Řada (\d+)"
        seat_pattern = r"Místo (\d+)"

        if len(reader.pages) == 0:
          raise Exception("No pages in PDF file")

        page = reader.pages[0]
        text = page.extract_text()
        words = text.split()
        
        date_matches = re.findall(date_pattern, text)
        row_matches = re.findall(row_pattern, text)
        seat_matches = re.findall(seat_pattern, text)
        
        name = words[0]

        day = int(date_matches[0][0])
        month = int(date_matches[0][1])
        
        balcony = True if "Balkon" in text else False

        row = int(row_matches[0])
        seat = int(seat_matches[0])

      os.rename(
        os.path.join(FOLDER, file_name),
        os.path.join(
          FOLDER, 
          f"{day}. {month}. {name}_" +
          ("balkon_" if balcony else "") +
          f"{row}_{seat}{EXTENSION}"
        )
      )
except Exception as e:
  print(f"The following error has occured: {e}")
