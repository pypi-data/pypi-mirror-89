
def set_matrix():
    rows=int(input("Enter no of Rows: "))
    columns=int(input("Enter no of Columns: "))
    matrix=[]
    try:
        k=1
        while k<=rows:
            string=input(f'Eneter Row items for Row {k}: ')
            mat=string.split(' ')
            if len(mat)!=columns:
               raise "Column condition not satisfied"
            matrix.append(mat)
            k+=1
    except Exception:
        print("Error Occured in Reading Column")

def show():
    print("=>Input Matrics is:")
    for j in range(len(matrix)): 
        for i in range(columns):
            print(matrix[j][i],end=" ")
            if (i==(columns-1)):
                print()

def Det():
    if rows==columns:
        if rows==2:
            det=(int(matrix[0][0])*int(matrix[1][1])-int(matrix[0][1])*int(matrix[1][0]))
            print("Determinant of given Matrics is: %d" %det)
        elif rows==3:
            pass
        else:
            print("Not Build Yet !!!")
    else:
        print("Can't Perform Determinant of a Non-Square Matrics:")
