\* Volume PredictionMay 2020 *\
Maximize
OBJ: 100 q0 + 133.333333333 q1 + 116.666666667 q3 + 125 q4 + 49.3333333333 q5
 + 900 q6
Subject To
_C1: q0 + q1 + q2 + q3 + q4 + q5 + q6 = 100
_C2: q0 >= 4
_C3: q1 >= 4
_C4: q2 = 0
_C5: q3 >= 4
_C6: q4 >= 4
_C7: q5 >= 4
_C8: q6 >= 4
Bounds
q0 <= 50
q1 <= 50
q2 <= 50
q3 <= 50
q4 <= 50
q5 <= 50
q6 <= 50
End
#TEST