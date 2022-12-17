import numpy as np
import matplotlib.pyplot as plt
import argparse
import satellite as sat
import pandas as pd

if __name__=='__main__' :
    parser = argparse.ArgumentParser(description="use the satellite modules to calculate collisions.")
    parser.add_argument("-a", "--minor_axis", required=True, type=float, help="minor axis of the elliptic function")
    parser.add_argument("-b", "--major_axis", required=True, type=float, help="major axis of the elliptic function")
    parser.add_argument("-t", "--period", nargs='+', required=True, type=float, help="list of periods for input satellites")
    parser.add_argument("-sp", "--start_point", nargs='+', required=False, type=float, help="list of starting point of each satellite in radian")
    parser.add_argument("-my", "--max_year", required=False, type=int, help="maximum number of year as a time period to calculate the possibility of collision")
    parser.add_argument("-o", "--collision_output", required=False, type=str, help="excel file contains the collision information")

    args = parser.parse_args()

    print(f"args.minor_axis = {args.minor_axis}")
    print(f"args.major_axis = {args.major_axis}")
    print(f"args.period = {args.period}")
    print(f"args.start_point = {args.start_point}")
    print(f"args.max_year = {args.max_year}")
    print(f"args.collision_output = {args.collision_output}")
    
    test = sat.Satellite(
        minor_axis = args.minor_axis,
        major_axis = args.major_axis,
        period = args.period,
        nsatellite=len(args.period),
    )

    # plot the path of first satellite as a test
    print("\nFirst Satellite Path:")
    index = 1
    t = np.linspace(0,args.period[index-1]*60)
    
    print(test.path(index, t))

    print("\nVisualization of first satellite path:")
    if args.start_point is None:
        x, y, z = test.path(index, t)
    else:
        x, y, z = test.path(index, t, start_point=args.start_point[index-1])
        
    plt.scatter(x,y,c=t)
    plt.xlabel("X location [km]")
    plt.ylabel("Y location [km]")
    plt.show()
    
    # angle of the satellite
    t = 3600
    print(f"\nAngle of all satellites at time {t} s:")
    if args.start_point is None:
        print(test.angle(t))
    else:
        print(test.angle(t, start_point=args.start_point))

    # collision of first and second satellite
    satellite_index = [1,2]
    if len(args.period) > 1:
        print("\nCollision of satellite 1 and 2:")
        if (args.start_point==None) & (args.max_year==None):
            x, y, theta, time = test.collision(satellite_index)
        elif (args.start_point==None) & (args.max_year!=None):
            x, y, theta, time = test.collision(satellite_index, max_year = args.max_year)
        elif (args.start_point!=None) & (args.max_year==None):
            x, y, theta, time = test.collision(
                satellite_index,
                start_point = [args.start_point[i] for i in (np.array(satellite_index)-1).astype(int).tolist()],
            )
        else:
            x, y, theta, time = test.collision(
                satellite_index,
                start_point = [args.start_point[i] for i in (np.array(satellite_index)-1).astype(int).tolist()],
                max_year = args.max_year
            )
            
        print(f"   x = {x} km\n   y = {y} km\n   theta = {theta} degree\n   time = {time} minutes")

    # all collisions
    if (args.start_point==None) & (args.max_year==None):
        output = test.collision_all()
    elif (args.start_point!=None) & (args.max_year==None):
        output = test.collision_all(start_point=args.start_point)
    elif (args.start_point==None) & (args.max_year!=None):
        output = test.collision_all(max_year=args.max_year)
    else:
        output = test.collision_all(start_point=args.start_point, max_year=args.max_year)
        

        
    df = pd.DataFrame(output)
    print(f"ouput {args.collision_output}")
    if args.collision_output is None:
        df.to_excel("../outputs/collision.xlsx", index=False)
    else:
        df.to_excel(f"../outputs/{args.collision_output}.xlsx", index=False)
