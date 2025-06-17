from collections import deque
import numpy as np
import pandas as pd

# Room node for Linked List
class RoomNode:
    def __init__(self, row, col, name):
        self.row = row
        self.col = col
        self.raw_name = name
        self.next = None

        # Defaults
        # Example: Room 101 | 3 Beds | Vacant
        self.room_name = None
        self.vacancy = True
        self.num_beds = 1

        # Try to parse the name into components
        try:
            parts = [part.strip() for part in name.split("|")]
            if len(parts) >= 1:
                self.room_name = parts[0]
            if len(parts) >= 2:
                if "bed" in parts[1].lower():
                    self.num_beds = int(parts[1].split()[0])
            if len(parts) >= 3:
                self.vacancy = parts[2].lower() in ["vacant", "available", "yes"]
        except Exception as e:
            print(f"Failed to parse room info '{name}': {e}")

# Lobby class to store linked list of rooms
class Lobby:
    def __init__(self, header_room, number_of_rooms=0):
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
            self.number_of_rooms = number_of_rooms
            self._set_bounds()

    def _set_bounds(self):
        rows = []
        cols = []
        ptr = self.room_header
        while ptr:
            rows.append(ptr.row)
            cols.append(ptr.col)
            ptr = ptr.next
        self.start_row = min(rows)
        self.end_row = max(rows)
        self.start_col = min(cols)
        self.end_col = max(cols)

    def __repr__(self):
        return f"Lobby(Rooms={self.number_of_rooms}, From=({self.start_row},{self.start_col}) To=({self.end_row},{self.end_col}))"

# Helper functions to classify cell types
def is_room(cell):
    return isinstance(cell, str) and cell.lower().startswith("room")

def is_hall(cell):
    return isinstance(cell, str) and cell.lower() == "hall"

def is_corridor(cell):
    return isinstance(cell, str) and cell.lower() == "corridor"

# Checks if cell is part of a lobby path
def is_valid_lobby_cell(cell):
    return is_room(cell) or is_hall(cell)

# Checks if this room is adjacent to a corridor
def is_corridor_adjacent(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and is_corridor(grid[nr][nc]):
            return True
    return False

# Simplified BFS to enforce earlier-style linear traversal
def bfs(grid, start, visited):
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    local_visited = set()
    room_nodes = []
    prev_room_node = None
    head = None

    while queue:
        r, c = queue.popleft()
        if (r, c) in visited or (r, c) in local_visited:
            continue

        cell = grid[r][c]
        if not is_valid_lobby_cell(cell):
            continue

        local_visited.add((r, c))

        if is_room(cell):
            node = RoomNode(r, c, cell)
            if not head:
                head = node
            if prev_room_node:
                prev_room_node.next = node
            prev_room_node = node
            room_nodes.append(node)

        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:  # Right, Down, Left, Up
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) not in visited and (nr, nc) not in local_visited:
                    if is_valid_lobby_cell(grid[nr][nc]):
                        queue.append((nr, nc))

    for r, c in local_visited:
        visited.add((r, c))

    return Lobby(head, len(room_nodes)) if head else None

# Finds all valid lobbies in a grid layout
def find_all_lobbies(grid):
    visited = set()
    lobbies = []
    rows, cols = len(grid), len(grid[0])
    priority = []  
    fallback = []  

    for r in range(rows):
        for c in range(cols):
            if is_room(grid[r][c]):
                if is_corridor_adjacent(grid, r, c):
                    priority.append((r, c))
                else:
                    fallback.append((r, c))

    for r, c in priority + fallback:
        if (r, c) not in visited:
            lobby = bfs(grid, (r, c), visited)
            if lobby and lobby.number_of_rooms > 0:
                lobbies.append(lobby)

    return lobbies
