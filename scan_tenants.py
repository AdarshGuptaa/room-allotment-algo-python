from collections import deque, defaultdict
import pandas as pd

def bfs_traverse_all_components(df):
    
    # Clean tenant_friends column
    df['tenant_friends'] = df['tenant_friends'].fillna('').apply(
        lambda x: [f.strip() for f in str(x).split(',') if f.strip()]
    )

    # Build undirected graph
    graph = defaultdict(list)
    for _, row in df.iterrows():
        tenant = row['tenant_id']
        friends = row['tenant_friends']

        if tenant not in graph:
            graph[tenant] = []

        for friend in friends:
            graph[tenant].append(friend)
            graph[friend].append(tenant)  # undirected

    # Traverse graph and collect components
    visited = set()
    components = []

    for tenant in graph:
        if tenant not in visited:
            queue = deque([tenant])
            visited.add(tenant)
            component = []

            while queue:
                current = queue.popleft()
                component.append(current)

                for neighbor in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            components.append(component)

    return components
