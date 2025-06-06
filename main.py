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
    def __init__(self, header_room = None, number_of_rooms = 0):
        if(header_room == None):
            self.room_header = None
            self.room_iter = None
            self.start_row = None
            self.end_row = None
            self.start_col = None
            self.end_col = None
            self.number_of_rooms = number_of_rooms
        else:
            self.room_header = header_room  # Linked list start
            self.room_iter = header_room
            self.start_row = header_room.row
            self.end_row = header_room.row
            self.start_col = header_room.col
            self.end_col = header_room.col
            self.number_of_rooms = number_of_rooms
    
    def add_room(self,room):
        if(self.room_header == None):
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
        self.number_of_rooms+=1


    def __repr__(self):
        return f"Lobby(Rooms={self.number_of_rooms}, From=({self.start_row},{self.start_col}) To=({self.end_row},{self.end_col}))"


def is_room(cell):
    return isinstance(cell, str) and cell.startswith("Room")




# Main
building = Building('building_test.xlsx')

for sheet_name, df in building.floorList.items():
    floor_layout = df.values.tolist()

    rows = len(floor_layout)
    cols = len(floor_layout[0])

    # print(floor_layout)

    linear_lobbies = []

    for r in range(rows):
        lobby = Lobby()
        for c in range(cols):
            if(is_room(floor_layout[r][c])):
                parts = floor_layout[r][c].split(':')
                if len(parts) >= 3:
                    room_number = parts[0].split()[1] 
                    bed_count = parts[1].strip().split()[0] 
                    is_vacant = parts[2].strip().lower() == 'vacant' 

                    room = Room(room_number,bed_count,is_vacant, r, c)
                    lobby.add_room(room)
                elif len(parts) ==1:
                    room_number = parts[0].split()[1]
                    
                    room = Room(room_number,1,True, r, c)
                    lobby.add_room(room)
                elif len(parts) ==2:
                    room_number = parts[0].split()[1]
                    
                    room = Room(room_number,bed_count,True, r, c)
                    lobby.add_room(room)
                else:
                    raise Exception("Not enough arguments in room cell declaration")
            else:
                if lobby.number_of_rooms > 0:
                    linear_lobbies.append(lobby)
                lobby = Lobby()
        if lobby.number_of_rooms > 0:
            linear_lobbies.append(lobby)


    print(linear_lobbies)
        

        
        

                    


    






