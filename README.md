# url-lookup-service

## Installation guide

- Install redis [https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298)
- Amazon Dynamodb for database, to run your application locally you can use [dynalite](http://pynamodb.readthedocs.io/en/latest/local.html#running-dynalite)
- [Python 3.6](https://www.python.org/downloads/release/python-360/)
- [Django 2.0](https://docs.djangoproject.com/en/2.0/releases/2.0/)

clone this [url-lookup-service](https://github.com/raghavendra990/url-lookup-service) into your local directory and go to root folder of the project and install python dependencies.

    git clone https://github.com/raghavendra990/url-lookup-service
    cd url-lookup-service
    
    virtualenv venv
    source venv/bin/activate
    
    pip install -r requirements.txt

Go to yaml file inside <code>cfg/dev.yml</code> and change the configuration in case you are deploying to the server.

After all this trying running

    python manage.py runserver 0.0.0.0:80

If you are able to run the django server locally you are good to go. 


## API guide

<code>GET /urlinfo/1/{hostname_and_port}/{original_path_and_query_string}</code>

Method: GET

Response:<code>{ "status":"SUCCESS",
   "url-status": "not-allowed",
    "host": "facebook.com",
    "query-string": ""
}</code>


<code>POST /urlupdate/1/ </code>

Method: POST

Request data: <code>{
   "url-status": "not-allowed",
    "host": "fee",
    "query-string": "r/ddd"
}</code>

Response data: <code>{"status":"SUCCESS"}</code>

Thought to the following:
- <b>The size of the URL list could grow infinitely, how might you scale this beyond the memory capacity of the system? Bonus if you implement this.</b>
  
  I will go with amazon dynamodb, its amazon's self scalable database service.
- <b>The number of requests may exceed the capacity of this system, how might you solve that? Bonus if you implement this.</b>
  
  Basic thing you can do caching of the responses to the query, it will reduce number of db call siginificantly also it is faster to read data from RAM rather then reading from hard drive. 
  I am using redis in memory caching for this, amazon also provides redis caching. For further improvement you can also use [Varnish](https://varnish-cache.org/) for http level caching. varnish sit between your web server and django server, it cache the response of the repeated http call.
- <b>What are some strategies you might use to update the service with new URLs? Updates may be as much as 5 thousand URLs a day with updates arriving every minute.</b>

  5000 url per day which is ok to have, dynamodb with 3 write capcaity per sec will be good to handle it, but if our load get increases in future I will prefer queue based soultion [AWS sqs](https://aws.amazon.com/sqs/?sc_channel=PS&sc_campaign=acquisition_IN&sc_publisher=google&sc_medium=sqs_b&sc_content=sqs_e&sc_detail=aws%20sqs&sc_category=sqs&sc_segment=159812085092&sc_matchtype=e&sc_country=IN&s_kwcid=AL!4422!3!159812085092!e!!g!!aws%20sqs&ef_id=Wp5qKgAAAHx-wTRz:20180522211531:s).
  We can queue the urls detail in SQS, and our listner will read the data and process it on the basis of db capacity.
  
