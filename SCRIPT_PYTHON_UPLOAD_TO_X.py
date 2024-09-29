import tweepy
import sys
import shutil
import os
import json

# initialisation
DEST_FOLDER = r"C:\AI_TEMP_UPLOAD\_AI_UPLOAD_X\done"

# Obtenir le chemin absolu du répertoire contenant le script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin complet vers le fichier JSON
credentials_path = os.path.join(script_dir,'twitter_credentials.json')

# Charger les clés et tokens d'accès depuis le fichier JSON
with open(credentials_path, 'r') as file:
    credentials = json.load(file)

consumer_key = credentials['consumer_key']
consumer_secret = credentials['consumer_secret']
access_token = credentials['access_token']
access_token_secret = credentials['access_token_secret']

# Initialisation du client Tweepy avec l'API Twitter v2
client = tweepy.Client(consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

# AUTOMATIC
# Lecture des arguments : Texte du tweet et chemins des images
tweet_text = sys.argv[1]  # Premier argument après le nom du script
image_paths = sys.argv[2:]  # Tous les arguments après le texte du tweet

# DEBUG MANUEL (décommenter pour tester manuellement)
# tweet_text = "#Eevin #SkeletonKnight #AIFANART"
# image_paths = [r"C:\AI_TEMP_UPLOAD\_AI_UPLOAD_X\ToonGenAI_00060927.png",
#                r"C:\AI_TEMP_UPLOAD\_AI_UPLOAD_X\ToonGenAI_00060928.png",
#                r"C:\AI_TEMP_UPLOAD\_AI_UPLOAD_X\ToonGenAI_00060929.png"]

# Authentification avec l'API v1 pour l'upload des images
tweepy_auth = tweepy.OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
tweepy_api_for_image = tweepy.API(tweepy_auth)

# Chargement et collecte des ID des médias
media_ids = []
for image_path in image_paths:
    media = tweepy_api_for_image.media_upload(image_path)
    media_ids.append(media.media_id_string)
    # Déplacement des fichiers
    shutil.move(image_path, os.path.join(DEST_FOLDER, os.path.basename(image_path)))

# Création et envoi du tweet avec les images
response = client.create_tweet(text=tweet_text, media_ids=media_ids)

# Affichage de la réponse
print(response)
