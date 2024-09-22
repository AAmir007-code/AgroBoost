# AgroBoost

![title poster](assets/poster.png)

AgroBoost is an innovative solution designed to enhance agricultural productivity through advanced analytics and
automation. It leverages cutting-edge technologies to provide farmers with actionable insights, optimize resource
utilization, and increase crop yields.

## Table of Contents

- [Features](#features)
- [Criteria checklist](#criteria-checklist)
    - [Code Quality](#code-quality)
    - [Performance & Efficiency](#performance--efficiency)
    - [Scalability](#scalability)
    - [Architecture & Code Design](#architecture--code-design)
    - [Documentation](#documentation)
        - [Project Structure](#project-structure)
        - [Drone Controller Documentation](#drone-controller-documentation)
    - [Training Model for Segmentation](#training-model-for-segmentation)
- [Demo](#demo)
- [Team members](#team-members)


## Features

- **Predictive Analytics:** Utilize machine learning models to forecast crop yields and pest infestations.
- **Data Visualization:** Interactive dashboards for visualizing agricultural data trends.
- **User-Friendly Interface:** An intuitive web application that makes data accessible for all users.
- **Customizable Reports:** Generate tailored reports to meet specific agricultural needs.


## Criteria checklist
### Code Quality
- **Technologies:** Python, Vue.js
- **Frameworks:** Django for backend, FastAPI for APIs, MinIO for object storage
- **Best Practices:** Adheres to modular programming, separation of concerns, clear folder structures, and Docker Compose for consistent environment setup. While the project exhibits clean code, further improvements could include comprehensive testing (unit and integration) and thorough documentation to enhance maintainability and collaboration.


### Performance & Efficiency

-	**Optimizations:** Docker-based containerization ensures efficient resource usage. FastAPI enhances API performance due to its asynchronous nature. The drone captures images at 1 frame per second, ensuring resource-efficient data acquisition. MinIO for object storage ensures optimized file management, and asynchronous API operations minimize latency during large-scale data transfers.
-	**Areas for Improvement:** Profiling for specific bottlenecks in image processing could yield further optimizations.

### Scalability
-	**Infrastructure:** The project leverages Docker Compose, enabling easy scaling of services across multiple containers. MinIO provides scalable object storage, while FastAPI ensures efficient handling of a large number of API requests. These components, combined with a modular architecture, allow for the system to scale horizontally with minimal refactoring.
-	**Future Enhancements:** Introduction of load balancing, distributed processing (e.g., using Kubernetes), and optimized database management can improve scalability further as the project grows in complexity and usage.

### Architecture & Code Design
- The project architecture is [here](https://miro.com/app/board/uXjVLcIyaoo=/?share_link_id=287040409386).
-	**Design Patterns:** The project follows the MVC pattern, separating concerns between models, views, and controllers. The use of FastAPI for APIs ensures a clean separation between the frontend and backend, enhancing modularity and maintainability.
-	**Code Design:** The codebase is well-structured, with clear folder organization and modular components. The use of Django and FastAPI allows for easy extension and modification of features. However, further documentation and comments could enhance code readability and maintainability.

### Documentation
   - Documentation is available in the [docs](docs) folder.
   - **Project structure:** There are a several part of the project:
   - **Drone Controller:** This part of the project controls the drone using the **pymavlink** library, executing a sequence of operations including takeoff, movement, image capture, and returning to home. The `DroneController` class encapsulates this logic, allowing interaction with the drone through MAVLink protocol and API communication for image transmission.
    
   - **Image Processing:** This part of the project processes images captured by the drone, detecting and classifying objects of interest. The meta SAM(semantic annotation module) module uses machine learning models to analyze images and generate annotations. The `ImageProcessor` class encapsulates this logic, allowing interaction with the image processing pipeline.

   - **Data Analysis:** This part of the project analyzes agricultural data to provide insights and predictions for farmers. The `DataAnalyzer` class uses machine learning models to forecast crop yields and pest infestations based on historical data. The `DataAnalyzer` class encapsulates this logic, allowing interaction with the data analysis pipeline.

   - **Dashboard:** This part of the project provides a user-friendly interface for farmers to visualize agricultural data trends and generate reports. The `Dashboard` class uses the **Vue.js** framework to create interactive dashboards and reports. The `Dashboard` class encapsulates this logic, allowing interaction with the dashboard interface.

#### Project Structure
```
AgroBoost/
│
├── api/                      # Image Processing
│
├─ docs/                      # Documentation
│
├── drone-control/            # Drone Controller
│
├── frontend/                 # Dashboard
│
├── vision/                   # Data Analysis
│
├── docker-compose.yml       # Docker Compose configuration file
│
└── README.md                # Documentation and setup guide
```

#### Drone Controller Documentation
This part of the project controls the drone using the **pymavlink** library, executing a sequence of operations including takeoff, movement, image capture, and returning to home. The `DroneController` class encapsulates this logic, allowing interaction with the drone through MAVLink protocol and API communication for image transmission.

**Key Functions**:
- `arm_and_takeoff`: Arms the drone and ascends to a target altitude.
- `move_to`: Moves the drone to specified GPS coordinates.
- `capture_image`: Triggers image capture and sends the image data to a designated API.
- `generate_snake_waypoints`: Generates waypoints in a snake-like pattern to cover a defined area.
- `snake_pattern`: Executes the snake pattern and captures images at each waypoint.
- `return_to_home`: Commands the drone to return to its home position.
- `execute_mission`: Manages the full mission, from takeoff through waypoint navigation to return.

**Example Usage**:
```python
drone = DroneController(connection_string='tcp:127.0.0.1:5760', api_url='http://api.ecomobile.uz/api/upload')
drone.execute_mission(start_lat=37.7749, start_lon=-122.4194, end_lat=37.7849, end_lon=-122.4094, altitude=20)
```

### Training Model for Segmentation

The training process for the **Segment Anything** model focuses on fine-tuning a pre-trained segmentation model with domain-specific data (e.g., agricultural field images). This ensures accurate segmentation of crops, plants, and other objects.

**Steps for Training**:
1. **Dataset Preparation**: Organize labeled image data for training.
2. **Model Selection**: Use a pre-trained segmentation model like SAM (Segment Anything Model).
3. **Fine-Tuning**: Adjust model parameters using your custom dataset to improve segmentation accuracy.

**Example**:
```python
from segment_anything import SamTrainer
trainer = SamTrainer(model_path="path/to/model", data_path="path/to/dataset")
trainer.train()
```

**Output**: A fine-tuned segmentation model specific to your use case.

## Demo

[![AgroBoost Demo](https://img.youtube.com/vi/p3eykX59K-4/0.jpg)](https://www.youtube.com/watch?v=p3eykX59K-4)

*Click the image above to watch the demo video.*
* https://ecomobile.uz/ - The project is deployed on this domain.

## Team members

- [Bekhruz Nutfilloev]()
- [Amirbek Aslonov]()
- [Humoyun Ochilov]()
- [Iskandar Hamroyev]()