import sys
print("Testing tensorflow import only...")

try:
    import tensorflow as tf
    print(f"tensorflow imported: {tf.__version__}")
except Exception as e:
    print(f"tensorflow failed: {e}")

print("Finished")
