import tkinter as tk
import cv2
import os

#creating the window of the user interface
win = tk.Tk()
win.title('Sign Language Recognition')
win.geometry('700x500')

#creating the text of the user interface
canvas = tk.Canvas(win, width = 1000, height = 750)
canvas.create_text(350, 50, text = 'Welcome to Sign Language Recognition!', fill = 'black')
canvas.create_text(350, 70, text = 'Please click the Detect Button to start translating.', fill = 'black')
canvas.create_text(350, 90, text = 'Kindly note that sign language numbers cannot be recognized.', fill = 'black')
canvas.create_text(350, 110, text = 'Please click the User Manual Button to learn how to operate the program.', fill = 'black')


canvas.pack()


#contains the code for the recognition of ASL letters
def clicked():
    import cv2
    import mediapipe as mp

    #drawing the hand landmarks
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    #storing coordinates of the fingertips in a list and separately
    finger_tips = [8, 12, 16, 20]
    index_tip = 8
    middle_tip = 12
    ring_tip = 16
    pinky_tip = 20
    thumb_tip = 4

    while True:

        #processing the webcam image
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        results = hands.process(img)

        #appending the sensed coordinates of the fingers in various lists
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmark.landmark):
                    lm_list.append(lm)

                finger_fold_status = []
                finger_fold_GH = []
                finger_above_palm = []
                thumb_between = []

                for tip in finger_tips:
                    x, y = int(lm_list[tip].x*w), int(lm_list[tip].y*h)

                    #drawing circles at the finger tips
                    cv2.circle(img, (x, y), 15, (255, 0, 0), cv2.FILLED)

                    #for determining if the fingers are above the palm
                    if lm_list[tip].y > lm_list[tip - 3].y:
                        finger_fold_status.append(True)
                    else:
                        finger_fold_status.append(False)
                        
                    #for determining if the fingers are fully opened and straight
                    if lm_list[tip].y > lm_list[tip - 2].y:
                        finger_above_palm.append(True)
                    else:
                        finger_above_palm.append(False)

                    #for determining if the fingers are fully opened and straight when the hand is sideways
                    if lm_list[tip].x > lm_list[tip - 3].x:
                        finger_fold_GH.append(True)
                    else:
                        finger_fold_GH.append(False)
                        
                    #for determining if the fist is fully closed
                    if lm_list[tip].y <= lm_list[tip - 3].y:
                        thumb_between.append(True)
                    else:
                        thumb_between.append(False)
                    
                
                #this is for A, S, M, N
                if all(finger_fold_status): 
                    if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x <= lm_list[thumb_tip - 2].x:
                        cv2.putText(img, 'A', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                 
                    if lm_list[thumb_tip].x <= lm_list[ring_tip].x and lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x:
                        cv2.putText(img, 'S', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                    if lm_list[thumb_tip].x > lm_list[pinky_tip].x:
                        cv2.putText(img, 'M', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                    if lm_list[thumb_tip].x < lm_list[pinky_tip].x and lm_list[thumb_tip].x > lm_list[ring_tip].x:
                        cv2.putText(img, 'N', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)






                #this is for E, T      
                if all(finger_above_palm):
                    if lm_list[thumb_tip].y >= lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x > lm_list[thumb_tip - 2].x:
                        cv2.putText(img, 'E', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                    
                if all(finger_above_palm) and any(finger_fold_status) == False:
                    if lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x > lm_list[thumb_tip - 2].x and lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y:
                        cv2.putText(img, 'T', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    





                    
                #this is for B
                if finger_fold_status[0] == False and finger_fold_status[1] == False and finger_fold_status[2] == False and finger_fold_status[3] == False and all(thumb_between) and any(finger_above_palm) == False:
                    if lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x > lm_list[thumb_tip - 2].x:
                        cv2.putText(img, 'B', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)



                #this is for Y, I
                if finger_fold_status[0] == True and finger_fold_status[1] == True and finger_fold_status[2] == True:
                    if lm_list[pinky_tip].y < lm_list[pinky_tip - 1].y < lm_list[pinky_tip - 2].y and lm_list[pinky_tip].x > lm_list[pinky_tip - 1].x > lm_list[pinky_tip - 2].x:
                        if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x < lm_list[thumb_tip - 2].x:
                    
                            cv2.putText(img, 'Y', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                        if lm_list[thumb_tip].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x >= lm_list[thumb_tip - 2].x:
                            cv2.putText(img, 'I', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)




                #this is for L, D, X
                if finger_fold_status[1] == True and finger_fold_status[2] == True and finger_fold_status[3] == True:  
                    if lm_list[index_tip].y < lm_list[index_tip - 1].y < lm_list[index_tip - 2].y and lm_list[index_tip].x >= lm_list[index_tip - 2].x:
                    
                        if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x < lm_list[thumb_tip - 2].x:
                            cv2.putText(img, 'L', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                    if lm_list[index_tip].y < lm_list[index_tip - 1].y < lm_list[index_tip - 2].y and lm_list[index_tip].x < lm_list[index_tip - 2].x:
                        if lm_list[thumb_tip].y <= lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x > lm_list[thumb_tip - 2].x:
                            cv2.putText(img, 'D', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                    if lm_list[index_tip].y <= lm_list[index_tip - 2].y and lm_list[index_tip].x >= lm_list[index_tip - 2].x:
                        if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x >= lm_list[thumb_tip - 1].x >= lm_list[thumb_tip - 2].x:
                            cv2.putText(img, 'X', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)






                #this is for G, H
                if finger_fold_GH[2] == True and finger_fold_GH[3] == True:         
                    if lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x < lm_list[thumb_tip - 2].x and lm_list[thumb_tip].y < lm_list[thumb_tip - 2].y:
                        if finger_fold_GH[1] == True and finger_fold_GH[0] == False:
                            cv2.putText(img, 'G', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        
                        if finger_fold_GH[1] == False and finger_fold_GH[0] == False:
                            cv2.putText(img, 'H', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


                #this is for V, U, R, K
                if finger_fold_status[2] == True and finger_fold_status[3] == True and finger_fold_status[0] == False and finger_fold_status[1] == False:   
                    if lm_list[thumb_tip].y <= lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x > lm_list[thumb_tip - 2].x:
                        if lm_list[middle_tip].y < lm_list[middle_tip - 1].y < lm_list[middle_tip - 2].y and lm_list[middle_tip].x > lm_list[middle_tip - 1].x > lm_list[middle_tip - 2].x:
                            if lm_list[index_tip].y < lm_list[index_tip - 1].y < lm_list[index_tip - 2].y and lm_list[index_tip].x < lm_list[index_tip - 1].x < lm_list[index_tip - 2].x:
                                cv2.putText(img, 'V', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                            if lm_list[index_tip].y < lm_list[index_tip - 1].y < lm_list[index_tip - 2].y and lm_list[index_tip].x > lm_list[index_tip - 1].x > lm_list[index_tip - 2].x:
                                cv2.putText(img, 'U', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


                        else:
                            cv2.putText(img, 'R', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


                    if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x < lm_list[thumb_tip - 2].x:
                        if lm_list[middle_tip].y < lm_list[middle_tip - 1].y < lm_list[middle_tip - 2].y and lm_list[middle_tip].x > lm_list[middle_tip - 1].x > lm_list[middle_tip - 2].x:
                            if lm_list[index_tip].y < lm_list[index_tip - 1].y < lm_list[index_tip - 2].y and lm_list[index_tip].x < lm_list[index_tip - 1].x < lm_list[index_tip - 2].x:
                                cv2.putText(img, 'K', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)



                #this is for F
                if finger_fold_status[1] == False and finger_fold_status[2] == False and finger_fold_status[3] == False:
                    if lm_list[index_tip].y > lm_list[index_tip - 1].y >= lm_list[index_tip - 2].y:
                        if lm_list[middle_tip].y < lm_list[middle_tip - 1].y < lm_list[middle_tip - 2].y:
                            cv2.putText(img, 'F', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)



                #this is for W
                if finger_fold_status[0] == False and finger_fold_status[1] == False and finger_fold_status[2] == False and finger_fold_status[3] == True:
                    cv2.putText(img, 'W', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            
                #this is for Q
                if finger_fold_GH[0] == False and finger_fold_GH[1] == True and finger_fold_GH[2] == True and finger_fold_GH[3] == True:
                    if lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y:
                        cv2.putText(img, 'Q', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)



                    
                #this is for P
                if finger_fold_GH[0] == False and finger_fold_GH[1] == False and finger_fold_GH[2] == True and finger_fold_GH[3] == True:
                    if lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y:
                        cv2.putText(img, 'P', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)




                #this is for C, O
                if finger_fold_GH[0] == False and finger_fold_GH[1] == False and finger_fold_GH[2] == False and finger_fold_GH[3] == False:
                    if lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x < lm_list[thumb_tip - 2].x:
                        if lm_list[pinky_tip].y < lm_list[pinky_tip - 1].y < lm_list[pinky_tip - 2].y:
                            cv2.putText(img, 'C', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        if lm_list[middle_tip].y > lm_list[middle_tip - 1].y > lm_list[middle_tip - 2].y:
                            cv2.putText(img, 'O', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)










                #for drawing the connections between the hand landmarks
                mp_draw.draw_landmarks(img, hand_landmark,
                                       mp_hands.HAND_CONNECTIONS,
                                       mp_draw.DrawingSpec((0, 0, 255), 2, 2),
                                       mp_draw.DrawingSpec((0, 255, 0), 4, 2))
                
        #for naming the webcam window
        cv2.imshow('hand tracking', img)

        #when 'q' key is pressed the webcam window closes
        if cv2.waitKey(1) == ord('q'):
            break


#contains code for opening the user manual
def user_manual():
    path = 'C:/Users/Kedar/OneDrive/Documents/Iras File/Python AI/AI-App User Manual.pdf'
    os.startfile(path)


#creating the button on the user interface
#the button opens the webcam when clicked and allows the ASL recognition code to start
btn = tk.Button(win, text = 'Detect', width = 10, height = 2, command = clicked)
  
btn.place(x=300, y=150)


#creating the button on the user interface
#the button opens the user manual when clicked
bt = tk.Button(win, text = 'User Manual', width = 20, height = 2, command = user_manual)

bt.place(x=265, y=200)





win.mainloop()
