import os

FOLDER = "./csv"
EXTENSION = ".csv"
NUM_OF_ROWS = 19
SEATS_PER_ROW = 18

def get_clean_lines(file):
    lines = file.readlines()
    for i in range(len(lines)):
      clean_line = lines[i].strip()
      words = clean_line.split(",")
      lines[i] = words
    return lines

def write_to_file(file_name, tickets):
    with open(file_name, "a") as file:
      for ticket in tickets:
        table, seat, name = ticket
        file.write(f"{table},{seat},{name}\n")

def process_seats(path):
  with open(path, "r") as file:
    lines = get_clean_lines(file)

    rows = list(range(1, NUM_OF_ROWS + 1))
    seats = [i for i in range(SEATS_PER_ROW, 0, -1)]

    tickets = []
    for i in range(len(lines) - 1):
      row = rows[i]
      for j, name in enumerate(lines[i]):
        if j == 0:
          seat = seats[j]
          tickets.append((row, seat, name))
        elif j == len(lines[i]) - 1:
          seat = seats[-1]
          tickets.append((row, seat, name))
        else:
          seat = seats[((j - 1) * 2) + 1]
          tickets.append((row, seat, name))
          seat = seats[((j - 1) * 2) + 2]
          tickets.append((row, seat, name))

    for j, name in enumerate(lines[-1]):
      row = rows[-1]
      seat = seats[j * 2]
      tickets.append((row, seat, name))
      seat = seats[(j * 2) + 1]
      tickets.append((row, seat, name))

    write_to_file("processed_seats.csv", tickets)

def process_tables(path):
  with open(path, "r") as file:
    lines = get_clean_lines(file)

    tickets = []
    for i in range(1, len(lines), 2):
      num_of_repetitions = len(lines[i]) // len(lines[0])
      tables = [table for table in lines[0] for _ in range(num_of_repetitions)]
      ticket = zip(tables, lines[i], lines[i + 1])
      tickets += list(ticket)

    write_to_file("processed_tables.csv", tickets)

try:
  for file_name in os.listdir(FOLDER):
    if not file_name.endswith(EXTENSION):
      raise Exception("Invalid extension")
    
    path = os.path.join(FOLDER, file_name)
    if "seats" in file_name:
      process_seats(path)
    elif "tables" in file_name:
      process_tables(path)
except Exception as e:
  print(f"The following error has occured: {e}")
