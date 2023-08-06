from emoji import emojize, demojize, UNICODE_EMOJI

class Emoji(object):
	def __init__(self, Name: str):
		self.unicode = [Emoji for Emoji in emojize(Name, use_aliases = True) if Emoji in UNICODE_EMOJI.keys()][0]
		self.shortcode = demojize(self.unicode)
		self.codepoints = [
			emojize(self.unicode).encode("unicode-escape").upper(),
			"U+{0}".format(self.unicode).encode("unicode-escape").decode().upper().split("0")[-1],
			]