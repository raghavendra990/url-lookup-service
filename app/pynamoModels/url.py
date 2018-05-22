from __future__ import print_function
from django.db import models

from pynamodb.models import Model
from pynamodb.attributes import (
    ListAttribute, UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, BooleanAttribute
)
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

from config import config_data

# Attendance
class Url_GSI_host_name(GlobalSecondaryIndex):
    class Meta:
        index_name = 'host-name-query-string-index'
        projection = AllProjection()
        read_capacity_units = 1
        write_capacity_units = 1
    host_name = UnicodeAttribute(hash_key = True, attr_name = 'host-name')
    query_string = UnicodeAttribute(range_key = True, attr_name = 'query-string')

class Url(Model):
    class Meta:
        table_name = config_data['dynamodb']['table_url']
        region = config_data['dynamodb']['region']
        host = "http://localhost:8000"
        read_capacity_units = 1
        write_capacity_units = 1
    uid = UnicodeAttribute(hash_key = True)
    active = NumberAttribute( default = 1)
    typ = UnicodeAttribute(attr_name = 'type', default = 'url', null = True)
    name = UnicodeAttribute(null = True)
    created = UTCDateTimeAttribute(null = True)
    modified = UTCDateTimeAttribute(null = True)
    created_ts = NumberAttribute(attr_name = 'created-ts', null = True)
    modified_ts = NumberAttribute(attr_name = 'modified-ts', null = True)
    host_name = UnicodeAttribute(attr_name = 'host-name')
    query_string = UnicodeAttribute(attr_name = 'query-string')
    status = UnicodeAttribute()
    host_name_query_string_index = Url_GSI_host_name()


