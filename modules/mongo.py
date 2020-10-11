from pymongo import MongoClient

#Conexión con la base de datos
con = MongoClient()
db = con.Dante

def news_insertMongoDB(target, url, title, autor, text, date, top_image, movies, html):

    data = {"target": target, "url":url, "title":title, "autor":autor, "text":text, "date":date, "top_image":top_image, "movies":movies, "html":html}

    x = db.DG.find_one({"url":url})

    if x:

        print(f"|----[DB][>] Found URL in DB -> {url}")
        pass
    else:

        db.DG.insert(data)
        print(f"|----[DB][>] Insert INFO in DB-> {url}")

def personalData_Wikipedia_insertMongoDB(target, data, url, option):

    if option == 1:
        data = {"target": target, "birth":data, "url": url}

        x = db.DG.find_one({"birth":data})

        if x:
            pass

        else:
            db.DG.insert(data)

    elif option == 2:
        data = {"target": target, "death":data, "url": url}

        x = db.DG.find_one({"death":data})

        if x:
            pass

        else:
            db.DG.insert(data)

    elif option == 3:
        data = {"target": target, "horoscopo":data, "url": url}

        x = db.DG.find_one({"horoscopo":data})

        if x:
            pass

        else:
            db.DG.insert(data)

    elif option == 4:
        data = {"target": target, "employment":data, "url": url}

        x = db.DG.find_one({"employment":data})

        if x:
            pass

        else:
            db.DG.insert(data)

    elif option == 5:
        data = {"target": target, "religion":data, "url": url}

        x = db.DG.find_one({"religion":data})

        if x:
            pass

        else:
            db.DG.insert(data)

    elif option == 6:
        data = {"target": target, "sons":data, "url": url}

        x = db.DG.find_one({"sons":data})

        if x:
            pass

        else:
            db.DG.insert(data)

    elif option == 7:
        data = {"target": target, "political party":data, "url": url}

        x = db.DG.find_one({"political party":data})

        if x:
            pass

        else:
            db.DG.insert(data)

def companies_insertMongoDB(target, companies):

    data = {"target": target, "companies":data}

    x = db.DG.find_one({"url":url})

    if x:
        
        print(f"|----[DB][>] Found URL in DB -> {url}")
        pass
    else:

        db.DG.insert(data)
        print(f"|----[DB][>] Insert INFO in DB-> {url}")

#BUSCADORES
def find_in_BOE(target):

    cursor = db.DG_BOE.find({"texto": {"$regex": target, "$options":"i"}})
    if cursor:
        for x in cursor:
            print("|----[INFO][BOE][>] Looking for the target in the BOE...")
            print("|--------[INFO][BOE][TITLE][>]" + x.get("titulo"))
            print("|--------[INFO][BOE][TEXT][>]" + x.get("texto"))
            print("|--------[INFO][BOE][SOURCE][>]" + x.get("identificador"))
    else:
        print("|----[INFO][BOE][>] The target has not been found in the BOE. Maybe you need to create or update database 'DG_BOE'... ")
