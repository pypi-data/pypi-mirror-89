# -*- coding: utf-8 -*-

import tweepy
from twitter2discord.utils import get_backup_status, get_logger, set_backup_status
from twitter2discord.twitter_stream_listener import TwitterStreamListener

logger = get_logger(__name__)


class Twitter2Discord:
    config = []
    skip_retweets = True
    skip_comments = True

    enabled_translation = True
    config_translation = {'src': 'auto', 'dest': 'en'}

    def custom_translation(self, text):
        return text

    def __init__(self, config=dict, twitter_credential=dict):
        consumer_key = twitter_credential.get('consumer_key', None)
        consumer_secret = twitter_credential.get('consumer_secret', None)
        access_token = twitter_credential.get('access_token', None)
        access_secret = twitter_credential.get('access_secret', None)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        self.config = config
        self._tweepyApi = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    def _twitter_follow_names(self):
        if self.config:
            return [c['twitter_name'] for c in self.config if 'twitter_name' in c]
        return []

    def _twitter_follow_ids(self):
        if self.config:
            return [c['twitter_id'] for c in self.config if 'twitter_id' in c]
        return []

    def _set_latest_status(self, screen_name, status):
        set_backup_status(screen_name, status)

    def _get_latest_status(self, screen_name):
        last_status = get_backup_status(screen_name)
        if not last_status:
            return None
        return last_status

    def check_latest_status(self, limit=50, follow_names=None):
        if follow_names is None:
            follow_names = self._twitter_follow_names()
        if len(follow_names) < 1:
            return
        streamListener = TwitterStreamListener()
        for follow_name in follow_names:
            statuses = []
            since_id = self._get_latest_status(follow_name)
            for status in self._tweepyApi.user_timeline(screen_name=follow_name, since_id=since_id, count=limit):
                if status.get('text', '').startswith('RT @'):
                    continue
                if status.get('in_reply_to_screen_name', None) is not None:
                    continue
                twitter_screen_name = status.get('user', {}).get('screen_name', None)
                if twitter_screen_name != follow_name:
                    continue
                statuses.append(status)
            if len(statuses) > 0:
                self._set_latest_status(follow_name, statuses[0])
                if since_id is not None:
                    _config = [c for c in self.config if c['twitter_name'] == follow_name]
                    for status in statuses:
                        streamListener.send_tweet_to_discord(status, _config[0]['webhook_url'])

    def run(self):
        TWITTER_FOLLOWS = self._twitter_follow_ids()
        streamListener = TwitterStreamListener(follow_ids=TWITTER_FOLLOWS, config=self.config)
        streamListener.skip_retweets = self.skip_retweets
        streamListener.skip_comments = self.skip_comments
        streamListener.enabled_translation = self.enabled_translation
        streamListener.custom_translation = self.custom_translation
        streamListener.config_translation = self.config_translation

        me = self._tweepyApi.me()
        logger.info('me: {} {}'.format(me['name'], me['screen_name']))
        tweepyStream = tweepy.Stream(auth=self._tweepyApi.auth, listener=streamListener)
        tweepyStream.filter(follow=TWITTER_FOLLOWS)

    def loop(self):
        while True:
            try:
                self.run()
            except Exception:
                pass
