import twint

def search_Twitter(target):

	print("|--[INFO][TWITTER][>] \n")
	c = twint.Config()
	c.Search = target
	twint.run.Search(c)
