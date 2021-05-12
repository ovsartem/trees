"""
board game
"""

from btree import LinkedBinaryTree
from copy import deepcopy


class Board:
    """
    main class
    """

    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.last_move = None

    def __str__(self):
        string = ""
        for element in self.board:
            string += str(element) + "\n"
        return string.strip()

    def get_status(self):
        """
        get_status
        """
        left = []
        right = []
        first = []
        second = []
        third = []
        raw = 1
        for i in range(len(self.board)):
            combination = []
            for j in range(len(self.board[i])):
                combination.append(self.board[i][j])
                if j == 0:
                    first.append(self.board[i][j])
                elif j == 1:
                    second.append(self.board[i][j])
                else:
                    third.append(self.board[i][j])

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

    def make_move(self, position, turn):
        """
        make_move
        """
        try:
            if self.board[position[0]][position[1]] != " ":
                print("Ця клітинка вже замальована")
                raise IndexError
            self.board[position[0]][position[1]] = turn
            self.last_move = turn
        except:
            raise IndexError
            print("Ви неправильно ввели координати!")

    def make_computer_move(self):
        """
        Make move for computer.
        """
        self.board = self.build_tree(self).board
        self.last_move = "0"

    def make_person_move(self):
        """
        make_person_move
        """
        okmove = False
        while okmove != True:
            xcoord = input("Введіть номер рядка: ")
            ycoord = input("Введіть номер колонки: ")
            try:
                if self.board[int(xcoord)-1][int(ycoord)-1] != " ":
                    print("Ця клітинка вже замальована")
                    raise ValueError
                self.board[int(xcoord)-1][int(ycoord)-1] = "x"
                self.last_move = "x"
                okmove = True
            except:
                print("Ви неправильно ввели координати!")

    def possibilities(self):
        """
        possibilities
        """
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == " ":
                    moves.append((i, j))
        return moves

    def build_tree(self, board):
        """
        build_tree
        """
        tree = LinkedBinaryTree(board)

        def recurse(board, tree):
            """
            Recursive function for building a tree.
            """
            possible = board.possibilities()
            if len(possible) == 1:
                position = possible[0]
                left_board = deepcopy(board)
                right_board = deepcopy(board)
                if board.last_move == "x":
                    left_board.board[position[0]
                                     ][position[1]] = "0"
                    right_board.board[position[0]
                                      ][position[1]] = "0"
                if board.last_move == "0":
                    left_board.board[position[0]
                                     ][position[1]] = "x"
                    right_board.board[position[0]
                                      ][position[1]] = "x"
                tree.insert_left(left_board)
                tree.insert_right(right_board)
                return
            else:
                left_position = possible[0]
                right_position = possible[1]
                left_board = deepcopy(board)
                right_board = deepcopy(board)
                if board.last_move == "x":
                    new_move = "0"
                else:
                    new_move = "x"
                left_board.board[left_position[0]
                                 ][left_position[1]] = new_move
                right_board.board[right_position[0]
                                  ][right_position[1]] = new_move
                left_board.last_move = new_move
                right_board.last_move = new_move
                tree.insert_left(left_board)
                tree.insert_right(right_board)
                recurse(left_board, tree.get_left_child())
                recurse(right_board, tree.get_right_child())

        recurse(board, tree)
        left_points = self.get_points(tree.get_left_child())
        right_points = self.get_points(tree.get_right_child())
        if left_points > right_points:
            return tree.get_left_child().key
        return tree.get_right_child().key

    def get_points(self, tree):
        """
        get_points
        """
        count = 0

        def points_recurse(tree, count):
            """
            points_recurse
            """
            board = tree.key
            if board.get_status() == 'continue':
                count += points_recurse(tree.left_child, count)
                count += points_recurse(tree.right_child, count)
                return count
            elif board.get_status() == "0":
                count += 1
                return count
            elif board.get_status() == "x":
                count -= 1
                return count
            else:
                return count

        return points_recurse(tree, count)
