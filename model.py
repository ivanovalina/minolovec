import random
import itertools

class Field:

	def __init__(self, is_mine, x, y, number_of_neighbour_mines = 0):
		self._is_mine = is_mine
		self._x = x
		self._y = y
		self._number_of_neighbour_mines = number_of_neighbour_mines
		self._is_open = False

	@property
	def number_of_neighbour_mines(self):
		return self._number_of_neighbour_mines

	@property
	def is_mine(self):
		return self._is_mine

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def is_open(self):
		return self._is_open
	

	def display(self):
		if not self._is_open:
			return 'x'
		if self.is_mine:
			return 'M'
		return str(self._number_of_neighbour_mines)


	def open(self):
		self._is_open = True
	
class Table:

	def __init__(self, number_of_mines, x_size, y_size):

		self._number_of_mines = number_of_mines
		self._x_size = int(x_size)
		self._y_size = int(y_size)
		self._table = []
		self._generate_table()
		self._is_gameover = False
		self._generate_mine_locations()
		self._fill_the_remaining_fields()

	def _generate_table(self):
		for x in range(self._x_size):
			self._table.append([None] * self._y_size)

	def open_xy(self, x, y):

		if self._is_gameover:
			raise ValueError("Game is over")

		if x < 0 or x >= self._x_size:
			raise ValueError("Wrong x location, x has to be between 0 and {}".format(self._x_size))

		if y < 0 or y >= self._y_size:
			raise ValueError("Wrong y location, y has to be between 0 and {}".format(self._y_size))

		field = self._table[x][y]
		if field.is_mine:
			self.open_everything()
			self._is_gameover = True
		else:
			field.open()

		if field.number_of_neighbour_mines == 0:
			self.open_neighbour(x, y)
			
	def open_neighbour(self, x, y):

		for c_x in range(x-1, x+2):
			if c_x < 0 or c_x >= self._x_size:
				continue
			for c_y in range(y-1, y+2):
				if c_y < 0 or c_y >= self._y_size:
					continue
				if self._table[c_x][c_y].number_of_neighbour_mines == 0 and not self._table[c_x][c_y].is_open:
					self._table[c_x][c_y].open()
					self.open_neighbour(c_x, c_y)

				if self._table[c_x][c_y].number_of_neighbour_mines > 0:
					self._table[c_x][c_y].open()
		return sum



	def _generate_mine_locations(self):
		current = []

		while True:
			rx = random.randint(0, self._x_size - 1)
			ry = random.randint(0, self._y_size - 1)
			if (rx, ry) not in current:
				current.append((rx, ry))

			if len(current) >= self._number_of_mines:
				break

		for x, y in current:
			self._table[x][y] = Field(True, x, y)

	def _fill_the_remaining_fields(self):

		for x in range(self._x_size):
			for y in range(self._y_size):

				if self._table[x][y] is not None:
					continue

				self._table[x][y] = Field(False, x, y, self._sum_neighour(x, y))

	def _sum_neighour(self, x, y):
		sum = 0
		for c_x in range(x-1, x+2):
			if c_x < 0 or c_x >= self._x_size:
				continue
			for c_y in range(y-1, y+2):
				if c_y < 0 or c_y >= self._y_size:
					continue
				if self._table[c_x][c_y] is not None and self._table[c_x][c_y].is_mine:
					sum += 1

		return sum


		
	def str(self):
		strlst = []
		for x in range(self._x_size):
			row = []
			for y in range(self._y_size):
				row.append(self._table[x][y].display())
			
			strlst.append(' '.join(row))

		return '\n'.join(strlst)

	def is_winner(self):
		for x in range(self._x_size):
			for y in range(self._y_size):
				if not self._table[x][y]._is_open and not self._table[x][y]._is_mine: 
					return False
		return True




if __name__ == "__main__":
	t = Table(1, 15, 10)
	print(t.str())
	print('\n')
	t.open_xy(5,7)
	print(t.str())
	print(t.is_winner())


	
	