from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from djangotoolbox import http

from datafeed import models as df_models

class SpitColumns(http.RESTBase):

    def get(self, request, *args, **kwargs):
        states = request.REQUEST.get('states', '').split(',')
        fields = request.REQUEST.get('fields', '').split(',')

        valid_state_object = [df_models.CODE2STATE_MAP[x.strip()] for x in states
                              if x.strip() in df_models.CODE2STATE_MAP]

        valid_data_columns = [x.strip() for x in fields
                              if x.strip() in df_models.CODE2COLUMN_MAP]
                
        resp = {}
        resp['columns'] = []
        for column_code in valid_data_columns:
            column = df_models.CODE2COLUMN_MAP[column_code]
            resp['columns'].append({'title': column.name,
                                    'desc': column.description})
        

        raw_data = df_models.StateData.objects.filter(state__in = valid_state_object)

        resp['data'] = []
        for row in raw_data:
            requested_data = [row.state.code]
            for column_code in valid_data_columns:
                requested_data.append(getattr(row, column_code))
            resp['data'].append(requested_data)

        resp = {"data": [["CA", "CA gas #1", "CA coal #1"], 
                         ["PA", "PA gas #1", "PA coal #1"]], 
                "columns":[{"desc": "", "title": "Gas"}, 
                           {"desc": "", "title": "Coal"}]}

        return http.JSONResponse(resp)

spit_columns = SpitColumns()
