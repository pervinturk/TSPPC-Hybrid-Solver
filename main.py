import numpy as np
import random
import time

class Location:
    def __init__(self, id_val, x, y, prec):
        self.id, self.x, self.y, self.prec = id_val, x, y, prec

def read_data(file_name):
    locs = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            next(f)
            for line in f:
                d = line.strip().split('\t')
                if len(d) < 4: d = line.strip().split()
                if len(d) < 4: continue
                locs.append(Location(int(d[0]), float(d[1]), float(d[2]), 
                                     int(d[3]) if d[3] not in ['-', '0'] else 0))
    except: return []
    return locs

def get_dist_matrix(locs):
    n = len(locs)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = int(np.ceil(np.sqrt((locs[i].x - locs[j].x)**2 + (locs[i].y - locs[j].y)**2)))
            matrix[i][j] = matrix[j][i] = d
    return matrix

def is_feasible(route, locs):
    # TSPPC öncelik kısıtlarını doğrular
    curr_max = 0
    for idx in route:
        p = locs[idx].prec
        if p > 0:
            if p < curr_max: return False
            curr_max = max(curr_max, p)
    return True

def build_smart_feasible_route(locs, depot_idx):
    # 0'ları rotaya rastgele dağıtan akıllı üretici
    others = [i for i in range(len(locs)) if i != depot_idx]
    p_groups = {p: [i for i in others if locs[i].prec == p] for p in range(1, 6)}
    zeros = [i for i in others if locs[i].prec == 0]
    
    skeleton = []
    for p in range(1, 6):
        group = p_groups[p]
        random.shuffle(group)
        skeleton.extend(group)
    
    for z_node in zeros:
        skeleton.insert(random.randint(0, len(skeleton)), z_node)
    return [depot_idx] + skeleton

def calculate_dist(r, m):
    return m[r[:-1], r[1:]].sum() + m[r[-1], r[0]]

def two_opt_lamarckian(route, dist_matrix, locs, max_attempts=100):
    """Lamarckian yerel arama: Rotadaki yolları milimetrik iyileştirir."""
    best_route = route[:]
    best_dist = calculate_dist(np.array(best_route), dist_matrix)
    
    for _ in range(max_attempts):
        i, j = sorted(random.sample(range(1, len(route)), 2))
        if j - i < 2: continue
        
        # Kesit ters çevirme (2-opt hamlesi)
        new_route = best_route[:i] + best_route[i:j][::-1] + best_route[j:]
        if is_feasible(new_route, locs):
            new_dist = calculate_dist(np.array(new_route), dist_matrix)
            if new_dist < best_dist:
                best_route, best_dist = new_route, new_dist
                
    return best_route, best_dist

def hybrid_final_master(locs, pop_size=100, generations=300):
    n = len(locs)
    dist_matrix = get_dist_matrix(locs)
    depot_idx = next(i for i, l in enumerate(locs) if l.id == 1)
    start_time = time.time()
    
    best_overall_dist = float('inf')
    best_overall_route = None
    all_runs_dist = []

    for run in range(10): # 10 Bağımsız çalıştırma
        population = []
        for _ in range(pop_size):
            r = build_smart_feasible_route(locs, depot_idx)
            population.append([r, calculate_dist(np.array(r), dist_matrix)])

        for gen in range(generations):
            population.sort(key=lambda x: x[1])
            new_pop = population[:10] # Elitizm
            
            # Lamarckian İyileştirme: Her nesilde en iyi 5 bireye yoğun SA/2-Opt
            for i in range(5):
                r_refined, d_refined = two_opt_lamarckian(new_pop[i][0], dist_matrix, locs)
                new_pop[i] = [r_refined, d_refined]

            while len(new_pop) < pop_size:
                # Dinamik Operatör Seçimi
                if random.random() < 0.6: # Akıllı Crossover
                    p1, p2 = random.sample(population[:30], 2)
                    cut = random.randint(1, n-2)
                    child = p1[0][:cut] + [x for x in p2[0] if x not in p1[0][:cut]]
                else: # Akıllı Mutasyon
                    child = random.choice(population[:20])[0][:]
                    # Blok taşıma mutasyonu
                    idx = random.randint(1, n-2)
                    node = child.pop(idx)
                    child.insert(random.randint(1, n-1), node)
                
                if is_feasible(child, locs):
                    new_pop.append([child, calculate_dist(np.array(child), dist_matrix)])
            
            population = new_pop

        best_run_r, best_run_d = population[0]
        all_runs_dist.append(best_run_d)
        if best_run_d < best_overall_dist:
            best_overall_dist = best_run_d
            best_overall_route = best_run_r

    t_avg = (time.time() - start_time) / 10
    avg_d = sum(all_runs_dist) / 10
    return [locs[i] for i in best_overall_route], best_overall_dist, avg_d, t_avg

# ÇALIŞTIRMA
locs = read_data("Sample Problem.txt")
if locs:
    best_route, best_d, avg_d, t_avg = hybrid_final_master(locs)
    with open("sonuc.txt", "w", encoding="utf-8") as f:
        f.write(f"Average computational time of 10 run: {t_avg:.4f} s\n")
        f.write(f"Average solution of 10 run: {avg_d:.2f}\n")
        f.write(f"The best solution obtained in 10 run: {best_d:.2f}\n")
        f.write(f"The route information of the best solution: ({'/'.join(str(l.id) for l in best_route)}/1)")
    print(f"Bitti! En iyi mesafe: {best_d} | Ortalama Süre: {t_avg:.2f}s")