def get_status(board):
    left = []
    right = []
    first = []
    second = []
    third = []
    raw = 1
    for i in range(len(board)):
        combination = []
        for j in range(len(board[i])):
            combination.append(board[i][j])
            if j == 0:
                first.append(board[i][j])
            elif j == 1:
                second.append(board[i][j])
            else:
                third.append(board[i][j])

            if len(combination) == 3:
                if raw == 1:
                    left.append(combination[0])
                    right.append(combination[2])
                    raw += 1
                elif raw == 2:
                    left.append(combination[1])
                    right.append(combination[1])
                    raw += 1
                else:
                    left.append(combination[2])
                    right.append(combination[0])

                if combination[0] != "" and combination[0] == combination[1] == combination[2]:
                    return combination[0]
    if left[0] != "" and left[0] == left[1] == left[2]:
        return left[0]
    if right[0] != "" and right[0] == right[1] == right[2]:
        return right[0]
    if first[0] != "" and first[0] == first[1] == first[2]:
        return first[0]
    if second[0] != "" and second[0] == second[1] == second[2]:
        return second[0]
    if third[0] != "" and third[0] == third[1] == third[2]:
        return third[0]
    if " " in left or " " in right or " " in first or " " in second or " " in third:
        print(second)
        return "continue"
    return "draw"


print(get_status([['o', ' ', 'x'],
                  ['x', 'o', ' '],
                  ['o', 'x', 'o']]))
