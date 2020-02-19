========Robot Arm Tennis Ball Catcher==============

Names:
William Ness - wine1039@colorado.edu
Nasurudin Furi - nafu7706@colorad.edu
Jessica Sanborn - jesa0696@colorado.edu 
Alexander Haynie - alha0195@colorado.edu
Abstract
In our project we plan to program the Rethink Robotics Sawyer Arm to catch a tennis ball that is thrown towards it. We plan to have the robot hold a bucket to catch the ball. The ball will be thrown from the same distance with varying degrees of velocity and ending location. Should it be too easy for the robot to catch the ball with a bucket, we will decrease the size of the bucket.
Equipment
Rethink Robotics Sawyer Arm
Motion Capture
Deliverables & Implementation Plans
Track ball/vision system - Lead: Jessica & Nasurudin, Deadline: Dec 4th
Decide how to utilize camera to keep track of x,y,z coordinates
Use motion capture to get ball position
Be able to identify ball with camera
Use size of ball to see how close the ball is to the robot
Implementation Plan
First figure out how to use the motion capture cameras and best placement for it. We will then find a method to identify the ball that needs to be caught through making it recognize the image or color of the ball. Using information gained from the camera, we will get the ball’s position in the robot’s worldview so it is easier to give the information to the robot to know where the ball is for it to catch.
Math for where the ball will land - Lead: Alex, Deadline: Nov 13th
Establish knowns/unknowns for physics equations, and which we get from our sensors
Write down necessary physics equations
Convert to code
Implementation Plan
Calculate velocity of x and y of the tennis ball
Calculate area of bucket opening
Calculate the y when x equals zero
Calculate where the center of the bucket needs to be.
Convert calculations into code
Implementation notes
We implemented the correct physics equations
We calculated if a ball would land in a reachable zone by having a set X where the bot would catch at, and then defining an acceptable Y and Z range. The robot can catch anywhere in this range (you can see this range visualized in our video when it shows the rviz panel)
This worked very well when the mocap was giving us consistent data. What was nice, is as long as the mocap captured the start of the throw smoothly, it usually ends up doing well even if the second half of the throw isn’t caught. If we wanted to take this project further we’d probably print a mocap dot holder that we can attach to the tennis ball (instead of tape), and as well use a mocap system not optimized for low robots (since we have to throw the ball through the middle of the room but the mocap works best on the bottom couple of feet closest to the floor).
Catch ball in bucket/hand - Lead: Will, Deadline: Dec 4th 
Create inverse kinematics to move arm to any position
Integrate with ball system
Implementation Plan
Our goal for this step is to create an inverse kinematics system where we can give the robot arm the coordinates of where the ball will land (x, y), and it will move there. Once this is done, all we need to do is to integrate it with the tracking system which will be outputting where it thinks the ball will land for each loop. The arm will be updated as the ball gets closer and closer.
Implementation notes
This step was made pretty easy via the easy to use API we used for the Sawyer arm.
Had to add in extra logic to convert coordinates in mocap space to arm coordinates. We did this by placing the arm origin set position in the center of the reachable zone, and then using differences from the center of the reachable zone in mocap space to convert coordinates relative to the origin position of the robot arm.
We also created a proof of concept program that we used to show that the robot could successfully move to any point on the XYZ plane defined as the catch region. We confirmed that arm can move along the YZ square while remaining at X.
