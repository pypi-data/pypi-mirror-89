import requests, re, json


def scrape(id, lang="de", upload=False):
	if lang == "en":
		langWeb = "com"
	else:
		langWeb = "de"
	website = requests.get("https://www.anisearch.{}/anime/{}".format(langWeb, id), headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"})
	if website.status_code != 200:
		return {"id": id, "error": True}
	else:
		dictionary = {"id": id, "error": False}
		sc = website.text
	sc_relations = requests.get("https://www.anisearch.{}/anime/{}/relations".format(langWeb, id), headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"}).text

	# Japanese Dictionary
	try:
		jap_dict = re.findall('<li><div class="title" lang="(?:ja|hk|id|my|kp|ph|sg|kr|tw|th|vn|cn)">.*?<\/li>', sc)[0]
	except:
		jap_dict = None

	# Japanese Name
	try:
		if jap_dict == None:
			raise Exception
		dictionary["jap"] = re.findall('<img src="https:\/\/cdn\.anisearch\.(?:de|com)\/media\/country\/.{2}\.png" class="flag" alt=".*?" title=".*?"> <strong>(.*?)<\/strong>', jap_dict)[0]
	except:
		dictionary["jap"] = None

	# Japanese Kanji
	try:
		if jap_dict == None:
			raise Exception
		dictionary["kan"] = re.findall('<img src="https:\/\/cdn\.anisearch\.(?:de|com)\/media\/country\/.{2}\.png" class="flag" alt=".*?" title=".*?"> <strong>.*?<\/strong> <div class="grey">(.*?)<\/div>', jap_dict)[0]
	except:
		dictionary["kan"] = None

	# Japanese Status
	try:
		if jap_dict == None:
			raise Exception
		dictionary["japstat"] = re.findall('<div class="status"><span class="grey">Status:<\/span> (.*?)<\/div>', jap_dict)[0]
	except:
		dictionary["japstat"] = None

	# Japanese Dates
	try:
		if jap_dict == None:
			raise Exception
		dates = re.findall('<div class="released"><span class="grey">(?:Veröffentlicht|Release Date):<\/span> (.*?)<\/div>', jap_dict)[0]
		dates = dates.replace("&#8209;", "-")
		if dates == "?":
			raise Exception
		dates = dates.split(" - ")
		dictionary["japstart"] = dates[0]
		if dates[1] == "?":
			dictionary["japend"] = None
		else:
			dictionary["japend"] = dates[1]

	except:
		dictionary["japstart"] = None
		dictionary["japend"] = None

	# Japanese Studio

	try:
		if jap_dict == None:
			raise Exception
		studios = re.findall('<span class="grey">Studio:<\/span>(.*?)<\/div>', jap_dict)[0]
		dictionary["japstudios"] = re.findall('<a.*?>(.*?)<\/a>', studios)

	except:
		dictionary["japstudios"] = []

	# English Dictionary
	try:
		eng_dict = re.findall(
			'<li><div class="title" lang="en">.*?<\/li>',
			sc)[0]
	except:
		eng_dict = None

	# English name
	try:
		if eng_dict == None:
			raise Exception
		dictionary["eng"] = re.findall('<img src="https:\/\/cdn\.anisearch\.(?:de|com)\/media\/country\/en\.png" class="flag" alt=".*?" title=".*?"> .*?<strong>(.*?)<\/strong>', eng_dict)[0]
	except:
		dictionary["eng"] = None

	# English Status
	try:
		if eng_dict == None:
			raise Exception
		dictionary["engstat"] = re.findall('<div class="status"><span class="grey">Status:<\/span> (.*?)<\/div>', eng_dict)[0]
	except:
		dictionary["engstat"] = None

	# English Dubbed
	try:
		if eng_dict == None:
			raise Exception
		dictionary["engdub"] = len(re.findall('<span class="speaker" title=".*?">', eng_dict)) > 0
	except:
		dictionary["engdub"] = False

	# English Dates
	try:
		if eng_dict == None:
			raise Exception
		dates = re.findall('<div class="released"><span class="grey">(?:Veröffentlicht|Release Date):<\/span> (.*?)<\/div>', eng_dict)[0]
		dates = dates.replace("&#8209;", "-")
		if dates == "?":
			raise Exception
		dates = dates.split(" - ")
		dictionary["engstart"] = dates[0]
		if dates[1] == "?":
			dictionary["engend"] = None
		else:
			dictionary["engend"] = dates[1]
	except:
		dictionary["engstart"] = None
		dictionary["engend"] = None

	# English Publisher
	try:
		if eng_dict == None:
			raise Exception
		studios = re.findall('<span class="grey">Publisher:<\/span>(.*?)<\/div>', eng_dict)[0]
		dictionary["engstudios"] = re.findall('<a.*?>(.*?)<\/a>', studios)

	except:
		dictionary["engstudios"] = []

	# German Dictionary
	try:
		ger_dict = re.findall(
			'<li><div class="title" lang="de">.*?<\/li>',
			sc)[0]
	except:
		ger_dict = None

	# German name
	try:
		if ger_dict == None:
			raise Exception
		dictionary["ger"] = re.findall('<img src="https:\/\/cdn\.anisearch\.(?:de|com)\/media\/country\/de\.png" class="flag" alt=".*?" title=".*?"> .*?<strong>(.*?)<\/strong>', ger_dict)[0]
	except:
		dictionary["ger"] = None

	# German Status
	try:
		if ger_dict == None:
			raise Exception
		dictionary["gerstat"] = re.findall('<div class="status"><span class="grey">Status:<\/span> (.*?)<\/div>', ger_dict)[0]
	except:
		dictionary["gerstat"] = None

	# German Dubbed
	try:
		if ger_dict == None:
			raise Exception
		dictionary["gerdub"] = len(re.findall('<span class="speaker" title=".*?">', ger_dict)) > 0
	except:
		dictionary["gerdub"] = False

	# German Dates
	try:
		if ger_dict == None:
			raise Exception
		dates = re.findall('<div class="released"><span class="grey">(?:Veröffentlicht|Release Date):<\/span> (.*?)<\/div>', ger_dict)[0]
		dates = dates.replace("&#8209;", "-")
		if dates == "?":
			raise Exception
		dates = dates.split(" - ")
		dictionary["gerstart"] = dates[0]
		if dates[1] == "?":
			dictionary["gerend"] = None
		else:
			dictionary["gerend"] = dates[1]
	except:
		dictionary["gerstart"] = None
		dictionary["gerend"] = None

	# German Publisher
	try:
		if ger_dict == None:
			raise Exception
		studios = re.findall('<span class="grey">Publisher:<\/span>(.*?)<\/div>', ger_dict)[0]
		dictionary["gerstudios"] = re.findall('<a.*?>(.*?)<\/a>', studios)

	except:
		dictionary["gerstudios"] = []

	# Synonyms Dictionary
	try:
		syn_dict = re.findall(
			'<div class="synonyms"><span class="grey">(?:Synonyme|Synonyms):<\/span> (.*?)<\/div>',
			sc)[0]
		synonyms = syn_dict.split(', <span class="grey">')
		synonyms_str = "SPLITHERE".join(synonyms)
		if synonyms_str.endswith("</span>"):
			synonyms_str = synonyms_str[:-7]
		synonyms = synonyms_str.split("</span>, ")
		synonyms_str = "SPLITHERE".join(synonyms)
		dictionary["syn"] = synonyms_str.split("SPLITHERE")
	except:
		dictionary["syn"] = []

	# Description
	try:
		desc = re.findall('<span itemprop="description" lang="(?:de|en)" id="desc-(?:de|en)" class="desc-zz textblock">(.*?)<\/span>', sc)[0]
		desc = desc.replace("<br />", "\n")
		desc = re.sub("\<.*?\>", '', desc)
		dictionary["description"] = desc
	except:
		dictionary["description"] = None

	# Typ
	try:
		type = re.findall('<li><span>(?:Typ|Type)<\/span>(.*?)<\/li>', sc)[0]
		if type == "Unknown" or type == "Unbekannt":
			dictionary["type"] = None
		else:
			dictionary["type"] = type
	except:
		dictionary["type"] = None

	# Time
	try:
		dictionary["time"] = re.findall('datetime=".*?">(\d*)min<\/time>', sc)[0]
	except:
		dictionary["time"] = None
	# Episodes
	try:
		eps = re.findall('<span>(?:Episoden|Episodes)<\/span>(.*?)(?: |<\/li>)', sc)[0]
		if ">?<" in eps:
			dictionary["episodes"] = None
		else:
			dictionary["episodes"] = eps
	except:
		dictionary["episodes"] = None
	# Date
	dictionary["date"] = {}
	try:
		date = re.findall('<meta itemprop="dateCreated" content="(.*?)">', sc)[0]
		date = date.split("-")
		if date[0] != "0000":
			dictionary["date"]["year"] = date[0]
		else:
			dictionary["date"]["year"] = None
		if date[1] != "00":
			dictionary["date"]["month"] = date[1]
		else:
			dictionary["date"]["month"] = None
		if date[2] != "00":
			dictionary["date"]["day"] = date[2]
		else:
			dictionary["date"]["day"] = None
	except:
		dictionary["date"]["year"] = None
		dictionary["date"]["month"] = None
		dictionary["date"]["day"] = None
	# Country
	try:
		origin = re.findall('<span>(?:Herkunft|Country of Origin)<\/span>(.*?)<\/li>', sc)[0]
		if ">-<" in origin:
			dictionary["origin"] = None
		else:
			dictionary["origin"] = origin
	except:
		dictionary["origin"] = None
	# Adaption
	try:
		adaption_of = re.findall('<span>(?:Adaptiert von|Adapted From)<\/span>(.*?)<\/li>', sc)[0]
		if ">-<" in adaption_of:
			dictionary["adaption_of"] = None
		else:
			dictionary["adaption_of"] = adaption_of
	except:
		dictionary["adaption_of"] = None
	# TargetGroup
	try:
		targetgroup = re.findall('<span>(?:Zielgruppe|Target Group)<\/span>(.*?)<\/li>', sc)[0]
		if ">-<" in targetgroup:
			dictionary["targetgroup"] = None
		else:
			dictionary["targetgroup"] = targetgroup
	except:
		dictionary["targetgroup"] = None

	dictionary["genres"] = {}
	# Main Genre
	genre_main = re.findall('href="anime\/genre\/main\/.*?\" class=\"gg showpop\" data-tooltip=\".*?\">(.*?)<\/a><\/li>', sc)
	for i in range(len(genre_main)):
		genre_main[i] = genre_main[i].replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&nbsp;", " ").replace("\/", "/").replace("&#039;", "\'")
	dictionary["genres"]["genre_main"] = genre_main

	# Sub Genre
	genre_sub = re.findall('href="anime\/genre\/subsidiary\/.*?\" class=\"gc showpop\" data-tooltip=\".*?\">(.*?)<\/a><\/li>', sc)
	for i in range(len(genre_sub)):
		genre_sub[i] = genre_sub[i].replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&nbsp;", " ").replace("\/", "/").replace("&#039;", "\'")
	dictionary["genres"]["genre_sub"] = genre_sub

	# Tags
	tags = re.findall('href="anime\/index\/.*?\" class=\"gt showpop\" data-tooltip=\".*?\">(.*?)<\/a><\/li>', sc)
	for i in range(len(tags)):
		tags[i] = tags[i].replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&nbsp;", " ").replace("\/", "/").replace("&#039;", "\'")
	dictionary["genres"]["tags"] = tags

	# Hentai Tags
	tags = re.findall('href="anime\/index\/.*?\" class=\"gh showpop\" data-tooltip=\".*?\">(.*?)<\/a><\/li>', sc)
	for i in range(len(tags)):
		tags[i] = tags[i].replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&nbsp;", " ").replace("\/", "/").replace("&#039;", "\'")
	dictionary["genres"]["hentai_tags"] = tags

	# Image
	link = re.findall('<figure id="cover-container"><img itemprop="image" src="(.*?)" alt=".*?" title=".*?" id="details-cover">', sc)[0]
	if link.endswith("/0.jpg"):
		dictionary["img"] = None
	else:
		int_id = int(id)
		link = "https://cdn.anisearch.{}/images/anime/cover/full/{}/{}.jpg".format(langWeb, int_id // 1000, int_id)
		dictionary["img"] = link

	# Hoster
	if upload != False:
		if dictionary["img"] == None:
			dictionary["hoster"] = None
		elif upload == "imgur":
			imgurReply = json.loads(requests.post("https://api.imgur.com/3/upload", headers={"Authorization": "Client-ID 54a331a8b74a2ea"}, data={"image": link, "type": "url"}).text)
			dictionary["hoster"] = imgurReply["data"]["link"]
		elif upload == "imgbb":
			try:
				import time
				s = requests.session()
				getAuthToken = s.get("https://imgbb.com/").text
				authToken = re.findall('PF\.obj\.config\.auth_token="(.*?)";', getAuthToken)[0]
				linkDict = json.loads(s.post("https://imgbb.com/json", data={"source": link, "type": "url", "action": "upload", "timestamp": str(int(time.time())), "auth_token": authToken}).text)
				dictionary["hoster"] = linkDict["image"]["url"]
			except:
				raise
				dictionary["hoster"] = "imgbb_error"
		else:
			dictionary["hoster"] = None
	else:
		dictionary["hoster"] = None

	# Rating
	dictionary["rating"] = {}
	stars = re.findall('<div class="value">(.*?)<\/div>', sc)
	dictionary["rating"]["1"] = int(stars[0].replace(".", ""))
	dictionary["rating"]["2"] = int(stars[1].replace(".", ""))
	dictionary["rating"]["3"] = int(stars[2].replace(".", ""))
	dictionary["rating"]["4"] = int(stars[3].replace(".", ""))
	dictionary["rating"]["5"] = int(stars[4].replace(".", ""))

	# Rating Average
	try:
		dictionary["rating_average"] = re.findall('<span itemprop="ratingValue">(\d.\d\d) = \d+%<\/span>', sc)[0]
	except:
		dictionary["rating_average"] = None

	# Relations
	dictionary["relations"] = {}
	dictionary["relations"]["anime"] = {}
	dictionary["relations"]["manga"] = {}
	try:
		relations = json.loads(re.findall('<div id="flowchart" data-mode="full" data-graph="(\{.*?\})">', sc_relations)[0].replace("&quot;", '"'))
		for i in relations["nodes"]["anime"]:
			dictionary["relations"]["anime"][relations["nodes"]["anime"][i]["title"].split("&lt;span")[0]] = relations["nodes"]["anime"][i]["url"].split("/")[-1].split(",")[0]
		for i in relations["nodes"]["manga"]:
			dictionary["relations"]["manga"][relations["nodes"]["manga"][i]["title"].split("&lt;span")[0]] = relations["nodes"]["manga"][i]["url"].split("/")[-1].split(",")[0]
	except:
		pass
	return dictionary



