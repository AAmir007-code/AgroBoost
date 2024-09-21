# sim_vehicle.py -v ArduCopter --console --map

import time
from pymavlink import mavutil

class DroneTest:
    def __init__(self, connection_string):
        # Connect to the SITL drone
        self.connection = mavutil.mavlink_connection(connection_string)
        self.connection.wait_heartbeat()
        print("Connected to the drone (SITL)!")

    def arm_and_takeoff(self, target_altitude):
        """
        Arms the drone and takes off to the target altitude.
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
        time.sleep(5)  # Wait for the drone to reach the waypoint

    def capture_image(self):
        """
        Sends the MAV_CMD_IMAGE_START_CAPTURE command to trigger image capture.
        """
        print("Simulating image capture using MAV_CMD_IMAGE_START_CAPTURE...")

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
        print("Image capture simulated.")

    def return_to_home(self):
        """
        Commands the drone to return to its home position.
        """
        print("Returning to home...")
        self.set_mode("RTL")
        time.sleep(10)

if __name__ == "__main__":
    # Connection string for SITL (adjust if needed)
    connection_string = 'tcp:127.0.0.1:5760'

    # Create a test drone instance
    drone = DroneTest(connection_string)

    # Test scenario: take off, move, capture image, return home
    altitude = 10  # Test with a safe altitude in meters

    # Arm and takeoff
    drone.arm_and_takeoff(altitude)

    # Move to a new GPS location (simulated)
    test_lat = 47.397742  # Example lat, you can adjust
    test_lon = 8.545593   # Example lon, you can adjust
    drone.move_to(test_lat, test_lon, altitude)

    # Capture image
    drone.capture_image()

    # Return to home
    drone.return_to_home()