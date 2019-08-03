# Udacity Logs Analysis Project
This is the first project for the Udacity Full Stack Web Developer Nanodegree program.

## Overview
The goal of the project is to create a reporting tool which outputs data. Three types of report will be outputted. 
The purpose is that each report can be created by executing one SQL statement. 
The used technologies for this project are
* python 3.7
* psycopg2
* git
* vagrant 

## Executing the project
In order to execute the project, we need to go through a couple of steps

### 1. Install Virtualbox and Vagrant
Make sure to first install [Virtualbox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/downloads.html). 

### 2. Set up VM with configuration of Udacity and git repository
The configuration of Udacity called [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip), needs to be downloaded. 
Change into this directory after you've unzipped the directory. Find a folder called Vagrant and `cd` into this directory. 
Afterwards, do a git clone of my repository into this folder so that my project folder is inside this Vagrant folder. 
As a final thing, make sure to download the [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) from Udacity and also place it inside this Vagrant folder

### 3. Start up virtual machine
Start up the virtual machine by running the command `vagrant up`. After running `vagrant up`, run `vagrant ssh` to login
to the virtual machine. 

### 4. Load the data into the database
Load the data into the database by running the following command
```
psql -d news -f newsdata.sql
```

## 5. Views created for the project
Four views were created to aid in solving the third query of the project. 
The purpose of these views is to simplify the complex sql statements into separate parts so that it's easier to understand. 
These four views that were created were
* errors_per_day
* requests_per_day
* combined_per_day
* stats_per_day

These views can be created by running the follows commands as follows:

### `errors_per_day`
```postgresql
create view errors_per_day as
select 
    status, 
    cast(time as date) as datum, 
    count(*) as requests from log
where 
    status = '404 NOT FOUND'
group by 
    status, datum
```

### `requests_per_day`
```postgresql
create view requests_per_day as
select 
    CAST(time as date) as datum, 
    count(*) as requests 
from 
    log 
group by datum
```

### `combined_per_day`
```postgresql
create view combined_per_day as
SELECT
    error_per_day.datum,
    error_per_day.requests AS error_requests,
    requests_per_day.requests AS total_requests
FROM 
	error_per_day,
    requests_per_day
WHERE 
	error_per_day.datum = requests_per_day.datum
ORDER BY 
	error_per_day.requests DESC;
```

### `stats_per_day`
```postgresql
create view stats_per_day as
select 
	datum,
	error_requests,
	total_requests,
	round(error_requests * 100.0 / total_requests, 1) as error_rate
from 
	combined_per_day
as 
	error_stat
```

### 6. Run the python command to generate the reports
As a final step, run `python news.py` inside my git folder to generate the reports. 
The generated report can also be seen in my repository in `news-result.png`.


