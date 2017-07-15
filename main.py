import json
from datetime import datetime

import spotipy
import spotipy.util as util


def dump_to_file(filename, playlists):
    with open(filename, 'w') as playlists_file:
        playlists_file.write(json.dumps(playlists))


def get_playlists(token, username):
    sp = spotipy.Spotify(auth=token)

    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] != username:
            print(playlist)
            continue

        results = sp.user_playlist(username, playlist['id'],
                                   fields='tracks,next')

        tracks = results['tracks']
        playlist['tracksList'] = []

        while True:
            playlist['tracksList'] += tracks['items']

            if not tracks['next']:
                break

            tracks = sp.next(tracks)

        yield playlist


def main(spotify_api_config, username, filename):
    token = util.prompt_for_user_token(
        username,
        scope='playlist-read-private',
        client_id=spotify_api_config['client_id'],
        client_secret=spotify_api_config['client_secret'],
        redirect_uri=spotify_api_config['redirect_uri']
    )

    if not token:
        print('Unable to get token for user: {}'.format(username))

    playlists = get_playlists(token, username)

    dump_to_file(filename, list(playlists))


if __name__ == '__main__':
    spotify_api_config = {
        'client_id': 'YOUR-SPOTIFY-CLIENT-ID',
        'client_secret': 'YOUR-SPOTIFY-CLIENT-SECRET',
        'redirect_uri': 'YOUR-APP-REDIRECT-URI'
    }
    username = 'YOUR-USERNAME'
    filename = 'spotify-playlists_{}.json'.format(
        datetime.now().strftime('%Y-%m-%d'))

    main(spotify_api_config, username, filename)
