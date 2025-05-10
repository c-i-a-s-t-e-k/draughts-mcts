import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def measure_execution_time(func, n_runs=1000):
    """
    Measure the execution time of a function over multiple runs.
    
    Args:
        func: The function to measure
        n_runs: Number of times to run the function
        
    Returns:
        List of execution times in seconds
    """
    execution_times = []
    
    for _ in range(n_runs):
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    
    return execution_times

def plot_execution_time_distribution(execution_times):
    """
    Create visualization of execution time distribution.
    
    Args:
        execution_times: List of execution times
    """
    # Convert to milliseconds for better readability
    execution_times_ms = [t * 1000 for t in execution_times]
    
    plt.figure(figsize=(12, 8))
    
    # Plot 1: Histogram with KDE
    plt.subplot(2, 2, 1)
    plt.hist(execution_times_ms, bins=30, alpha=0.7, density=True, color='skyblue')
    
    # Add KDE curve
    x = np.linspace(min(execution_times_ms), max(execution_times_ms), 1000)
    kde = stats.gaussian_kde(execution_times_ms)
    plt.plot(x, kde(x), 'r-', linewidth=2)
    
    plt.title('Distribution of Execution Time')
    plt.xlabel('Execution Time (ms)')
    plt.ylabel('Density')
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Box plot
    plt.subplot(2, 2, 2)
    plt.boxplot(execution_times_ms, vert=False, patch_artist=True, 
                boxprops=dict(facecolor='lightgreen', color='blue'),
                whiskerprops=dict(color='blue'),
                medianprops=dict(color='red'))
    plt.title('Box Plot of Execution Times')
    plt.xlabel('Execution Time (ms)')
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Time series
    plt.subplot(2, 1, 2)
    plt.plot(range(len(execution_times_ms)), execution_times_ms, 'o-', markersize=3, alpha=0.5)
    plt.axhline(y=np.mean(execution_times_ms), color='r', linestyle='-', label=f'Mean: {np.mean(execution_times_ms):.4f} ms')
    plt.axhline(y=np.median(execution_times_ms), color='g', linestyle='--', label=f'Median: {np.median(execution_times_ms):.4f} ms')
    plt.title('Execution Time per Run')
    plt.xlabel('Run Number')
    plt.ylabel('Execution Time (ms)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Add statistics as text
    stats_text = f"""
    Statistics (in milliseconds):
    - Mean: {np.mean(execution_times_ms):.4f}
    - Median: {np.median(execution_times_ms):.4f}
    - Min: {min(execution_times_ms):.4f}
    - Max: {max(execution_times_ms):.4f}
    - Std Dev: {np.std(execution_times_ms):.4f}
    - 95th Percentile: {np.percentile(execution_times_ms, 95):.4f}
    """
    plt.figtext(0.5, 0.01, stats_text, ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.suptitle('Function Execution Time Analysis', fontsize=16)
    plt.subplots_adjust(top=0.9, bottom=0.15)
    
    return plt

# Example function to measure
def f():
    """
    Example function to measure execution time.
    Replace this with your actual function.
    """
    # Simulate some work
    result = 0
    for i in range(10000):
        result += i * i
    
    # Add some random variation to execution time
    time.sleep(abs(np.random.normal(0.001, 0.0005)))
    return result

# Main execution
if __name__ == "__main__":
    print("Measuring execution time of function f()...")
    times = measure_execution_time(f, n_runs=200)
    
    print(f"Completed {len(times)} runs")
    print(f"Mean execution time: {np.mean(times) * 1000:.4f} ms")
    print(f"Median execution time: {np.median(times) * 1000:.4f} ms")
    
    plt = plot_execution_time_distribution(times)
    plt.show()