## Views created for the project
Four views were created to aid in solving the third query of the project. 
The purpose of these views is to simplify the complex sql statements into separate parts so that it's easier to understand.

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

###`combined_per_day`
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

###`stats_per_day`
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


