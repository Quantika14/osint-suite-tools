from facebook_scraper import get_posts

def get_postsFB(target):
    try:
        for post in get_posts(target, pages=1):
            print(f"|----[INFO][FACEBOOK][URL][>] {post['post_url']} TIME: {post['time']}")
            print(f"|--------[INFO][FACEBOOK][TEXT][>] {post['text'][:100]}")
            #print(f"|--------[INFO][FACEBOOK][REACTIONS][>] {post['reactions']}")
    
    except Exception as e:
        print(f"|----[WARNING][FACEBOOK][>] Error... {e}")