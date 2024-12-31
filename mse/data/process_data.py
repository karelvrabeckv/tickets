import os

FOLDER = "./csv"
EXTENSION = ".csv"

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
        row, seat, guest = ticket
        file.write(f"{row},{seat},{guest}\n")

def process_seats(path, name):
  with open(path, "r") as file:
    lines = get_clean_lines(file)

    rows = list(map(int, lines[0]))
    seats = list(map(int, lines[1]))
    guests = lines[2:]

    tickets = []
    for i in range(len(rows)):
      for j in range(len(seats)):
        tickets.append((rows[i], seats[j], guests[i][j]))

    write_to_file(f"processed_{name}.csv", tickets)

def process_lodges(path, name):
  with open(path, "r") as file:
    lines = get_clean_lines(file)

    seats = list(map(int, lines[0]))
    seats_guests = lines[1]
    lodges_seats = list(map(int, lines[2]))
    lodges_guests = lines[3:]

    tickets = []

    for i in range(len(seats)):
      tickets.append((0, seats[i], seats_guests[i]))

    for i in range(5):
      for j in range(len(lodges_seats)):
        tickets.append((i+1, lodges_seats[j], lodges_guests[i][j]))

    write_to_file(f"processed_{name}.csv", tickets)

try:
  for file_name in os.listdir(FOLDER):
    if not file_name.endswith(EXTENSION):
      raise Exception("Invalid extension")
    
    path = os.path.join(FOLDER, file_name)
    name = file_name.split(".")[0]

    if file_name in {"hall.csv", "balcony.csv"}:
      process_seats(path, name)
    elif file_name in {"balcony_left.csv", "balcony_right.csv"}:
      process_lodges(path, name)
except Exception as e:
  print(f"The following error has occured: {e}")
