import gpxpy
import os
import pandas as pd



class RouteError(Exception):
    pass

def route_or_track(gpx):
    if len(gpx.tracks):
        return "track"
    if len(gpx.routes):
        return "route"
    raise RouteError("Neither route nor track")

def create_profile_record(file_path):
    with open(file_path) as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        numWaypoints = len(gpx.waypoints)

        routeType = route_or_track(gpx)

        if routeType == "route":
            numRoutes = len(gpx.routes)
            numSegments = 0
        elif routeType == "track":
            numRoutes = len(gpx.tracks)
            numSegments = sum([len(t.segments) for t in gpx.tracks])
        

        name = gpx.name

        return {
            "name": name,
            "routeType": routeType,
            "numRoutes": numRoutes,
            "numSegments": numSegments,
            "numWaypoints": numWaypoints,
        }
        
    pass

routeData = []

errors = []

folder_path = "./bpt-gpx"

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and file_path[-4:] == ".gpx":
        # Do something with the file
        print(file_path)

        try: 
            record = create_profile_record(file_path)
            routeData.append(record)
        except RouteError as e:
            errors.append({
                "file": file_path,
                "error": e.message
            })

            
routeFrame = pd.DataFrame(routeData)
routeFrame.to_csv("./profiling/routeProfileFrame.csv")

errorsFrame = pd.DataFrame(errors)
errorsFrame.to_csv("./profiling/profileErrors.csv")

