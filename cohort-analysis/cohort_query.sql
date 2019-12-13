with cohort_items as (
  select
    date_trunc('month', U.created_at)::date as cohort_month,
    user_id as user_id
  from client_client U
  order by 1, 2
),
-- (user_id, month_number): user X has activity in month number X
user_activities as (
  select
    A.user_id,
	(
    SELECT (DATE_PART('year', A.created_at) - DATE_PART('year', C.cohort_month)) * 12 +
    (DATE_PART('month', A.created_at) - DATE_PART('month', C.cohort_month))
    -- DATE_PART('day', A.created_at ::timestamp - C.cohort_month::timestamp)
	) as month_number
  from order_order A
  left join cohort_items C ON A.client_id = C.user_id
  group by 1, 2
),
-- (cohort_month, size)
cohort_size as (
  select cohort_month, count(1) as num_users
  from cohort_items
  group by 1
  order by 1
),
-- (cohort_month, month_number, cnt)
B as (
  select
    C.cohort_month,
    A.month_number,
    count(1) as num_users
  from user_activities A
  left join cohort_items C ON A.user_id = C.user_id
  group by 1, 2
)
-- our final value: (cohort_month, size, month_number, percentage)
select
  B.cohort_month,
  S.num_users as total_users,
  B.month_number,
  B.num_users::float * 100 / S.num_users as percentage
from B
left join cohort_size S ON B.cohort_month = S.cohort_month
where B.cohort_month IS NOT NULL
order by 1, 3