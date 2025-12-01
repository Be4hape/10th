import pandas as pd

# def maxx(lst) : 
#     lst.sort(reverse = True)
#     return lst[0];

# list1 = ([3,1,9,2])

# value_max = maxx(list1)
# print(value_max)

## ===============================

# def passfail(x) : 
#     if (x >= 60) : 
#         return "Pass"
#     else : 
#         return "Fail"

# data = [['asd',90],['zxc',50],['qwe',60],['rty',70]]
# df = pd.DataFrame(data, columns=['이름', '점수'])

# df['합격여부'] = df["점수"].apply(passfail)
# print(df)

## =================================


# data = [['2024-01-20', 3.14], ['2024-01-30', 5.14], ['2024-02-20', 7.14],
#         ['2024-03-20', 9.14], ['2024-04-20', 11.14], ['2024-05-20', 13.14],
#         ['2024-01-22', 33.14], ['2024-01-26', 53.14], ['2024-01-25', 73.14]        
# ]

# df = pd.DataFrame(data, columns=['order_date', 'amount'])
# df['order_date'] = pd.to_datetime(df['order_date'])


# month_13 = df.loc[(df['order_date'] >= '2024-01-01') & (df['order_date'] <= '2024-03-31')]

# month_13["month"] = month_13["order_date"].dt.to_period("M")
# revemon = month_13.groupby("month", as_index=False)["amount"].sum().rename(columns={"amount" : "revenue"})

# revemon = revemon.sort_values("month")
# print(revemon)

## ==================================





