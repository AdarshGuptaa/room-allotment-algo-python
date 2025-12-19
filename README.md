# Automated Room Allotment System 🏠

A graph-based allocation engine designed to optimize student housing assignments. This system prioritizes **friendship preservation** and **group cohesion** over random allocation, using graph theory to map social networks to physical room clusters.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Data-Pandas%20%7C%20NumPy-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

## 📖 Overview

Manual room allocation for hostels or dormitories is often inefficient and fails to account for student preferences, leading to split friend groups and dissatisfaction.

This project automates the process by:
1.  **Modeling Social Graphs:** Treating students as nodes and friendships as edges to identify connected components (cliques).
2.  **Parsing Physical Layouts:** Converting 2D Excel floor plans into traversable Linked List structures.
3.  **Constraint Solving:** Mapping social groups to room clusters based on capacity and adjacency constraints.

## 🚀 Key Features

* **Friendship Preservation:** Uses **Breadth-First Search (BFS)** to traverse friendship graphs and ensure groups are allocated to the same or adjacent rooms.
* **Dynamic Layout Parsing:** Reads raw Excel grids (visual representations of floor plans) and converts them into structured data, allowing the system to adapt to any building layout without code changes.
* **Excel Integration:** Simple input/output via `.xlsx` files for easy adoption by non-technical administrators.
* **Conflict Resolution:** Automatically handles room capacity constraints and overflows.

## 🛠️ Technical Implementation

The system is built on three core modules:

### 1. Social Graph Analysis (`scan_tenants.py`)
* **Algorithm:** BFS for Connected Components.
* **Complexity:** $O(V + E)$ where $V$ is tenants and $E$ is friendship links.
* **Logic:** Scans the `tenants_test.xlsx` file, builds an adjacency list of friends, and groups them into "Families" that must be kept together.

### 2. Grid Layout Parsing (`layout_loader.py`)
* **Algorithm:** Grid Traversal & Linked List Construction.
* **Complexity:** $O(R \times C)$ where $R, C$ are grid dimensions.
* **Logic:** Iterates through a visual Excel grid (`building_test.xlsx`), identifying "Rooms", "Corridors", and "Halls". It links valid rooms into a linear data structure for easy allocation.

### 3. Allocation Engine (`main.py`)
* **Logic:** Matches the size of tenant groups (Families) to the capacity of available room clusters (Lobbies).
* **Optimization:** Uses hash-map bucketing to pre-sort tenants by room type preference, reducing allocation complexity from $O(M \times N)$ to $O(M + N)$.

## 💻 Installation & Usage

### Prerequisites
* Python 3.x
* Pandas, NumPy, OpenPyXL, XlsxWriter

```bash
pip install pandas numpy openpyxl xlsxwriter
