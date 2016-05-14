# Movie Recommending System using Spark

TODO description

## Requirements and installation

Please see requirements.txt.
To install these packages, use the following command in a <a href="http://docs.python-guide.org/en/latest/dev/virtualenvs/" target="_blank"> virtualenv</a>.
```bash
$ pip install -r requirements.txt
```
Download Spark v1.6.1 from <a href="http://spark.apache.org/downloads.html"> here</a>.
```bash
$ tar -xf <name_of_spark_archive>.tar
```
Follow instructions from spark-1.6.1/README.md to build and install.
<br />
Environment variables in your ~/.bash_profile for OS X or ~/.bashrc for Linux.
```bash
export SPARK_HOME=~/path/to/spark-1.6.1
export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/pyhon/lib/py4j-0.9-src.zip:$PYTHONPATH
```
Verify it was successfully installed by running 
```bash
$ ./bin/pyspark
```
from spark-1.6.1/
<br />
Copy <i>spark-env.sh</i>, <i>spark-defaults.conf</i> and <i>slaves</i> files 
from <i>spark_utils/</i> to <i>path/to/spark/conf/</i>. 
- <i>spark-env.sh</i> 
       - settings regarding the master node, like number of workers if manages, etc.
- <i>spark-defaults.conf</i> 
       - settings regarding the workers. 
          Any values specified as flags or in the properties file will be 
          passed on to the 	application and merged with those specified 
          through SparkConf invocation in the code. 
          Properties set directly on the SparkConf take highest precedence, 
          then flags passed to spark-submit or spark-shell, 
          then options in the spark-defaults.conf file.
- <i>slaves</i> 
       - addresses of the workers.
<br />
To download the dataset that will be used, run the following script
```bash
$ python download_dataset.py
```

## Usage
TODO Write <b>full</b> instructions and an example. 
### 1. Starting the Spark Master and Workers. 
```bash
$ sbin/start-master.sh
$ sbin/start-slaves.sh
```
or 
```bash
$ sbin/start-all.sh
```
See Spark stats via UI at 
http://localhost:8080
http://localhost:4040
### 2. Sending the Python sources to Spark and run them
Run from project directory, but not from virtualenv, the following
```bash
$ sh path/to/spark/bin/spark-submit \
           --master spark://<server_name/server_ip>:7077 \
           --num-executors 2 \
           --total-executor-cores 2 \
           --executor-memory 2g \
           server.py > stdout 2> stderr
```
Where server_name is yosemite/ubuntu/localhost if it's running locally. 
<br />
Logs can be seen in the above provided files.
```bash
$ tail -f stdout
$ tail -f stderr
```
By default, as it is mentioned in <i>server.py</i>, CherryPy will use 
port 5433. 

Change it from the same file if it is busy.
### 3. <b>Operations on the constructed model</b>
- <b>POSTing new ratings</b> to the model
```bash
$ curl --data-binary @user_ratings.file http://0.0.0.0:5433/<user_id>/ratings
```
where user_id is 0 by default representing a total new user, 
outside from those mentioned in the dataset.
<br />
POSTs user_id's ratings from <i>user_ratings.file</i>, where 
every line has movie_id,rating.
<br />
Will start some computations and end up with an output representing 
the ratings that has been submitted as a list of lists. 
In the server output window you will see the actual Spark computation 
output together with CherryPy's output messages about HTTP requests.
<br />
Output represents ratings as - (user_id, movie_id, rating)
rating awarded by the user from user_ratings.file.
- [ ] <b>GETing best recommendations</b>
```bash
$ curl http://0.0.0.0:5433/<user_id>/ratings/top/<num_movies>
```
or in browser
<br />
http://0.0.0.0:5433/user_id/ratings/top/num_movies
<br />
Example
http://0.0.0.0:5433/0/ratings/top/10
<br />
Will present the best num_movies recommendations for user with user_id.
- <b>GETing individual ratings</b>
```bash
$ curl http://0.0.0.0:5433/<user_id>/ratings/<movie_id>
```
or in browser
http://0.0.0.0:5433/user_id/ratings/movie_id
<br />
Example 
http://0.0.0.0:5433/0/ratings/500
<br />
Will get the predicted movie rating, from the model, of 
user_id for movie_id. 

## Tests
TODO

