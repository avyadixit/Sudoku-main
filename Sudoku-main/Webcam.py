import cv2
import numpy as np

import Extract_Digits
import Predict_Digits
import Solve_Sudoku

Solved = False
Solution = None
Empty_Cells = []

# Use local webcam instead of IP camera
cap = cv2.VideoCapture(0)  # 0 is default webcam

if not cap.isOpened():
    print("ERROR: Could not open local webcam.")
    exit()

while True:
    ret, Image = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    Image = Image[200:1000, 200:1000]
    display = Image.copy()

    Image_List, Centres = Extract_Digits.Extract(Image)

    if not Image_List or not Centres:
        Solved = False
        Empty_Cells = []
    elif not Solved:
        Grid = Predict_Digits.Predict(Image_List)
        Solution, Empty_Cells = Solve_Sudoku.Solve(Grid)

        if Solution:
            Solved = True
        else:
            Empty_Cells = []

    if Solved and Solution:
        for i, j in Empty_Cells:
            idx = i * 9 + j
            if idx < len(Centres):
                origin = (Centres[idx][0] - 15, Centres[idx][1] + 15)
                cv2.putText(display, str(Solution[i][j]), origin,
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Live Video Feed', display)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()