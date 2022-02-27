# Sign-Language-Recognition
This code translates American Sign Language letters into English letters with maximum accuracy.

Libraries used in the Code:

Tkinter/tk - to create the user interface (available in Python itself)

os - for the User Manual to be opened when the button is clicked (available in Python itself)

cv2/opencv - to draw the hand structure, and to give the coordinates of each finger in order to recognize the letter (have to download externally)

Algorithms:

Based on the letters, letters were classified into groups - letters which looked similar/had same placements for the fingers were coded with one algorithm

Letters which had the same fingers closed/opened were coded with one algorithm

Letters which were in the ‘x’ axis, ‘y’ axis and ‘z’ axis were coded with different algorithms respectively

Approach:

Finger and palm positions were tracked by their ‘x’ and ‘y’ coordinates

Depending on the value of the coordinates, it was determined wether the finger was opened or closed

Using the same algorithm, it was determined how many of the fingers were closed/opened

For letters which have all fingers closed/opened, the thumb’s ‘x’ and ‘y’ coordinates were taken into account to differentiate between similar letters



App User Interface:
![image](https://user-images.githubusercontent.com/65762697/155881080-35f7cee3-0661-407d-bf2b-34f2733d0d13.png)
![hand tracking](https://user-images.githubusercontent.com/65762697/155881210-61db0d58-6866-4858-a5b2-77922d7d5560.png)


Detect Button - Opens computer webcam to start translating ASL letters

User Manual Button - Opens the User Manual which elaborates on the inner workings of the App
