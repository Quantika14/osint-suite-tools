import twint

def search_Twitter(phone):

	print("|--[INFO][TWITTER][>] \n")
	c = twint.Config()
	c.Search = phone
	twint.run.Search(c)