import numpy as np
import pandas as pd
from layout_loader import find_all_lobbies
from scan_tenants import bfs_traverse_all_components


def main():
    # Loading Building xlsx file
    df_building = pd.read_excel("building_test.xlsx", header=None)
    grid = df_building.replace({np.nan: None}).values.tolist()

    # print(f"Grid loaded: {len(grid)} rows × {len(grid[0]) if grid else 0} columns")

    # Loading Tenant xlsx file
    df_tenant = pd.read_excel('tenants_test.xlsx')

    # BFS-ed sequence of tenants as components
    bfs_tenants = bfs_traverse_all_components(df_tenant)

    # Finding all room lobbies connected to corridors
    lobbies = find_all_lobbies(grid)

    # Printing each lobby and its sequence of rooms
    # for lobby in lobbies:
    #     print(lobby)
    #     ptr = lobby.room_header
    #     while ptr:
    #         print(f"  -> Room {ptr.room_name} at ({ptr.row},{ptr.col}), Beds: {ptr.num_beds}, Vacant: {ptr.vacancy}")
    #         ptr = ptr.next



if __name__ == "__main__":
    main()
