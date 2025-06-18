import numpy as np
import pandas as pd
import itertools
from layout_loader import find_all_lobbies
from scan_tenants import bfs_traverse_all_components

def export_tenant_assignments_to_excel(flat_tenant_list, output_file='room_assignments.xlsx'):
    data = [{
        "tenant_id": tenant.tenant_id,
        "room_type": tenant.room_type,
        "room_number": tenant.room_number if tenant.room_number else "UNASSIGNED"
    } for tenant in flat_tenant_list]

    df_result = pd.DataFrame(data)
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df_result.to_excel(writer, index=False, sheet_name='Room_Assignments')

    print("Exported room assignments to Excel.")

def main():
    df_building = pd.read_excel("building_test.xlsx", header=None)
    grid = df_building.replace({np.nan: None}).values.tolist()

    df_tenant = pd.read_excel('tenants_test.xlsx')
    bfs_tenants = bfs_traverse_all_components(df_tenant)
    flat_tenant_list = list(itertools.chain(*bfs_tenants))
    total_tenants = len(flat_tenant_list)


    lobbies = find_all_lobbies(grid)

    i = 0 
    for lobby in lobbies:
        room = lobby.room_header
        while room:
            if room.vacancy and room.vacant_beds > 0:
                # Try assigning eligible tenants until room is full
                for tenant in flat_tenant_list:
                    if tenant.room_number is None and tenant.room_type == room.num_beds:
                        tenant.room_number = room.room_name
                        room.vacant_beds -= 1
                        if room.vacant_beds == 0:
                            room.vacancy = False
                            break  # Room is full
            room = room.next

    unassigned = [t for t in flat_tenant_list if t.room_number is None]
    if unassigned:
        print(f"Not enough rooms. {len(unassigned)} tenants could not be assigned.")
    else:
        print("All tenants assigned successfully.")

    export_tenant_assignments_to_excel(flat_tenant_list)


if __name__ == "__main__":
    main()
