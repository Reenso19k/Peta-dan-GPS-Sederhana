import sys
import time

def tulisan_berjalan(teks, delay=0.1):
    for char in teks:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # pindah baris setelah selesai

tulisan_berjalan("UAS STRUKTUR DATA Graph Provinsi Bali Kelompok 2", 0.1)
print("Anggota Kelompok: Tesalonika Agri Uli Hutajulu (24091397), Sindy Febriana (24091397), Risqon Abdi Pratama (24091397)")
print("Dosen Pengampu: I Gde Agung Sri Sidhimantra, S.Kom., M.Kom.")
print("================================================================")

import networkx as nx
import matplotlib.pyplot as plt
import itertools

# 1. Membuat graph dengan 10 kota dan 30 edge (jalur)
cities = [
    "Jimbaran", "Uluwatu", "Semarapura", "Seminyak", "Canggu",
    "Tabanan", "Ubud", "Sanur", "Denpasar", "Kuta"
]

coordinates = {
    "Jimbaran": (-8.7932, 115.1655),
    "Uluwatu": (-8.8296, 115.0840),
    "Semarapura": (-8.5226, 115.4042),
    "Seminyak": (-8.6912, 115.1672),
    "Canggu": (-8.6478, 115.1385),
    "Tabanan": (-8.5409, 115.1253),
    "Ubud": (-8.5069, 115.2625),
    "Sanur": (-8.6930, 115.2521),
    "Denpasar": (-8.6705, 115.2126),
    "Kuta": (-8.7178, 115.1687)
}

edges = [
    ("Jimbaran", "Uluwatu", 13.9),
    ("Jimbaran", "Semarapura", 45),
    ("Jimbaran", "Seminyak", 11.8),
    ("Jimbaran", "Canggu", 12.7),
    ("Jimbaran", "Tabanan", 35),
    ("Jimbaran", "Ubud", 39.1),
    ("Jimbaran", "Sanur", 18.9),
    ("Jimbaran", "Denpasar", 13.8),
    ("Jimbaran", "Kuta", 10.1),

    ("Uluwatu", "Semarapura", 55),
    ("Uluwatu", "Seminyak", 26.7),
    ("Uluwatu", "Canggu", 34),
    ("Uluwatu", "Tabanan", 49.8),
    ("Uluwatu", "Ubud", 53),
    ("Uluwatu", "Sanur", 30),
    ("Uluwatu", "Denpasar", 26.7),
    ("Uluwatu", "Kuta", 22.5),

    ("Semarapura", "Seminyak", 43),
    ("Semarapura", "Canggu", 46),
    ("Semarapura", "Tabanan", 50),
    ("Semarapura", "Ubud", 38),
    ("Semarapura", "Sanur", 29),
    ("Semarapura", "Denpasar", 33),
    ("Semarapura", "Kuta", 47),

    ("Seminyak", "Canggu", 10),
    ("Seminyak", "Tabanan", 20),
    ("Seminyak", "Ubud", 30),
    ("Seminyak", "Sanur", 15),
    ("Seminyak", "Denpasar", 10),
    ("Seminyak", "Kuta", 5),

    ("Canggu", "Tabanan", 15),
    ("Canggu", "Ubud", 25),
    ("Canggu", "Sanur", 20),
    ("Canggu", "Denpasar", 15),
    ("Canggu", "Kuta", 10),

    ("Tabanan", "Ubud", 30),
    ("Tabanan", "Sanur", 35),
    ("Tabanan", "Denpasar", 30),
    ("Tabanan", "Kuta", 25),

    ("Ubud", "Sanur", 24),
    ("Ubud", "Denpasar", 23),
    ("Ubud", "Kuta", 36),

    ("Sanur", "Denpasar", 6),
    ("Sanur", "Kuta", 12),

    ("Denpasar", "Kuta", 10)
]

# 2. mode transportasi, bobot diubah (waktu tempuh dalam jam)
def make_graph(edges, speed_factor):
    G = nx.Graph()
    for u, v, km in edges:
        # waktu tempuh = jarak / kecepatan (jam)
        waktu = round((km / speed_factor), 2)  # dua desimal, satuan jam
        G.add_edge(u, v, weight=waktu)
    return G

# Kecepatan rata-rata (km/jam) untuk tiap moda
speed_motor = 40    # motor
G = make_graph(edges, speed_motor)
moda = "Sepeda Motor"

# 3. Dijkstra: Fungsi mencari rute tercepat
def dijkstra_path(G, asal, tujuan):
    path = nx.dijkstra_path(G, asal, tujuan, weight='weight')
    total = nx.dijkstra_path_length(G, asal, tujuan, weight='weight')
    return path, total

# 4. Input pengguna
print("Daftar Kota Provinsi Bali:", ', '.join(cities))
asal = input("Masukkan kota asal: ").title()
tujuan = input("Masukkan kota tujuan: ").title()

# 5. Output rute tercepat
try:
    path, total = dijkstra_path(G, asal, tujuan)
    print(f"\nModa: {moda}")
    print("Jalur tercepat(Djisktra):", " -> ".join(path))
    print(f"Total waktu tempuh: {total} jam")
    print("\nRincian waktu tempuh tiap rute:")
    for i in range(len(path)-1):
        kota_awal = path[i]
        kota_tujuan = path[i+1]
        # Cari jarak asli dari edges
        jarak = next(km for u, v, km in edges if (u == kota_awal and v == kota_tujuan) or (u == kota_tujuan and v == kota_awal))
        waktu = G[kota_awal][kota_tujuan]['weight']
        print(f"{kota_awal} -> {kota_tujuan}: {jarak} km / {speed_motor} km/jam = {waktu} jam")
except nx.NetworkXNoPath:
    print("Tidak ada jalur yang menghubungkan kota asal dan tujuan.")

# --- TSP dapat ditambahkan di bawah ini sesuai instruksi tugas ---

def tsp_brute_force(G, start):
    nodes = list(G.nodes)
    nodes.remove(start)
    min_path = None
    min_cost = float('inf')
    for perm in itertools.permutations(nodes):
        path = [start] + list(perm) + [start]
        try:
            cost = sum(
                G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)
            )
            if cost < min_cost:
                min_cost = cost
                min_path = path
        except KeyError:
            continue  # skip if path is not possible
    return min_path, min_cost

# Menu TSP
# Menu TSP
print("\n=== TSP (Traveling Salesman Problem) ===")
tsp_start = input("Masukkan kota awal untuk TSP: ").title()
if tsp_start not in G.nodes:
    print("Kota tidak ditemukan di graf.")
else:
    tsp_path, tsp_cost = tsp_brute_force(G, tsp_start)
    if tsp_path:
        print("Rute TSP tercepat:", " -> ".join(tsp_path))
        print(f"Total waktu tempuh TSP: {tsp_cost} jam")
        print("\nRincian waktu tempuh tiap rute TSP:")
        for i in range(len(tsp_path)-1):
            kota_awal = tsp_path[i]
            kota_tujuan = tsp_path[i+1]
            # Cari jarak asli dari edges
            jarak = next(km for u, v, km in edges if (u == kota_awal and v == kota_tujuan) or (u == kota_tujuan and v == kota_awal))
            waktu = G[kota_awal][kota_tujuan]['weight']
            print(f"{kota_awal} -> {kota_tujuan}: {jarak} km / {speed_motor} km/jam = {waktu} jam")
    else:
        print("Tidak ada rute TSP yang mengunjungi semua kota dan kembali ke asal.")

# Visualisasi connected graf (sepeda motor)
plt.figure(figsize=(10,7))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=12)
edge_labels = nx.get_edge_attributes(G, 'weight')
edge_labels_jam = {k: f"{v} jam" for k, v in edge_labels.items()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_jam, font_color='red')
plt.title("Peta Kota & Waktu Tempuh (Sepeda Motor, jam)")
plt.show()


#Visualisasi dijkstra dengan upload ke mymaps
import csv
def simpan_ke_csv(rute, nama_file):
    with open(nama_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Latitude', 'Longitude'])
        for kota in rute:
            if kota in coordinates:
                lat, lon = coordinates[kota]
                writer.writerow([kota, lat, lon])
            else:
                print(f"Koordinat untuk {kota} tidak ditemukan.")
simpan_ke_csv(path, "rute_dijkstra.csv")
print("\n>> File 'rute_dijkstra.csv' berhasil dibuat. Upload ke Google MyMaps untuk visualisasi.")


def save_urutan_tsp(rute, nama_file):
    with open(nama_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name'])
        for kota in rute:
            writer.writerow([kota])

tsp_path_mymaps = tsp_path[:10]
filename = f"tsp_{tsp_start.lower()}.csv"
simpan_ke_csv(tsp_path_mymaps, filename)
print(f"File '{filename}' telah dibuat. Upload ke Google MyMaps untuk visualisasi rute TSP")


