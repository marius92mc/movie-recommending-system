# Movie Recommending System using Spark

### Requirements
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
### To download the dataset that will be used, run the following script
```bash
$ python download_dataset.py
```

