import heapq
import os

class Huff_Coding:
	def __init__(self, path):
		self.path = path
		self.leap = []
		self.code = {}
		self.reverse_map = {}

	class PrimeApex:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.rt = None
			self.lt = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq 

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other,PrimeApex)):
				return False
			return self.freq == other.freq

	# functions for compression:

	def mde_wave_dict(self, text):
		wave = {}
		for role in text:
			if not role in wave:
				wave[role] = 0
			wave[role] += 1
		return wave

	def made_leap(self, wave):
		for y in wave:
			Apex = self.PrimeApex(y, wave[y])
			heapq.heappush(self.leap, Apex)

	def unite_Apex(self):
		while(len(self.leap)>1):
			nodea = heapq.heappop(self.leap)
			nodeb = heapq.heappop(self.leap)

			Int = self.PrimeApex(None, nodea.freq + nodeb.freq)
			Int.rt = nodea
			Int.lt = nodeb

			heapq.heappush(self.leap, Int)


	def mde_crypt_aide(self, root, Live_Apex):
		if(root == None):
			return

		if(root.char != None):
			self.code[root.char] = Live_Apex
			self.reverse_map[Live_Apex] = root.char
			return

		self.mde_crypt_aide(root.rt, Live_Apex + "0")
		self.mde_crypt_aide(root.lt, Live_Apex + "1")


	def mde_crypt(self):
		root = heapq.heappop(self.leap)
		Live_Apex = ""
		self.mde_crypt_aide(root, Live_Apex)


	def combine_integer(self, text):
		sign_work = ""
		for role in text:
			sign_work += self.code[role]
		return sign_work


	def pack_integer(self, sign_work):
		etc_packing = 8 - len(sign_work) % 8
		for i in range(etc_packing):
			sign_work += "0"

		pack_stats = "{0:08b}".format(etc_packing)
		sign_work = pack_stats + sign_work
		return sign_work


	def bc_range(self, work_integer):
		if(len(work_integer) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		c = bytearray()
		for i in range(0, len(work_integer), 8):
			d = work_integer[i:i+8]
			c.append(int(d, 2))
		return c


	def compact(self):
		file, file_ext = os.path.splitext(self.path)
		return_way = "Compressed_" + file + ".bin"

		with open(self.path, 'r+') as file, open(return_way, 'wb') as output:
			text = file.read()
			text = text.rstrip()

			wave = self.mde_wave_dict(text)
			self.made_leap(wave)
			self.unite_Apex()
			self.mde_crypt()

			sign_work = self.combine_integer(text)
			work_integer = self.pack_integer(sign_work)

			x = self.bc_range(work_integer)
			output.write(bytes(x))

		print("File is Compressed")
		return return_way