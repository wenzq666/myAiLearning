import pandas as pd



kc_train_data = pd.read_csv("./data/kc_train.csv", names=[
    'sale_date', 'sale_price', 'h_num', 'bath_num', 'h_m2', 'h_p2', 'h_high', 'score', 'total_m2', 'under_m2', 'house_year', 'repair_year', 'weidu', 'jingd'
])

print(kc_train_data)

kc_train_data.info()

# price_data = kc_train_data['sale_price']
# print(price_data)
# price_data.to_csv("./data/kc_train_price_data.csv", index=False, header=False)

train_data_new = kc_train_data.drop('sale_price')
print(train_data_new)
