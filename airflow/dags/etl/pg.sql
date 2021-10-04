select *
from (
         SELECT ref_date,
                close,
                AVG(b.close * 1.1600)
                OVER (ORDER BY b.ref_date ASC ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
                    AS avg_close
         FROM main_data b
         where ref_date BETWEEN ('2021-09-28'::date - '6 days'::INTERVAL) AND '2021-09-28'::date) as c
ORDER BY ref_date DESC
LIMIT 1;