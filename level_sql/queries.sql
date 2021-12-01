-- First query: dematerialization_rate

WITH liberal_doctors AS (SELECT sender_name, telecom, CASE WHEN telecom = 'paper' THEN 'True' END AS papered_com FROM communication WHERE sender_category = 'liberal')
SELECT sender_name, (COUNT(papered_com) / COUNT(*)) AS dematerialization_rate FROM liberal_doctors GROUP BY sender_name;

-- Second query: doctors with at least 5 communications following their first communication

WITH first_communication AS (SELECT sender_name, MIN(DATE_ADD(created_at, INTERVAL 7 DAY)) AS first_com_plus_7 
FROM communication 
GROUP BY sender_name),
seven_days_communication AS (SELECT communication.sender_name, communication.id, created_at, first_com_plus_7 
FROM communication JOIN first_communication
ON communication.sender_name = first_communication.sender_name
WHERE created_at <= first_com_plus_7)
SELECT sender_name FROM seven_days_communication GROUP BY sender_name HAVING COUNT(*)>=5;
        

