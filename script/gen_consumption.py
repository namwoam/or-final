import datetime
import requests
import pandas as pd
import os
start_date = datetime.datetime(2012, 1, 1)
end_data = datetime.datetime(2023, 1, 5)
current_date = start_date
df = pd.DataFrame(
    None, columns=["date", "market_code", "market_name", "mean_price", "quantity"])
while current_date != end_data:
    current_date += datetime.timedelta(days=1)

    url = f"https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx?StartDate={current_date.year-1911}{current_date.strftime('.%m.%d')}&Crop=%E7%94%98%E8%97%8D"
    req = requests.get(url)
    data = req.json()
    print(current_date.isoformat(), len(data))
    assert len(data) < 1000
    clean_data = {}
    for el in data:
        if el["市場代號"] not in clean_data:
            clean_data[el["市場代號"]] = [el["交易日期"], int(el["市場代號"]), el["市場名稱"],
                                      float(el["平均價"]), float(el["交易量"])]
        else:
            try:
                prev_quantity = clean_data[el["市場代號"]][4]
                prev_mean = clean_data[el["市場代號"]][3]
                new_quantity = prev_quantity + float(el["交易量"])

                new_mean = (prev_mean*prev_quantity +
                            float(el["交易量"])*float(el["平均價"]))/new_quantity
                clean_data[el["市場代號"]][3] = new_mean
                clean_data[el["市場代號"]][4] = new_quantity
            except BaseException as e:
                print("Error", e)
                pass
    for el in clean_data.values():
        df.loc[len(df)] = el
    df.to_csv(os.path.join(os.path.dirname(
        __file__), "../data/consumption.csv"))
df.to_csv(os.path.join(os.path.dirname(__file__), "../data/consumption.csv"))
