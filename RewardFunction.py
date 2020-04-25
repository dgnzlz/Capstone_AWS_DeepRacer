def reward_function(params):
    
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    progress=params['progress']
    speed = params['speed']
    SPEED_THRESHOLD = 1.0
    
    # Give a very low reward by default
    reward = 1e-3

    # Give a high reward if no wheels go off the track, 
    #the speed is higher than 1.0 and
    # the agent is somewhere in between the track borders
    if not all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward = reward - 1.0
    elif speed < SPEED_THRESHOLD:
    # Penalize if the car goes too slow
        reward = reward - 2.0
    else:
    # High reward if the car stays on track and goes fast
        reward = reward + 2.0
    
    #Incentive for finishing the lap
    if progress == 100:
        reward = reward + 100

    # Always return a float value
    return float(reward)
