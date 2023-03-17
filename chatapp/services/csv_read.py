import pandas as pd



def read_excel(file):
    excel_data = pd.read_excel(file)
    data = pd.DataFrame(excel_data, columns=[
        'message'], )

    if "message" not in excel_data :
        print("invalid")
        return False

    return data.to_json()





    # for index, row in data.iterrows():
    #     print(index, row['message'])



