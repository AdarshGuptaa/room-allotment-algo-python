import numpy as np
import pandas as pd
from layout_loader import find_all_lobbies


def main():
    # Loading from Building xlsx file
    df = pd.read_excel("building_test.xlsx", header=None)
    grid = df.replace({np.nan: None}).values.tolist()

    print(f"Grid loaded: {len(grid)} rows × {len(grid[0]) if grid else 0} columns")

    # Finding all room lobbies connected to corridors
    lobbies = find_all_lobbies(grid)

    # Printing each lobby and its sequence of rooms
    for lobby in lobbies:
        print(lobby)
        ptr = lobby.room_header
        while ptr:
            print(f"  -> Room {ptr.room_name} at ({ptr.row},{ptr.col}), Beds: {ptr.num_beds}, Vacant: {ptr.vacancy}")
            ptr = ptr.next

if __name__ == "__main__":
    main()
