from itertools import cycle
import copy
import math
import random
import time
from music import Music, Jazz
import sys
import os
	
class PianoKeys(Jazz):

	def __init__(self):
		super().__init__()

		self.__C_scale()
		pass


	def __C_scale(self):
		'''
		Terminal outout
		single scale C major
		'''

		s = """
		|   | |  | |   |   | |  | |  | |   
		|   | |  | |   |   | |  | |  | |   
		|   | |  | |   |   | |  | |  | |   
		|   |_|  |_|   |   |_|  |_|  |_|   
		|    |    |    |    |    |    |    
		|    |    |    |    |    |    |    
		|    |    |    |    |    |    |    """ #  (1 3 3 2 3 3 1 3 3 2 3 2 3 3 1) / (5 5 5 5 5 5 1)

		self.layout_raw = [list(l.strip('\t')) for l in s.split('\n')]

		self.key_hit_pos = {
		1: (6, 1+2),
		3: (6, 1+4+1+2),
		5: (6, 1+4+1+4+1+2),
		6: (6, 1+4+1+4+1+4+1+2),
		8: (6, 1+4+1+4+1+4++1+4+1+2),
		10: (6, 1+4+1+4+1+4++1+4++1+4+1+2),
		12: (6, 1+4+1+4+1+4++1+4++1+4++1+4+1+2),

		2: (3, 1+3+1),
		4: (3, 1+3+3+2+1),		
		7: (3, 1+3+3+2+3+3+1+3+1),
		9: (3, 1+3+3+2+3+3+1+3+3+2+1),
		11: (3, 1+3+3+2+3+3+1+3+3+2+3+2+1)
		}

	def __layout_print(self, keynotes, rep=1):
		"""
		print the keyboard layout with notes, on multiple scales
		
		:param keynotes: list; in scale key name - e.g. C major C D E F ...
		:param rep: how many scales to repeat, especially for scales not starting at C
		:return 
		"""

		layout_mapped = copy.deepcopy(self.layout_raw)

		for note in keynotes:
			note_inx = self.key_loc[note]
			row, col = self.key_hit_pos[note_inx]
			layout_mapped[row][col] = 'O'

		for l in layout_mapped:
			for i in range(rep):
				print(''.join(l), end='')
			print('\t')   # works better than \n

		return 

	def on_notes(self, keynotes, rep):
		"""

		"""
		self.__layout_print(keynotes, rep=rep)


class ChordTerminal():
	def __init__(self):
		pass

	def __chord_terminal_output(self, chord_root, chord_name):
		"""
		use unix bash tool figlet
		e.g.
		"figlet -f ./big.flf GbM7"
		"""

		chord_output = {
		"M": 'M',
		"m": 'm',
		"Aug": '+',
		"M7": 'M7',
		"m7": 'm7',
		"7": '7',
		"7dim": '^o', 
		"7half-dim": '^phi',
		}
		#chord_root output as is
		print('\n\n\n\n\n\n\n\n')
		os.system("figlet -f big ___%s%s__"%(chord_root, chord_output[chord_name]))
		print('\n\n\n\n\n\n\n\n')
	
	def run(self, chord_root_set, chord_name_set, N, time_interval):
		"""
		"""
		for i in range(N):
			chord_root = random.choice(chord_root_set)
			chord_name = random.choice(chord_name_set)
			self.__chord_terminal_output(chord_root, chord_name)
			time.sleep(time_interval)



class Tasks(Music):
	def __init__(self):
		super().__init__()
		pass

	def chord_scale_generation(self, chord_sheet, root_change_to):
		"""
		Output the scale given chords, terminal will output the keybord layout

		:params chord_sheet: [('C', 'Aug')]
		:params root_change_to: 'D'
		"""

		musicFactory = Jazz()  # for music theory computations
		piano = PianoKeys() # given the notes, generate the layout on keyboard and print in the terminal

		print_chord = True  
		print_scale = True 

		for chord_root, chord_name in chord_sheet:
			print("%s%s moved to %s" % (chord_root, chord_name, root_change_to))

			if print_chord:
				notes = musicFactory.key_change_chord(chord_name, chord_root, root_change_to)  # do the computations
				piano.on_notes(notes, rep=3)
			
			if print_scale:	
				scale_name = musicFactory.scale_given_chord(chord_name)
				print("Displaying %s on %s" % (scale_name, root_change_to))

				scale_root = chord_root
				notes = musicFactory.key_change_scale(scale_name, scale_root, root_change_to)  # do the computations				
				piano.on_notes(notes, rep=3)

	def chord_random(self, N, time_interval, chord_root_set=[], chord_name_set=[]):
		"""
		Randomly generate N chords from a chord_root_set x chord_type_set each staying for time_interval secs
		"""
		generator = ChordTerminal()
		if chord_root_set == []:
			chord_root_set = list(self.key_loc.keys())

		if chord_name_set == []:
			chord_name_set = list(self.chords.keys())

		print(chord_root_set, chord_name_set)
		generator.run(chord_root_set, chord_name_set, N, time_interval)



if __name__ == "__main__":

	Tasks_factory = Tasks()
	# Tasks_factory.chord_random(20, 4)
	Tasks_factory.chord_scale_generation([('C', 'Aug')], 'D')




