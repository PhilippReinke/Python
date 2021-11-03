import requests

links = open("links.txt", "r").read().splitlines()

for idx, link in enumerate(links):
	# isolate file type
	fileType = link[link.rfind("."):]
	idxQuestionMark = fileType.rfind("?")
	if idxQuestionMark != -1:
		fileType = fileType[:idxQuestionMark]

	# download file and save it
	targetFolder = "files/"
	r = requests.get(link, allow_redirects=True)
	open(targetFolder + str(idx) + fileType, "wb").write(r.content)

	#
	print("Got %i / %i" % (idx+1, len(links)))