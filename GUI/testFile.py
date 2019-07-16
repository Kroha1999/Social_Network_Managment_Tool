import instaloader
from instaloader import Profile


L = instaloader.Instaloader()
L.load_session_from_file('_bod.ka',"sessions\\_bod.ka.se")
print(L.test_login())
print(L.get_hashtag_posts('#cat'))
