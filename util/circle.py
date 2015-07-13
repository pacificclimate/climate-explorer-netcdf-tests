__all__ = ["wkt_circle"]

# from https://cynici.wordpress.com/2011/09/16/how-to-make-a-circle-geometry-in-kml-or-wkt/
from math import asin,cos,pi,sin

rEarth_km = 6371.01 # Earth's average radius in km
epsilon = 0.000001 # threshold for floating-point equality

def deg2rad(angle):
    return angle*pi/180

def rad2deg(angle):
    return angle*180/pi

def pointRadialDistance(lat1_deg, lon1_deg, bearing_deg, distance_m):
    """
    Return final coordinates (lat2,lon2) [in degrees] given initial coordinates
    (lat1,lon1) [in degrees] and a bearing [in degrees] and distance [in m]
    """
    rlat1 = deg2rad(lat1_deg)
    rlon1 = deg2rad(lon1_deg)
    rbearing = deg2rad(bearing_deg)
    rdistance = distance_m / (rEarth_km*1000) # normalize linear distance to radian angle
    rlat = asin( sin(rlat1) * cos(rdistance) + cos(rlat1) * sin(rdistance) * cos(rbearing) )
    if cos(rlat) == 0 or abs(cos(rlat)) < epsilon: # Endpoint a pole
        rlon=rlon1
    else:
        rlon = ( (rlon1 - asin( sin(rbearing)* sin(rdistance) / cos(rlat) ) + pi ) % (2*pi) ) - pi
    lat = rad2deg(rlat)
    lon = rad2deg(rlon)
    return (lat, lon)

def wkt_circle(lat_deg=54, lon_deg=-125, sides=8, radius_m=100000):
    theta = 360/sides
    result = []
    for i in range(sides):
        lat, lon = pointRadialDistance(lat_deg, lon_deg, i*theta, radius_m)
        result.append("%f%s%f" % (lon, ' ', lat))
    # Close the polygon
    result.append(result[0])

    return 'POLYGON((%s))' % ','.join(result)
