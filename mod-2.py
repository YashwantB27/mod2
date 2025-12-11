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



2. How to Do the Module (The Logic)This module works on simple physics: Velocity = Distance / Time.Step A: Get the InputsYou need the "Centroid" (center point) of the cloud cluster from three specific timestamps2:$T_{0}$ (1 hour ago)$T_{30}$ (30 mins ago)$T_{60}$ (Current time)Step B: Calculate Displacement (The Vector)You need to measure how far the storm traveled over the full hour ($T_{0}$ to $T_{60}$).Formula:$$\Delta X = X_{60} - X_{0}$$$$\Delta Y = Y_{60} - Y_{0}$$(This tells you the total distance moved in 60 minutes)3.Step C: Calculate VelocitySince the displacement happened over 60 minutes:$Speed_X = \Delta X / 60$ pixels per minute.$Speed_Y = \Delta Y / 60$ pixels per minute.Step D: Predict the Future ($T_{90}$)You need to predict where it will be 30 minutes from now.Formula (Linear Extrapolation):$$X_{90} = X_{60} + (Speed_X \times 30)$$$$Y_{90} = Y_{60} + (Speed_Y \times 30)$$(You take the current position $X_{60}$ and add 30 minutes worth of travel to it)4.3. How to Test It (Verification)You don't need real satellite data to test if your math is working. You can use "Mock Data" (fake coordinates) to prove your logic is correct.Test Case 1: The "Steady Mover"Scenario: Imagine a storm moving steadily to the right by 10 pixels every 30 minutes.Mock Inputs:$T_{0}: (100, 100)$$T_{30}: (110, 100)$$T_{60}: (120, 100)$Manual Check:Displacement ($T_0$ to $T_{60}$): $120 - 100 = 20$ pixels.Time: 60 minutes.Velocity: $20 / 60 = 0.33$ pixels/min.Prediction for $T_{90}$ (30 mins later): It should move another 10 pixels.Expected Result: $(130, 100)$.Action: Feed these numbers into your code. If your code outputs (130, 100), it passes.Test Case 2: The "Diagonal Diver"Scenario: A storm moving South-East (Down and Right).Mock Inputs:$T_{0}: (0, 0)$$T_{60}: (60, 60)$Manual Check:It moved 60 pixels right and 60 pixels down in 60 minutes.Speed is 1 pixel/minute.In the next 30 minutes, it should move 30 pixels further.Expected Result: $(90, 90)$.Test Case 3: Visual Verification (The Dashboard)Use the dashboard code I provided earlier.Look at the Trajectory Map (Line Graph)5.Pass Condition: The "Red Dashed Line" (Prediction) should look like a straight extension of the "Blue Solid Line" (Past Path). If the red line shoots off in a crazy direction (like backwards), your plus/minus signs in the formula are wrong.



2. How to Do It (The Logic)You need to analyze two physical properties of the cloud cluster: Size (Area) and Shape (Circularity).Step A: Analyze the Area TrendConcept: Storms gather energy by pulling in moisture, which makes them grow.The Rule:If Area is Increasing compared to the previous frame ($T_{prev}$), the storm is Strengthening3.If Area is Decreasing, the storm is Weakening4.Step B: Analyze the Shape (Circularity)Concept: Cyclones rotate. This rotation naturally pulls the clouds into a tight, circular shape. Disorganized storms look messy and irregular.The Math: We use a formula called "Circularity" to measure how round a shape is.$$Circularity = \frac{4 \pi \times Area}{Perimeter^2}$$1.0: Perfect Circle (Danger).< 0.5: Irregular/Jagged Shape (Safe).The Rule:Circular Shape $\rightarrow$ Developing Storm5.Irregular/Scattered Shape $\rightarrow$ Dissipating System6.Step C: Making the DecisionCombine the two checks:WARNING: Area $\uparrow$ (Increasing) AND Shape is Circular.SAFE: Area $\downarrow$ (Decreasing) AND Shape is Irregular.3. Implementation (Python Code)This code takes the contour found in Module 1 and the area from the previous time step.Pythonimport cv2
import numpy as np

def module_3_severity_classification(current_contour, previous_area):
    # 1. Calculate Current Area (Size)
    current_area = cv2.contourArea(current_contour)
    
    # 2. Calculate Perimeter
    perimeter = cv2.arcLength(current_contour, True)
    
    # 3. Calculate Circularity (Shape)
    # Formula: (4 * Pi * Area) / (Perimeter^2)
    if perimeter == 0: 
        circularity = 0
    else:
        circularity = (4 * np.pi * current_area) / (perimeter ** 2)
        
    print(f"Stats -> Area: {current_area} | Circularity: {circularity:.2f}")

    # 4. The Decision Logic
    # We need a previous_area to compare against. If it's the first frame, we can't decide yet.
    if previous_area is None:
        return "MONITORING", current_area

    # Rule 1: Developing Storm (WARNING) 
    # Area is growing AND shape is round (Circularity > 0.6 is a good threshold)
    if current_area > previous_area and circularity > 0.6:
        status = "WARNING"
        
    # Rule 2: Dissipating System (SAFE) 
    # Area is shrinking AND shape is messy
    elif current_area < previous_area and circularity < 0.5:
        status = "SAFE"
        
    else:
        status = "MONITORING" # If it doesn't fit either perfectly
        
    return status, current_area
4. How to Test Module 3You can verify this logic without full satellite imagery by passing "fake" shapes to the function.Test Case 1: The Growing Cyclone (Should be WARNING)Input 1 (Previous): Area = 1000.Input 2 (Current): A perfect circle with Area = 1200.Logic Check:$1200 > 1000$ (Area Increasing? Yes).Circle shape has Circularity $\approx 0.9$ (Circular? Yes).Result: The function should return "WARNING".Test Case 2: The Dying Storm (Should be SAFE)Input 1 (Previous): Area = 1000.Input 2 (Current): A jagged, long rectangle with Area = 800.Logic Check:$800 < 1000$ (Area Decreasing? Yes).Jagged shape has Circularity $\approx 0.3$ (Irregular? Yes).Result: The function should return "SAFE".

