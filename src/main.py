# src/main.py

from datetime import time
import json
import os
from typing import List, Dict, Tuple
import time as timer # `time` modülü ile karışmaması için `timer` olarak adlandırıldı
import webbrowser
import sys
from pathlib import Path
import logging

# Proje kök dizinini Python path'ine ekle
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Gerekli Kütüphaneler
try:
    import folium
    from folium import plugins
    import matplotlib # models.py için gerekli olabilir
except ImportError:
    print("Lütfen gerekli kütüphaneleri kurun: pip install folium numpy matplotlib")
    sys.exit(1)

# Proje Modülleri
from src.models import Drone, DeliveryPoint, NoFlyZone
from src.algorithms.genetic_algorithm import GeneticAlgorithm
from src.algorithms.path_planning import PathPlanner # PathPlanner'ı import et
from src.data_generator import DataGenerator
from src.visualization import RouteVisualizer

def run_scenario(scenario_num: int,
                 drones: List[Drone],
                 deliveries: List[DeliveryPoint],
                 no_fly_zones: List[NoFlyZone],
                 output_file: str) -> Tuple[dict, float]:
    """Test senaryosunu çalıştırır ve sonuçları döndürür"""
    logging.info(f"Senaryo {scenario_num} başlatılıyor...")
    start_time_exec = timer.time() # `timer` modülünü kullan
    
    optimizer = GeneticAlgorithm(
        population_size=100,  
        generations=50, # PDF'e göre ayarlanabilir
        mutation_rate=0.25,   
        elitism_count=5,
        charging_time_per_mah=0.001 # PDF'te belirtilen şarj süresi faktörü
    )
    
    result = optimizer.optimize(
        drones=drones,
        deliveries=deliveries,
        no_fly_zones=no_fly_zones,
        current_time=time(9, 0) # Başlangıç zamanı
    )
    
    end_time_exec = timer.time() # `timer` modülünü kullan
    execution_time = end_time_exec - start_time_exec
    
    total_deliveries = len(deliveries)
    completed_deliveries = len(result.assignments)
    completion_rate = (completed_deliveries / total_deliveries) * 100 if total_deliveries > 0 else 0.0
    
    total_energy = sum(a.energy_consumption for a in result.assignments)
    
    # Toplam mesafe hesaplaması (PathPlanner.calculate_distance kullanarak)
    total_distance = 0.0
    for assignment in result.assignments:
        if assignment.route and len(assignment.route) > 1:
            for i in range(len(assignment.route) - 1):
                point1 = assignment.route[i]
                point2 = assignment.route[i+1]
                total_distance += PathPlanner.calculate_distance(point1, point2)
                
    rule_violations = sum(a.rule_violations for a in result.assignments)
    
    avg_energy = total_energy / completed_deliveries if completed_deliveries > 0 else 0.0
    
    metrics = {
        "scenario": scenario_num,
        "total_deliveries": total_deliveries,
        "completed_deliveries": completed_deliveries,
        "completion_rate": completion_rate, #
        "total_distance_meters": total_distance, #
        "total_energy_mah": total_energy, #
        "avg_energy_per_delivery_mah": avg_energy, #
        "rule_violations": rule_violations, #
        "execution_time_seconds": execution_time, #
        "fitness_score": result.fitness #
    }
    
    logging.info(f"Senaryo {scenario_num} tamamlandı. Süre: {execution_time:.2f} saniye.")
    
    # Görselleştirme
    logging.info(f"{output_file} için harita oluşturuluyor...")
    center_lat, center_lon = 41.015137, 28.979530 # İstanbul merkezi
    visualizer = RouteVisualizer(center=(center_lat, center_lon), zoom=11)
    
    # NoFlyZone ekleme:
    # Eğer NoFlyZone nesnelerinizde 'id' attribute'u varsa add_no_fly_zones kullanın.
    # Eğer yoksa veya DataGenerator ID atamıyorsa, add_no_fly_zones_without_id kullanın.
    # Bir önceki yanıtta add_no_fly_zones_without_id önerilmişti.
    if hasattr(no_fly_zones[0] if no_fly_zones else None, 'id'):
         visualizer.add_no_fly_zones(no_fly_zones)
    else:
         visualizer.add_no_fly_zones_without_id(no_fly_zones)
         
    visualizer.add_delivery_points(deliveries)
    # add_routes metoduna 'drones' listesini (drones_info olarak) gönder
    visualizer.add_routes(result.assignments, drones) 
    visualizer.add_heatmap(deliveries)
    visualizer.save(output_file)
    
    return metrics, execution_time

def main():
    """Ana program"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    
    generator = DataGenerator() 
    
    # Senaryo 1
    logging.info("Senaryo 1 verileri üretiliyor...")
    drones1, deliveries1, zones1 = generator.generate_scenario_1()
    metrics1, time1 = run_scenario(1, drones1, deliveries1, zones1, "scenario_1_results.html")
    logging.info(f"Senaryo 1 Sonuçları: Tamamlanan Teslimat: {metrics1['completed_deliveries']}/{metrics1['total_deliveries']} ({metrics1['completion_rate']:.1f}%)")
    logging.info(f"Toplam Mesafe: {metrics1['total_distance_meters']/1000:.1f} km, Ortalama Enerji: {metrics1['avg_energy_per_delivery_mah']:.0f} mAh, Çalışma Süresi: {time1:.2f} sn")
    
    # Senaryo 2
    logging.info("Senaryo 2 verileri üretiliyor...")
    drones2, deliveries2, zones2 = generator.generate_scenario_2()
    metrics2, time2 = run_scenario(2, drones2, deliveries2, zones2, "scenario_2_results.html")
    logging.info(f"Senaryo 2 Sonuçları: Tamamlanan Teslimat: {metrics2['completed_deliveries']}/{metrics2['total_deliveries']} ({metrics2['completion_rate']:.1f}%)")
    logging.info(f"Toplam Mesafe: {metrics2['total_distance_meters']/1000:.1f} km, Ortalama Enerji: {metrics2['avg_energy_per_delivery_mah']:.0f} mAh, Çalışma Süresi: {time2:.2f} sn")
    
    results = {"scenario_1": metrics1, "scenario_2": metrics2}
    with open("results.json", "w", encoding='utf-8') as f: # encoding eklendi
        json.dump(results, f, indent=2, ensure_ascii=False) # ensure_ascii eklendi
    
    logging.info("Sonuçlar kaydedildi ve haritalar oluşturuldu.")
    
    try:
        # Mutlak yolları kullanarak tarayıcıda açmayı dene
        report1_path = os.path.abspath("scenario_1_results.html")
        report2_path = os.path.abspath("scenario_2_results.html")
        webbrowser.open(f"file://{report1_path}")
        webbrowser.open(f"file://{report2_path}")
    except Exception as e:
        logging.warning(f"Haritalar tarayıcıda otomatik açılamadı: {e}. Lütfen manuel olarak açın.")

if __name__ == "__main__":
    main()