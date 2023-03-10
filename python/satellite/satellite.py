import numpy as np

class Satellite:
    def __init__(self, minor_axis, major_axis, period, nsatellite):
        """
        variable definition below:
        
        nsatellite: number of satellites in each orbit
        period: it is a list of period in minutes for each satellite.
                Please note thatit has to match with the nsatellite.
        major_axis: it is the major axis for elliptic orbit in kilometer.
        minor_axis: it is the minor axis for elliptic orbit in kilometer.
        
        Note: All stellites are separated with 360/n degree.
        
        """
        self.minor_axis = minor_axis
        self.major_axis = major_axis
        self.nsatellite = nsatellite
        self.period = period
        
        if (type(minor_axis)!=float) & (type(minor_axis)!=int):
            raise TypeError("minor_axis must be a number")
        if (type(major_axis)!=float) & (type(major_axis)!=int):
            raise TypeError("major_axis must be a number")
        if type(period) is not list:
            raise TypeError("period must be a list and has the same length as nsat")
        if type(nsatellite) is not int:
            raise TypeError("nsatellite must be a an integer")
        if (nsatellite != len(period)):
            raise ValueError("number of satellites do not match with the number of periods!")
        
    def path(self, sat_index, time, start_point=np.radians(90)):
        """
        path calculates x, y, and z of each satellite for a given time.
        
        variables:
        
        sat_index: it is the index of satellite corresponding to each period.
                   it must start from one
        time: it is the time variable in seconds.
        start_point: it is an optional argument to define the starting point of
                     the satellite in radians. The default value is at north
                     pole at np.radian(90).
        
        return respectively:
        - x: the X location of satellite in elliptic plate in kilometer
        - y: the Y location of satellite in elliptic plate in kilometer
        - z: the Z location in degree
        """
        
        if (sat_index % 1 != 0):
            raise TypeError("sat_index must be an integer")
        if (sat_index < 1):
            raise ValueError("sat_index must be greater than zero")
        
        
        sat_index -= 1
        
        theta = np.radians(360) / self.period[sat_index] / 60.0 * time + start_point
        
        x = self.minor_axis * np.cos(theta)
        y = self.major_axis * np.sin(theta)
        z = 360./self.nsatellite * (sat_index)
        
        return x,y,z
    
    def angle(self, time, start_point = np.radians(90)):
        """
        angle calculates the angle of satellite with respect to earth
        assuming that north pole is at degree 90 and south pole at 270.
        
        time: it is the variable time in unit of seconds.
        start_point: it is an optional variable where it defines where the
                     satellite starting point is. the unit is in radians.
        
        return:
        
        theta: the angle of satellite with respect to the earth.
        """
        
        theta = (np.radians(360) / np.array(self.period) / 60.0 * time + start_point)/np.pi*180 % 360

        return theta
    
    def possible_collision_time(self, sat_index, start_point=np.radians(90)):
        """
        possible_collision_time calculates the first time where the satellite
        reach out to the the two possible collision location.
        
        variables:
        sat_index: the index of desired satellite. please note that it has
                   to start from one.
        start_point: it is optional and it is the value where the satellite
                     starting point is. The de
        
        return variable:
        time: in minutes where it reaches the first possible location for collision.
        """
        
        if (sat_index % 1 != 0):
            raise TypeError("sat_index must be an integer")
        if (sat_index < 1):
            raise TypeError("sat_index must be greater than zero")
            
        sat_index -= 1
        collision_points = np.array([np.pi/2.0, 3.0*np.pi/2.0])
        time = (collision_points - start_point) / (2.0 * np.pi) * self.period[sat_index]
        if 0 in time:
            time[time==0] = self.period[sat_index]
            
        return time
    
    def collision(self, sat_index, start_point=[np.radians(90), np.radians(90)], max_year = 2):
        """
        collision calcaulates the time where two satellite collide with each other.
        
        variables:
        sat_index: index of the two desired satellite. please note that
                   the input has to be a list of 2 indecies. the starting index is one.
        start_point: is optional. it is the location in radians where each
                     satellite starts its journey.
        max_year: is optional. it is the maximum period that you want to check
                  whether they will collide or not.
        
        return respectively:
        x: the X location of collision in km
        y: the Y location of collision in km
        theta: the angle with respect to earth the collision happens in degree
        time: the first possible collision time in minutes
        
        """
        n = 2
        
        if type(sat_index) is not list:
            raise TypeError("sat_index must be a list of two satellite")
        elif (len(sat_index) != n):
            raise ValueError("sat_index must have two satellites at a time")
        elif 0 in sat_index:
            raise ValueError("sat_index has a minimum value of 1. the index does NOT start from zero.")
        elif (sat_index[0] == sat_index[1]):
            raise ValueError("sat_index contains of two same index. Satellite cannot collide with itself")
        elif type(start_point) is not list:
            raise TypeError("sat_index must be a list of two satellite")
        elif (len(start_point) != n):
            raise TypeError("start_point must have two satellite starting points")    
        
            
        sat_index = np.array(sat_index)-1
        
        time = []
        for i in range(n):
            time.append(self.possible_collision_time(sat_index[i]+1, start_point[i]))
        time = np.array(time)
      
        while ( 
            ((time[0, 0]-time[1, 0])!=0) & 
            ((time[0, 1]-time[1, 1])!=0) & 
            (time[0, 0]<=max_year*365.*24.*3600.) 
        ):
            for i in range(n):
                if time[0, i]> time[1][i]:
                    time[1, i] += self.period[sat_index[1]]
                else:
                    time[0, i] += self.period[sat_index[0]]
                
        
        if (time[0, 0]-time[1, 0])==0:
            x,y,z = self.path(sat_index[0]+1, time[0][0], start_point[0])
            theta = 90.0
            collision_time = time[0, 0] # [min]
        elif (time[0, 1]-time[1, 1])==0:
            x,y,z = self.path(sat_index[0]+1, time[0][1], start_point[0])
            theta = 180.0
            collision_time = time[0, 1] # [min]
        else:
            print(f"Satellite {sat_index[0]+1} and {sat_index[1]+1} Those two satellites will"+
                  f" not collide in {max_year} years.")
            x = y = z = theta = collision_time = np.nan
        
        return x, y, theta, collision_time
    
    def collision_all(self, start_point=None, max_year=2):
        """
        collision_all calculates all satellite collision possibilities.
        
        optional variables:
        start_point: it is optional if you want to have a different starting point than default.
                     the default start position is np.radian(90). the input has to be in radian.
        max_year: it is an optional. it is the maximum number of years you want to check if the
                  collision will occur.
        
        """
        if start_point is None:
            start_point = [np.radians(90.0) for i in self.period]

        if len(start_point)!=len(self.period):
            raise ValueError("start_point length must be equal to the number of satellite")
        if type(start_point)!=list:
            raise TypeError("start_point must be a list of radians")
        if (type(max_year)!=int):
            raise TypeError("max_year must be an integer")
            
        ctr = 0
        collision_sat = {'satellites':[], 'X':[], 'Y':[], 'Theta':[], 'Time':[]}
        for i in range(1, len(self.period)):
            for j in range(i+1, len(self.period)+1):
                x, y, theta, time = self.collision(
                    [i, j],
                    start_point = [start_point[i-1], start_point[j-1]],
                    max_year= max_year
                )

                collision_sat['satellites'] += [(i,j)]
                collision_sat['X'] += [x]
                collision_sat['Y'] += [y]
                collision_sat['Theta'] += [theta]
                collision_sat['Time'] += [time]
                
        return collision_sat
