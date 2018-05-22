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
    		print('cache_response', cache_response)
    		url_item = cache_response
    	else:
    		
	    	url_items = Url.host_name_query_string_index.query(url, query_string)
	    	url_item = isGeneratorObjectEmpty(url_items)

	    	if url_item:
	    		set_cache(key, url_item)

    	if url_item:
    		url_status = url_item.status

    		data = {"status":"SUCCESS", "url_status":url_status, "host": url, "query-string":query_string}
    		logger.info(data)

    		return Response(data, status=status.HTTP_200_OK)

    	else:
    		data = {"status":"SUCCESS", "url_status":'not-allowed', "host": url, "query-string":query_string}
    		logger.info(data)
    		return Response(data, status=status.HTTP_200_OK)
    	
    	