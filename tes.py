import time
import memory_profiler
import requests
import random
from functools import partial
import matplotlib.pyplot as plt

# Simulasi fungsi-fungsi utama dari kode JavaScript
class RouteOptimizer:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.map_bounds = {
            'min_lat': -2.35,
            'max_lat': -2.05,
            'min_lon': 113.8,
            'max_lon': 114.05
        }
    
    def get_coordinates(self, address):
        """Simulasi pencarian koordinat"""
        params = {
            'q': f"{address}, Palangka Raya",
            'format': 'json',
            'addressdetails': 1
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        if not data:
            raise ValueError(f"Lokasi {address} tidak ditemukan.")
        
        location = data[0]
        return {
            'lat': float(location['lat']),
            'lon': float(location['lon']),
            'address': location.get('address', {})
        }
    
    def is_in_palangka_raya(self, location):
        """Memeriksa apakah lokasi berada dalam Palangka Raya"""
        city = location['address'].get('city', '') or \
               location['address'].get('town', '') or \
               location['address'].get('village', '')
        return 'palangka raya' in city.lower()
    
    def calculate_route(self, origin, destination, priority='medium'):
        """Simulasi perhitungan rute dengan berbagai metrik"""
        # Simulasi beberapa alternatif rute
        num_routes = 3
        routes = []
        
        for i in range(num_routes):
            # Simulasi data rute dengan variasi acak
            distance = self.calculate_distance(origin, destination) * (0.9 + random.random() * 0.2)
            time = distance * (1.5 + random.random())  # waktu berdasarkan jarak dengan variasi
            
            routes.append({
                'summary': {
                    'totalDistance': distance * 1000,  # dalam meter
                    'totalTime': time * 60  # dalam detik
                },
                'coordinates': self.generate_route_coordinates(origin, destination, 10)
            })
        
        # Pilih rute berdasarkan prioritas
        if priority == 'high':
            chosen_route = min(routes, key=lambda x: x['summary']['totalTime'])
        elif priority == 'low':
            chosen_route = min(routes, key=lambda x: x['summary']['totalDistance'])
        else:
            chosen_route = routes[0]
        
        return {
            'routes': routes,
            'chosen_route': chosen_route
        }
    
    def calculate_distance(self, point1, point2):
        """Menghitung jarak Haversine antara dua titik"""
        from math import radians, sin, cos, sqrt, atan2
        
        lat1, lon1 = radians(point1['lat']), radians(point1['lon'])
        lat2, lon2 = radians(point2['lat']), radians(point2['lon'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        radius = 6371  # Radius bumi dalam km
        return radius * c
    
    def generate_route_coordinates(self, origin, destination, num_points):
        """Generate koordinat rute acak antara dua titik"""
        coordinates = []
        for i in range(num_points):
            frac = i / (num_points - 1)
            lat = origin['lat'] + (destination['lat'] - origin['lat']) * frac
            lon = origin['lon'] + (destination['lon'] - origin['lon']) * frac
            
            # Tambahkan sedikit variasi acak
            lat += (random.random() - 0.5) * 0.01
            lon += (random.random() - 0.5) * 0.01
            
            coordinates.append({'lat': lat, 'lon': lon})
        
        return coordinates

# Fungsi untuk pengujian performa
def test_performance(optimizer, num_tests=5):
    """Menguji performa dengan berbagai metrik"""
    results = []
    
    for i in range(1, num_tests + 1):
        # Buat alamat acak untuk pengujian
        origin = f"Lokasi {i} Origin"
        destination = f"Lokasi {i} Destination"
        priority = random.choice(['high', 'medium', 'low'])
        
        # Ukur waktu eksekusi
        start_time = time.time()
        
        # Ukur penggunaan memori
        mem_usage = memory_profiler.memory_usage(
            partial(optimizer.calculate_route, 
                   origin={'lat': -2.2 + random.random()*0.1, 'lon': 113.9 + random.random()*0.1},
                   destination={'lat': -2.2 + random.random()*0.1, 'lon': 113.9 + random.random()*0.1},
                   priority=priority)
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        max_memory = max(mem_usage) - min(mem_usage)
        
        # Hitung kualitas solusi
        result = optimizer.calculate_route(
            origin={'lat': -2.2 + random.random()*0.1, 'lon': 113.9 + random.random()*0.1},
            destination={'lat': -2.2 + random.random()*0.1, 'lon': 113.9 + random.random()*0.1},
            priority=priority
        )
        
        quality_score = calculate_quality_score(result['chosen_route'], priority)
        
        results.append({
            'test_num': i,
            'execution_time': execution_time,
            'memory_usage': max_memory,
            'quality_score': quality_score,
            'priority': priority
        })
    
    return results

def calculate_quality_score(route, priority):
    """Menghitung skor kualitas solusi"""
    distance = route['summary']['totalDistance'] / 1000  # dalam km
    time = route['summary']['totalTime'] / 60  # dalam menit
    
    # Normalisasi (asumsi maksimum)
    distance_score = 1 - min(distance / 50, 1)  # asumsi maks 50 km
    time_score = 1 - min(time / 120, 1)  # asumsi maks 120 menit
    
    # Berikan bobot berdasarkan prioritas
    if priority == 'high':
        return 0.7 * time_score + 0.3 * distance_score
    elif priority == 'low':
        return 0.3 * time_score + 0.7 * distance_score
    return 0.5 * time_score + 0.5 * distance_score

def test_scalability(optimizer, max_nodes=10):
    """Menguji skalabilitas dengan peningkatan jumlah node"""
    scalability_results = []
    
    for num_nodes in range(1, max_nodes + 1):
        # Buat daftar lokasi acak
        locations = [
            {'lat': -2.2 + random.random()*0.1, 'lon': 113.9 + random.random()*0.1}
            for _ in range(num_nodes)
        ]
        
        # Ukur waktu untuk menghitung rute antara semua pasangan node
        start_time = time.time()
        for i in range(num_nodes - 1):
            optimizer.calculate_route(locations[i], locations[i+1])
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Ukur penggunaan memori
        mem_usage = memory_profiler.memory_usage(
            partial(optimizer.calculate_route, locations[0], locations[-1])
        )
        max_memory = max(mem_usage) - min(mem_usage)
        
        scalability_results.append({
            'num_nodes': num_nodes,
            'execution_time': execution_time,
            'memory_usage': max_memory
        })
    
    return scalability_results

def visualize_results(performance_results, scalability_results):
    """Visualisasi hasil pengujian"""
    # Visualisasi performa
    plt.figure(figsize=(15, 5))
    
    # Waktu eksekusi
    plt.subplot(1, 3, 1)
    plt.plot([r['test_num'] for r in performance_results], 
             [r['execution_time'] for r in performance_results], 'bo-')
    plt.title('Waktu Eksekusi per Tes')
    plt.xlabel('Nomor Tes')
    plt.ylabel('Waktu (detik)')
    
    # Penggunaan memori
    plt.subplot(1, 3, 2)
    plt.plot([r['test_num'] for r in performance_results], 
             [r['memory_usage'] for r in performance_results], 'ro-')
    plt.title('Penggunaan Memori per Tes')
    plt.xlabel('Nomor Tes')
    plt.ylabel('Memori (MB)')
    
    # Kualitas solusi
    plt.subplot(1, 3, 3)
    priorities = {'high': 'r', 'medium': 'g', 'low': 'b'}
    for r in performance_results:
        plt.scatter(r['test_num'], r['quality_score'], 
                    color=priorities[r['priority']], label=r['priority'])
    plt.title('Kualitas Solusi per Tes')
    plt.xlabel('Nomor Tes')
    plt.ylabel('Skor Kualitas')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Visualisasi skalabilitas
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot([r['num_nodes'] for r in scalability_results], 
             [r['execution_time'] for r in scalability_results], 'go-')
    plt.title('Skalabilitas Waktu Eksekusi')
    plt.xlabel('Jumlah Node')
    plt.ylabel('Waktu (detik)')
    
    plt.subplot(1, 2, 2)
    plt.plot([r['num_nodes'] for r in scalability_results], 
             [r['memory_usage'] for r in scalability_results], 'mo-')
    plt.title('Skalabilitas Penggunaan Memori')
    plt.xlabel('Jumlah Node')
    plt.ylabel('Memori (MB)')
    
    plt.tight_layout()
    plt.show()

# Jalankan pengujian
if __name__ == "__main__":
    optimizer = RouteOptimizer()
    
    print("Menguji performa sistem...")
    performance_results = test_performance(optimizer, num_tests=10)
    
    print("\nMenguji skalabilitas dengan peningkatan node...")
    scalability_results = test_scalability(optimizer, max_nodes=15)
    
    print("\nVisualisasi hasil...")
    visualize_results(performance_results, scalability_results)
    
    # Tampilkan hasil dalam tabel
    print("\nHasil Pengujian Performa:")
    print("Test | Waktu (s) | Memori (MB) | Skor Kualitas | Prioritas")
    print("-" * 60)
    for res in performance_results:
        print(f"{res['test_num']:4} | {res['execution_time']:.4f} | {res['memory_usage']:.2f} | {res['quality_score']:.2f} | {res['priority']}")
    
    print("\nHasil Pengujian Skalabilitas:")
    print("Node | Waktu (s) | Memori (MB)")
    print("-" * 40)
    for res in scalability_results:
        print(f"{res['num_nodes']:4} | {res['execution_time']:.4f} | {res['memory_usage']:.2f}")


