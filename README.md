# Satellite Class

The structure of this folder is:
- `outputs` where the output files are
- `python` where the python codes are

## Objective
Satellite is written in `python/satellite` directory. The class is stored in `satellite.py` file. The class needs four inputs:
- `minor_axis` as the minor axis of elliptic function
- `major_axis` as the major axis of elliptic function
- `period` is the time takes a satellite finish a full orbit.
- `nsatellite` is the number of satellites in the class.

example to initialize the class:
```
import satellite as sat

example = sat.Satellite(
	minor_axis = 6378.1370, # [km]
	major_axis = 6356.7523, # [km]
	period = [90, 120, 180, 200], # [min]
	nsatellite =4,
)
```

### Functions inside the Satellite class
- `path` this function calculates `x`, `y`, `z` of a satellite for each time in seconds.
example:
```
x, y, z = example.path(index, time=3600)
```
- `angle` this function calculates the angle of satellite with respect to earth at a given time assuming that north pole is 90 degree and south pole is at 270 degree and the rotation of satellite is counter clock-wise.
example:
```
example.angle(time=3600)
```
- `possible_collision_time` calculates the first time where the satellite reach out to the the two possible collision location.
example:
```
example.possible_collision_time(1)
```
- `collision` This function collision calcaulates the time where two satellites collide with each other.
example:
```
example.collision(sat_index=[1,2])
```
- `collision_all` calculates all satellite collision possibilities.
example:
```
example.collision_all() 
```


## Important notes
- Index of satellites in the class starts from 1 <b>not</b> zero.

### Assumptions
- Each satellite rotates in a counter clock-wise orbit.
- North pole is at 90 degree.
- South pole is at 270 degree.
- The collision point of satellites are on either north pole or south pole.

## How to run the program
First you need to setup your virtual environment as follows:
1. `python -m venv .venv`
2.  `source .venv/bin/activate`
3. `pip install --upgrade pip`
4. `pip install -r requirements.txt`
5. Now you can run `main.py`

To run `main.py` you need to know the arguments to pass it into the program. The arguments are as follows:
1. `-a` or `--minor_axis`  minor axis of the elliptic function
2. `-b`, `--major_axis` major axis of the elliptic function
3. `-t`, `--period` list of periods for input satellites
4. `-sp`, `--start_point` is optional. It is a list of starting point of each satellite in rad
5. `-my`, `--max_year` is optional. It is the maximum number of year as a time period to calculate the possibility of collision.
6. `-o`, `--collision_output` is optional. It is the name of excel file contains the collision information.

If you are confused, do not worry. You can take a look at the example below to run it on commandline.
Simple examples:
```
$ python main.py -a 6378.1370 -b 6356.7523 -t 90 100 120 70 80 60
```
More complex example where the starting point of each satellite is different:
```
$ python main.py -a 6378.1370 -b 6356.7523 -t 90 100 120 70 -sp 0.52359878 1.04719755 1.57079633 2.0943951 -my 5 -o test-v1
```
