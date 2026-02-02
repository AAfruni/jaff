import os
import sys

import numpy as np


class Photochemistry:
	# ****************
	def __init__(self):
		self.xsecs = {}

		self.load_xsecs_leiden()

	# ****************
	def load_xsecs_leiden(self):
		from glob import glob

		folder = os.path.join(os.path.dirname(__file__), "data", "xsecs")

		for fname in glob(folder + "/*.dat"):
			# take last commented line as header, remove #, and split by spaces
			with open(fname) as f:
				header = (
					[x for x in f.readlines() if x.startswith("#")][-1]
					.lower()
					.replace("#", "")
					.strip()
					.split()
				)
			header = [x for x in header if x != ""]

			# get the name of the file without path and extension, i.e. the reaction name in the form R__P_P
			frea = os.path.basename(fname).split(".")[0]

			rrs = frea.split("__")[0].split("_")
			pps = frea.split("__")[1].split("_")

			rea_serialized = "_".join(sorted(rrs)) + "__" + "_".join(sorted(pps))

			# count the charges in the reactants and products
			rcharge = np.sum([x.count("+") for x in rrs])
			pcharge = np.sum([x.count("+") for x in pps])

			# determine if the reaction is dissociation or ionization
			if pcharge > rcharge:
				mode = "ion"
			else:
				mode = "dis"

			# determine the index of the read and wave columns
			iread = iwave = None
			for i, h in enumerate(header):
				if mode in h:
					iread = i
				if "wave" in h:
					iwave = i

			if iread is None or iwave is None:
				print("ERROR: could not find read or wave in header of %s" % fname)
				sys.exit(1)

			data = np.loadtxt(fname, comments="#").T

			clight = 2.99792458e10  # cm/s
			hplanck = 6.62607015e-27  # erg s

			energy = clight * hplanck / (data[iwave].astype(float) * 1e-7)  # nm -> erg
			xs = data[iread].astype(float)  # cm^2

			self.xsecs[rea_serialized] = {"energy": energy, "xsecs": xs}

	# ****************
	# returns a dictionary with keys "energy" and "xsecs"
	# energy in erg, xsecs in cm^2
	def get_xsec(self, reaction):
		if reaction.serialized not in self.xsecs:
			print(
				"ERROR: reaction %s not found in photochemistry data."
				% reaction.serialized
			)
			print("Add the file to the data/xsecs folder as %s.dat" % reaction.serialized)
			sys.exit(1)

		return self.xsecs[reaction.serialized]
