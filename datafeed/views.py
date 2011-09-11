import math
from django.conf import settings
from django.db import models as base_models
from django.http import HttpResponseRedirect, HttpResponse
from djangotoolbox import http

from datafeed import models as df_models

def state_data_check(request):
    year = request.REQUEST.get('year', None)
    state_code = request.REQUEST.get('state', None)
    if not year or not state_code:
        return False
    has_data = False
    try:
        has_data = df_models.StateData.objects.filter(state__code=state_code, year=year)
    except:
        pass 
    return not has_data


SUPPORTED_ENTITIES = {
    'column': df_models.Column,
    'state': df_models.State,
    'state_data': df_models.StateData
}

PREINSERT_CHECKS = {
    'state_data': state_data_check
}

class SpitColumns(http.RESTBase):

    def get(self, request, *args, **kwargs):
        states = request.REQUEST.get('states', '').split(',')
        fields = request.REQUEST.get('fields', '').split(',')

        valid_state_object = [df_models.CODE2STATE_MAP[x.strip()] for x in states
                              if x.strip() in df_models.CODE2STATE_MAP]

        valid_data_columns = [x.strip() for x in fields
                              if x.strip() in df_models.CODE2COLUMN_MAP]
                
        resp = {}
        resp['columns'] = [{'title': 'State', 'desc':'State'}]
        for column_code in valid_data_columns:
            column = df_models.CODE2COLUMN_MAP[column_code]
            resp['columns'].append({'title': column.name,
                                    'desc': column.description})
        
        raw_data = []
        IN_LIMIT = 30
        for i in range(0, math.ceil(len(valid_state_object)/IN_LIMIT)):
            in_st = valid_state_object[i*IN_LIMIT:i*IN_LIMIT + IN_LIMIT]
            if not in_st: break
            raw_data.extend(df_models.StateData.objects.filter(state__in=in_st))

        resp['data'] = []
        for row in raw_data:
            requested_data = [row.state.code]
            for column_code in valid_data_columns:
                requested_data.append(getattr(row, column_code))
            resp['data'].append(requested_data)

        return http.JSONResponse(resp)

    def post(self, request):
        entity_name = request.REQUEST.get('datafeed_entity', '').lower()

        if entity_name not in SUPPORTED_ENTITIES:
            return http.JSONResponse({'status': 'failed', 'reason': 'Unsupported/missing entity.'})

        entity = SUPPORTED_ENTITIES[entity_name]()
        for field in entity._meta.fields:
            value = request.REQUEST.get(field.name, None)
            if isinstance(field, base_models.ForeignKey):
                if value:
                    value = field.rel.to.objects.get(pk=value)
            try:
                setattr(entity, field.name, value)
            except ValueError as e:
               return http.JSONResponse({'status': 'failure', 'reason': unicode(e)}) 

        if entity_name in PREINSERT_CHECKS:
            if not PREINSERT_CHECKS[entity_name](request):
                return http.JSONResponse({'status': 'failure', 'reason': 'Invalid\duplicating Data'})

        try:
            entity.save()
        except Exception as e:
            return http.JSONResponse({'status': 'failure', 'reason': unicode(e)}) 

        return http.JSONResponse({'status': 'success'})                 

spit_columns = SpitColumns()
