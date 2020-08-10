import curses
import sys
import random

stdscr = curses.initscr()
board = [['[ ]' for x in range(3)] for y in range(3)]
stats = open('stats', 'r+')


def setCurses(stdscr):
	curses.curs_set(0)
	curses.noecho()
	curses.cbreak()
	stdscr.nodelay(True)

	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_BLUE, 0)
	curses.init_pair(3, curses.COLOR_RED, 0)

	stdscr.keypad(True)

def displayMenu():
	stdscr.clear()
	maxY, maxX = stdscr.getmaxyx()

	stdscr.addstr(2,maxX//2-8, 'TIC TAC TOE!')

	menu = ['SINGLEPLAYER', 'MULTIPLAYER', 'STATS', 'EXIT']

	for i, row in enumerate(menu):
		x = maxX//2 - len(row)//2-2
		y = maxY//3+2+i
		stdscr.addstr(y, x, row, A_STANDOUT)

def printBoard(stdscr, currRow, currCol):
	maxY, maxX = stdscr.getmaxyx()
	x = maxX//2 - len(board[0]) - len(board[0])//2
	y = maxY//2 - len(board)//2

	for i, row in enumerate(board):
		 for j, col in enumerate(row):
		 	if board[i][j] == '[X]':
		 		stdscr.attron(curses.color_pair(2))

		 	if board[i][j] == '[O]':
		 		stdscr.attron(curses.color_pair(3))

		 	if currRow == i and currCol == j:
		 		stdscr.attron(curses.color_pair(1))

		 	stdscr.addstr(y+i*2-2, x+j*5-5, board[i][j])
		 	
		 	stdscr.attroff(curses.color_pair(1))
		 	stdscr.attroff(curses.color_pair(2))
		 	stdscr.attroff(curses.color_pair(3))

	stdscr.refresh()

def clearBoard(strscr, board):
	board = [['[ ]' for x in range(3)] for y in range(3)]

def move(currRow, currCol, state):
	if isEmpty(currRow, currCol):
		board[currRow][currCol] = state

def isEmpty(currRow, currCol):
	return board[currRow][currCol] == '[ ]'

def moveAI():
	return True

def displayDraw(stdscr):
	maxY, maxX = stdscr.getmaxyx()
	stdscr.addstr(4, maxX//2, 'Draw')
	stdscr.addstr(5, maxX//2-len('Press [R] to return to MENU...'), 'Press [R] to return to MENU...', curses.A_BLINK)


def displayWin(stdscr, turn):
	if turn % 2 == 0:
		state = '[X]'
	elif not turn % 2 == 0:
		state = '[O]'

	maxY, maxX = stdscr.getmaxyx()
	stdscr.addstr(4, maxX//2 - len(str(state) + ' wins'), str(state) + ' wins')
	stdscr.addstr(5, maxX//2-len('Press [R] to return to MENU...')//2, 'Press [R] to return to MENU...', curses.A_BLINK)

def printStats(stdscr, stats):
	stdscr.clear()
	stats.seek(1)
	maxY, maxX = stdscr.getmaxyx()
	stdscr.addstr(2,maxX//2-8, 'TIC TAC TOE!', curses.A_BOLD)
	stdscr.addstr(4, maxX//2-7, 'STATISTICS')
	stdscr.addstr(6, maxX//2-8, 'SINGLEPLAYER:')
	stdscr.addstr(11, maxX//2-7, 'MULTIPLAYER:')

	for i, line in enumerate(stats):
		if i == 0:
			continue

		x = maxX//2 - len(line)*3
		if i < 4:
			y = maxY//4+i
		else:
			y = 8 + i

		#SINGLEPLAYER
		if i == 1: #No. Games
			stdscr.addstr(y, x, 'Games Played: ' + line)
		elif i == 2: #X wins
			stdscr.addstr(y, x, '[X] Wins: ' + line)
		elif i == 3: #O wins
			stdscr.addstr(y, x, '[O] Wins: ' + line)

		#MULTIPLAYER
		elif i == 4: #No.Games
			stdscr.addstr(y, x, ' Games Played: ' + line)
		elif i == 5: #wins
			stdscr.addstr(y, x, 'Wins: ' + line)
		elif i == 6: #Losses
			stdscr.addstr(y, x, 'Losses: ' + line)
		elif i == 7:
			stdscr.addstr(y, x, '   Win %: ' + line)

	stdscr.refresh()

def main(stdscr):
	setCurses(stdscr)

	maxY, maxX = stdscr.getmaxyx()
	running = True
	inGame = True
	inMenu = True
	win = False
	draw = False
	multiplayer = False
	keyLock = False
	inStats = False

	menuIndex = 0
	gamemode = 'SINGLEPLAYER'
	state = '[X]'

	#MAIN GAME LOOP
	while running:
		#GAME SETUP
		currRow = 0
		currCol = 0
		currCell = board[currRow][currCol]
		turn = 1

		stdscr.clear()
		stdscr.addstr(2,maxX//2-8, 'TIC TAC TOE!', curses.A_BOLD)
		stdscr.addstr(0,0, gamemode)



		#MAIN MENU LOOP	
		while inMenu:
			stdscr.clear()	
			maxY, maxX = stdscr.getmaxyx()
			stdscr.addstr(2,maxX//2-8, 'TIC TAC TOE!', curses.A_BOLD)

			menu = ['SINGLEPLAYER', 'MULTIPLAYER', 'STATS', 'EXIT']

			for i, row in enumerate(menu):
				x = maxX//2 - len(row)//2-2
				y = maxY//3+2+i
				if menuIndex == i:
					stdscr.addstr(y, x, row, curses.A_STANDOUT)
				else:
					stdscr.addstr(y, x, row)

			#INPUT CONTROLS MAIN MENU
			key = stdscr.getch()
			if key == curses.KEY_UP:
				if menuIndex > 0:
					menuIndex = menuIndex - 1
				else:
					menuIndex = 3

			elif key == curses.KEY_DOWN:
				if menuIndex < 3:
					menuIndex = menuIndex + 1
				else:
					menuIndex = 0

			elif key == ord('q') or key == ord('Q'):
				curses.endwin()
				exit()

			elif key == ord('z') or key == ord('z'):
				curses.endwin()
				if menuIndex == 0: #SINGLEPLAYER
					gamemode = 'SINGLEPLAYER'
					stdscr.clear()
					break;
				elif menuIndex == 1: #MULTIPLAYER
					multiplayer = True
					gamemode = 'MULTIPLAYER'
					stdscr.clear()
					break;
				elif menuIndex == 2: #STATS
					stdscr.clear()
					stdscr.refresh()
					inGame = False
					inStats = True
					break;

				elif menuIndex == 3: #EXIT
					stdscr.clear()
					curses.endwin()
					exit()

			stdscr.refresh()

		#STATS MENU LOOP
		while inStats:
			printStats(stdscr, stats)
			key = stdscr.getch()
			if key == ord('q') or key == ord('Q'):
				curses.endwin()
				exit()
			elif key == ord('z') or key == ord('Z'):
				inMenu = True
				inStats = False
				break;

		#MATCH LOOP
		stdscr.clear()
		clearBoard(stdscr, board)
		inGame = True
		win = False
		keyLock = False
		draw = False
		turn = 1
		inMenu = False
		
		while inGame:
			stdscr.addstr(2,maxX//2-8, 'TIC TAC TOE!', curses.A_BOLD)	
			stdscr.addstr(0, 0, gamemode)
			stdscr.addstr(1, 0, 'Turn: ' + str(turn))

			#DEBUG
			stdscr.addstr(6,0, 'Menu: ' + str(inMenu))
			stdscr.addstr(7,0, 'KeyLock' + str(keyLock))
			stdscr.addstr(8,0, 'win' + str(win))
			stdscr.addstr(9,0, 'draw' + str(draw))


			stdscr.refresh()

			printBoard(stdscr, currRow, currCol)

			if multiplayer:
				if (turn) % 2 == 0:
					state = '[O]'
				elif not turn % 2 == 0:
					state = '[X]'

			#INPUT CONTROLS GAME
			key = stdscr.getch()
			if key == curses.KEY_UP and not keyLock and not win:
				if currRow <= 0:
					currRow = 3-1
				else: 
					currRow -= 1
				currCell = board[currRow][currCol]

			elif key == curses.KEY_DOWN and not keyLock and not win:
				if currRow >= 3-1:
					currRow = 0
				else: 
					currRow += 1
				currCell = board[currRow][currCol]

			elif key == curses.KEY_LEFT and not keyLock and not win:
				if currCol <= 0:
					currCol = 3-1
				else: 
					currCol -= 1
				currCell = board[currRow][currCol]

			elif key == curses.KEY_RIGHT and not keyLock and not win:
				if currCol >= 3-1:
					currCol = 0
				else: 
					currCol += 1
				currCell = board[currRow][currCol]

			elif key == ord('q') or key == ord('Q'):
				curses.endwin()
				exit()

			elif key == ord('z') or key == ord('X') and not keyLock and (not win or not draw):
				move(currRow, currCol, state)
				turn = turn + 1

			elif key == ord('R') or key == ord('r') and (win or draw):
				inGame = False
				inMenu = True
				turn = turn
				break

			if multiplayer:
				moveAI()

			#CHECK COL
			for i in range(3):
				if not board[i][currCol] == state:
					break
				if i == 2:
					keyLock = True
					win = True
				
			#CHECK ROW
			for i in range(3):
				if not board[currRow][i] == state:
					break
				if i == 2:
					keyLock = True
					win = True

			#CHECK DIAG
			if currRow ==  currCol:
				#WERE ON DIAGONAL
				for i in range(3):
					if not board[i][i] == state:
						break
					if i == 2:
						keyLock = True
						win = True

			#CHECK ANT DIAG
			if currCol + currRow == 2:
				for i in range(3):
					if not board[i][3-1] == state:
						break
					if i == 2:
						keyLock = True	
						win = True

			#CHECK DRAW
			if turn == 10:
				stdscr.addstr(2, 0, 'DRAW')
				keyLock = True
				draw = True

			if win:
				keyLock = True
				displayWin(stdscr, turn)
				key = stdscr.getch()
		
			elif draw:
				keyLock = True
				displayDraw(stdscr)

			
		# #UPDATE STATS
		# stats.seek(0)
		# newStats = ''
		# for i, line in enumerate(stats):
		# 	if i == 0 and multiplayer: #Games played + 1
		# 		cur = int( line )
		# 		newCur = cur + 1
		# 		newStats += str(newCur)

		# stats.seek(0)
		# stats.write(newStats)
			
		stdscr.refresh()

curses.endwin()
curses.wrapper(main)
stats.close()
