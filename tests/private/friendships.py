import unittest

from ..common import (
    ApiTestBase, compat_mock
)


class FriendshipTests(ApiTestBase):

    @classmethod
    def init_all(cls, api):
        return [
            {
                'name': 'test_autocomplete_user_list',
                'test': FriendshipTests('test_autocomplete_user_list', api)
            },
            {
                'name': 'test_autocomplete_user_list_mock',
                'test': FriendshipTests('test_autocomplete_user_list_mock', api)
            },
            {
                'name': 'test_user_following',
                'test': FriendshipTests('test_user_following', api, user_id='124317')
            },
            {
                'name': 'test_user_followers',
                'test': FriendshipTests('test_user_followers', api, user_id='124317')
            },
            {
                'name': 'test_friendships_show',
                'test': FriendshipTests('test_friendships_show', api, user_id='329452045')
            },
            {
                'name': 'test_friendships_show_many',
                'test': FriendshipTests('test_friendships_show_many', api, user_id='329452045')
            },
            {
                'name': 'test_friendships_show_many2',
                'test': FriendshipTests('test_friendships_show_many', api, user_id=['329452045', '124317'])
            },
            {
                'name': 'test_friendships_pending',
                'test': FriendshipTests('test_friendships_pending', api)
            },
            {
                'name': 'test_friendships_create',
                'test': FriendshipTests('test_friendships_create', api)
            },
            {
                'name': 'test_friendships_create_mock',
                'test': FriendshipTests('test_friendships_create_mock', api)
            },
            {
                'name': 'test_friendships_destroy',
                'test': FriendshipTests('test_friendships_destroy', api)
            },
            {
                'name': 'test_friendships_destroy_mock',
                'test': FriendshipTests('test_friendships_destroy_mock', api)
            },
            {
                'name': 'test_friendships_block',
                'test': FriendshipTests('test_friendships_block', api, user_id='2958144170')
            },
            {
                'name': 'test_friendships_block_mock',
                'test': FriendshipTests('test_friendships_block_mock', api, user_id='2958144170')
            },
        ]

    @unittest.skip('Heavily throttled.')
    def test_autocomplete_user_list(self):
        results = self.api.autocomplete_user_list()
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('users', [])), 0, 'No users returned.')

    @compat_mock.patch('instagram_private_api.Client._call_api')
    def test_autocomplete_user_list_mock(self, call_api):
        call_api.return_value = {
            'status': 'ok', 'users': [
                {'pk': 100, 'profile_pic_url': ''},
                {'pk': 200, 'profile_pic_url': ''},
            ]}
        self.api.autocomplete_user_list()
        call_api.assert_called_with('friendships/autocomplete_user_list/',
                                    query={'followinfo': 'True', 'version': '2'})

    def test_user_following(self):
        results = self.api.user_following(self.test_user_id)
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('users', [])), 0, 'No users returned.')
        self.assertIsNotNone(results.get('users', [])[0].get('id'), 'Is not patched.')

    def test_user_followers(self):
        results = self.api.user_followers(self.test_user_id)
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('users', [])), 0, 'No users returned.')
        self.assertIsNotNone(results.get('users', [])[0].get('id'), 'Is not patched.')

    def test_friendships_pending(self):
        results = self.api.friendships_pending()
        self.assertEqual(results.get('status'), 'ok')

    def test_friendships_show(self):
        results = self.api.friendships_show(self.test_user_id)
        self.assertEqual(results.get('status'), 'ok')

    def test_friendships_show_many(self):
        results = self.api.friendships_show_many(self.test_user_id)
        self.assertEqual(results.get('status'), 'ok')
        self.assertGreater(len(results.get('friendship_statuses', [])), 0, 'No statuses returned.')

    @unittest.skip('Modifies data.')
    def test_friendships_create(self):
        results = self.api.friendships_create('2958144170')
        self.assertEqual(results.get('status'), 'ok')
        self.assertEqual(results.get('friendship_status', {}).get('following'), True)

    @compat_mock.patch('instagram_private_api.Client._call_api')
    def test_friendships_create_mock(self, call_api):
        call_api.return_value = {
            'status': 'ok',
            'friendship_status': {'following': True}}
        user_id = '2958144170'
        params = {'user_id': user_id, 'radio_type': self.api.radio_type}
        params.update(self.api.authenticated_params)
        self.api.friendships_create(user_id)
        call_api.assert_called_with(
            'friendships/create/%(user_id)s/' % {'user_id': user_id},
            params=params)

    @unittest.skip('Modifies data.')
    def test_friendships_destroy(self):
        results = self.api.friendships_destroy('2958144170')
        self.assertEqual(results.get('status'), 'ok')
        self.assertEqual(results.get('friendship_status', {}).get('following'), False)

    @compat_mock.patch('instagram_private_api.Client._call_api')
    def test_friendships_destroy_mock(self, call_api):
        call_api.return_value = {'status': 'ok', 'following': False}
        user_id = '2958144170'
        params = {'user_id': user_id, 'radio_type': self.api.radio_type}
        params.update(self.api.authenticated_params)
        self.api.friendships_destroy(user_id)
        call_api.assert_called_with(
            'friendships/destroy/%(user_id)s/' % {'user_id': user_id},
            params=params)

    @unittest.skip('Modifies data.')
    def test_friendships_block(self):
        results = self.api.friendships_block(self.test_user_id)
        self.assertEqual(results.get('status'), 'ok')
        self.assertTrue(results.get('blocking'))

    @compat_mock.patch('instagram_private_api.Client._call_api')
    def test_friendships_block_mock(self, call_api):
        call_api.return_value = {'status': 'ok', 'blocking': True}
        user_id = '2958144170'
        params = {'user_id': user_id}
        params.update(self.api.authenticated_params)
        self.api.friendships_block(user_id)
        call_api.assert_called_with(
            'friendships/block/%(user_id)s/' % {'user_id': user_id},
            params=params)
