import math


class Reward:
    def __init__(self, verbose=False):
        self.first_racingpoint_index = None
        self.verbose = verbose

    def reward_function(self, params):

        # Import package (needed for heading)
        import math

        ################## HELPER FUNCTIONS ###################

        def dist_2_points(x1, x2, y1, y2):
            return abs(abs(x1-x2)**2 + abs(y1-y2)**2)**0.5

        def closest_2_racing_points_index(racing_coords, car_coords):

            # Calculate all distances to racing points
            distances = []
            for i in range(len(racing_coords)):
                distance = dist_2_points(x1=racing_coords[i][0], x2=car_coords[0],
                                         y1=racing_coords[i][1], y2=car_coords[1])
                distances.append(distance)

            # Get index of the closest racing point
            closest_index = distances.index(min(distances))

            # Get index of the second closest racing point
            distances_no_closest = distances.copy()
            distances_no_closest[closest_index] = 999
            second_closest_index = distances_no_closest.index(
                min(distances_no_closest))

            return [closest_index, second_closest_index]

        def dist_to_racing_line(closest_coords, second_closest_coords, car_coords):
            
            # Calculate the distances between 2 closest racing points
            a = abs(dist_2_points(x1=closest_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=closest_coords[1],
                                  y2=second_closest_coords[1]))

            # Distances between car and closest and second closest racing point
            b = abs(dist_2_points(x1=car_coords[0],
                                  x2=closest_coords[0],
                                  y1=car_coords[1],
                                  y2=closest_coords[1]))
            c = abs(dist_2_points(x1=car_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=car_coords[1],
                                  y2=second_closest_coords[1]))

            # Calculate distance between car and racing line (goes through 2 closest racing points)
            # try-except in case a=0 (rare bug in DeepRacer)
            try:
                distance = abs(-(a**4) + 2*(a**2)*(b**2) + 2*(a**2)*(c**2) -
                               (b**4) + 2*(b**2)*(c**2) - (c**4))**0.5 / (2*a)
            except:
                distance = b

            return distance

        # Calculate which one of the closest racing points is the next one and which one the previous one
        def next_prev_racing_point(closest_coords, second_closest_coords, car_coords, heading):

            # Virtually set the car more into the heading direction
            heading_vector = [math.cos(math.radians(
                heading)), math.sin(math.radians(heading))]
            new_car_coords = [car_coords[0]+heading_vector[0],
                              car_coords[1]+heading_vector[1]]

            # Calculate distance from new car coords to 2 closest racing points
            distance_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                        x2=closest_coords[0],
                                                        y1=new_car_coords[1],
                                                        y2=closest_coords[1])
            distance_second_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                               x2=second_closest_coords[0],
                                                               y1=new_car_coords[1],
                                                               y2=second_closest_coords[1])

            if distance_closest_coords_new <= distance_second_closest_coords_new:
                next_point_coords = closest_coords
                prev_point_coords = second_closest_coords
            else:
                next_point_coords = second_closest_coords
                prev_point_coords = closest_coords

            return [next_point_coords, prev_point_coords]

        def racing_direction_diff(closest_coords, second_closest_coords, car_coords, heading):

            # Calculate the direction of the center line based on the closest waypoints
            next_point, prev_point = next_prev_racing_point(closest_coords,
                                                            second_closest_coords,
                                                            car_coords,
                                                            heading)

            # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
            track_direction = math.atan2(
                next_point[1] - prev_point[1], next_point[0] - prev_point[0])

            # Convert to degree
            track_direction = math.degrees(track_direction)

            # Calculate the difference between the track direction and the heading direction of the car
            direction_diff = abs(track_direction - heading)
            if direction_diff > 180:
                direction_diff = 360 - direction_diff

            return direction_diff

        # Gives back indexes that lie between start and end index of a cyclical list 
        # (start index is included, end index is not)
        def indexes_cyclical(start, end, array_len):

            if end < start:
                end += array_len

            return [index % array_len for index in range(start, end)]

        # Calculate how long car would take for entire lap, if it continued like it did until now
        def projected_time(first_index, closest_index, step_count, times_list):

            # Calculate how much time has passed since start
            current_actual_time = (step_count-1) / 15

            # Calculate which indexes were already passed
            indexes_traveled = indexes_cyclical(first_index, closest_index, len(times_list))

            # Calculate how much time should have passed if car would have followed optimals
            current_expected_time = sum([times_list[i] for i in indexes_traveled])

            # Calculate how long one entire lap takes if car follows optimals
            total_expected_time = sum(times_list)

            # Calculate how long car would take for entire lap, if it continued like it did until now
            try:
                projected_time = (current_actual_time/current_expected_time) * total_expected_time
            except:
                projected_time = 9999

            return projected_time

        #################### RACING LINE ######################

        # Optimal racing line for the Spain track
        # Each row: [x,y,speed,timeFromPreviousPoint]
        racing_track = [[0.34775, -2.173, 4.0, 0.07904],
                        [0.03162, -2.17293, 4.0, 0.07903],
                        [-0.28452, -2.17311, 4.0, 0.07904],
                        [-0.60066, -2.17318, 4.0, 0.07903],
                        [-0.91682, -2.17293, 4.0, 0.07904],
                        [-1.23295, -2.17295, 4.0, 0.07903],
                        [-1.54907, -2.17315, 4.0, 0.07903],
                        [-1.86524, -2.17319, 4.0, 0.07904],
                        [-2.18141, -2.17303, 4.0, 0.07904],
                        [-2.49703, -2.17286, 4.0, 0.07891],
                        [-2.81231, -2.17287, 3.67826, 0.08571],
                        [-3.12023, -2.17178, 3.36387, 0.09154],
                        [-3.40832, -2.16639, 3.11746, 0.09243],
                        [-3.67315, -2.15481, 2.91304, 0.091],
                        [-3.91587, -2.13615, 2.74019, 0.08884],
                        [-4.13906, -2.11004, 2.59065, 0.08674],
                        [-4.34538, -2.07631, 2.46067, 0.08496],
                        [-4.53716, -2.03485, 2.34319, 0.08374],
                        [-4.71631, -1.98551, 2.23387, 0.08318],
                        [-4.88433, -1.92804, 2.13488, 0.08318],
                        [-5.04235, -1.86205, 2.13488, 0.08021],
                        [-5.19122, -1.78697, 2.13488, 0.0781],
                        [-5.33151, -1.70198, 2.13488, 0.07683],
                        [-5.46347, -1.60589, 2.13488, 0.07646],
                        [-5.587, -1.49694, 2.50447, 0.06576],
                        [-5.70146, -1.37258, 3.07226, 0.05501],
                        [-5.80898, -1.23583, 4.0, 0.04349],
                        [-5.91154, -1.09012, 4.0, 0.04455],
                        [-6.01148, -0.9397, 4.0, 0.04515],
                        [-6.0995, -0.80946, 4.0, 0.0393],
                        [-6.18728, -0.68165, 4.0, 0.03876],
                        [-6.27492, -0.55603, 4.0, 0.03829],
                        [-6.36252, -0.43242, 4.0, 0.03788],
                        [-6.45016, -0.31068, 4.0, 0.0375],
                        [-6.5379, -0.19068, 4.0, 0.03716],
                        [-6.6258, -0.07232, 4.0, 0.03686],
                        [-6.71393, 0.04449, 4.0, 0.03658],
                        [-6.80234, 0.15983, 4.0, 0.03633],
                        [-6.89109, 0.27378, 3.71387, 0.03889],
                        [-6.98023, 0.3864, 3.03045, 0.0474],
                        [-7.06985, 0.49777, 2.61858, 0.05459],
                        [-7.16, 0.60792, 2.33605, 0.06093],
                        [-7.34242, 0.82509, 2.33605, 0.12141],
                        [-7.51721, 1.0459, 2.33605, 0.12055],
                        [-7.67697, 1.27353, 2.33168, 0.11927],
                        [-7.81458, 1.51025, 2.2637, 0.12095],
                        [-7.92294, 1.75686, 2.19952, 0.12247],
                        [-7.99486, 2.012, 2.13463, 0.12418],
                        [-8.03258, 2.27135, 2.13463, 0.12278],
                        [-8.03667, 2.53161, 2.13463, 0.12194],
                        [-8.00552, 2.78942, 2.13463, 0.12165],
                        [-7.93746, 3.04073, 2.13463, 0.12197],
                        [-7.83093, 3.28049, 2.30799, 0.11368],
                        [-7.68478, 3.50219, 2.41869, 0.10979],
                        [-7.50619, 3.70355, 2.54606, 0.10571],
                        [-7.2994, 3.88253, 2.68781, 0.10175],
                        [-7.0684, 4.03801, 2.85105, 0.09767],
                        [-6.81682, 4.16957, 3.04632, 0.09319],
                        [-6.54806, 4.27741, 3.28731, 0.08809],
                        [-6.26528, 4.36241, 3.59377, 0.08216],
                        [-5.97143, 4.42617, 4.0, 0.07517],
                        [-5.6692, 4.47093, 3.70808, 0.0824],
                        [-5.36095, 4.49949, 3.02882, 0.10221],
                        [-5.04869, 4.51517, 2.62147, 0.11926],
                        [-4.73409, 4.5216, 2.34382, 0.13426],
                        [-4.41918, 4.52269, 2.13877, 0.14724],
                        [-4.14695, 4.51532, 1.97844, 0.13765],
                        [-3.91151, 4.49653, 1.84539, 0.12799],
                        [-3.7048, 4.4656, 1.7342, 0.12052],
                        [-3.5217, 4.4226, 1.63402, 0.1151],
                        [-3.35902, 4.36803, 1.45633, 0.11782],
                        [-3.21485, 4.30258, 1.45633, 0.10872],
                        [-3.08807, 4.22706, 1.45633, 0.10133],
                        [-2.97818, 4.14236, 1.45633, 0.09527],
                        [-2.88509, 4.04944, 1.45633, 0.09031],
                        [-2.80911, 3.94939, 1.45892, 0.08612],
                        [-2.75307, 3.84294, 1.45892, 0.08245],
                        [-2.71495, 3.73266, 1.51194, 0.07717],
                        [-2.69466, 3.62029, 1.56647, 0.07289],
                        [-2.69044, 3.5075, 1.62279, 0.06955],
                        [-2.7009, 3.39547, 1.68465, 0.06679],
                        [-2.72498, 3.28512, 1.75006, 0.06454],
                        [-2.76177, 3.17716, 1.82263, 0.06258],
                        [-2.81056, 3.0722, 1.89343, 0.06113],
                        [-2.87069, 2.97075, 1.99628, 0.05908],
                        [-2.94169, 2.87328, 2.11279, 0.05708],
                        [-3.02285, 2.78011, 2.24716, 0.05499],
                        [-3.11347, 2.69144, 2.40949, 0.05261],
                        [-3.21279, 2.6074, 2.60909, 0.04987],
                        [-3.32, 2.52796, 2.86347, 0.0466],
                        [-3.43416, 2.45293, 2.6432, 0.05169],
                        [-3.55428, 2.38197, 2.17238, 0.06422],
                        [-3.67924, 2.31457, 1.8861, 0.07527],
                        [-3.80787, 2.25006, 1.68759, 0.08527],
                        [-3.93614, 2.18893, 1.53879, 0.09234],
                        [-4.06004, 2.12529, 1.41938, 0.09813],
                        [-4.17613, 2.05724, 1.41938, 0.09481],
                        [-4.28186, 1.98342, 1.41938, 0.09085],
                        [-4.37538, 1.90299, 1.41938, 0.0869],
                        [-4.4553, 1.81542, 1.41938, 0.08353],
                        [-4.52032, 1.72028, 1.53686, 0.07498],
                        [-4.56869, 1.61687, 1.59239, 0.07169],
                        [-4.60276, 1.50645, 1.65207, 0.06995],
                        [-4.62264, 1.38906, 1.71608, 0.06939],
                        [-4.62773, 1.26433, 1.78799, 0.06982],
                        [-4.61657, 1.13147, 1.86957, 0.07131],
                        [-4.58656, 0.9891, 1.96042, 0.07422],
                        [-4.5332, 0.83495, 2.05988, 0.07919],
                        [-4.4483, 0.6652, 2.16004, 0.08787],
                        [-4.31593, 0.47389, 2.19343, 0.10606],
                        [-4.1156, 0.26497, 2.22222, 0.13025],
                        [-3.87159, 0.0865, 2.24818, 0.13447],
                        [-3.61395, -0.04165, 2.27402, 0.12654],
                        [-3.36566, -0.12046, 2.29642, 0.11344],
                        [-3.13683, -0.1602, 2.31769, 0.10021],
                        [-2.927, -0.17127, 2.33883, 0.08984],
                        [-2.73327, -0.16075, 2.35863, 0.08226],
                        [-2.55287, -0.13312, 2.37286, 0.07691],
                        [-2.38357, -0.09112, 2.38661, 0.07309],
                        [-2.22372, -0.0364, 2.39352, 0.07059],
                        [-2.07202, 0.03012, 2.3947, 0.06917],
                        [-1.92748, 0.10816, 2.3947, 0.06859],
                        [-1.78927, 0.19798, 2.64412, 0.06234],
                        [-1.65666, 0.3006, 2.78442, 0.06022],
                        [-1.52811, 0.41511, 2.94568, 0.05844],
                        [-1.40281, 0.54205, 3.13542, 0.05689],
                        [-1.28, 0.68231, 3.36467, 0.05541],
                        [-1.15892, 0.83709, 3.6421, 0.05395],
                        [-1.03877, 1.00792, 4.0, 0.05221],
                        [-0.91862, 1.19676, 3.68404, 0.06076],
                        [-0.79737, 1.40593, 2.94366, 0.08213],
                        [-0.67367, 1.63804, 2.51931, 0.1044],
                        [-0.54587, 1.8957, 2.23675, 0.12859],
                        [-0.41214, 2.1805, 2.03055, 0.15495],
                        [-0.27186, 2.45834, 1.86713, 0.1667],
                        [-0.11843, 2.71914, 1.73627, 0.17427],
                        [0.05252, 2.95406, 1.73627, 0.16733],
                        [0.24282, 3.1558, 1.73627, 0.15973],
                        [0.4523, 3.31851, 1.73627, 0.15277],
                        [0.6794, 3.4369, 1.73627, 0.1475],
                        [0.92148, 3.50479, 1.95437, 0.12864],
                        [1.17407, 3.51372, 2.11404, 0.11956],
                        [1.42993, 3.47367, 2.31717, 0.11176],
                        [1.68478, 3.38833, 2.5896, 0.10378],
                        [1.9352, 3.26155, 2.98246, 0.09411],
                        [2.1787, 3.09844, 3.62855, 0.08077],
                        [2.41403, 2.90595, 4.0, 0.07601],
                        [2.64178, 2.69291, 4.0, 0.07796],
                        [2.86447, 2.46933, 4.0, 0.07889],
                        [3.08676, 2.2447, 3.22907, 0.09787],
                        [3.30934, 2.02005, 2.65999, 0.11889],
                        [3.53187, 1.79508, 2.31065, 0.13695],
                        [3.75427, 1.56983, 2.06878, 0.15301],
                        [3.97641, 1.34721, 1.88874, 0.16651],
                        [4.19715, 1.14479, 1.74488, 0.17164],
                        [4.41321, 0.97574, 1.62782, 0.16853],
                        [4.61966, 0.84634, 1.53154, 0.15909],
                        [4.81352, 0.75553, 1.44494, 0.14816],
                        [4.99381, 0.69892, 1.36805, 0.13812],
                        [5.16051, 0.67175, 1.3, 0.12993],
                        [5.31387, 0.67004, 1.3, 0.11798],
                        [5.45403, 0.69082, 1.3, 0.10899],
                        [5.58085, 0.73199, 1.3, 0.10257],
                        [5.69365, 0.79243, 1.3, 0.09844],
                        [5.79096, 0.87188, 1.37873, 0.09112],
                        [5.87004, 0.97096, 1.47004, 0.08624],
                        [5.93072, 1.08736, 1.57685, 0.08325],
                        [5.97211, 1.21983, 1.71094, 0.08111],
                        [5.99266, 1.36774, 1.88391, 0.07927],
                        [5.99044, 1.5307, 2.12066, 0.07685],
                        [5.96345, 1.70826, 2.46894, 0.07274],
                        [5.91045, 1.89955, 2.27125, 0.0874],
                        [5.83221, 2.10287, 2.02895, 0.10737],
                        [5.7335, 2.31514, 1.85064, 0.1265],
                        [5.63686, 2.50726, 1.70721, 0.12597],
                        [5.55635, 2.69304, 1.59134, 0.12724],
                        [5.49578, 2.87069, 1.4939, 0.12564],
                        [5.45645, 3.03926, 1.40987, 0.12278],
                        [5.4382, 3.19832, 1.33463, 0.11996],
                        [5.44032, 3.34759, 1.33463, 0.11186],
                        [5.46216, 3.48672, 1.33463, 0.10552],
                        [5.50334, 3.61508, 1.33463, 0.101],
                        [5.56401, 3.73161, 1.33463, 0.09844],
                        [5.64513, 3.83446, 1.65679, 0.07906],
                        [5.74889, 3.92024, 1.73875, 0.07743],
                        [5.86816, 3.99315, 1.83096, 0.07635],
                        [6.00303, 4.05237, 1.93405, 0.07616],
                        [6.15417, 4.09658, 2.05482, 0.07664],
                        [6.32298, 4.12377, 2.19828, 0.07778],
                        [6.5118, 4.13106, 2.31507, 0.08162],
                        [6.72455, 4.11405, 2.29787, 0.09288],
                        [6.96924, 4.06504, 2.27981, 0.10946],
                        [7.23605, 3.97246, 2.25811, 0.12507],
                        [7.43782, 3.87107, 2.2331, 0.10112],
                        [7.60293, 3.76378, 2.20505, 0.0893],
                        [7.74238, 3.65197, 2.20505, 0.08106],
                        [7.86188, 3.5364, 2.20505, 0.07539],
                        [7.96479, 3.41757, 2.20505, 0.07129],
                        [8.05322, 3.29577, 2.20505, 0.06826],
                        [8.12853, 3.17115, 2.38864, 0.06096],
                        [8.19155, 3.04381, 2.59316, 0.05479],
                        [8.2447, 2.91427, 2.85739, 0.049],
                        [8.28972, 2.78301, 3.21281, 0.04319],
                        [8.32812, 2.65059, 3.74461, 0.03682],
                        [8.3613, 2.51757, 4.0, 0.03427],
                        [8.39063, 2.38441, 4.0, 0.03409],
                        [8.41744, 2.25135, 4.0, 0.03393],
                        [8.44605, 2.11888, 4.0, 0.03388],
                        [8.47641, 1.98572, 4.0, 0.03414],
                        [8.5082, 1.85198, 4.0, 0.03437],
                        [8.54111, 1.71779, 4.0, 0.03454],
                        [8.57477, 1.58329, 3.88727, 0.03567],
                        [8.60883, 1.44862, 3.55754, 0.03905],
                        [8.64619, 1.29642, 3.29481, 0.04757],
                        [8.68404, 1.13291, 3.10924, 0.05398],
                        [8.72093, 0.95736, 2.94774, 0.06086],
                        [8.7547, 0.77082, 2.8059, 0.06756],
                        [8.78272, 0.57589, 2.67642, 0.07358],
                        [8.80238, 0.37615, 2.55908, 0.07843],
                        [8.81154, 0.17535, 2.45225, 0.08197],
                        [8.80892, -0.0233, 2.35362, 0.08441],
                        [8.79385, -0.21739, 2.26053, 0.08612],
                        [8.76608, -0.40519, 2.17117, 0.08744],
                        [8.72555, -0.58546, 2.0881, 0.08848],
                        [8.67236, -0.75727, 2.0881, 0.08613],
                        [8.60661, -0.91991, 2.0881, 0.08401],
                        [8.52835, -1.07276, 2.0881, 0.08224],
                        [8.43746, -1.2152, 2.0881, 0.08092],
                        [8.33356, -1.34653, 2.27364, 0.07365],
                        [8.2158, -1.4659, 2.37408, 0.07063],
                        [8.08601, -1.57512, 2.48104, 0.06837],
                        [7.94437, -1.67477, 2.60203, 0.06655],
                        [7.79071, -1.76521, 2.73873, 0.0651],
                        [7.62452, -1.84667, 2.8987, 0.06385],
                        [7.44497, -1.91922, 3.0896, 0.06268],
                        [7.25094, -1.98282, 3.32007, 0.0615],
                        [7.04109, -2.03732, 3.60931, 0.06007],
                        [6.81386, -2.08251, 3.98257, 0.05817],
                        [6.56783, -2.11817, 4.0, 0.06215],
                        [6.30214, -2.14423, 4.0, 0.06674],
                        [6.01745, -2.16104, 4.0, 0.0713],
                        [5.71684, -2.16974, 4.0, 0.07518],
                        [5.40604, -2.17253, 4.0, 0.0777],
                        [5.08989, -2.17261, 4.0, 0.07904],
                        [4.77373, -2.173, 4.0, 0.07904],
                        [4.45759, -2.17311, 4.0, 0.07903],
                        [4.14147, -2.17298, 4.0, 0.07903],
                        [3.82532, -2.17289, 4.0, 0.07904],
                        [3.50917, -2.17299, 4.0, 0.07904],
                        [3.19303, -2.17314, 4.0, 0.07903],
                        [2.87689, -2.1731, 4.0, 0.07904],
                        [2.56075, -2.17295, 4.0, 0.07903],
                        [2.2446, -2.17299, 4.0, 0.07904],
                        [1.92847, -2.17312, 4.0, 0.07903],
                        [1.61233, -2.17306, 4.0, 0.07904],
                        [1.29618, -2.17296, 4.0, 0.07904],
                        [0.98004, -2.17304, 4.0, 0.07903],
                        [0.6639, -2.17313, 4.0, 0.07904]]

        ################## INPUT PARAMETERS ###################

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
        is_offtrack = params['is_offtrack']

        ############### OPTIMAL X,Y,SPEED,TIME ################

        # Get closest indexes for racing line (and distances to all points on racing line)
        closest_index, second_closest_index = closest_2_racing_points_index(
            racing_track, [x, y])

        # Get optimal [x, y, speed, time] for closest and second closest index
        optimals = racing_track[closest_index]
        optimals_second = racing_track[second_closest_index]

        # Save first racingpoint of episode for later
        if self.verbose == True:
            self.first_racingpoint_index = 0 # this is just for testing purposes
        if steps == 1:
            self.first_racingpoint_index = closest_index

        ################ REWARD AND PUNISHMENT ################

        ## Define the default reward ##
        reward = 1

        ## Reward if car goes close to optimal racing line ##
        DISTANCE_MULTIPLE = 1
        dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])
        distance_reward = max(1e-3, 1 - (dist/(track_width*0.5)))
        reward += distance_reward * DISTANCE_MULTIPLE

        ## Reward if speed is close to optimal speed ##
        SPEED_DIFF_NO_REWARD = 1
        SPEED_MULTIPLE = 2
        speed_diff = abs(optimals[2]-speed)
        if speed_diff <= SPEED_DIFF_NO_REWARD:
            # we use quadratic punishment (not linear) bc we're not as confident with the optimal speed
            # so, we do not punish small deviations from optimal speed
            speed_reward = (1 - (speed_diff/(SPEED_DIFF_NO_REWARD))**2)**2
        else:
            speed_reward = 0
        reward += speed_reward * SPEED_MULTIPLE

        # Reward if less steps
        REWARD_PER_STEP_FOR_FASTEST_TIME = 1 
        STANDARD_TIME = 37
        FASTEST_TIME = 27
        times_list = [row[3] for row in racing_track]
        projected_time = projected_time(self.first_racingpoint_index, closest_index, steps, times_list)
        try:
            steps_prediction = projected_time * 15 + 1
            reward_prediction = max(1e-3, (-REWARD_PER_STEP_FOR_FASTEST_TIME*(FASTEST_TIME) /
                                           (STANDARD_TIME-FASTEST_TIME))*(steps_prediction-(STANDARD_TIME*15+1)))
            steps_reward = min(REWARD_PER_STEP_FOR_FASTEST_TIME, reward_prediction / steps_prediction)
        except:
            steps_reward = 0
        reward += steps_reward

        # Zero reward if obviously wrong direction (e.g. spin)
        direction_diff = racing_direction_diff(
            optimals[0:2], optimals_second[0:2], [x, y], heading)
        if direction_diff > 30:
            reward = 1e-3
            
        # Zero reward of obviously too slow
        speed_diff_zero = optimals[2]-speed
        if speed_diff_zero > 0.5:
            reward = 1e-3
            
        ## Incentive for finishing the lap in less steps ##
        REWARD_FOR_FASTEST_TIME = 1500 # should be adapted to track length and other rewards
        STANDARD_TIME = 37  # seconds (time that is easily done by model)
        FASTEST_TIME = 27  # seconds (best time of 1st place on the track)
        if progress == 100:
            finish_reward = max(1e-3, (-REWARD_FOR_FASTEST_TIME /
                      (15*(STANDARD_TIME-FASTEST_TIME)))*(steps-STANDARD_TIME*15))
        else:
            finish_reward = 0
        reward += finish_reward
        
        ## Zero reward if off track ##
        if all_wheels_on_track == False:
            reward = 1e-3

        ####################### VERBOSE #######################
        
        if self.verbose == True:
            print("Closest index: %i" % closest_index)
            print("Distance to racing line: %f" % dist)
            print("=== Distance reward (w/out multiple): %f ===" % (distance_reward))
            print("Optimal speed: %f" % optimals[2])
            print("Speed difference: %f" % speed_diff)
            print("=== Speed reward (w/out multiple): %f ===" % speed_reward)
            print("Direction difference: %f" % direction_diff)
            print("Predicted time: %f" % projected_time)
            print("=== Steps reward: %f ===" % steps_reward)
            print("=== Finish reward: %f ===" % finish_reward)
            
        #################### RETURN REWARD ####################
        
        # Always return a float value
        return float(reward)


reward_object = Reward() # add parameter verbose=True to get noisy output for testing


def reward_function(params):
    return reward_object.reward_function(params)
