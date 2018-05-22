import redis
from redis.exceptions import RedisError, ConnectionError

import sys
import json
import logging
import _pickle as pickle

ttl_seconds = 86400

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

from config import config_data

r = redis.StrictRedis(host=config_data['redis']['host'], port=6379)
ttl_seconds = 86400

def delete_cache(key):
    logger.info("delete_cache ")

    try:
        resp = r.delete(key)
        logger.debug('delete_cache: ' + key)
        logger.debug(resp)

    except (RedisError, ConnectionError):
        logger.exception(sys.exc_info())
        return False

def set_cache(key, value , score= False  ):
    try:
        if score == False:
            value = pickle.dumps(value)
            r.set(key, value)
            r.expire(key, ttl_seconds)
            logger.info("set cache: " + str(key) )
        else:
            value = pickle.dumps(value)
            r.zadd(key, score ,  value )
            r.expire(key, ttl_seconds)
            logger.info("set cache: " + str(key) )
    except (RedisError, ConnectionError):
        logger.exception(sys.exc_info())
        return False

def get_cache(key, past=0, future=0 , withscores= False):
    try:
        response = r.get(key)
        if response is None:
            return False
        else:
            response = pickle.loads(response)
            logger.info("get_cache: "+ str(response))
            return response
    except RedisError:
        logger.exception(sys.exc_info())
        return False