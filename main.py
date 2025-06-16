from collections import deque
import pandas as pd

class Building:
    def __init__(self, file):
        self.excel_file = pd.ExcelFile(file)
        self.floorList = {}  # floor name -> dataframe
        for sheet_name in self.excel_file.sheet_names:
            if sheet_name in self.floorList:
                raise Exception(f"Floor '{sheet_name}' already exists")
            else:
                self.floorList[sheet_name] = self.excel_file.parse(sheet_name)

class Room:
    def __init__(self, name, beds, status, row, col):
        self.name = name
        self.beds = int(beds)
        self.status = bool(status)  # True = vacant
        self.row = row
        self.col = col
        self.next = None  # For LinkedList traversal

    def __repr__(self):
        return f"Room({self.name}, Beds={self.beds}, Vacant={self.status}, Pos=({self.row},{self.col}))"

class Lobby:
    def __init__(self, header_room=None, number_of_rooms=0):
        if header_room is None:
            self.room_header = None
            self.room_iter = None
            self.start_row = None
            self.end_row = None
            self.start_col = None
            self.end_col = None
            self.number_of_rooms = number_of_rooms
        else:
            self.room_header = header_room
            self.room_iter = header_room
            self.start_row = header_room.row
            self.end_row = header_room.row
            self.start_col = header_room.col
            self.end_col = header_room.col
            self.number_of_rooms = number_of_rooms

    def add_room(self, room):
        if self.room_header is None:
            self.room_header = room
            self.room_iter = room
            self.start_row = room.row
            self.end_row = room.row
            self.start_col = room.col
            self.end_col = room.col
        else:
            self.room_iter.next = room
            self.room_iter = room
            self.end_row = room.row
            self.end_col = room.col
        self.number_of_rooms += 1

    def __repr__(self):
        return f"Lobby(Rooms={self.number_of_rooms}, From=({self.start_row},{self.start_col}) To=({self.end_row},{self.end_col}))"

# Helpers
def is_room(cell):
    return isinstance(cell, str) and cell.lower().startswith("room")

def is_valid(cell):
    return isinstance(cell, str) and (cell.lower().startswith("room") or cell.lower() == "hall")

# BFS to gather connected rooms/halls
def bfs(grid, start, visited):
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    lobby = Lobby()

    while queue:
        r, c = queue.popleft()
        if (r, c) in visited:
            continue

        visited.add((r, c))
        cell = grid[r][c]

        if is_room(cell):
            parts = cell.split(':')
            try:
                room_number = parts[0].strip().split()[1] if len(parts[0].strip().split()) > 1 else "?"
                bed_count = int(parts[1].strip().split()[0]) if len(parts) > 1 else 1
                is_vacant = parts[2].strip().lower() == 'vacant' if len(parts) > 2 else True

                room = Room(room_number, bed_count, is_vacant, r, c)
                lobby.add_room(room)
            except Exception as e:
                print(f"Error parsing room at ({r},{c}): '{cell}' -> {e}")

        # Check 4-directionally
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if is_valid(grid[nr][nc]):
                    queue.append((nr, nc))

    return lobby

# Find all room clusters
def find_all_lobbies(grid):
    visited = set()
    lobbies = []
    rows, cols = len(grid), len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and is_room(grid[r][c]):
                lobby = bfs(grid, (r, c), visited)
                if lobby.number_of_rooms > 1:
                    lobbies.append(lobby)

    return lobbies

# Main driver
building = Building('building_test.xlsx')

for sheet_name, df in building.floorList.items():
    floor_layout = df.values.tolist()
    print(f"\nLobbies in Floor: {sheet_name}")
    lobby_list = find_all_lobbies(floor_layout)
    for lobby in lobby_list:
        print(lobby)
        iter = lobby.room_header
        while iter != None:
            print(iter)
            iter = iter.next
    # print(floor_layout)
