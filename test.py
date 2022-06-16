import leaderboard

board = leaderboard.Leaderboard("test/test_leaderboard.txt")
board.read_leaderbard()
print(board.print_data())
board.update_leaderboard( [75,"kevin"] )
print(board.print_data())
board.write_new_score()
print(board.print_data())