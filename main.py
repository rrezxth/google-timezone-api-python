import requests
import time

outputFormat = "json"
coordinates = "43.79614407228324,-79.34857003914883"    # this is SenecaCollege's coordinates
unixTimestamp = time.time()  # using built-in function to get the Unix Timestamp
apiKey = "AIzaSyBZQBnlke9vzjcTo0PL1HmggIlhNBh4chU"
timezone_api = f"https://maps.googleapis.com/maps/api/timezone/{outputFormat}?location={coordinates}&timestamp={unixTimestamp}&key={apiKey}"


def get_current_time(timestamp, dstOS, rawOS):
    # Calculate from timestamp
    seconds = int(timestamp % 60)
    minutes = int((timestamp // 60) % 60)
    hours = (int(timestamp // 3600) % 24)

    totalOffset = (dstOS + rawOS) // 3600
    hours += totalOffset

    # Turn to string and "fill" values
    seconds_fill = str(seconds).zfill(2)
    minutes_fill = str(minutes).zfill(2)
    hours_fill = str(hours).zfill(2)

    # Convert military time into AM/PM
    if hours >= 12:
        if hours == 12:
            return f"{hours_fill}:{minutes_fill}:{seconds_fill} PM"
        else:
            return f"{(str(hours % 12).zfill(2))}:{minutes_fill}:{seconds_fill} PM"
    else:
        return f"{hours_fill}:{minutes_fill}:{seconds_fill} AM"


try:
    # SEND a GET request
    response = requests.get(timezone_api)

    # CHECK if the request was successful
    if response.status_code == 200:
        # Save the JSON response of dstOffset, rawOffset and timezone
        data = response.json()
        dstOffset = int(data["dstOffset"])
        rawOffset = int(data["rawOffset"])
        timeZoneName = data["timeZoneName"]

        current_time = get_current_time(unixTimestamp, dstOffset, rawOffset)
        print(current_time, timeZoneName)
    else:
        # Any non-200 code response is error
        print("Error: API request failed with status code", response.status_code)
except requests.exceptions.RequestException:
    print("Error: An exception occurred during the API request")