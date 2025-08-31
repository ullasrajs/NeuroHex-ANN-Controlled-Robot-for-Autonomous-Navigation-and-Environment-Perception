# NeuroHex-ANN-Controlled-Robot-for-Autonomous-Navigation-and-Environment-Perception

This is my Final year project in my UG from RNSIT, Bangalore. The project is based on implementing Object detection Model on a SBC Raspberry Pi 3B+ and also controlling the robot which is a 6WD Vehicle through real world. The uniqueness of this project is implementing an OBject detection model on Raspberry Pi 3B+ Board which hasn't been tried before.
This project, NeuroHex, is an autonomous robot that leverages an Artificial Neural Network (ANN) for intelligent navigation and environment perception. Designed to handle complex and uneven terrains, the robot uses a fusion of hardware and software components to perceive its surroundings, detect objects, and navigate autonomously.

## Software and Hardware Requirements 
Both hardware and software requirements are equally essential for reaching the aim of the project. A good hardware is what which is going to drive the necessary tools and applications of software meet the required result metrics.

### Hardware Setup
First, we are going to setup our hardware which is foundation. The hardware setup includes both mechanical designing of project and also electronic setup. The mechanical design was done using Solidedge Software which is a Mechanical CAD. As the idea was to build a 6WD robot chassis, we created a design aligned with it. The design file was later given to a workshop where it was built by a Fabricator. It was made from Industrial grade steel. The 4 wheels front and back were powered by 10 RPM Geared DC Motor. These motors needed 12V 1.6Amp power. It was provided by a Lipo Battery 12V 1.6A.

The CAD modelling can be seen below: 

<div align="center">
  <img src="./Images/CAD_Modelling_page-0001.jpg" alt="CAD Modelling of the Robot Chassis" width="400">
  <img src="Images/CAD_Modelling_with_Dimentions_page-0001.jpg" alt="CAD Modelling of the Robot Chassis" width="400">
</div>
<div align="center">
<b>CAD Modelling of the Robot Chassis and Dimensions of the Components</b>
</div>

Once the Robot chassis is fabricated, I and my team have made the necessary connections as shown in the image below : 
<div align="center">
<img src="Images/Circuit_Connection_Image_page-0001.jpg" alt="Circuit Connect on Robot Chassis" width="400">
</div>
<div align="center">
<b>Circuit Connect on Robot Chassis</b>
</div>


We have used the following components :

1. Raspberry Pi 3B+ and a 16GB MicroSD card as OS for the same.

2. 4 Ultrasonic Sensors -> 2 each at 2 corners (facing forward and facing diagonal)
     
3. 4 10 ROM DC Geared Motors
    
4. 2 2WD DC Motor Drivers L298N
     
5. Raspberry Pi Camera Module 3
   
6. Power source for Pi (Phone Power bank)
     
7. Wires and Data/Power Cable
     
8. LIPO Battery 1.3A 12V (comes along with a charger)

   Once the connection of above components are done. The hardware setup is done and lets move to the software setup. The images of the same can be viewed below:
<div align="center">
<img src="Images/Robot_Pic1.jpg" alt="Front View Connection of Circuit as per Circuit connection image(Note: A peakhole has been made for the camera lens) " width="400">
</div>
<div align="center">
<img src="Images/Robot_Pic2.jpg" alt="Top View Connection of Circuit as per Circuit connection image(Note: A peakhole has been made for the camera lens) " width="400">
</div>
<div align="center">
<b>Front and Top View Connection of Circuit as per Circuit connection image(Note: A peakhole has been made for the camera lens)</b>
</div>


### Software Setup 
1. Raspberry Pi's OS :
   The OS used for the entire project was 32Bit OS Debian Bookworm with Desktop. The OS is loaded in the SD card which was a 16GB Samsung MicroSD card. It was first formatted using [SD Card Formatter](https://www.sdcard.org/downloads/formatter/) You can dowanload the software based on your OS used in PC.
<div align="center">
<img src="Images/SD_card_formatted.jpg" alt="" width="400">
</div>
<div align="center">
<b>SD card formatted </b>
</div>                 
    Once formating the SD card is done, the MicroSD card is loaded with ISO image. It can be done easily using 
    [Raspberry Pi Imager](https://www.raspberrypi.com/software/) and choosing the OS. 
    
    
    
   


