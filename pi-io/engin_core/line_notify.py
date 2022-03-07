import requests


class LineNotifyAgentMixIn(object):
    line_url = 'https://notify-api.line.me/api/notify'
    agent_name = 'OR-AGENT'
    token = "LzLFXiJ360riKSr8uQduOxxHY6tiCYxGZanrYltS5Qr"

    def get_line_notify_agent(self):
        return self.agent_name

    def line_notify(self, message, agent=''):
        header = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        try:
            requests.post(self.line_url,
                          headers=header,
                          data={'message': message})
        except Exception as e:
            pass
        return
