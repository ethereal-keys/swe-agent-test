import threading
import time
import random

class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        """Increment the counter by 1"""
        # Read the current value
        current = self.count
        
        # Simulate some work that takes time
        time.sleep(random.random() * 0.01)
        
        # Update with new value
        self.count = current + 1
    
    def get_count(self):
        """Get the current counter value"""
        return self.count

def worker(counter, iterations):
    """Worker function that increments the counter multiple times"""
    for _ in range(iterations):
        counter.increment()

def main():
    # Create a shared counter
    counter = Counter()
    
    # Number of threads and iterations
    num_threads = 10
    iterations_per_thread = 100
    total_expected = num_threads * iterations_per_thread
    
    # Create and start threads
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(counter, iterations_per_thread))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # Display results
    print(f"Expected count: {total_expected}")
    print(f"Actual count: {counter.get_count()}")
    print(f"Missing increments: {total_expected - counter.get_count()}")

if __name__ == "__main__":
    main()
