import re
from requests import get
from emoji import emojize, demojize

class Utils(object):
	def get_image(Character: str, Info: dict = {"Vendor": "Version"}):
		"""Gets an emoji image based on `Character` and `Info`."""
		Character	=	emojize(Character, use_aliases = True)
		##
		Code	=	""
		Vendor	=	list(Info.keys())[0].lower()
		Version	=	list(Info.values())[0]
		Image_Size	=	144
		#---#
		if Vendor == "vendor":		Vendor = None
		if Version == "version":	Version = None
		#---#
		##- Table -##
		# Replacements (Unused)
		if Vendor == "instagram":	Vendor = "facebook"
		if Vendor == "linkedin":	Vendor = "samsung"
		if Vendor == "nintendo":	Vendor = "openmoji"
		if Vendor == "roblox":		Vendor = "openmoji"
		# Replacements (Vendors)
		if Vendor == "discord": 	Vendor = "twitter";		Code = "windows-";	Version = "13.0.1"
		if Vendor == "skype": 		Vendor = "microsoft";	Code = "windows-";	Version = "10"
		if Vendor == "slack": 		Vendor = "google";		Code = "android-";	Version = "8.1"
		if Vendor == "snapchat":	Vendor = "apple";		Code = "ios-";		Version = "9.3"
		if Vendor == "telegram":	Vendor = "apple";		Code = "ios-";		Version = "9.3"
		# Aliases
		if Vendor == "android":		Vendor = "google"
		if Vendor == "ios":			Vendor = "apple"
		if Vendor == "windows":		Vendor = "microsoft"
		if Vendor == "twemoji": 	Vendor = "twitter"
		# Auto-assigned
		if Vendor == "messenger":	Version = "1.0"
		if Vendor == "mozilla":		Version = "2.5"
		#---#
		if Vendor == "au-kddi":		Code = "type-";	Version = "-".join(list(Version))
		if Vendor == "htc":			Code = "sense-"	
		if Vendor == "lg":			Code = "G"
		if Vendor == "twitter":		Code = "twemoji-"
		#---#
		if Vendor == "apple":
			Vendor = Vendor;		Code = "ios-"
			if Version == "2.2":	Code = "iphone-os-"
		if Vendor == "google":
			Vendor = Vendor;		Code = "android-"
			if Version.startswith("10.0-m20fd"):	Version = "10.0-march-2020-feature-drop"
			if Version.startswith("gmail"):	Code = "";	Version = "gmail"
		if Vendor == "microsoft":
			Vendor = Vendor;	Code = "windows-"
			#---#
			if Version == "10may19":Version = "10-may-2019-update"
			if Version == "10oct18":Version = "10-october-2018-update"
			if Version == "10apr18":Version = "10-april-2018-update"
			if Version == "10fc":	Version = "10-fall-creators-update"
			if Version == "10c":	Version = "10-creators-update"
			if Version == "10a":	Version = "10-anniversary-update"
			if Version == "10":		Version = "10"
			if Version == "8.1":	Version = "8.1"
			if Version == "8.0":	Version = "8.0"
		if Vendor == "samsung":
			Vendor = Vendor;	Code = "one-ui-"
			#---#
			if Version.startswith("experience"):	Code = "experience-";	Version = Version.split("experience")[-1]
			if Version.startswith("touchwiz"):		Code = "touchwiz-";		Version = Version.split("touchwiz")[-1]
		#-----#
		Style_Page = get("https://emojipedia.org/{0}/{1}{2}".format(
		Vendor, Code, Version if Version != "latest" else ""))
		if Style_Page.status_code != 200: raise ValueError(Info)

		for Link in re.findall("(?P<url>https?://[^\s]+)", Style_Page.text):
			if str(Image_Size) in Link:
				if Character.encode("unicode-escape").decode()[5:] in Link:
					return Link

	def center_image(Image_URL: str):
		"""Centers visible emoji image."""
		from PIL import Image
		im = Image.open(get(Image_URL, stream = True).raw)
		im = im.crop(im.getbbox())
		im2 = Image.new("RGBA", (im.size[0] if im.size[0] > im.size[1] else im.size[1],) * 2, (0,) * 4)
		im2.paste(im, ((im2.size[0] - im.size[0]) // 2, (im2.size[1] - im.size[1]) // 2), im)
		return im2