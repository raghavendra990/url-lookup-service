from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from app.caching.cache import set_cache, get_cache, delete_cache

from app.pynamoModels.url import Url

from app.commons import isGeneratorObjectEmpty

from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class urlInfoDetail(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request, url, query_string):

        logger.info('urlInfoDetail GET - BEGIN')

        key = "url-cache-" + url + query_string

        cache_response = get_cache(key)

        if cache_response:
            logger.info('cache true')
            url_item = cache_response
        else:

            url_items = Url.host_name_query_string_index.query(url, query_string)
            url_item = isGeneratorObjectEmpty(url_items)

            if url_item:
                set_cache(key, url_item)

        if url_item:
            logger.info(url_item)
            url_status = url_item.status

            data = {"status":"SUCCESS", "url_status":url_status, "host": url, "query-string":query_string}
            logger.info(data)

            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {"status":"SUCCESS", "url-status":'not-allowed', "host": url, "query-string":query_string}
            logger.info(data)
            return Response(data, status=status.HTTP_200_OK)

class urlUpdate(APIView):

    renderer_classes = (JSONRenderer,)

    def post(self, request):
        logger.info('urlUpdate GET - BEGIN')

        print(request.data)

        url = request.data.get('host')
        query_string = request.data.get('query-string')
        url_status = request.data.get('url-status')

        current_time = datetime.utcnow()

        uid = str(uuid.uuid4())
        
        key = "url-cache-" + url + query_string

        cache_response = get_cache(key)

        if cache_response:
            logger.info('cache true')
            url_item = cache_response
        else:

            url_items = Url.host_name_query_string_index.query(url, query_string)
            url_item = isGeneratorObjectEmpty(url_items)

            if url_item:
                set_cache(key, url_item)

        if url_item:
            logger.info('url update')
            url_item.update(attributes = {  "name": {"value":url, "action":"put"},
                                            "host_name": {"value":url, "action":"put"},
                                            "query-string": {"value":query_string, "action":"put"},
                                            "status": {"value":status, "action":"put"},
                                            "modified": {"value":current_time, "action":"put"},
                                            "modified_ts": {"value":current_time.timestamp(), "action":"put"},

                })
        else:
            logger.info('url create')
            url_item = Url(uid = uid, 
                            name = url,
                            created = current_time,
                            modified = current_time,
                            created_ts = current_time.timestamp(),
                            modified_ts = current_time.timestamp(),
                            host_name = url, 
                            query_string = query_string,
                            status = url_status
                            )
            url_item.save()

        data = {"status":"SUCCESS"}

        return Response(data, status=status.HTTP_200_OK)
        