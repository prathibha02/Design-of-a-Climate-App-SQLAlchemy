# sqlalchemy-challenge
Using Python and SQLAlchemy to perform basic climate analysis and data exploration of a climate database
#### Precipitation Analysis

To perform an analysis of precipitation in the area, we do the following:

* Find the most recent date in the dataset.

* Using this date, retrieve the previous 12 months of precipitation data by querying the 12 previous months of data.

* Select only the `date` and `prcp` values.

* Load the query results into a Pandas DataFrame, and set the index to the date column.

* Sort the DataFrame values by `date`.

* Plot the results by using the DataFrame `plot` method

* Use Pandas to print the summary statistics for the precipitation data.

#### Station Analysis

To perform an analysis of stations in the area, we do the following:

* Design a query to calculate the total number of stations in the dataset.

* Design a query to find the most active stations (the stations with the most rows).

    * List the stations and observation counts in descending order.

    * Which station id has the highest number of observations?

    * Using the most active station id, calculate the lowest, highest, and average temperatures.


* Design a query to retrieve the previous 12 months of temperature observation data (TOBS).

    * Filter by the station with the highest number of observations.

    * Query the previous 12 months of temperature observation data for this station.

    * Plot the results as a histogram with `bins=12`