import concurrent.futures
import re
import logging

logger = logging.getLogger(__name__)

class XNSRecord:

    def __init__(self, CLOUDXNS, domain_id):
        self.xns = CLOUDXNS
        self.domain_id = domain_id
        self._data = self._get_domain_host_list()
        self.data = []
        self.result = []

    def _get_domain_host_list(self):
        return self.xns.domain_host_list(self.domain_id)['hosts']

    def _get_record_list(self, host_id):
        record = self.xns.domain_host_record_list(self.domain_id, host_id=host_id)['data']
        return record[0] if isinstance(record, list) else record

    def filter_host(self, name):
        data = [i for i in self._data if re.match(f'.*{name}.*', i['host'])]
        self.data = self.data + data
        return data



    def filter_site(self, name):
        data = [i for i in self._data if re.match(f'.*{name}[^\d].*', i['host'])]
        self.data = self.data + data
        return data

    def get_record_list(self):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._get_record_list, d['id']) for d in self.data]
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    self.result.append(result)
                except Exception as exc:
                    print('generated an exception: %s' % (exc))


class FilterRecord:

    def __init__(self, CLOUDXNS) -> object:
        self.xns = CLOUDXNS
        self.data = []
        self._filter_result = []


    @property
    def result(self):
        recordlist = [i for i in self._filter_result if i['status'] == 'ok']
        return [{'name': host['host'], 'value': host['value'], 'line': host['line_zh'],'type':host['type'], 'status': '生效中'} for host in recordlist]


    def filter_type(self,type):
        self._filter_result = [i for i in self._filter_result if i['type'] == type]
        return self._filter_result


    def filter_value(self,name):
        for i in self.data:
            if name in i['value']:
                self._filter_result.append(i)


    def filter_site_xns(self, domain_id_list, namelist):

        for domain_id in domain_id_list:
            xns = XNSRecord(CLOUDXNS=self.xns,domain_id=domain_id)
            for name in namelist:
                xns.filter_site(name=name)
            xns.get_record_list()
            # self.data = self.data + xns.result
            for i in xns.result:
                self.data.append(i)

        return self.data



    def filter_value_xns(self, domain_id_list):

        for domain_id in domain_id_list:
            xns = XNSRecord(CLOUDXNS=self.xns,domain_id=domain_id)
            xns.get_record_list()
            # self.data = self.data + xns.result
            for i in xns.result:
                self.data.append(i)

        return self.data

    def filter_name_xns(self, domain_id_list, namelist):

        for domain_id in domain_id_list:
            xns = XNSRecord(CLOUDXNS=self.xns, domain_id=domain_id)
            for name in namelist:
                xns.filter_host(name=name)
            xns.get_record_list()

            # self.data = self.data + xns.result
            for i in xns.result:
                self.data.append(i)

        return self.data




