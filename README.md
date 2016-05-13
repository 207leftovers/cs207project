# cs207project

[![Build Status](https://travis-ci.org/207leftovers/cs207project.svg?branch=master)](https://travis-ci.org/207leftovers/cs207project)
[![Coverage Status](https://coveralls.io/repos/github/207leftovers/cs207project/badge.svg?branch=master)](https://coveralls.io/github/207leftovers/cs207project?branch=master)

#Description
A project for CS207 at Harvard University, Spring 2016.  This project implements a package for a persistent time series database.
<br />

The timeseries module contains code for a TimeSeries class to handle ordered data and corresponding information.  <br />

The pype module is a Domain Specific Language to compile simple programs. <br />

The tsdb module is a database to store and retrieve TimeSeries objects. It can be run via go_server.py and go_client.py. <br />

It also has a REST API that can be run via rest_server.py and REST_commands.sh


### Persistent Architecture
* [`PersistentDB`](/tsdb/persistentdb.py): A database to store and search through TimeSeries.  
* [`BinaryTree`](/tsdb/tsdb_indexes.py): A Binary Tree that is used to store the full database rows indexed by primary key.
* [`ArrayBinaryTree`](/tsdb/tsdb_indexes.py): A Binary Tree that is used to index all non-primary keys.  Each value is given its own node, and all primary keys that have that value are stored in an array in the node.
* [`DBRow`](/tsdb/tsdb_row.py): A Row object that is used to convert database rows between strings and objects.


### Additional Features:
* `Kalman Filter`: A common issue in time series is that noise will obscure the underlying time series. Kalman filter is able to filter out Gaussian white noise from the innovations using Bayesian inference and estimating a joint probability distribution. We write a Cython version of Kalman filter to filter out the underlying "true" path.

* `Lomb-Scargle FFT for calculating periods`: Regular FFT is not advised for irregular time series. Hence comes the need for the FFT which works for irregular time series and approximates it better that regular FFT. The algorithm used for this purpose is Lomb-Scargle FFT. The original complexity is N^2 but the implementation here is NlogN.


### DB Functions
* `begin_transaction`: Get a transaction id to use in other DB functions.
* `commit`: Commits a transaction and stores all changes to disk.
* `rollback`: Rolls back the indicated transaction.
* `insert_ts`: Insert time series data. Can be followed by a trigger which is a pre-defined function.
* `delete_ts`: Delete time series data and the metadata for that particular time series.
* `upsert_meta`: Update/Insert the time series metadata.
* `select`: Perform select operation on the time series and the metadata.
* `augmented-select`: Perform augmented select (query, followed by a pre-defined function) of time series data and/or metadata.
* `create_vp`: Create a new vantage point by using a primary key available in the database.
* `ts_similarity_search`: Run a similarity search on the basis of vantage points in order to find the closest time series.
* `add_trigger`: Add a trigger such that it will cause a pre-defined function to be run upon execution of a particular database operation.
* `remove_trigger`: Remove a trigger associated with a certain database operation.


### Procedures
* `corr`: Calculate the correlation between two time series. Used internally for the similarity search in the database.
* `stats`: Computes the mean and the standard deviation for the time series.
* `KalmanFilter` - We generate a time series with constant Gaussian innovations, and obscured the series by Gaussian noice. Using this algorithm, we can estimate the sigma_eta: the variance of innovations and sigma_epsilon: the variance of noise. The estimate turns out to be accurate (<10%).
* `period` - Computes the period of the irregular time series. Uses the Lomb-Scargle method to compute the FFT approximation. The FFT values are then used to find the period of the signal. The Lomb-Scargle FFT code is clearly described in the procs folder.


Group Members:<br />
Avery Faller | averyfaller <br />
Abhishek Malali | abhishekmalali <br />
Thomas Seah <br />
Haosu Tang | haosutang <br />
