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
### Server
* [`Server`](/tsdb/go_server.py): This sets up an asyncio server that can process requests from a client.
* [`Server Overwrite`](/tsdb/go_server_overwrite.py): This sets up an asyncio server that can process requests from a client that overwrites any existing database files.
  * Demo: [`Client`](/tsdb/go_client.py): This sets up a client that runs a similarity search on 50 TimeSeries objects.

### Rest Server
* [`Rest Server`](/tsdb/rest_server.py): This sets up an aiohttp rest server that can process requests from a client.
* [`Rest Server Overwrite`](/tsdb/rest_server_overwrite.py): This sets up an aiohttp rest server that can process requests from a client that overwrites any existing database files.
  * Demo: [`Rest Client`](/tsdb/rest_client.py): This sets up a rest client that runs a similarity search on 50 TimeSeries objects.

### Persistent Architecture
* [`PersistentDB`](/tsdb/persistentdb.py): A database to store and search through TimeSeries.  
* [`BinaryTree`](/tsdb/tsdb_indexes.py#258): A Binary Tree that is used to store the full database rows indexed by primary key.
* [`ArrayBinaryTree`](/tsdb/tsdb_indexes.py#359): A Binary Tree that is used to index all non-primary keys.  Each value is given its own node, and all primary keys that have that value are stored in an array in the node.
* [`DBRow`](/tsdb/tsdb_row.py): A Row object that is used to convert database rows between strings and objects.


### Additional Features:
* `Kalman Filter`: A common issue in time series is that noise will obscure the underlying time series. Kalman filter is able to filter out Gaussian white noise from the innovations using Bayesian inference and estimating a joint probability distribution. We write a Cython version of Kalman filter to filter out the underlying "true" path.
  * Demo: [`go_client_kalman.py`](go_client_kalman.py)

* `Lomb-Scargle FFT for calculating periods`: Regular FFT is not advised for irregular time series. Hence comes the need for the FFT which works for irregular time series and approximates it better that regular FFT. The algorithm used for this purpose is Lomb-Scargle FFT. The original complexity is N^2 but the implementation here is NlogN.
  * Demo: [`go_client_fft.py`](go_client_fft.py)
    * This uses astronomical data and combines both of the additional features
  * Demo: [`go_client_macho_LPV.py`](go_client_macho_LPV.py)
    * This is a demo for long-period variables
  * Demo: [`go_client_macho_ML.py`](go_client_macho_ML.py)
    * This is a demo for Micro-Lensing
  

### DB Functions
* [`begin_transaction`](/tsdb/tsdb_server.py#L29): Get a transaction id to use in other DB functions.
* [`commit`](/tsdb/tsdb_server.py#L37): Commits a transaction and stores all changes to disk.
* [`rollback`](/tsdb/tsdb_server.py#L45): Rolls back the indicated transaction.
* [`insert_ts`](/tsdb/tsdb_server.py#L53): Insert time series data. Can be followed by a trigger which is a pre-defined function.
* [`delete_ts`](/tsdb/tsdb_server.py#L62): Delete time series data and the metadata for that particular time series.
* [`upsert_meta`](/tsdb/tsdb_server.py#L70): Update/Insert the time series metadata.
* [`select`](/tsdb/tsdb_server.py#L75): Perform select operation on the time series and the metadata.
* [`augmented-select`](/tsdb/tsdb_server.py#L89): Perform augmented select (query, followed by a pre-defined function) of time series data and/or metadata.
* [`create_vp`](/tsdb/tsdb_server.py#L147): Create a new vantage point by using a primary key available in the database.
* [`ts_similarity_search`](/tsdb/tsdb_server.py#L180): Run a similarity search on the basis of vantage points in order to find the closest time series.
* [`add_trigger`](/tsdb/tsdb_server.py#L108): Add a trigger such that it will cause a pre-defined function to be run upon execution of a particular database operation.
* [`remove_trigger`](/tsdb/tsdb_server.py#L120): Remove a trigger associated with a certain database operation.


### Procedures
* [`corr`](/procs/corr.py): Calculate the correlation between two time series. Used internally for the similarity search in the database.
* [`stats`](/procs/stats.py): Computes the mean and the standard deviation for the time series.
* [`KalmanFilter`](/procs/KalmanFilter.py) - We generate a time series with constant Gaussian innovations, and obscured the series by Gaussian noice. Using this algorithm, we can estimate the sigma_eta: the variance of innovations and sigma_epsilon: the variance of noise. The estimate turns out to be accurate (<10%).
* [`period`](/procs/period.py) - Computes the period of the irregular time series. Uses the Lomb-Scargle method to compute the FFT approximation. The FFT values are then used to find the period of the signal. The Lomb-Scargle FFT code is clearly described in the procs folder.


Group Members:<br />
Avery Faller | averyfaller <br />
Abhishek Malali | abhishekmalali <br />
Thomas Seah <br />
Haosu Tang | haosutang <br />
