import os
from requests import get
from platform import system

def search(phrase: str, version: int) -> list:
	"""Returns list of possible dialogs found on soundofgothic.pl"""
	Response = get("https://soundofgothic.pl/text?filter={0}&versions={1}".format(phrase, version), timeout = (3, 25)).text
	Counter = 1
	List = []
	while 1:
		try:
			Response1 = Response.split("app-collector")[1][23:].split("records")[Counter].split('sc6="">')[1]
			Counter += 1
		except IndexError:
			break
		List.append({
		"Content": Response1.split("<!---->")[1].split("<!---->")[0][1:-1],
		"Section" if version != 3 else "Name": Response1.split("Plik")[1].split("</")[0][:-1] if version != 3 else Response1.split('"filesource">')[1][1:].split("</a>")[0][:-1],
		"URL": Response1.split('src="')[1].split('"')[0],
		"File": Response1.split('src="')[1].split('"')[0].split("/")[-1],
		"Version": len(Response1.split("version")[1][10:].split("<br")[0][:-1]),
		})
	return List

def download(url: str, path: str):
	"""Downloads dialog from given URL to given path."""
	local_filename = url.split("/")[-1]
	os.chdir(path)
	with get(url, stream = True) as Response:
		with open(local_filename, "wb") as File:
			for chunk in Response.iter_content(chunk_size = 1024): 
				File.write(chunk)
	return print("{0}{1}{2}".format(os.getcwd(), "/" if system() != "Windows" else "\\", local_filename))

class Find:
	"""Dialog finding utilities."""
	class URL:
		def by_content(list_: list, contains: str) -> list:
			"""Tries to locate all sound URLs that are matching with the `contains` argument."""
			return [Element["URL"] for Element in list_ if contains in Element["Content"]][0]
	class File:
		def by_content(list_: list, contains: str) -> list:
			"""Tries to locate all sound filenames that are matching with the `contains` argument."""
			return [Element["File"] for Element in list_ if contains in Element["Content"]][0]