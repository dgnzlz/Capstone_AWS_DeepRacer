def reward_function(params):
    
    ## Read input parameters ##
    all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    heading = params['heading']
    progress = params['progress']
    steps = params['steps']
    speed = params['speed']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    
    ## Define the default reward ##
    reward = 1.0
    
    ## Penalize if the car goes too slow (relative penalization) ##
    if speed < 1:
        reward *= 0.5
    elif speed < 1.5:
        reward *= 0.9
    
    ## Incentive for using less steps (absolute reward) ##
    SLOWEST_STEPS = 500 # about 35 seconds
    FASTEST_STEPS = 200 # about 13 seconds
    SPLIT_TRACK_N_PARTS = 20
    for i in range(SLOWEST_STEPS, FASTEST_STEPS, -10):
        check_after_n_steps = int(i / SPLIT_TRACK_N_PARTS)
        if (steps % check_after_n_steps) == 0 and progress > (steps / i) * 100:
            reward += 1
    
    ## Incentive for finishing the lap (absolute reward) ##
    if progress == 100:
        reward += 100

    ## Zero reward if off track ##
    if not all_wheels_on_track or (0.5*track_width - distance_from_center) < 0.05:
        reward = 1e-3
        
    # Always return a float value
    return float(reward)
