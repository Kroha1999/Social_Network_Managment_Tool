import tkinter as tk  


class AnimatedGif(tk.Button):
	"""
	Class to show animated GIF file in a label
	Use start() method to begin animation, and set the stop flag to stop it
	"""
	def __init__(self, root, img_file, gif_file, delay=0.04,**kw):
		"""
		:param root: tk.parent
		:param gif_file: filename (and path) of animated gif
		:param delay: delay between frames in the gif animation (float)
		:com = command
		"""
		
		tk.Button.__init__(self, root,activebackground="white",bg="white",**kw)
		self.root = root
		self.gif_file = gif_file
		self.delay = delay  # Animation delay - try low floats, like 0.04 (depends on the gif in question)
		self.stop = False  # Thread exit request flag
		global AnimImg 
		AnimImg  = tk.PhotoImage(file=img_file)
		self.configure(image=AnimImg)
		self._num = 0
		
		
	def start(self):
		""" Starts non-threaded version that we need to manually update() """
		self._animate()

	def stop(self):
		""" This stops the after loop that runs the animation, if we are using the after() approach """
		self.stop = True

	def _animate(self):
		try:
			self.gif = tk.PhotoImage(file=self.gif_file, format='gif -index {}'.format(self._num))  # Looping through the frames
			self.configure(image=self.gif)
			#print(self._num)
			self._num += 1
		except tk.TclError:  # When we try a frame that doesn't exist, we know we have to start over from zero
			#print(self._num)
			self._num = 1
			#self.configure(image=AnimImg)
			#self.stop = True #PLAY ONCE
		if not self.stop:    # If the stop flag is set, we don't repeat
			self.root.after(int(self.delay*1000), self._animate)

