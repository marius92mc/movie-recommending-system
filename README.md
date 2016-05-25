# Movie Recommending System using Spark

TODO description

## Requirements and installation

It is highly recommended to use <a href="http://docs.python-guide.org/en/latest/dev/virtualenvs/" target="_blank">virtualenv</a>. 

Please see requirements.txt.
To install these packages, use the following command in a <a href="http://docs.python-guide.org/en/latest/dev/virtualenvs/" target="_blank"> virtualenv</a>.

    $ pip install -r requirements.txt

Download Spark v1.6.1 from <a href="http://spark.apache.org/downloads.html"> here</a>.

    $ tar -xf <name_of_spark_archive>.tar

Follow instructions from spark-1.6.1/README.md to build and install.

Environment variables in your ~/.bash_profile for OS X or ~/.bashrc for Linux.

    export SPARK_HOME=~/path/to/spark-1.6.1
    export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
    export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/pyhon/lib/py4j-0.9-src.zip:$PYTHONPATH
    
Verify it was successfully installed by running 

    $ ./bin/pyspark

from spark-1.6.1/

Copy <i>spark-env.sh</i>, <i>spark-defaults.conf</i> and <i>slaves</i> files 
from <i>spark_utils/</i> to <i>path/to/spark/conf/</i>. 

- <i>spark-env.sh</i> 
       - settings regarding the master node, like number of workers if manages, etc.
         Note: Edit the SCALA_HOME, SPARK_WORKER_DIR environment variables 
         to your local needs. 
- <i>spark-defaults.conf</i> 
       - settings regarding the workers. 
          Any values specified as flags or in the properties file will be 
          passed on to the 	application and merged with those specified 
          through SparkConf invocation in the code. 
          Properties set directly on the SparkConf creation, in code, take highest precedence, 
          then flags passed to spark-submit or spark-shell, 
          then options in the spark-defaults.conf file.
- <i>slaves</i> 
       - addresses of the workers.

For database we use PostgreSQL. 
Download and install it from [here](http://www.postgresql.org/download/).

Add the following to ~/.bash_profile 
    
    export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin 

to ~/.bash_profile. 

    $ which psql
 
should output like this
    
    /Applications/Postgres.app/Contents/Versions/latest/bin/psql

Create a PostgreSQL database

    $ createdb rs
    
To see the created database, got to Terminal and type 
"psql", then in the <i>postgres</i> console type "\l", 
which will list all the databases available, 
"\connect rs;" to connect to the newly created rs database created above, 
and "\d" will show the available tables from the connected database.

To download the <b>dataset</b> that will be used, run the following script

    $ python download_dataset.py

## Usage
- [ ] Write <b>full</b> instructions and an example. 

Activate the created virtualenv directory.

    source name_of_virtualenv_directory/bin/activate

### 1. Starting the Spark Master and Workers.
From path/to/spark type
    
    $ sbin/start-master.sh
    $ sbin/start-slaves.sh

or 

    $ sbin/start-all.sh

Similar, to stop the Master and Workers. 

    $ sbin/stop-master.sh
    $ sbin/stop-slaves.sh

or 

    $ sbin/stop-all.sh


See Spark stats via UI at
 
http://localhost:8080 

http://localhost:4040

### 2. Sending the Python sources to Spark and run them
Run from project directory, the following

    $ sh path/to/spark/bin/spark-submit \
               --master spark://<server_name/server_ip>:7077 \
               --num-executors 2 \
               --total-executor-cores 2 \
               --executor-memory 2g \
               server.py [options] > stdout 2> stderr

where server_name is yosemite/ubuntu/localhost if it's running locally. 

Options, all <b>optional</b>, include:

    --dataset <name>
      Specify a dataset, e.g. "ml-latest" or "ml-latest-small". 
      If omitted, defaults to "ml-latest".

Logs can be seen in the above provided files.

    $ tail -f stdout
    $ tail -f stderr

By default, as it is mentioned in <i>server.py</i>, CherryPy will use 
port 5433. 
Change it from the same file if it is busy.
### 3. <b>Operations on the constructed model</b>
- <b>POSTing new ratings</b> to the model

```
$ curl --data-binary @user_ratings/user_ratings.file http://0.0.0.0:5433/<user_id>/ratings
```

where user_id is 0 by default representing a total new user, 
outside from those mentioned in the dataset.

<b>Description</b>: POSTs user_id's ratings from <i>user_ratings.file</i>, where 
every line has movie_id,rating. <br />
Will start some computations and end up with an output representing 
the ratings that has been submitted as a list of lists. <br />
In the server output window you will see the actual Spark computation 
output together with CherryPy's output messages about HTTP requests.

Output represents ratings as - (user_id, movie_id, rating)
rating awarded by the user from user_ratings.file.

- <b>GETing best recommendations</b>

```
$ curl http://0.0.0.0:5433/<user_id>/ratings/top/<num_movies>
```

or in browser 

http://0.0.0.0:5433/user_id/ratings/top/num_movies

Example

    $ curl http://0.0.0.0:5433/0/ratings/top/10
    $ curl http://0.0.0.0:5433/3/ratings/top/10

http://0.0.0.0:5433/0/ratings/top/10

<b>Description</b>: Will present the best num_movies recommendations for user with user_id.

- <b>GETing individual ratings</b>

```
$ curl http://0.0.0.0:5433/<user_id>/ratings/<movie_id>
```

or in browser

http://0.0.0.0:5433/user_id/ratings/movie_id

Example

```
curl http://0.0.0.0:5433/0/ratings/500
curl http://0.0.0.0:5433/3/ratings/500
```

http://0.0.0.0:5433/0/ratings/500

http://0.0.0.0:5433/1/ratings/500

<b>Description</b>: Will get the predicted movie rating, from the model, of 
user_id for movie_id. 

## Tests
TODO

## License
TODO