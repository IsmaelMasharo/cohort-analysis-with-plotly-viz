with cohort_items as (
  select
    date_trunc('month', user.created_at) :: date as cohort_month,
    user_id
  from
    user
  order by
    1, 2
),

-- (user_id, month_number): user X has activity in month number X
user_activities as (
  select
    I.user_id,
    (
      SELECT
        (
          DATE_PART('year', I.created_at) - DATE_PART('year', C.cohort_month)
        ) * 12 + (
          DATE_PART('month', I.created_at) - DATE_PART('month', C.cohort_month)
        )
    ) as month_number
  from
    interaction as I
    left join cohort_items C ON I.client_id = C.user_id
  group by
    1, 2
),

-- (cohort_month, size)
cohort_size as (
  select
    cohort_month,
    count(1) as num_users
  from
    cohort_items
  group by
    1
  order by
    1
),

-- (cohort_month, month_number, cnt)
base_cohort as (
  select
    C.cohort_month,
    A.month_number,
    count(1) as num_users
  from
    user_activities as A
    left join cohort_items as C ON A.user_id = C.user_id
  group by
    1, 2
) 

-- our final value: (cohort_month, size, month_number, percentage)
select
  B.cohort_month,
  S.num_users as total_users,
  B.month_number,
  B.num_users :: float * 100 / S.num_users as percentage
from
  base_cohort as B
  left join cohort_size as S ON B.cohort_month = S.cohort_month
where
  B.cohort_month IS NOT NULL
order by
  1, 3