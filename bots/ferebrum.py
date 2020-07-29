import tweepy
import logging
from config import consumer_key, consumer_token, access_secret, access_token_secret


def lambda_handler(event, context):
    """
    Gets user profiles and retrieves x most recent tweets from user.
    Check the tweet so see if it contains an image or a url -- if so retweet it
    if not catch the error
    if the tweet is already retweeted, go to the next user
    :param users:
    :return:
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")

    users = ['archillect',
             'CyberpunkIsNow',
             'everycolorbot',
             'HomeDecorPic',
             'artistbasquiat',
             'archdaily',
             'wayback_exe',
             'artistsofcolour',
             'HomeAdore',
             'ThrowbackHoops',
             'ModernNotoriety',
             'pablocubist',
             'teemusphoto',
             'noealz',
             'interiorsofine'
             ]


    try:
        for user in users:
            for tweet in tweepy.Cursor(api.user_timeline, user).items(1):
                try:
                    if tweet.retweeted is True:
                        continue
                    elif tweet.retweeted is False:
                        if tweet.entities['media'] is not None:
                            logger.info(f" Retweeting {tweet.text} from {user}.")
                            api.retweet(tweet.id)
                except KeyError as e:
                    try:
                        if (tweet.entities['urls'] is not None) and (tweet.in_reply_to_user_id is None):
                            logger.info(f" Retweeting {tweet.text} from {user}.")
                            api.retweet(tweet.id)
                    except KeyError as e:
                        logger.error(f' This tweet from {user} does not contain an image or url', exc_info=True)
    except tweepy.TweepError as e:
        logger.error("Error on getting user information", exc_info=True)




