from sqlgenerator import *
from connector import *
import numpy as np
import pandas as pd
query_sql = """
                (SELECT
                    securitycode,
                    securityname,
                    marketcode,
                    `day`,
                    round(`close` / 1000,2) AS bclose,
                    round(`high` / 1000,2) as `high`,
                    round(`low`/1000,2) as `low`,
                    round(`open`/1000,2) as `open`
                FROM
                    day_k_line 
                WHERE
                    securitycode = '{}'
                    AND date_format(`day`, '%%Y-%%m-%%d') >= DATE_SUB( CURDATE( ), INTERVAL 2 year) 
                ORDER BY
                    `DAY` ASC)
              """


# root@        HandsomeBoy666!
# mysql -h81.71.26.183 -uroot -pHandsomeBoyMysql
if __name__ == "__main__":
    