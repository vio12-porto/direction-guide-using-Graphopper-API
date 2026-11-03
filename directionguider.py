import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "graphhoper_key"  # ganti dengan API key Anda


def geocoding(location, key):
    while location == "":
        location = input("Enter the location again: ")

    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_status = replydata.status_code
    json_data = replydata.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit["name"]
        value = hit["osm_value"]
        country = hit.get("country", "")
        state = hit.get("state", "")

        if state and country:
            new_loc = name + ", " + state + ", " + country
        elif country:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) +
                  "\nError message: " + json_data["message"])
    return json_status, lat, lng, new_loc


while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    vehicle = input("Enter a vehicle profile from the list above: ")
    if vehicle == "quit" or vehicle == "q":
        break
    elif vehicle in profile:
        pass
    else:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")

    loc1 = input("Starting Location: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)

    loc2 = input("Destination: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        response = requests.get(paths_url)
        paths_status = response.status_code
        paths_data = response.json()

        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
        print("=================================================")

        if paths_status == 200:
            km = paths_data["paths"][0]["distance"] / 1000
            miles = km / 1.61
            total_ms = paths_data["paths"][0]["time"]
            sec = int(total_ms / 1000 % 60)
            min = int(total_ms / 1000 / 60 % 60)
            hr = int(total_ms / 1000 / 60 / 60)

            print("Distance Traveled: {0:.1f} miles / {1:.1f} km".format(miles, km))
            print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            for step in paths_data["paths"][0]["instructions"]:
                d = step["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} miles )".format(step["text"], d / 1000, d / 1000 / 1.61))
            print("=================================================")
        else:
            print("Error message: " + paths_data["message"])
            print("*************************************************")
