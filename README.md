# Cohort analysis
Supporting scripts for a [post](https://medium.com/@ismaelmasharo/cohort-analysis-95a794b4e58c) I published about cohort analysis. The result is an interactive cohort table build with Plotly. You can check the final version [here](https://plot.ly/~masharo/20/).

The analysis is made over a mocked dataset and cohorts are generated for a monthly frequency. 

**Files:**
- **cohort_query.sql**: Reference SQL script for generating monthly cohorts from a database (no dumped data is attached). The schema is the next one:
  - `user(user_id, created_at)`
  - `interaction(id, user_id, created_at)`
- **cohort_2018.csv**: Test output after applying the previous operation. This file is used as the base dataset for the jupyter notebook.
- **cohort_analysis.ipynb**: Notebook with transformations to generate the cohort table visualization.
