import tweepy

def lambda_handler(event, context):
    """
    Gets user profiles and retrieves x most recent tweets from user.
    Check the tweet so see if it contains an image or a url -- if so retweet it
    if not catch the error
    if the tweet is already retweeted, go to the next user
    :param users:
    :return:
    """

    consumer_key = "jX85ExJrQmPYNIvNpLR9YDwz2"
    consumer_secret = "X6soUnOcsck2FX6p5e8cxpMLebf5ZK4Jw5pUkOHIJpySwYdkoy"
    access_token = "1283953081487699968-UM40wFGhGsCekHCDbkgqsoSj7FK5RG"
    access_token_secret = "gibgEJ8LKWbmIMKT91yyBOIcyroJmyJFDrsMUwX2msgAB"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        print("Error creating API")
        raise e
    print("API created")

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

    # Validate that
    valid_users = []
    for user in users:
        try:
            api.get_user(screen_name=user)
        except tweepy.TweepError as e:
            if 'User not found.' or 'User has been suspended.' in e:
                print(e)
            else:
                break
        else:
            valid_users.append(user)

    try:
        for user in valid_users:
            for tweet in tweepy.Cursor(api.user_timeline, user).items(1):
                try:
                    if tweet.retweeted is False:
                        if tweet.entities['media'] is not None:
                            print(f" Retweeting {tweet.text} from {user}.")
                            api.retweet(tweet.id)
                except KeyError as e:
                    try:
                        if (tweet.entities['urls'] is not None) and (tweet.in_reply_to_user_id is None):
                            print(f" Retweeting {tweet.text} from {user}.")
                            api.retweet(tweet.id)
                    except KeyError as e:
                        print(f' This tweet from {user} does not contain an image or url')
    except tweepy.TweepError as e:
        print("Error on getting user information")




