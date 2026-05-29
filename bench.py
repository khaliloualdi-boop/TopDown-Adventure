import timeit
import cProfile
import arcade
from navmesh import create_graph
from gameview import GameView
import matplotlib.pyplot as plt

WINDOW = arcade.open_window(64, 64, "bench")

DELTA_TIME_S = 1/60
DELTA_TIME_MS = 1000/60

def make_map_doc(W: int, H: int, n_blobs: int = 0) -> str:
    ''' crée une Map valide sous forme de str respectant la longuer, la largeur et le nombre de blobs indiquée par les paramètres.'''

    grid = [[' '] * W for i in range(H)]

    for x in range(W):
        grid[0][x] = 'X'
        grid[H - 1][x] = 'X'
    for y in range(H):
        grid[y][0] = 'X'
        grid[y][W - 1] = 'X'

    px, py = W // 2, H // 2
    grid[py][px] = 'P'

    placed = 0
    for gy in range(2, H - 2):
        for gx in range(2, W - 2):
            if placed >= n_blobs:
                break
            if not (gx == px and gy == py):
                grid[gy][gx] = 'B'
                placed += 1
        if placed >= n_blobs:
            break

    file_rows = [''.join(grid[gy]) for gy in range(H - 1, -1, -1)]
    header = f"width: {W}\nheight: {H}\ntheme: overworld\nswitches: []\ngates: []\n"
    return header + "---\n" + "\n".join(file_rows)

def bench_load_map_and_navmesh_creation() -> tuple[list[int], list[float]]:
    from parsing import parse_map_doc
    sizes = [3, 5, 10, 20, 30, 50, 70, 100]
    results_c: list[int] = []
    results_t: list[float] = []

    print("Benchmark load_map + create_graph en fonction des dimensions de la carte")
    for W in sizes:
        doc = make_map_doc(W, W)
        t = timeit.timeit(lambda: create_graph(parse_map_doc(doc)), number=5) / 5 * 1000
        results_c.append(W * W)
        results_t.append(t)
        print(f"  W={W:4d}  C={W*W:6d}  t={t:.4f} ms")

    return results_c, results_t

def bench_on_update() -> tuple[list[int], list[float]]:
    from parsing import parse_map_doc
    MAP_W, MAP_H = 40, 40
    blob_counts = [0, 1, 3, 5, 10, 20, 30, 50]
    results_b: list[int] = []
    results_t: list[float] = []

    print("\nBenchmark on_update() en fonction du nombre de blobs :")
    for B in blob_counts:
        doc = make_map_doc(MAP_W, MAP_H, n_blobs=B)
        m = parse_map_doc(doc)
        view = GameView(m)
        WINDOW.show_view(view)

        for i in range(5):
            view.on_update(DELTA_TIME_S)

        t = timeit.timeit(lambda: view.on_update(DELTA_TIME_S), number=30) / 30 * 1000
        results_b.append(B)
        results_t.append(t)

        flag = " ← DÉPASSE BUDGET" if t > DELTA_TIME_MS else ""
        print(f"  B={B:4d} blobs  t={t:.4f} ms/frame{flag}")

    return results_b, results_t

def profile_loading(W: int = 70) -> None:
    from parsing import parse_map_doc
    doc = make_map_doc(W, W)
    profile = cProfile.Profile()
    profile.enable()
    create_graph(parse_map_doc(doc))
    profile.disable()
    profile.dump_stats("bench_load.prof")

def profile_update(B: int = 30) -> None:
    from parsing import parse_map_doc
    doc = make_map_doc(40, 40, n_blobs=B)
    view = GameView(parse_map_doc(doc))
    WINDOW.show_view(view)
    for _ in range(5):
        view.on_update(DELTA_TIME_MS)
    profile = cProfile.Profile()
    profile.enable()
    for _ in range(30):
        view.on_update(DELTA_TIME_S)
    profile.disable()
    profile.dump_stats("bench_update.prof")


def plot(results_c: list[int], times_load: list[float],
         results_b: list[int], times_update: list[float]) -> None:

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    ax1.plot(results_c, times_load, 'o-', color='steelblue', label='mesuré')
    k1 = times_load[-1] / (results_c[-1] ** 1.5)
    ax1.plot(results_c, [k1 * c ** 1.5 for c in results_c],'--', color='gray', label=r'$\Theta(C^{1.5})$ référence')
    ax1.set_xlabel('C = W × H (nombre de cellules)')
    ax1.set_ylabel('Temps moyen (ms)')
    ax1.set_title('Chargement (parse + navmesh) vs C')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(results_b, times_update, 'o-', color='tomato', label='mesuré')
    nonzero = [(b, t) for b, t in zip(results_b, times_update) if b > 0]
    k2 = nonzero[-1][1] / nonzero[-1][0]
    ax2.plot(results_b, [k2 * b for b in results_b],'--', color='gray', label=r'$\Theta(B)$ référence')
    ax2.axhline(y=DELTA_TIME_MS, color='red', linestyle=':', linewidth=1.5, label=f'budget 60fps ({DELTA_TIME_MS:.1f} ms)')
    ax2.set_xlabel('B (nombre de Blobs)')
    ax2.set_ylabel('Temps moyen par frame (ms)')
    ax2.set_title('on_update vs nombre de Blobs')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('bench_results.png', dpi=150, bbox_inches='tight')


results_c, times_load = bench_load_map_and_navmesh_creation()
results_b, times_update = bench_on_update()
plot(results_c, times_load, results_b, times_update)
profile_loading()
profile_update()
WINDOW.close()
