import os
import requests
import click
from halo import Halo

from wave_cli import COMMAND_NAME


class Backend:
    def __init__(self, context):
        self.ctx = context
        self.base_url = self.ctx.obj['base_url']
        self.access_token = self.ctx.obj['access_token']
        self.client_id = 'default'
        self.query_params = {'clientId': self.client_id, 'code': self.access_token}

    def sync_cache(self):
        endpoint = self.base_url + '/verify-token'
        if 'access_token' not in self.ctx.obj:
            access_token = click.prompt('Your Access Token', type=click.STRING)
            self.ctx.obj['access_token'] = access_token
        else:
            access_token = self.ctx.obj['access_token']
        spinner = Halo(spinner='dots3', text_color='cyan')
        try:
            spinner.start(text='Syncing')
            res = requests.get(url=endpoint, params=self.query_params)
            if res.status_code == 200:
                spinner.succeed(text='voila! synchronized')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! Access Token is Invalid')
                self.ctx.obj.pop('access_token', None)
                return self.sync_cache()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['errorMessage']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def register_device(self, data):
        endpoint = self.base_url + '/registry/devices'
        spinner = Halo(spinner='dots3', text_color='cyan').start(text='Registering')
        try:
            res = requests.post(url=endpoint, json=data, params=self.query_params)
            if res.status_code == 201:
                device = res.json()
                spinner.succeed(text='voila! {} device registered successfully'.format(device['environment']))
                return device
            elif res.status_code == 401:
                spinner.fail(text='oops!! Access Token is Invalid. Run `{} sync --access-token [Your Access Token]` to Refresh Token.'
                             .format(COMMAND_NAME))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['errorMessage']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def get_error_flags(self):
        endpoint = self.base_url + '/error-flags'
        spinner = Halo(spinner='dots3', text_color='cyan')
        try:
            spinner.start('Fetching')
            res = requests.get(url=endpoint, params=self.query_params)
            if res.status_code == 200:
                spinner.succeed(text='Fetched')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! Access Token is Invalid. Run `{} sync --access-token [Your Access Token]` to Refresh Token.'
                             .format(COMMAND_NAME))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['errorMessage']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def get_devices_list(self, query_filter={}):
        endpoint = self.base_url + '/devices'
        spinner = Halo(spinner='dots3', text_color='cyan')
        try:
            spinner.start('Fetching')
            params = {**self.query_params, **query_filter}
            res = requests.get(url=endpoint, params=params)
            if res.status_code == 200:
                spinner.succeed(text='Fetched')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! Access Token is Invalid. Run `{} sync --access-token [Your Access Token]` to Refresh Token.'
                             .format(COMMAND_NAME))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['errorMessage']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def update_devices(self, data={}):
        endpoint = self.base_url + '/update-devices'
        spinner = Halo(spinner='dots3', text_color='cyan')
        try:
            spinner.start('Running')
            res = requests.post(url=endpoint, params=self.query_params, json=data)
            if res.status_code == 200:
                spinner.succeed(text='Result:')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! Access Token is Invalid. Run `{} sync --access-token [Your Access Token]` to Refresh Token.'
                             .format(COMMAND_NAME))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['errorMessage']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def reboot_devices(self, query_filter={}):
        endpoint = self.base_url + '/reboot-device-command'
        spinner = Halo(spinner='dots3', text_color='cyan')
        try:
            spinner.start('Running')
            params = {**self.query_params, **query_filter}
            res = requests.get(url=endpoint, params=params)
            if res.status_code == 200:
                spinner.succeed(text='Result:')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! Access Token is Invalid. Run `{} sync --access-token [Your Access Token]` to Refresh Token.'
                             .format(COMMAND_NAME))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['errorMessage']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def reset_service(self, query_filter={}):
        endpoint = self.base_url + '/reset-service-command'
        spinner = Halo(spinner='dots3', text_color='cyan')
        try:
            spinner.start('Running')
            params = {**self.query_params, **query_filter}
            res = requests.get(url=endpoint, params=params)
            if res.status_code == 200:
                spinner.succeed(text='Result:')
                return res.json()
            elif res.status_code == 401:
                spinner.fail(text='oops!! Access Token is Invalid. Run `{} sync --access-token [Your Access Token]` to Refresh Token.'
                             .format(COMMAND_NAME))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['errorMessage']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def delete_device(self, query_filter={}):
        endpoint = self.base_url + '/delete-device'
        spinner = Halo(spinner='dots3', text_color='cyan')
        try:
            spinner.start('Deleting device {0}'.format(
                'with deviceId ' + query_filter['deviceId'] if query_filter['deviceId'] else 'with serialNumber ' + query_filter['serialNumber'])
            )
            params = {**self.query_params, **query_filter}
            res = requests.get(url=endpoint, params=params)
            if res.status_code == 204:
                spinner.succeed('voila! succeed')
            elif res.status_code == 404:
                spinner.fail(text='oops!! {0}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 401:
                spinner.fail(text='oops!! Access Token is Invalid. Run `{} sync --access-token [Your Access Token]` to Refresh Token.'
                             .format(COMMAND_NAME))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['errorMessage']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def request_device_logs(self, body):
        endpoint = self.base_url + '/request-device-logs'
        params = {**self.query_params}
        spinner = Halo(spinner='dots3', text_color='cyan').start('Preparing logs')
        try:
            res = requests.post(url=endpoint, json=body, params=params)
            if res.status_code == 200:
                spinner.succeed('Prepared')
                return res.json()
            elif res.status_code == 404:
                spinner.fail(text='oops!! {0}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 401:
                spinner.fail(text='oops!! Access Token is Invalid. Run `{} sync --access-token [Your Access Token]` to Refresh Token.'
                             .format(COMMAND_NAME))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['errorMessage']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()

    def download_device_logs(self, blob_name):
        endpoint = self.base_url + '/download-device-logs'
        params = {**self.query_params, "blobName": blob_name}
        spinner = Halo(spinner='dots3', text_color='cyan').start('Downloading logs')
        try:
            res = requests.get(url=endpoint, params=params)
            if res.status_code == 200:
                file = res.content
                spinner.succeed('Downloaded')
                local_path = os.path.expanduser("~/Desktop")
                local_file_path = blob_name.replace('/', '_')
                download_file_path = os.path.join(local_path, local_file_path)
                with open(download_file_path, 'wb+') as download_file:
                    download_file.write(file)
                return download_file_path
            elif res.status_code == 404:
                spinner.fail(text='oops!! {0}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 401:
                spinner.fail(text='oops!! Access Token is Invalid. Run `{} sync --access-token [Your Access Token]` to Refresh Token.'
                             .format(COMMAND_NAME))
                exit()
            elif res.status_code == 422:
                spinner.fail(text='oops!! Unprocessable!: {}'.format(res.json()['errorMessage']))
                exit()
            elif res.status_code == 400:
                spinner.fail(text='oops!! {}'.format(res.json()['errorMessage']))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(text='oops!! Connection Error. Make sure you are connected to Internet.')
            exit()
        except requests.Timeout as e:
            spinner.fail(text='oops!! Timeout Error')
            exit()
        except requests.RequestException as e:
            spinner.fail(text='oops!! General Error')
            exit()
        except KeyboardInterrupt:
            spinner.fail(text='Someone closed the program')
            exit()
