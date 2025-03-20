# searchapi-job-scraper
Use the SearchAPI backend to collect as many jobs as possible form the Charlotte region of North Carolina

Modify the search values of each iteration, inside the `categories` array. Be specific about the type of job you're looking for.

To modify the headers outputted in the csv, make sure to select from the keys under `"jobs":`and follow the documentation on [this page](https://www.searchapi.io/docs/google-jobs#:~:text=York%22%0A%20%20%7D%2C-,%22jobs%22%3A%20%5B,-%7B%0A%20%20%20%20%20%20%22position%22). From there, simply edit the `fieldnames` array, and then the headers in `.writerow(...//)` accordingly.

`BASE_PARAMS` may be modified as well if needed; ensure that you follow the syntax from SearchAPI here as well.

The script is currently set to look for jobs that fall within the last 6 months, but you can adjust that in the `six_months_ago` variable.
