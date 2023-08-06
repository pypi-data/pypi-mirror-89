"""
advanced_math module for handling some advanced mathamatical operations
"""


import math


class Point:
	"""
	Creates a 2D point object
	"""

	def __init__(self, x, y, formatting="default"):
		if(type(x) in (int, float) and type(y) in (int, float)):
			self.x = x
			self.y = y
			self.formatting = formatting
		else:
			raise TypeError("Point object must contain all int or float type values!")

	def distance(self, another_point):
		"""
		Calculates the distance between two points
		:param another_point: Point
		:return: float
		"""
		if(type(another_point) is Point):
			distance = math.sqrt((another_point.x - self.x)**2 + (another_point.y - self.y)**2)
		else:
			raise TypeError("Arguement 2 must be Point, not " + type(another_point) + "!")

		return distance

	def form_vector2(self, another_point):
		"""
		Returns a new Vector2 object having x and y of subtraction of first point and second point.
		:param another_point: Point
		:return: Vector2
		"""
		if(type(another_point) is Point):
			new_vector2 = Vector2(another_point.x - self.x, another_point.y - self.y)
			return new_vector2
		else:
			raise TypeError("Point object must contain all int or float type values!")

	def to_tuple(self):
		"""
		Returns the point object in a tuple form
		:return: Tuple
		"""
		return (self.x, self.y)

	def format(self, formatting):
		"""
		Changes the format in which the point is printed (converted into str).
		Supported formats are: default, standard, expanded.
		Although, it doesn't throw errors if any invalid formatting is presented, it's a bad practice doing that!
		:param formatting: str
		:return: None
		"""
		self.formatting = formatting

	def __repr__(self):
		return f"Point({self.x}, {self.y})"

	def __str__(self):
		if(self.formatting == "standard"):
			return f"Point({self.x}, {self.y})"
		elif(self.formatting == "expanded"):
			return f"Point Object -> x: {self.x}, y: {self.y}"
		else:
			return f"({self.x}, {self.y})"

	def __add__(self, another_point):
		if(type(another_point) is Point):
			new_point = Point(self.x + another_point.x, self.y + another_point.y)
		else:
			raise TypeError("Arguement 2 must be Point, not " + type(another_point) + "!")

		return new_point

	def __sub__(self, another_point):
		if(type(another_point) is Point):
			new_point = Point(self.x - another_point.x, self.y - another_point.y)
		else:
			raise TypeError("Arguement 2 must be Point, not " + type(another_point) + "!")

		return new_point

	def __eq__(self, another_point):
		if(type(another_point) is Point):
			if(self.x == another_point.x and self.y == another_point.y):
				return True
			else:
				return False
		else:
			raise TypeError("Arguement 2 must be Point, not " + type(another_point) + "!")

	# static methods
	@staticmethod
	def make_point_from_seq(sequence):
		"""
		Creates a new point using a sequence
		:param sequence: Sequence
		:return: Point
		"""
		if(len(sequence) > 2):
			raise ValueError("Sequence must not contain more than 2 elements!")
		else:
			type_x, type_y = [type(i) for i in sequence]
			if((type_x is int or type_x is float) and (type_y is int or type_y is float)):
				x, y = [i for i in sequence]
				point = Point(x, y)
			else:
				raise TypeError("Sequence must contain all int or float type values!")

		return point

	@staticmethod
	def from_seq(sequence):
		point = Point.make_point_from_seq(sequence)
		return point

	@staticmethod
	def origin():
		"""
		Returns the origin point
		:return: Point
		"""
		return Point(0, 0)


class Vector2:
	"""
	Creates a new 2D vector object
	"""

	def __init__(self, x, y, formatting="default"):
		if(type(x) in (int, float) and type(y) in (int, float)):
			self.x = x
			self.y = y
			self.formatting = formatting
		else:
			raise TypeError("Vector2 object must contain all int or float type values!")

	def magnitude(self):
		"""
		Calculates the magnitude of a 2D vector
		:return: float
		"""
		magnitude = math.sqrt((self.x)**2 + (self.y)**2)
		return magnitude

	def direction(self):
		"""
		Calculates the direction of a vector
		:return: float
		"""
		tangent = self.y / self.x
		return math.atan(tangent)

	def to_tuple(self):
		"""
		Returns the vector object in a tuple form
		:return: Tuple
		"""
		return (self.x, self.y)

	def format(self, formatting):
		"""
		Changes the format in which the vector is printed (converted into str).
		Supported formats are: default, standard, expanded.
		Although, it doesn't throw errors if any invalid formatting is presented, it's a bad practice doing that!
		:param formatting: str
		:return: None
		"""
		self.formatting = formatting

	def __repr__(self):
		return f"Vector2({self.x}, {self.y})"

	def __str__(self):
		if(self.formatting == "standard"):
			return f"Vector2({self.x}, {self.y})"
		elif(self.formatting == "expanded"):
			return f"Vector2 Object -> x: {self.x}, y: {self.y}"
		else:
			return f"{self.x}i + {self.y}j"

	def __add__(self, another_vector):
		if(type(another_vector) is Vector2):
			resultant_vector = Vector2(self.x + another_vector.x, self.y + another_vector.y)
		else:
			raise TypeError("Arguement 2 must be Vector2, not " + str(type(another_vector)) + "!")

		return resultant_vector

	def __sub__(self, another_vector):
		if(type(another_vector) is Vector2):
			resultant_vector = Vector2(self.x - another_vector.x, self.y - another_vector.y)
		else:
			raise TypeError("Arguement 2 must be Vector2, not " + str(type(another_vector)) + "!")

		return resultant_vector

	def __mul__(self, value):
		# constant multiplication
		if(type(value) is int or type(value) is float):
			product = Vector2(value * self.x, value * self.y)
		else:
			raise TypeError("Arguement 2 must be int or float, not " + str(type(value)) + "!")

		return product

	def __truediv__(self, value):
		if(type(value) is int or type(value) is float):
			quotient = Vector2(self.x / value, self.y / value)
		else:
			raise TypeError("Arguement 2 must be int or float, not " + str(type(value)) + "!")

		return quotient

	def __floordiv__(self, value):
		if(type(value) is int or type(value) is float):
			quotient = Vector2(self.x // value, self.y // value)
		else:
			raise TypeError("Arguement 2 must be int or float, not " + str(type(value)) + "!")

		return quotient

	def __eq__(self, another_vector):
		if(type(another_vector) is Vector2):
			if(self.magnitude() == another_vector.magnitude() and self.direction() == another_vector.direction()):
				return True
			else:
				return False
		else:
			raise TypeError("Arguement 2 must be Vector2, not " + str(type(another_vector)) + "!")

	# static methods
	@staticmethod
	def make_vector_from_seq(sequence):
		"""
		Creates a new vector using a sequence
		:param sequence: Sequence
		:return: Vector2
		"""
		if(len(sequence) > 2):
			raise ValueError("Sequence must not contain more than 2 elements!")
		else:
			type_x, type_y = [type(i) for i in sequence]
			if((type_x is int or type_x is float) and (type_y is int or type_y is float)):
				x, y = [i for i in sequence]
				vector = Vector2(x, y)
			else:
				raise TypeError("Sequence must contain all int or float type values!")

		return vector

	def from_seq(sequence):
		vector = Vector2.make_vector_from_seq(sequence)
		return vector

	@staticmethod
	def zero():
		"""
		Returns the null or zero vector
		"""
		return Vector2(0, 0)

	@staticmethod
	def up():
		"""
		Returns a unit vector in negative y direction
		"""
		return Vector2(0, -1)

	@staticmethod
	def down():
		"""
		Returns a unit vector in positive y direction
		"""
		return Vector2(0, 1)

	@staticmethod
	def left():
		"""
		Returns a unit vector in negative x direction
		"""
		return Vector2(-1, 0)

	@staticmethod
	def right():
		"""
		Returns a unit vector in positive x direction
		"""
		return Vector2(1, 0)


class Point3D:
	"""
	Creates a 3D point object
	"""

	def __init__(self, x, y, z, formatting="default"):
		if(type(x) in (int, float) and type(y) in (int, float) and type(z) in (int, float)):
			self.x = x
			self.y = y
			self.z = z
			self.formatting = formatting
		else:
			raise TypeError("Point3D object must contain all int or float type values!")

	def distance(self, another_point):
		"""
		Calculates the distance between two points
		:param another_point: Point3D
		:return: float
		"""
		if(type(another_point) is Point3D):
			distance = math.sqrt((another_point.x - self.x)**2 + (another_point.y - self.y)**2 + (another_point.z - self.z)**2)
		else:
			raise TypeError("Arguement 2 must be Point3D, not " + type(another_point) + "!")

		return distance

	def form_vector3(self, another_point):
		"""
		TODO: IMPLEMENT AFTER VECTOR3
		Returns a new Vector2 object having x and y of subtraction of first point and second point.
		:param another_point: Point
		:return: Vector2
		"""
		if(type(another_point) is Point):
			new_vector2 = Vector2(another_point.x - self.x, another_point.y - self.y)
			return new_vector2
		else:
			raise TypeError("Point object must contain all int or float type values!")          # TODO

	def to_tuple(self):
		"""
		Returns the point3D object in a tuple form
		:return: Tuple
		"""
		return (self.x, self.y, self.z)

	def format(self, formatting):
		"""
		Changes the format in which the point3D is printed (converted into str).
		Supported formats are: default, standard, expanded.
		Although, it doesn't throw errors if any invalid formatting is presented, it's a bad practice doing that!
		:param formatting: str
		:return: None
		"""
		self.formatting = formatting

	def __repr__(self):
		return f"Point3D({self.x}, {self.y}, {self.z})"

	def __str__(self):
		if(self.formatting == "standard"):
			return f"Point3D({self.x}, {self.y}, {self.z})"
		elif(self.formatting == "expanded"):
			return f"Point3D Object -> x: {self.x}, y: {self.y}, z:{self.z}"
		else:
			return f"({self.x}, {self.y}, {self.z})"

	def __add__(self, another_point):
		if(type(another_point) is Point3D):
			new_point = Point3D(self.x + another_point.x, self.y + another_point.y, self.z + another_point.z)
		else:
			raise TypeError("Arguement 2 must be Point3D, not " + type(another_point) + "!")

		return new_point

	def __sub__(self, another_point):
		if(type(another_point) is Point3D):
			new_point = Point3D(self.x - another_point.x, self.y - another_point.y, self.z - another_point.z)
		else:
			raise TypeError("Arguement 2 must be Point3D, not " + type(another_point) + "!")

		return new_point

	def __eq__(self, another_point):
		if(type(another_point) is Point3D):
			if(self.x == another_point.x and self.y == another_point.y and self.z == another_point.z):
				return True
			else:
				return False
		else:
			raise TypeError("Arguement 2 must be Point3D, not " + type(another_point) + "!")

	@staticmethod
	def from_seq(sequence):
		"""
		Creates a new point using a sequence
		:param sequence: Sequence
		:return: Point3D
		"""
		if(len(sequence) > 3):
			raise ValueError("Sequence must not contain more than 3 elements!")
		else:
			type_x, type_y, type_z = [type(i) for i in sequence]
			if((type_x is int or type_x is float) and (type_y is int or type_y is float) and (type_z is int or type_z is float)):
				x, y, z = [i for i in sequence]
				point = Point3D(x, y, z)
			else:
				raise TypeError("Sequence must contain all int or float type values!")

		return point

	@staticmethod
	def origin():
		"""
		Returns the origin point
		:return: Point3D
		"""
		return Point3D(0, 0, 0)


class Vector3:
	"""
	Creates a new 3D vector object
	"""

	def __init__(self, x, y, z, formatting="default"):
		if(type(x) in (int, float) and type(y) in (int, float) and type(z) in (int, float)):
			self.x = x
			self.y = y
			self.z = z
			self.formatting = formatting
		else:
			raise TypeError("Vector3 object must contain all int or float type values!")

	def magnitude(self):
		"""
		Calculates the magnitude of a 3D vector
		:return: float
		"""
		magnitude = math.sqrt((self.x)**2 + (self.y)**2 + (self.z)**2)
		return magnitude

	def direction(self):     # TODO
		"""
		TODO: IMPLEMENT LATER
		Calculates the direction of a vector
		:return: float
		"""
		tangent = self.y / self.x
		return math.atan(tangent)

	def to_tuple(self):
		"""
		Returns the vector object in a tuple form
		:return: Tuple
		"""
		return (self.x, self.y, self.z)

	def format(self, formatting):
		"""
		Changes the format in which the vector is printed (converted into str).
		Supported formats are: default, standard, expanded.
		Although, it doesn't throw errors if any invalid formatting is presented, it's a bad practice doing that!
		:param formatting: str
		:return: None
		"""
		self.formatting = formatting

	def __repr__(self):
		return f"Vector3({self.x}, {self.y}, {self.z})"

	def __str__(self):
		if(self.formatting == "standard"):
			return f"Vector3({self.x}, {self.y}, {self.z})"
		elif(self.formatting == "expanded"):
			return f"Vector3 Object -> x: {self.x}, y: {self.y}, z: {self.z}"
		else:
			return f"{self.x}i + {self.y}j + {self.z}k"

	def __add__(self, another_vector):
		if(type(another_vector) is Vector3):
			resultant_vector = Vector3(self.x + another_vector.x, self.y + another_vector.y, self.z + another_vector.z)
		else:
			raise TypeError("Arguement 2 must be Vector3, not " + str(type(another_vector)) + "!")

		return resultant_vector

	def __sub__(self, another_vector):
		if(type(another_vector) is Vector3):
			resultant_vector = Vector3(self.x - another_vector.x, self.y - another_vector.y, self.z - another_vector.z)
		else:
			raise TypeError("Arguement 2 must be Vector3, not " + str(type(another_vector)) + "!")

		return resultant_vector

	def __mul__(self, value):
		# constant multiplication
		if(type(value) is int or type(value) is float):
			product = Vector3(value * self.x, value * self.y, value * self.z)
		else:
			raise TypeError("Arguement 2 must be int or float, not " + str(type(value)) + "!")

		return product

	def __truediv__(self, value):
		if(type(value) is int or type(value) is float):
			quotient = Vector3(self.x / value, self.y / value, self.z / value)
		else:
			raise TypeError("Arguement 2 must be int or float, not " + str(type(value)) + "!")

		return quotient

	def __floordiv__(self, value):
		if(type(value) is int or type(value) is float):
			quotient = Vector3(self.x // value, self.y // value, self.z // value)
		else:
			raise TypeError("Arguement 2 must be int or float, not " + str(type(value)) + "!")

		return quotient

	def __eq__(self, another_vector):
		if(type(another_vector) is Vector3):
			if(self.magnitude() == another_vector.magnitude() and self.direction() == another_vector.direction()):
				return True
			else:
				return False
		else:
			raise TypeError("Arguement 2 must be Vector3, not " + str(type(another_vector)) + "!")

	# static methods
	def from_seq(sequence):
		"""
		Creates a new vector using a sequence
		:param sequence: Sequence
		:return: Vector2
		"""
		if(len(sequence) > 3):
			raise ValueError("Sequence must not contain more than 3 elements!")
		else:
			type_x, type_y, type_z = [type(i) for i in sequence]
			if((type_x is int or type_x is float) and (type_y is int or type_y is float) and (type_z is int or type_z is float)):
				x, y, z = [i for i in sequence]
				vector = Vector3(x, y, z)
			else:
				raise TypeError("Sequence must contain all int or float type values!")

		return vector

	@staticmethod
	def zero():
		"""
		Returns the null or zero vector
		"""
		return Vector3(0, 0, 0)

	@staticmethod
	def up():
		"""
		Returns a unit vector in negative y direction
		"""
		return Vector3(0, -1, 0)

	@staticmethod
	def down():
		"""
		Returns a unit vector in positive y direction
		"""
		return Vector3(0, 1, 0)

	@staticmethod
	def left():
		"""
		Returns a unit vector in negative x direction
		"""
		return Vector3(-1, 0, 0)

	@staticmethod
	def right():
		"""
		Returns a unit vector in positive x direction
		"""
		return Vector3(1, 0, 0)

	@staticmethod
	def inward():
		"""
		Returns a unit vector in positive z direction
		"""
		return Vector3(0, 0, 1)

	@staticmethod
	def outward():
		"""
		Returns a unit vector in negative z direction
		"""
		return Vector3(0, 0, -1)
