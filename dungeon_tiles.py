from PIL import Image
import pandas as pd
import pygame as pg
import sys




class MapConstructor:
	def __init__(self):
		pg.init()
		pg.key.set_repeat(100,200)
		self.TSIZE = 64
		self.ONELINE = 4
		self.hold = [0]
		self.poslist = {}
		self.tilepos = {}
		self.myimages = {}
		self.WIDTH, self.HEIGHT = 1024, 640
		self.positions = {'h':1, 'w':self.WIDTH-self.TSIZE*self.ONELINE, 'line' : 0}
		self.clock = pg.time.Clock()
		self.surface = pg.display.set_mode((self.WIDTH,self.HEIGHT))

	def eq_pos(self, mx,my):
		return mx//self.TSIZE*self.TSIZE, my//self.TSIZE*self.TSIZE

	def quit(self):
		pg.quit()
		sys.exit()

	def assignhold(self, mx,my):
		mx //= self.TSIZE
		my //= self.TSIZE
		try:
			self.hold[0] = self.poslist[mx,my]
		except KeyError:
			print('empty keyvalue on click')
			self.hold[0] = 0

	def addtoscr(self, tile, pos):
		mx,my = pos
		pos = self.eq_pos(mx,my)
		self.tilepos[pos] = tile

	def left_click(self):
		mx,my = pg.mouse.get_pos()
		if self.WIDTH-self.TSIZE*self.ONELINE < mx < self.WIDTH:
			if 0 < my < self.TSIZE: self.scroll()
			elif  self.HEIGHT-self.TSIZE < my < self.HEIGHT: self.scroll(False)
			else: self.assignhold(mx,my)
		elif self.hold[0]:
			self.addtoscr(self.hold[0], (mx,my))	

	def right_click(self):
		mx,my = pg.mouse.get_pos()
		
		if not (self.WIDTH-self.TSIZE*self.ONELINE < mx < self.WIDTH) and not self.hold[0]:
			try:
				del self.tilepos[self.eq_pos(mx,my)]
			except KeyError:
				print("KeyError: can't del, not in tilepos")
		self.hold[0] = 0

	def events(self):
		for event in pg.event.get(): 
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): quit()
			elif pg.mouse.get_pressed() != (0, 0, 0):
				left,middle,right = pg.mouse.get_pressed()
				if left: self.left_click()
				elif right: self.right_click()
			elif event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 4: self.scroll()
				elif event.button == 5: self.scroll(False)
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_q:
					self.offload()
				elif event.key == pg.K_c:
					self.tilepos = {}
				elif event.key == pg.K_r:
					self.hold[0] = self.rotate(self.hold[0], 90)

	def scroll(self, up=True):
		self.positions['line'] = max(0, self.positions['line']-self.ONELINE) if up else min(self.positions['line']+self.ONELINE, len(self.myimages.keys())-7*self.ONELINE)

	def draw(self):
		startline = self.WIDTH-(self.TSIZE*self.ONELINE)
		self.surface.fill((0,0,0))

		for key in self.tilepos.keys():
			self.surface.blit(self.tilepos[key][0], key)
		mx,my = pg.mouse.get_pos()
		mx,my = self.eq_pos(mx,my)
		if not self.hold[0]:
			pg.draw.rect(self.surface, (255,0,0), (mx,my, self.TSIZE, self.TSIZE), 2)
		else: self.surface.blit(self.hold[0][0], (mx,my))

		h = self.positions['h']*self.TSIZE
		w = self.positions['w']
		for x in range(self.positions['line'], len(self.myimages.keys())):
			self.surface.blit(self.myimages[x], (w,h))

			self.poslist[w//self.TSIZE,h//self.TSIZE] = self.myimages[x], x, 0 #img, index, angle

			if w+self.TSIZE >= self.WIDTH:
				w = self.WIDTH-self.TSIZE*self.ONELINE
				h += self.TSIZE
			else: w+=self.TSIZE


		distance = self.WIDTH-(self.TSIZE*self.ONELINE)
		pg.draw.rect(self.surface, (150,150,150), (distance,0, self.TSIZE*self.ONELINE, self.TSIZE))
		pg.draw.rect(self.surface, (150,70,70), (distance,0, self.TSIZE*self.ONELINE, self.TSIZE), 1)
		pg.draw.rect(self.surface, (150,150,150), (distance ,self.HEIGHT-self.TSIZE, self.TSIZE*self.ONELINE, self.TSIZE))
		pg.draw.rect(self.surface, (150,70,70), (distance ,self.HEIGHT-self.TSIZE, self.TSIZE*self.ONELINE, self.TSIZE), 1)
		for x in range(self.TSIZE, self.HEIGHT//self.TSIZE*self.TSIZE-1, self.TSIZE):
			pg.draw.line(self.surface, (255,0,0), (distance,x), (self.WIDTH ,x))
		for x in range(4):
			pg.draw.line(self.surface, (255,0,0), (distance,self.TSIZE), (distance,self.HEIGHT-self.TSIZE))
			distance += self.TSIZE
		pg.draw.polygon(self.surface, (50, 50, 50), ((self.WIDTH-self.TSIZE*2,self.TSIZE//3), (self.WIDTH-self.TSIZE*2-self.TSIZE//4,self.TSIZE//1.5),
			(self.WIDTH-self.TSIZE*2+self.TSIZE//4,self.TSIZE//1.5)))
		pg.draw.polygon(self.surface, (50, 50, 50), ((self.WIDTH-self.TSIZE*2,self.HEIGHT-self.TSIZE//3), (self.WIDTH-self.TSIZE*2-self.TSIZE//4,self.HEIGHT-self.TSIZE//1.5),
			(self.WIDTH-self.TSIZE*2+self.TSIZE//4,self.HEIGHT-self.TSIZE//1.5)))
		pg.display.flip()

	def rotate(self):
		hold

	def upload(self, sheet = 'Shocknew1.png'):
		size = self.TSIZE
		my_image = Image.open(sheet)
		tiles = pd.read_csv('tocsv2.csv')	
		for x in range(len(tiles)):
			start = (tiles.iloc[x,2], tiles.iloc[x,3])
			vector = start[0]+self.TSIZE, start[1]+self.TSIZE
			tile = my_image.crop((*start, *vector))
			img = pg.image.frombuffer(tile.tobytes(), tile.size, tile.mode)
			img = img.convert_alpha() if img.get_alpha() else img.convert()
			self.myimages[x] = img

	def rotate(self, data, degree = False):
		angle =degree if data[2]+degree > 360 else data[2]+degree
		img = self.myimages[data[1]]
		img = Image.frombytes("RGBA", img.get_size(), pg.image.tostring(img, "RGBA", False))
		rotated_image = img.rotate(angle, resample = Image.BICUBIC)
		raw_str = rotated_image.tobytes('raw', 'RGBA')
		return pg.image.fromstring(raw_str, img.size, "RGBA"), data[1], angle

	def offload(self):
		newdf = pd.DataFrame([{'tile_index':self.tilepos[key][1], 'pos':key, 'angle':self.tilepos[key][2]} for key in self.tilepos.keys()])
		tiles = pd.read_csv('tocsv2.csv')
		total = pd.merge(newdf,tiles, left_on = 'tile_index', right_index = True, how = 'inner')
		total = total.loc[:, ~total.columns.str.contains('^Unnamed')]
		total.to_csv('newmap.csv')

	def load(self):
		self.upload()
		try:
			tiles = pd.read_csv('newmap.csv')
			print(tiles)
			for x in range(len(tiles)):

				txt = tiles.iloc[x,2].replace('(','').replace(')','').split(',')
				pos = int(txt[0]), int(txt[1])
				img = self.myimages[tiles.iloc[x,3]], tiles.iloc[x,3], tiles.iloc[x,1]

				self.tilepos[pos] = self.rotate(img) if tiles.iloc[x,1] != 0 else img
		except Exception as e:
			print(e) 
			print('No map found, you can start drawing a new one')

	def run(self):
		self.load()
		while True:
			self.clock.tick(60)
			self.events()
			self.draw()


if __name__ == '__main__':

	construct = MapConstructor()
	construct.run()

