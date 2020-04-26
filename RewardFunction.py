def reward_function(params):
    
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    progress=params['progress']
    speed = params['speed']
    
    # Define the default reward
    reward = 1.0
    # Penalize if the car goes too slow
    if speed < 1:
        reward *= 0.5
    elif speed < 1.5:
        reward *= 0.9
    
    #Incentive for finishing the lap
    if progress == 100:
        reward = reward + 100

    if not all_wheels_on_track or (0.5*track_width - distance_from_center) < 0.05:
        reward = 1e-3
        
    # Always return a float value
    return float(reward)
