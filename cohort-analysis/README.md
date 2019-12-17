# Cohort analysis
What is it? One of the existing mechanisms used in behavioral analysis to identify trends in customer retention. 

### Okay, but what's a `Cohort`?
It's the `time frame` (weekly, monthly, etc) a group of interest have in common either because of its registration date or another common time variable. This clustered group is then analyzed as a whole for identifying its trends on its interactions over time with the platform they registered on (e-commerce, etc).

### What question does it answer?
Let's consider a `monthly time frame`, It'll main focus in the following:

- ##### What percentage of users `created on month X` are still active `after Y months` ?

  Here month ` X` is known as `Cohort`. The analysis is made on `users created on month X` and its behavior `Y months after` its creation.

- ##### How does users interactions vary from one cohort to another?

  While the first question analyzes `one cohort and its evolution over time`, this approach shows `how do different cohorts are compared to one another`. 

###  Database Schema Models: Our data source
The source of the analysis will be a database model with following schema:

```sql
table client_client(
   ID   INT   NOT NULL,
   created_at timestamp NOT NULL,
   PRIMARY KEY (ID)
);

table order_order(
   ID   INT  NOT NULL,
   created_at timestamp NOT NULL,
   client_id INT NOT NULL,
   PRIMARY KEY (ID)
);
```

Where `client_client` holds information on the registered users where as `order_order` records the user interactions and the date is being performed.

#### Desired output

So, we basically need to go from the schema to something like this:

| cohort_month     | total\_users | month\_number | percentage |
|-:-:--------------|-:-:----------|-:-:-----------|-:-:--------|
| 2017\-**09**\-01 | 3446         | 0             | 7\.25      |
| 2017\-**09**\-01 | 3446         | 1             | 7\.19      |
| 2017\-**09**\-01 | 3446         | 2             | 6\.44      |
| 2017\-**09**\-01 | 3446         | 3             | 7\.10      |
| ...              | ...          | ...           | ...        |
| 2017\-**10**\-01 | 239          | 0             | 18\.4      |
| 2017\-**10**\-01 | 239          | 1             | 8\.78      |
| 2017\-**10**\-01 | 239          | 2             | 7\.53      |
| 2017\-**10**\-01 | 239          | 3             | 5\.43      |
| ...              | ...          | ...           | ...        |


Here, I've highlighted the the month number since this is the `cohort` (time frame) we're considering for our analysis. You can see `the total_user` has a same value for a given cohort.

The `cohort_month` column is equivalent to the `X` variable (analyzed time frame) and the `month_number` to the `Y` one (evolution after Y time frames).

The `percentage` column is what we're aiming to get from the analysis. 

#### How do we interpret this?

Well, we could take for example the first set of rows corresponding to the first cohort. This is the base story:

> In the month of September, 2017 we had a total number of 3446 users registered in our platform. Of this users, only 250 (7.25%) of them made an interaction with the platform in its registration month. In the third month after its registration, only 244 (7.10%) made an interaction.

What was the question about? We wanted to know how does a set of users interact with our platform and not only that but the evolution of this interactions. 

Here, let me tell you another story taking the first row from the two cohorts shown in the table:

> From September to October the percentage of users registered decreased by 93% compared to the previous month. Taking a look at the percentage of active users in each cohort we could see that it reduced actually by 18% (250 active users in September against 44 in October).

What are we seeing here? How two different cohort vary from one another.

#### From schema to summarized table? SQL, your closest ally 
The main purpose is to get a base raw description of what is wanted to be answer.








We should remember the `cohort analysis is a tool` for answering big deal questions like **why does this happen?** **what do we do about it?** **how do we profit out of it?** 

#### Visualizing cohort tables

The sql query returns something we could handle with a little effort since we only analyzed two consecutive cohorts. But imagine you have dozens of cohorts, then you'll have dozens of dozens of values for each of them. What a work. But take a deep breathe and look at this.

<img src="cohort-table.png" width="800" align="center"> 



What, you can't see it clearly. I've used `Plotly` to generate the visualization. Checkout the ipython notebook to see the steps I've take. 

You can check the final product [here](https://plot.ly/~masharo/10.embed).

I'll expand the explanation in the following days. 

Thanks for the reading and happy coding!