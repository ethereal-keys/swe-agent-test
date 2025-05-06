"""
A custom LRU (Least Recently Used) cache implementation with a memory leak.
"""
import time
import gc
import sys

class CacheItem:
    """Item stored in the cache with a key, value, and expiration time."""
    def __init__(self, key, value, ttl):
        self.key = key
        self.value = value
        self.expiration = time.time() + ttl if ttl else None
        self.access_time = time.time()
    
    def is_expired(self):
        """Check if the item has expired."""
        if self.expiration is None:
            return False
        return time.time() > self.expiration
    
    def update_access_time(self):
        """Update the access time to the current time."""
        self.access_time = time.time()

class LRUCache:
    """
    A Least Recently Used (LRU) cache implementation with time-to-live (TTL) support.
    """
    def __init__(self, max_size=100, cleanup_interval=60):
        self.max_size = max_size
        self.cleanup_interval = cleanup_interval
        self.cache = {}  # Main cache dictionary
        self.item_references = {}  # BUG: Keeps references to all items ever added
        self.last_cleanup = time.time()
    
    def set(self, key, value, ttl=None):
        """Add or update an item in the cache with optional TTL in seconds."""
        # Create cache item
        item = CacheItem(key, value, ttl)
        
        # Store in main cache
        self.cache[key] = item
        
        # Store in references dictionary (this causes the memory leak)
        self.item_references[key] = item
        
        # Perform cleanup if needed
        self._cleanup_if_needed()
        
        # Enforce max size
        self._enforce_max_size()
    
    def get(self, key):
        """Retrieve an item from the cache by key."""
        # Check if key exists
        if key not in self.cache:
            return None
        
        # Get the item
        item = self.cache[key]
        
        # Check if item has expired
        if item.is_expired():
            self.delete(key)
            return None
        
        # Update access time and return value
        item.update_access_time()
        return item.value
    
    def delete(self, key):
        """Remove an item from the cache."""
        if key in self.cache:
            del self.cache[key]
            # BUG: We don't remove from item_references, causing a memory leak
    
    def _cleanup_if_needed(self):
        """Run cleanup if the cleanup interval has elapsed."""
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_expired()
            self.last_cleanup = current_time
    
    def _cleanup_expired(self):
        """Remove all expired items from the cache."""
        expired_keys = [key for key, item in self.cache.items() if item.is_expired()]
        for key in expired_keys:
            self.delete(key)
    
    def _enforce_max_size(self):
        """Remove least recently used items if cache exceeds max size."""
        if len(self.cache) <= self.max_size:
            return
        
        # Sort items by access time
        sorted_items = sorted(self.cache.items(), key=lambda x: x[1].access_time)
        
        # Calculate how many items to remove
        items_to_remove = len(self.cache) - self.max_size
        
        # Remove oldest items
        for i in range(items_to_remove):
            key = sorted_items[i][0]
            self.delete(key)
            
    def clear(self):
        """Clear all items from the cache."""
        self.cache.clear()
        # BUG: We don't clear item_references

    def get_stats(self):
        """Return statistics about the cache."""
        return {
            "cache_size": len(self.cache),
            "references_size": len(self.item_references),
            "memory_usage": sys.getsizeof(self.cache) + sys.getsizeof(self.item_references)
        }
        
    def __len__(self):
        """Return the number of items in the cache."""
        return len(self.cache)


def demonstrate_memory_leak():
    """Function to demonstrate the memory leak in the LRU cache."""
    # Create cache with small size to force evictions
    cache = LRUCache(max_size=10, cleanup_interval=1)
    
    print("Initial cache stats:")
    print(cache.get_stats())
    
    # Add many items to force evictions
    for i in range(100):
        cache.set(f"key{i}", f"value{i}", ttl=0.5)
        
        # Sleep briefly to allow some TTLs to expire
        if i % 20 == 0:
            time.sleep(1)
            # Force garbage collection to show it doesn't fix the issue
            gc.collect()
        
    # Wait for all TTLs to expire
    time.sleep(1)
    cache._cleanup_expired()
    
    print("\nAfter adding 100 items and cleaning expired:")
    print(cache.get_stats())
    
    # Add more items to demonstrate continued growth
    for i in range(100, 200):
        cache.set(f"key{i}", f"value{i}", ttl=0.5)
    
    # Wait for all TTLs to expire
    time.sleep(1)
    cache._cleanup_expired()
    
    print("\nAfter adding another 100 items and cleaning expired:")
    print(cache.get_stats())
    
    # Clear the cache
    cache.clear()
    print("\nAfter clearing the cache:")
    print(cache.get_stats())

if __name__ == "__main__":
    demonstrate_memory_leak()
