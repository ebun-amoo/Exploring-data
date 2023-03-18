
Before running these programs, you will need to install Python libraries for `sqlalchemy` and `matplotlib`.

### Pop Charts

Add new methods to the class. Use the SQLAlchemy ORM to generate queries to answer the following questions:

* How many songs are in the pop charts database?
* What is the most liked song?
* What is the most viewed song?
* What are the 10 top trending songs? (Hint: Find the songs with the largest percentage increase in views this week.)
* What song that has been ranked in the top 100 for the shortest amount of time?

### Football Players

Add new methods to the class, and find the answer the following questions:

* What country did the player with the most goals play for? After finding the player with the most goals in `get_most_goals`, write another query to find that player's country (you can use a query by country id, or add a [SQLAlchemy relationship](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#tutorial-orm-related-objects))
* What 10 players have the most caps?
* What country has the most goals scored by its players? (This will require [grouping and aggregating](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#aggregate-functions-with-group-by-having)).

