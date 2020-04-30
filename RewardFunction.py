def reward_function(params):
    
    # Import package (needed for heading)
    import math

    # Read all input parameters
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
    MAX_SPEED = 3
    # SPEED_GRANULARITY = 3
    if speed < MAX_SPEED/3 + 0.1:
        reward *= 0.7
    elif speed < MAX_SPEED/3*2 + 0.1:
        reward *= 0.95
    
    ## Incentive for using less steps (absolute reward) ##
    SLOWEST_STEPS = 500 # about 35 seconds; start giving additional reward if car is this fast
    STEPS_INCREMENT = 10 # increase the reward if car reduces steps by 10
    SPLIT_TRACK_N_PARTS = 20
    STEPS_REWARD = 1 # additional reward for each iteration in the for-loop
    for i in range(SLOWEST_STEPS, STEPS_INCREMENT, -STEPS_INCREMENT):
        check_after_n_steps = int(i / SPLIT_TRACK_N_PARTS)
        if (steps % check_after_n_steps) == 0 and progress > (steps / i) * 100:
            reward += STEPS_REWARD
    
    ## Incentive for finishing the lap (absolute reward) ##
    if progress == 100:
        FINISH_MULTIPLE = 1.0 # Defines how much of the steps-for-loop should be given for finishing the lap
        # Always give 100 reward, but more if reward from step-for-loop is higher
        reward += max(100, (SLOWEST_STEPS-steps)/STEPS_INCREMENT*SPLIT_TRACK_N_PARTS*STEPS_REWARD*FINISH_MULTIPLE)

    ## Zero reward if heading of car is too far off next waypoint (obviously stupid decision) ##
    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    # Convert to degree
    track_direction = math.degrees(track_direction)
    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    # Penalize the reward if the difference is too large
    if direction_diff > 45.0:
        reward = 1e-3
        
    ## Zero reward if off track ##
    if not all_wheels_on_track or (0.5*track_width - distance_from_center) < 0.05:
        reward = 1e-3
        
    # Always return a float value
    return float(reward)
