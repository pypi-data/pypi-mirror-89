import re
from requests import get

class Meta(object):
	class Emoji:
		def __init__(self, Character: str):
			self.__emote = Character
			self.__meta = get("https://emojipedia.org/{0}".format(self.__emote))
			self.name = self.__meta.text.split('"og:title" content="')[1].split('"')[0][2:]
			self.description = re.sub(re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});"), "", self.__meta.text.split('Emoji Meaning</h2>\n')[1].split("<h2>"
)[0]).replace("\n\n", "").replace("\n", " ")
			self.aliases = [Element[1:].split("<")[0] for Element in self.__meta.text.split("</h2>\n<ul>\n")[1].split("</span>")[1:]]
			self.url = self.__meta.url