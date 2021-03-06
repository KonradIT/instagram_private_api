
from ..common import ApiTestBase, ClientError


class FeedTests(ApiTestBase):

    @classmethod
    def init_all(cls, api):
        return [
            {
                'name': 'test_feed_timeline',
                'test': FeedTests('test_feed_timeline', api)
            },
            {
                'name': 'test_feed_liked',
                'test': FeedTests('test_feed_liked', api)
            },
            {
                'name': 'test_self_feed',
                'test': FeedTests('test_self_feed', api)
            },
            {
                'name': 'test_user_feed',
                'test': FeedTests('test_user_feed', api, user_id='124317')
            },
            {
                'name': 'test_username_feed',
                'test': FeedTests('test_username_feed', api, user_id='maruhanamogu')
            },
            {
                'name': 'test_private_user_feed',
                'test': FeedTests('test_private_user_feed', api, user_id='322244991')
            },
            {
                'name': 'test_reels_tray',
                'test': FeedTests('test_reels_tray', api)
            },
            {
                'name': 'test_user_reel_media',
                'test': FeedTests('test_user_reel_media', api, user_id='329452045')
            },
            {
                'name': 'test_reels_media',
                'test': FeedTests('test_reels_media', api, user_id='329452045')
            },
            {
                'name': 'test_user_story_feed',
                'test': FeedTests('test_user_story_feed', api, user_id='329452045')
            },
            {
                'name': 'test_location_feed',
                'test': FeedTests('test_location_feed', api)
            },
            {
                'name': 'test_feed_tag',
                'test': FeedTests('test_feed_tag', api)
            },
            {
                'name': 'test_saved_feed',
                'test': FeedTests('test_saved_feed', api)
            },
            {
                'name': 'test_feed_popular',
                'test': FeedTests('test_feed_popular', api)
            },
        ]

    def test_feed_liked(self):
        results = self.api.feed_liked()
        self.assertEqual(results.get('status'), 'ok')

    def test_feed_timeline(self):
        results = self.api.feed_timeline()
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('feed_items', [])), 0, 'No items returned.')
        self.assertIsNotNone(results.get('feed_items', [])[0]['media_or_ad'].get('link'))

    def test_feed_popular(self):
        results = self.api.feed_popular()
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('items', [])), 0, 'No items returned.')

    def test_user_feed(self):
        results = self.api.user_feed(self.test_user_id)
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('items', [])), 0, 'No items returned.')

    def test_private_user_feed(self):
        def check_private_user():
            self.api.user_feed(self.test_user_id)
        self.assertRaises(ClientError, check_private_user)

        try:
            check_private_user()
        except ClientError as e:
            self.assertEqual(e.code, 400)

    def test_self_feed(self):
        results = self.api.self_feed()
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('items', [])), 0, 'No items returned.')

    def test_username_feed(self):
        results = self.api.username_feed(self.test_user_id)
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('items', [])), 0, 'No items returned.')

    def test_reels_tray(self):
        results = self.api.reels_tray()
        self.assertEqual(results.get('status'), 'ok')

    def test_user_reel_media(self):
        results = self.api.user_reel_media(self.test_user_id)
        self.assertEqual(results.get('status'), 'ok')

    def test_reels_media(self):
        results = self.api.reels_media([self.test_user_id])
        self.assertEqual(results.get('status'), 'ok')

    def test_feed_tag(self):
        results = self.api.feed_tag('catsofinstagram')
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('items', [])), 0, 'No items returned.')
        self.assertGreater(len(results.get('ranked_items', [])), 0, 'No ranked_items returned.')

    def test_user_story_feed(self):
        results = self.api.user_story_feed(self.test_user_id)
        self.assertEqual(results.get('status'), 'ok')

    def test_location_feed(self):
        results = self.api.feed_location(229573811)
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('items', [])), 0, 'No items returned.')
        self.assertGreater(len(results.get('ranked_items', [])), 0, 'No ranked_items returned.')

    def test_saved_feed(self):
        results = self.api.saved_feed()
        self.assertEqual(results.get('status'), 'ok')
