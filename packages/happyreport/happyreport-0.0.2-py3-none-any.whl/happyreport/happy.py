import pandas as pd
import json
import os
from happyreport import excel_format
from happyreport import send_mail

class Setting(object):
    def __init__(self, job_url, jobs_from, data_url, save_path, host, port):
        self.job_url = job_url
        self.jobs_from = jobs_from
        self.data_url = data_url
        self.save_path = save_path
        self.host = host
        self.port = port

class MailJob(object):

    def __init__(self, job_id, settings, date):
        self.date = date
        self.settings = settings
        self.jobs_from = settings.jobs_from
        self.jobs_url = settings.job_url
        self.data_url = settings.data_url
        self.job_id = job_id
        self.job = pd.read_sql(f"select * from {self.jobs_from} where job_id = '{job_id}'",
                               settings.job_url).to_dict(orient='series')
        self.job = dict(zip(self.job.keys(), map(lambda x: x.values[0], self.job.values())))
        self.attaches = json.loads(self.job['table_fields'])
        self.save_path = settings.save_path

    def _get_data(self):
        res = []
        for at in self.attaches:
            sub = {"attach_name": at["attach_name"],
                   "data": [],
                   "sheet_names": []}
            for st in at['workbook']:
                sql = f"select {','.join(st['sheet']['select'])} from {st['sheet']['from']} where ds = '{self.date}'"
                print(sql)
                df = pd.read_sql(sql, self.data_url)
                df.columns = st['sheet']["as"]
                sub['data'].append(df)
                sub['sheet_names'].append(st['sheet_name'])
            res.append(sub)
        return res

    def _save(self, data_res):
        for wb in data_res:
            excel_format(wb['data'], wb['sheet_names'], os.path.join(self.save_path, wb["attach_name"]))

    def _send_email(self):
        send_mail(host=self.settings.host,
                  port=self.settings.port,
                  user=self.job['sender_email'],
                  password=self.job['password'],
                  receivers=self.job['receiver_email'].split(","),
                  subject=self.job['job_name'],
                  carbon_copy=self.job['acc_email'].split(","),
                  carbon_copy_mask=self.job['acc_email'].split(","),
                  content=self.job['content'],
                  attaches=[os.path.join(self.save_path, a['attach_name']) for a in self.attaches])

    def run(self):
        data_res = self._get_data()
        self._save(data_res)
        self._send_email()
