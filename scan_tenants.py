from collections import deque, defaultdict
import pandas as pd

# Define Tenant class
class Tenant:
    def __init__(self, tenant_id, room_number, room_type):
        self.tenant_id = tenant_id
        self.room_number = room_number
        self.room_type = room_type

    def __repr__(self):
        return f"Tenant(id={self.tenant_id}, room={self.room_number}, type={self.room_type})"

def bfs_traverse_all_components(df):
    # Clean tenant_friends column
    df['tenant_friends'] = df['tenant_friends'].fillna('').apply(
        lambda x: [f.strip() for f in str(x).split(',') if f.strip()]
    )

    # Build tenant lookup
    tenant_lookup = {
        row['tenant_id']: Tenant(row['tenant_id'], row.get('room_number', None), row['tenant_room_type'])
        for _, row in df.iterrows()
    }

    # Build undirected graph (using tenant_id as nodes)
    graph = defaultdict(list)
    for _, row in df.iterrows():
        tenant = row['tenant_id']
        friends = row['tenant_friends']

        if tenant not in graph:
            graph[tenant] = []

        for friend in friends:
            graph[tenant].append(friend)
            graph[friend].append(tenant)  # undirected

    # Traverse graph and collect components (Tenant objects)
    visited = set()
    components = []

    for tenant_id in graph:
        if tenant_id not in visited:
            queue = deque([tenant_id])
            visited.add(tenant_id)
            component = []

            while queue:
                current_id = queue.popleft()
                component.append(tenant_lookup[current_id])  # Store Tenant object

                for neighbor_id in graph[current_id]:
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        queue.append(neighbor_id)

            components.append(component)

    return components
