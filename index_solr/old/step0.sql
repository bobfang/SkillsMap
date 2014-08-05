#Step 0
#customer blacklist
SELECT c.customer_id, c.customer_company_name FROM dv_customers c
JOIN dv_customer_plans p on p.plan_customer_id = c.customer_id
WHERE
(c.customer_is_internal = 1
OR p.plan_subscription_status in (-4,-5,-6))
OR c.customer_notes LIKE '%already%'
OR c.customer_notes LIKE '%spam%'
OR c.customer_notes LIKE '%recruiter%'
OR c.customer_notes LIKE '%fake%';