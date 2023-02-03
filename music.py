from itertools import cycle
import copy
import math

class Music(object):

	def __init__(self):
		self.twelve_keys = []  # in note name
		self.key_uni = {} # note name: note name in twelve keys
		self.key_loc = {} # note name: 1-12, C as 1
		self.chords = {} # chord name: notes on root C
		self.scales = {} # scale name: a mapping on some root, not necessarily C as root

		self.__key_conversion()
		self.__chords_gen()
		self.__scale_gen()
		pass

	def __key_conversion(self):		
		self.twelve_keys = ['C', 'Db', 'D', 'Eb', 'E', 'F', 
		                'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

		self.key_uni = {
		"Cb": 'B',
		"C":  'C', 
		"C#": 'Db',
		"Db": 'Db',
		"D":  'D', 
		"D#": 'Eb',
		"Eb": 'Eb',
		"E":  'E', 
		"E#": 'F',
		"Fb": 'E',
		"F":  'F',
		"F#": 'Gb',
		"Gb": 'Gb', 
		"G":  'G',
		"G#": 'Ab', 
		"Ab": 'Ab',
		"A":  'A',
		"A#": 'Bb',
		"Bb": 'Bb', 
		"B":  'B',
		"B#": 'C',
		#
		"Bbb": 'A',
		}  # change all other names to self.twelve_keys, only to keep uniform

		self.key_loc = {
		"Cb": 12,
		"C":  1, 
		"C#": 2,
		"Db": 2,
		"D":  3, 
		"D#": 4,
		"Eb": 4,
		"E":  5, 
		"E#": 6,
		"Fb": 5,
		"F":  6,
		"F#": 7,
		"Gb": 7, 
		"G":  8,
		"G#": 9, 
		"Ab": 9,
		"A":  10,
		"A#": 11,
		"Bb": 11, 
		"B":  12,
		"B#": 1,
		#
		"Bbb": 10,
		}  # used in key layout 

	def __chords_gen(self):
		"""
		pos on root C
		"""

		self.chords = {
		"M": ['C', 'E', 'G'],
		"m": ['C', 'Eb', 'G'],
		"Aug": ['C', 'E', 'G#'],
		"M7": ['C', 'E', 'G', 'B'],
		"m7": ['C', 'Eb', 'G', 'Bb'],
		"7": ['C', 'E', 'G', 'Bb'],
		"7dim": ['C', 'Eb', 'Gb', 'Bbb'], 
		"7half-dim": ['C', 'Eb', 'Gb', 'Bb'],
		}

	def __scale_gen(self):

		"""
		pos on root C
		"""

		major_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
		melodic_minor_scale = ['C', 'D', 'Eb', 'F', 'G', 'A', 'B']

		self.scales = {
		# Major modes

		'Ionian':     major_scale[0:] + major_scale[:0],
		'Dorian':     major_scale[1:] + major_scale[:1], 
		'Phrygian':   major_scale[2:] + major_scale[:2],
		'Lydian':     major_scale[3:] + major_scale[:3],
		'Mixolydian': major_scale[4:] + major_scale[:4],
		'Aeolian':    major_scale[5:] + major_scale[:5],
		'Locrian':    major_scale[6:] + major_scale[:6],

		# Melodic minor modes
		'melod_m_1': melodic_minor_scale[0:] + melodic_minor_scale[:0],
		'melod_m_2': melodic_minor_scale[1:] + melodic_minor_scale[:1],
		'melod_m_3': melodic_minor_scale[2:] + melodic_minor_scale[:2],
		'melod_m_4': melodic_minor_scale[3:] + melodic_minor_scale[:3],
		'melod_m_5': melodic_minor_scale[4:] + melodic_minor_scale[:4],
		'melod_m_6': melodic_minor_scale[5:] + melodic_minor_scale[:5],
		'melod_m_7': melodic_minor_scale[6:] + melodic_minor_scale[:6],

		# Diminished scales
		'half/whole': ['C', 'Db', 'Eb', 'E', 'F#', 'G', 'A', 'Bb'],
		'whole/half': ['C', 'D', 'Eb', 'F', 'Gb', 'Ab', 'A', 'B'], 

		# whole tone
		'C_whole': ['C', 'D', 'E', 'F#', 'G#', 'A#'],
		'C#_whole': ['Db', 'Eb', 'F', 'G', 'A', 'B'],

		# 



		}

	def __key_change_steps(self, ori_key, to_key):
		"""
		:param ori_key e.g. 'C'
		:param to_key e.g. 'E'
		"""
		key_change = self.twelve_keys.index(self.key_uni[to_key]) - \
		                    self.twelve_keys.index(self.key_uni[ori_key])

		return key_change
		
	def __key_change_single(self, ori_note, key_change):
		"""
		move ori_note up key_change steps

		:param ori_note: e.g. 'C',
		:param key_change: int, 0-11
		:return : number of steps to take (could be negative)
		"""

		note_key = self.twelve_keys[(self.twelve_keys.index(self.key_uni[ori_note]) + key_change) % 12]		
		
		return note_key

	def __notes_map(self, map_onset, notes_root, key_change):
		"""
		:param map_onset: e.g. ['C#', 'F', 'A'], the chord map stored in the system
		:param notes_root: e.g. 'C', the root of the user given set of notes (i.e. chords) 
		:param ori_root: the root note of this chord/scale; the scale should differ in root and key if is mode
		:param key_change: int, 0-11; from ori_root to desired key
		:return : number of steps to take (could be negative)
		"""
		map_on_root = []
		
		root_change_internal = self.__key_change_steps(map_onset[0], notes_root)
		key_change += root_change_internal   # from the system stored map on some key, to the key desired

		for n in map_onset:
			note = self.__key_change_single(n, key_change)
			map_on_root.append(note)
		
		return map_on_root

			
	def key_change_chord(self, chord_name, chord_root, root_change_to):
		"""
		for chords
		"""
		steps = self.__key_change_steps(chord_root, root_change_to)
		map_onset = self.chords[chord_name]
		notes = self.__notes_map(map_onset, chord_root, steps)

		return notes
	
	def key_change_scale(self, scale_name, scale_root, root_change_to):
		"""
		for scales and modes; 
		"""
		steps = self.__key_change_steps(scale_root, root_change_to)
		map_onset = self.scales[scale_name]		
		notes = self.__notes_map(map_onset, scale_root, steps)

		return notes


class Jazz(Music):
	def __init__(self):

		super().__init__()
		self.chord_scale = {}  # chord name: [scale name], e.g. '7dim': [half/whole]

		self.__chord_scale_gen()

	def __chord_scale_gen(self):
		"""

		"""

		self.chord_scale = {

		'Aug': ['melod_m_3'],
		"M7": ['Ionian', 'Lydian'],
		"m7": ['Dorian', 'Aeolian', 'half/whole', 'melod_m_2'],
		"7": ['Mixolydian', 'half/whole', 'melod_m_4', 'melod_m_5'],
		"7dim": ['half/whole', 'whole/half'], 
		"7half-dim": ['Locrian', 'half/whole', 'melod_m_6', 'melod_m_7'],
		'mM7': ['melod_m_1'],

		}  # only input the chord-scale you want to use

	def scale_given_chord(self, chord):
		""""""
		scale = self.chord_scale[chord][0]

		return scale


	