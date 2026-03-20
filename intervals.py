import requests


class IntervalsAPI:

    def __init__(self, api_key: str):
        """Constructor method

        :param api_key: Intervals ICU API key
        :type api_key: str
        """
        self.api_key = api_key

    def get_activity(self, activity_id: str, fpath: str) -> None:
        """Gets FIT file by activity ID and saves to given location.

        :param activity_id: The ID of the activity to retrieve
        :type activity_id: str
        :param fpath: Where to save FIT
        :type fpath: str 
        :raises ValueError: If the response is not a valid FIT file
        :return: The FIT file as bytes
        :rtype: bytes
        """
        url = f'https://intervals.icu/api/v1/activity/{activity_id}/file'
        response = requests.get(url, auth=('API_KEY', self.api_key))

        content_type = response.headers['Content-Type']

        if response.status_code != 200:
            raise ValueError(f"Failed to get activity: {response.text}")

        with open(fpath, 'wb') as f:
            f.write(response.content)

    def put_activity(self, fpath: str) -> None:
        """Uploads a FIT file to Intervals.

        :param fpath: The path to the FIT file to upload
        :type fpath: str
        :raises ValueError: If the response is not successful
        """
        url = 'https://intervals.icu/api/v1/athlete/0/activities'

        with open(fpath, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, auth=(
                'API_KEY', self.api_key), files=files)

        if response.status_code != 201:
            raise ValueError(f"Failed to upload activity: {response.text}")

    def delete_activity(self, activity_id: str) -> None:
        """Deletes an activity by ID.

        :param activity_id: The ID of the activity to delete
        :type activity_id: str
        :raises ValueError: If the response is not successful
        """
        url = f'https://intervals.icu/api/v1/activity/{activity_id}'
        response = requests.delete(url, auth=('API_KEY', self.api_key))

        if response.status_code != 200:
            raise ValueError(f"Failed to delete activity: {response.text}")
