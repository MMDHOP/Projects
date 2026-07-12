import heapq
import math
from collections import defaultdict


# فاز ۱: ساختار داده‌ی گراف + خواندن فایل ورودی


class Graph:
 # کلاس نمایش‌دهنده‌ی گراف جهت‌دار وزن‌دار شهر
 
    def __init__(self):
        # هر گره به لیستی از یال‌های خروجیش نگاشت می‌شه
        self.adj = defaultdict(list)
        # اسم قابل‌خواندن هر تقاطع (صرفا برای نمایش بهتر خروجی)
        self.node_names = {}
        # مجموعه‌ی همه‌ی گره‌هایی که تا الان دیده شده‌اند
        self.nodes = set()

    def add_node(self, node_id, name=None):
        # اضافه کردن یک تقاطع به گراف (اگر از قبل نبوده)
        self.nodes.add(node_id)
        if name:
            self.node_names[node_id] = name
        elif node_id not in self.node_names:
            self.node_names[node_id] = node_id

    def add_edge(self, u, v, distance, traffic, weather, delay=0.0):
    # افزودن یک یال و محاسبه‌ی هزینه‌ی آن

        self.add_node(u)
        self.add_node(v)
        cost = distance * traffic * weather + delay
        self.adj[u].append({
            "to": v,
            "distance": distance,
            "traffic": traffic,
            "weather": weather,
            "delay": delay,
            "cost": cost,
        })

    def all_edges(self):
    # برگرداندن تمام یال‌های گراف
    
        for u in self.adj:
            for edge in self.adj[u]:
                yield u, edge["to"], edge["cost"]

    def has_negative_edge(self):
    # بررسی می‌کنه که آیا حداقل یک یال با وزن منفی توی گراف هست یا نه
    
        return any(cost < 0 for _, _, cost in self.all_edges())

    def __repr__(self):
        e_count = sum(len(v) for v in self.adj.values())
        return f"<Graph: {len(self.nodes)} node, {e_count} edge>"


def read_graph_from_file(file_path):

    graph = Graph()

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() != ""]

    if not lines:
        raise ValueError("فایل ورودی خالی است یا پیدا نشد.")

    v_count, e_count = map(int, lines[0].split())
    idx = 1

    # --- خواندن مشخصات گره‌ها ---
    for _ in range(v_count):
        parts = lines[idx].split(maxsplit=1)
        node_id = parts[0]
        name = parts[1] if len(parts) > 1 else node_id
        graph.add_node(node_id, name)
        idx += 1

    # --- خواندن مشخصات یال‌ها ---
    for _ in range(e_count):
        parts = lines[idx].split()
        u, v = parts[0], parts[1]
        d, t, w, delay = map(float, parts[2:6])
        graph.add_edge(u, v, d, t, w, delay)
        idx += 1

    return graph



# فاز ۲: کوتاه‌ترین مسیر با الگوریتم دایکسترا (Dijkstra)


def dijkstra(graph, source):
 # محاسبه‌ی کوتاه‌ترین مسیر با الگوریتم دایکسترا
    dist = {node: math.inf for node in graph.nodes}
    parent = {node: None for node in graph.nodes}
    dist[source] = 0

    # هر عضو صف به شکل (هزینه‌ی فعلی, گره) است
    pq = [(0, source)]

    while pq:
        du, u = heapq.heappop(pq)

        # این یعنی یه نسخه‌ی قدیمی و منسوخ از u توی صفه؛ نادیده‌اش می‌گیریم
        if du != dist[u]:
            continue

        for edge in graph.adj[u]:
            v = edge["to"]
            new_dist = dist[u] + edge["cost"]

            if new_dist < dist[v]:
                dist[v] = new_dist
                parent[v] = u
                heapq.heappush(pq, (new_dist, v))

    return dist, parent


def reconstruct_path(parent, source, target):
# بازسازی مسیر از روی آرایه‌ی والد

    if target not in parent:
        return []

    path = []
    current = target
    while current is not None:
        path.append(current)
        if current == source:
            break
        current = parent[current]
    else:
        # حلقه بدون رسیدن به source تموم شده، یعنی مسیری وجود نداره
        return []

    path.reverse()

    if not path or path[0] != source:
        return []

    return path



# فاز ۳: وزن‌های منفی و تشخیص دور منفی با الگوریتم بلمن-فورد


class NegativeCycleError(Exception):
# خطای مربوط به وجود دور با وزن منفی
    pass


def bellman_ford(graph, source):
# محاسبه‌ی کوتاه‌ترین مسیر با الگوریتم بلمن-فورد

    dist = {node: math.inf for node in graph.nodes}
    parent = {node: None for node in graph.nodes}
    dist[source] = 0

    v_count = len(graph.nodes)
    edges = list(graph.all_edges())

    for _ in range(v_count - 1):
        updated = False
        for u, v, cost in edges:
            if dist[u] != math.inf and dist[v] > dist[u] + cost:
                dist[v] = dist[u] + cost
                parent[v] = u
                updated = True
        # اگه یه دور کامل هیچ چیزی به‌روزرسانی نشد، دیگه لازم نیست ادامه بدیم
        if not updated:
            break

    # مرحله‌ی آخر: بررسی وجود دور منفی
    for u, v, cost in edges:
        if dist[u] != math.inf and dist[v] > dist[u] + cost:
            raise NegativeCycleError(
                f"A negative-weight cycle was detected in the graph (edge {u} -> {v}). "
                "The shortest path is undefined."
            )

    return dist, parent


def shortest_path(graph, source, target=None):
# انتخاب خودکار الگوریتم مناسب برای کوتاه‌ترین مسیر

    if graph.has_negative_edge():
        dist, parent = bellman_ford(graph, source)
    else:
        dist, parent = dijkstra(graph, source)

    if target is None:
        return dist, parent

    cost_to_target = dist.get(target, math.inf)
    path = reconstruct_path(parent, source, target)
    return cost_to_target, path



# فاز ۴: مسیریابی بین چند مقصد (نسخه‌ی ساده‌شده‌ی TSP)
# با الگوریتم حریصانه‌ی نزدیک‌ترین همسایه


def nearest_neighbor_route(graph, start, destinations):
 # مسیریابی چندمقصدی با روش نزدیک‌ترین همسایه
 
    route = [start]
    full_paths = []
    current = start
    unvisited = set(destinations)
    total_cost = 0.0

    while unvisited:
        best_node = None
        best_cost = math.inf
        best_path = []

        # از بین مقصدهای باقی‌مونده، نزدیک‌ترین به current رو پیدا می‌کنیم
        for candidate in unvisited:
            cost, path = shortest_path(graph, current, candidate)
            if cost < best_cost:
                best_cost = cost
                best_node = candidate
                best_path = path

        if best_node is None or best_cost == math.inf:
            raise ValueError(
                f"No route exists from node '{current}' to any of the remaining destinations."
            )

        route.append(best_node)
        full_paths.append(best_path)
        total_cost += best_cost
        current = best_node
        unvisited.remove(best_node)

    # در پایان باید حتما به نقطه‌ی شروع برگردیم
    return_cost, return_path = shortest_path(graph, current, start)
    if return_cost == math.inf:
        raise ValueError(f"No route exists from node '{current}' back to '{start}'.")

    total_cost += return_cost
    full_paths.append(return_path)
    route.append(start)

    return route, total_cost, full_paths



# ابزار کمکی: ساخت یک فایل نقشه‌ی نمونه برای تست سریع


def create_sample_map_file(file_path="sample_map.txt", with_negative_weight=False):
 # ایجاد فایل نمونه برای تست برنامه
 
    lines = []
    nodes = ["A", "B", "C", "D", "E", "F"]

    # فرمت هر یال: u v distance traffic weather delay
    # خیابون‌های شهر رو دوطرفه در نظر می‌گیریم، پس برای هر خیابون دو یال
    # (رفت و برگشت) تعریف می‌کنیم تا امکان بازگشت به نقطه‌ی شروع هم وجود داشته باشه.
    base_edges = [
        ("A", "B", 4, 1.2, 1.0, 0),
        ("A", "C", 2, 1.0, 1.1, 0),
        ("B", "C", 1, 1.0, 1.0, 0),
        ("B", "D", 5, 1.3, 1.0, 1),
        ("C", "D", 8, 1.1, 1.2, 0),
        ("C", "E", 10, 1.0, 1.0, 0),
        ("D", "E", 2, 1.0, 1.0, 2),
        ("E", "F", 3, 1.0, 1.0, 0),
        ("F", "D", 6, 1.0, 1.0, 0),
    ]

    edges = []
    for u, v, d, t, w, delay in base_edges:
        edges.append((u, v, d, t, w, delay))
        edges.append((v, u, d, t, w, delay))

    if with_negative_weight:
        # یک میان‌بر با هزینه‌ی منفی (مثلا یک جایزه‌ی فرضی برای عبور از این مسیر)
        edges.append(("D", "F", -6, 1.0, 1.0, 0))

    lines.append(f"{len(nodes)} {len(edges)}")

    for n in nodes:
        lines.append(f"{n} Intersection_{n}")

    for u, v, d, t, w, delay in edges:
        lines.append(f"{u} {v} {d} {t} {w} {delay}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return file_path



# اجرای نمونه از تمام فازها


#  فاز ۱: ساخت/خواندن گراف 
print("=" * 60)
print("Phase 1: Read Map and Build Graph")
print("=" * 60)

map_path = create_sample_map_file("sample_map.txt", with_negative_weight=False)
city_graph = read_graph_from_file(map_path)
print(f"Graph created: {city_graph}")

#  فاز ۲: دایکسترا 
print("\n" + "=" * 60)
print("Phase 2: Shortest Path using Dijkstra")
print("=" * 60)

source, target = "A", "F"
cost, path = shortest_path(city_graph, source, target)
print(f"Shortest path cost from {source} to {target}: {cost}")
print(f"Path: {' -> '.join(path)}")


    #  فاز ۳: بلمن-فورد و تشخیص دور منفی 
print("\n" + "=" * 60)
print("Phase 3: Negative Weights and Bellman-Ford")
print("=" * 60)

neg_map_path = create_sample_map_file("sample_map_negative.txt", with_negative_weight=True)
negative_graph = read_graph_from_file(neg_map_path)

try:
    cost, path = shortest_path(negative_graph, "A", "F")
    print(f"(Negative weights) Shortest path cost from A to F: {cost}")
    print(f"Path: {' -> '.join(path)}")
except NegativeCycleError as e:
    print(f"Error: {e}")


# حالا یه گراف با دور منفی واقعی می‌سازیم تا تشخیص دور رو هم ببینیم
cyclic_graph = Graph()
for n in ["A", "B", "C"]:
    cyclic_graph.add_node(n)

cyclic_graph.add_edge("A", "B", 1, 1, 1, 0)
cyclic_graph.add_edge("B", "C", 1, 1, 1, 0)
cyclic_graph.add_edge("C", "A", -5, 1, 1, 0)  # این دور مجموعش منفی می‌شه

try:
    bellman_ford(cyclic_graph, "A")
except NegativeCycleError as e:
    print(f"Negative cycle detected successfully -> {e}")

    #  فاز ۴: مسیریابی چند مقصدی 
print("\n" + "=" * 60)
print("Phase 4: Multi-Destination Routing (Nearest Neighbor)")
print("=" * 60)

start_node = "A"
destinations = ["C", "E", "F"]
route, total_cost, full_paths = nearest_neighbor_route(city_graph, start_node, destinations)

print(f"Visit order: {' -> '.join(route)}")
print(f"Total route cost: {total_cost}")
print("Complete path for each segment:")

for i, p in enumerate(full_paths, start=1):
    print(f"  Segment {i}: {' -> '.join(p)}")