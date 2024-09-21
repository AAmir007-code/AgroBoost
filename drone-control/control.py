from pymavlink import mavutil
import time
import requests

class DroneController:
    def __init__(self, connection_string, api_url):
        """
        Initialize the connection to the drone and API URL.
        :param connection_string: The connection string to the drone (e.g., 'tcp:127.0.0.1:5760' or 'udp:127.0.0.1:14550').
        :param api_url: URL of the API to send captured images to.
        """
        self.connection = mavutil.mavlink_connection(connection_string)
        self.connection.wait_heartbeat()
        print("Connected to the drone!")
        self.api_url = api_url

    def arm_and_takeoff(self, target_altitude):
        """
        Arms the drone and takes off to the target altitude.
        :param target_altitude: The altitude in meters to climb to after takeoff.
        """
        print("Arming motors...")
        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0
        )
        self.connection.motors_armed_wait()
        print("Motors armed!")

        # Set mode to GUIDED
        self.set_mode("GUIDED")

        # Takeoff to target altitude
        print(f"Taking off to {target_altitude} meters...")
        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0, 0, 0, 0, 0, 0, target_altitude
        )
        time.sleep(10)

    def set_mode(self, mode):
        """
        Sets the flight mode of the drone.
        :param mode: The desired flight mode (e.g., 'GUIDED', 'LOITER', 'RTL').
        """
        print(f"Setting mode to {mode}...")
        mode_id = self.connection.mode_mapping()[mode]
        self.connection.mav.set_mode_send(
            self.connection.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id
        )

    def move_to(self, latitude, longitude, altitude):
        """
        Commands the drone to move to a specified GPS coordinate (latitude, longitude, altitude).
        :param latitude: Target latitude in degrees.
        :param longitude: Target longitude in degrees.
        :param altitude: Target altitude in meters.
        """
        print(f"Moving to ({latitude}, {longitude}, {altitude})...")
        self.connection.mav.mission_item_int_send(
            self.connection.target_system,
            self.connection.target_component,
            0,  # Sequence
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            2,  # Current/Autocontinue
            0, 0, 0, 0, 0, 0,
            int(latitude * 1e7),
            int(longitude * 1e7),
            altitude
        )
        time.sleep(5)  # Allow time for the drone to reach the waypoint

    def capture_image(self):
        """
        Sends the MAV_CMD_IMAGE_START_CAPTURE command to trigger image capture.
        """
        print("Capturing image using MAV_CMD_IMAGE_START_CAPTURE...")

        # Command the drone to capture an image (camera_id = 0, capture_interval = 0 for one-shot capture)
        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_IMAGE_START_CAPTURE,
            0,    # Confirmation
            0,    # Camera ID (use 0 if there is only one camera)
            1,    # Number of images to capture (1 image)
            1,    # Interval between captures in seconds (1 for continuous capture, or 0 for one-shot)
            0, 0, 0, 0  # Unused parameters
        )
        time.sleep(1)  # Simulate time for capturing

        # Simulated placeholder for image data (replace with actual camera data)
        image_data = {"image": "image_data_placeholder"}  

        # Send the image to the API
        response = requests.post(self.api_url, json=image_data)
        if response.status_code == 200:
            print("Image sent successfully.")
        else:
            print(f"Failed to send image: {response.status_code}")

    def generate_snake_waypoints(self, start_lat, start_lon, end_lat, end_lon, altitude, spacing=0.0001):
        """
        Generates waypoints in a snake pattern to cover the entire area between the given coordinates.
        :param start_lat: Starting latitude.
        :param start_lon: Starting longitude.
        :param end_lat: Ending latitude.
        :param end_lon: Ending longitude.
        :param altitude: Altitude at which the drone should fly.
        :param spacing: Distance between each pass in degrees (adjust for resolution).
        :return: List of waypoints (latitude, longitude, altitude).
        """
        waypoints = []
        lat_direction = 1 if end_lat > start_lat else -1
        lon_direction = 1 if end_lon > start_lon else -1

        current_lat = start_lat
        snake_direction = lon_direction  # Start by moving east/west

        while abs(current_lat - end_lat) > spacing:
            # Move in a horizontal line (east/west)
            current_lon = start_lon if snake_direction == lon_direction else end_lon
            waypoints.append((current_lat, current_lon, altitude))

            # After reaching the edge, move north/south (vertical step)
            current_lat += spacing * lat_direction

            # Change direction for the next pass
            snake_direction *= -1

        return waypoints

    def snake_pattern(self, waypoints):
        """
        Follows the snake-like pattern and captures images.
        :param waypoints: List of GPS coordinates (latitude, longitude, altitude).
        """
        for waypoint in waypoints:
            lat, lon, alt = waypoint
            self.move_to(lat, lon, alt)
            self.capture_image()

    def return_to_home(self):
        """
        Commands the drone to return to its home position.
        """
        print("Returning to home...")
        self.set_mode("RTL")
        time.sleep(10)

    def execute_mission(self, start_lat, start_lon, end_lat, end_lon, altitude):
        """
        Executes the full mission: takeoff, follow waypoints, and return to home.
        :param start_lat: Starting latitude of the area.
        :param start_lon: Starting longitude of the area.
        :param end_lat: Ending latitude of the area.
        :param end_lon: Ending longitude of the area.
        :param altitude: Altitude at which the drone should fly.
        """
        # Take off to the specified altitude
        self.arm_and_takeoff(altitude)

        # Generate snake waypoints to cover the area
        waypoints = self.generate_snake_waypoints(start_lat, start_lon, end_lat, end_lon, altitude)

        # Follow the snake pattern
        self.snake_pattern(waypoints)

        # Return to the home location
        self.return_to_home()


if __name__ == "__main__":
    # Connection string to the drone
    connection_string = 'tcp:127.0.0.1:5760'

    # URL of the API to send captured images to
    api_url = 'http://api.ecomobile.uz/api/upload'

    # Define the area to cover (start and end latitudes and longitudes)
    start_latitude = 37.7749
    start_longitude = -122.4194
    end_latitude = 37.7849
    end_longitude = -122.4094

    # Altitude in meters
    altitude = 20

    # Create a drone controller instance
    drone = DroneController(connection_string, api_url)

    # Execute the mission
    drone.execute_mission(start_latitude, start_longitude, end_latitude, end_longitude, altitude)