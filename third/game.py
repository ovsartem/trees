from board import Board
roles = {"x": "You", "0": "Computer"}

if __name__ == '__main__':
    end = False
    board = Board()
    while end != True:
        board.make_person_move()
        result = board.get_status()
        if result == 'x' or result == '0':
            print(f"{roles[result]} won")
            next_action = input(
                "If you want to plat again type 1, if not - type 0: ")
            if next_action == "0":
                end = True
            else:
                board = Board()

        elif result == 'draw':
            print("Draw!")
            next_action = input(
                "If you want to plat again type 1, if not - type 0: ")
            if next_action == "0":
                end = True
            else:
                board = Board()
        else:
            print("Nice move!")
            print(board)

        board.make_computer_move()
        result = board.get_status()
        print(result)
        if result == 'x' or result == '0':
            print(f"{roles[result]} won")
            next_action = input(
                "If you want to plat again type 1, if not - type 0: ")
            if next_action == "0":
                end = True
            else:
                board = Board()
        elif result == 'draw':
            print("Draw!")
            next_action = input(
                "If you want to plat again type 1, if not - type 0: ")
            if next_action == "0":
                end = True
            else:
                board = Board()
        else:
            print("Board after computer's move")
            print(board)
