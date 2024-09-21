#!/bin/bash

# Start SITL (Software In The Loop) simulation for ArduCopter with a console and map
echo "Starting SITL for ArduCopter..."
sim_vehicle.py -v ArduCopter --console --map

# Ensure SITL runs on localhost (adjust ports if necessary)
echo "SITL started on tcp:127.0.0.1:5760"