import sqlite3
from auto_cpufreq.profiler.database import get_db_path

# Score threshold for an app to be considered performance-hungry.
# e.g., 0.5 means it spends 50% of its runtime in high load.
SCORE_THRESHOLD = 0.5
# Minimum total runtime in milliseconds before an app is considered for profiling.
# This prevents apps that run for a very short time from being misclassified.
MIN_RUNTIME_MS = 10000 # 10 seconds

def calculate_score(total_runtime_ms, high_load_runtime_ms):
    """Calculates a performance score for an application."""
    if total_runtime_ms == 0:
        return 0
    return high_load_runtime_ms / total_runtime_ms

def get_learned_performance_apps():
    """
    Analyzes the profiler database and returns a list of applications
    that are considered performance-hungry based on a scoring algorithm.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT process_name, total_runtime_ms, high_load_runtime_ms FROM applications")
    apps = cursor.fetchall()
    conn.close()

    performance_apps = []
    for app in apps:
        process_name, total_runtime_ms, high_load_runtime_ms = app
        if total_runtime_ms < MIN_RUNTIME_MS:
            continue

        score = calculate_score(total_runtime_ms, high_load_runtime_ms)
        if score >= SCORE_THRESHOLD:
            performance_apps.append(process_name)

    return performance_apps

if __name__ == '__main__':
    learned_apps = get_learned_performance_apps()
    if learned_apps:
        print("Learned performance-hungry applications:")
        for app in learned_apps:
            print(f"- {app}")
    else:
        print("No performance-hungry applications learned yet.")
