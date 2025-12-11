import math

def predict_next_position(centroids):
    """
    centroids: A list of tuples [(x0, y0), (x30, y30), (x60, y60)]
    representing position at T0, T30, and T60.
    """
    
    # Unpack coordinates
    (x0, y0) = centroids[0]   # T-60 mins
    (x30, y30) = centroids[1] # T-30 mins
    (x60, y60) = centroids[2] # Current Time (T0 relative to prediction)

    print(f"Tracking History: T0({x0},{y0}) -> T30({x30},{y30}) -> T60({x60},{y60})")

    # 1. Calculate Displacement Vector (Over the last 1 hour: T0 to T60)
    # The problem asks: "How much did (X, Y) change in 1 hour?"
    dx_total = x60 - x0
    dy_total = y60 - y0
    
    # 2. Calculate Velocity (Pixels per minute)
    # Total time elapsed is 60 minutes
    vx = dx_total / 60.0
    vy = dy_total / 60.0

    # 3. Predict Position for T90 (Next 30 mins)
    # New Pos = Current Pos + (Velocity * Time Step)
    time_step = 30 # minutes
    
    x90 = x60 + (vx * time_step)
    y90 = y60 + (vy * time_step)

    # Round to nearest integer for pixel coordinates
    predicted_centroid = (int(x90), int(y90))
    
    # --- OPTIONAL: Calculate Speed in km/h for the Dashboard ---
    # Assumption: 1 Pixel = 4 km (Example Scale for INSAT-3D)
    pixel_distance = math.sqrt(dx_total**2 + dy_total**2)
    km_distance = pixel_distance * 4
    speed_kmh = km_distance / 1.0 # since time is 1 hour
    
    return predicted_centroid, speed_kmh

# Example Usage:
history = [(100, 200), (110, 205), (125, 215)]
future_pos, speed = predict_next_position(history)
print(f"Storm Predicted at: {future_pos}, Speed: {speed:.2f} km/h")