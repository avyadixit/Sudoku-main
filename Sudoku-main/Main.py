import os
import cv2
import numpy as np

import Extract_Digits
import Predict_Digits
import Solve_Sudoku

Path = 'Sudoku'

if not os.path.isdir(Path):
    print("Sudoku folder not found")
    exit()

Images = sorted(
    [img for img in os.listdir(Path) if img.lower().endswith(('.png', '.jpg', '.jpeg'))],
    key=lambda x: int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else 0
)

if not os.path.isdir('Solution'):
    os.mkdir('Solution')

for Image_Name in Images:
    Image_Path = os.path.join(Path, Image_Name)
    Image = cv2.imread(Image_Path)

    if Image is None:
        print(f"Failed to load {Image_Name}")
        continue

    Image_List, Centres = Extract_Digits.Extract(Image)

    if Image_List and Centres:
        Grid = Predict_Digits.Predict(Image_List)

        print(f"{Image_Name} Grid:")
        for row in Grid:
            print(row)

        Solution, Empty_Cells = Solve_Sudoku.Solve(Grid)

        if Solution:
            for i, j in Empty_Cells:
                idx = i * 9 + j
                if idx < len(Centres):
                    origin = (Centres[idx][0] - 15, Centres[idx][1] + 15)
                    cv2.putText(Image, str(Solution[i][j]), origin,
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 100, 0), 3, cv2.LINE_AA)

            cv2.imwrite(os.path.join('Solution', Image_Name), Image)
            cv2.imshow('Solution', Image)
            cv2.waitKey(0)
        else:
            print(f'Sudoku Invalid Or Recognized Incorrectly In {Image_Name}!')
    else:
        print(f'Sudoku Recognition Failed In {Image_Name}!')

cv2.destroyAllWindows()