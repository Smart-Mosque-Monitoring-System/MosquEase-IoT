<p align="center">
  Find Mosque Easily!<p>
  </p>
<p align="center">
  <a href ="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License - GPLv3"></a>
  <img src="https://img.shields.io/badge/status-alpha-orange" alt="Status - Alpha"></a>
</p>

# MosquEase
A service to help find the nearest and most comfortable mosque for you.

## Table of Contents
- [How do I use it?](#howtouse)
- [Tech stack](#techstack)
- [License](#license)

## How do I use it?
<a name="howtouse"></a>
Currently, MosquEase is in alpha development and only supports one mosque location. Trial site will be announced soon. Follow these steps to run it locally.
Make sure your IoT devices are already connected to WiFi. Here's how you can run the service by yourself.

Clone this repository by using this command:

    git clone https://github.com/Smart-Mosque-Monitoring-System/MosquEase-IoT.git

Go to the repository location:

    cd MosquEase-IoT

Create a virtual environment:

    python -m venv mosquease_venv

Activate the virtual environment:

    #On Windows
    mosquease_venv\Scripts\activate

    #On macOS and Linux
    source mosquease_venv/bin/activate

Go to the directory where dependency list is located:

    cd fastapi-yolo-app

Install all the dependencies:

    pip install -r requirements.txt

After the installation is done, upload the arduino file to your microcontroller first using Arduino IDE or any other IDE you want.
Then, make sure that the IoT devices are already connected to the same network as your laptop.
Don't forget to edit the url of your IoT web servers in main.py.

Run the project:

    uvicorn main:app --reload

After the process is done, you can run the service. Make sure you have the correct enviroment secrets (like API Key).

## Tech stack
<a name="techstack"></a>
- **Ultralytics**: The core library for image processing.
- **Supabase**: Handles data storage and provides API service (BaaS).
- **Python**: Handles head count prediction using pre-trained YOLOv8 model, also acts as the API for the image procesing.
- **ESP32-CAM**: Handles image and data capture along with other ESP32's compatible sensors like OV2640 and BME280.

## License
<a name="license"></a>
This project is licensed under the [GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0) (GPLv3).