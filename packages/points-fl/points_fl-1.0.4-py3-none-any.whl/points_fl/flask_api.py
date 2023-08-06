import json

import requests

from points_fl.base import Base


class FlaskAPI(Base):

    def horizontal_predict(self, service_id, x=None, file=None):
        url = f'http://{self._flask_ip_address}/api/services/horizontal/{service_id}'
        data = json.dumps({'x': x}) if x else None
        files = {'file': file} if file else None

        return requests.post(url=url, data=data, files=files, headers=self._headers)

    def vertical_predict(self, service_id, uid=None, file=None):
        url = f'http://{self._flask_ip_address}/api/services/vertical/{service_id}'
        data = json.dumps({'uid': uid}) if uid else None
        files = {'file': file} if file else None

        return requests.post(url=url, data=data, files=files, headers=self._headers)

    def recommendation_predict(self, service_id, uid=None, rec_num=None):
        url = f'http://{self._flask_ip_address}/api/services/recommendation/{service_id}'
        data = json.dumps({'uid': uid, 'rec_num': rec_num})

        return requests.post(url=url, data=data,  headers=self._headers)