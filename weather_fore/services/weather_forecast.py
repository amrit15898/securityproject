import datetime
import pandas as pd
import re
import numpy as np
from weather_fore.models import weather_grids, weather_codes, weather_send_temp_packet, weather_forecast_logs

months = {
    "Jan": '01',
    "Feb": '02',
    "Mar": '03',
    "Apr": '04',
    "May": '05',
    "June": '06',
    "July": '07',
    "Aug": '08',
    "Sept": '09',
    "Oct": '10',
    "Nov": '11',
    "Dec": '12'
}


class weather_forecast:
    start_date = ""

    @classmethod
    def date_read(cls, row):
        data = row[1].split("-")
        if data is not None:
            char_str = ''.join((z for z in data[1] if not z.isdigit())).replace(" ", "")
            today = datetime.date.today()
            year = today.strftime("%y")
            cls.start_date = data[0] + str(months[char_str]) + str(year)
        else:
            error = 'error in getting date from csv file  '
            error_obj = weather_forecast_logs.objects.create(message=error)
            return False

    @classmethod
    def Range_area(cls, row, index):
        data = row[0].split('-')
        return_data = {}
        if weather_grids.objects.filter(sect_id=str(data[0]).replace(" ", "")).exists():
            grid_data = weather_grids.objects.get(sect_id=str(data[0]).replace(" ", ""))
            grids = []
            for j in grid_data.natsat_grids.all():
                grids.append(j.grid_id)
            return_data['forecast_area'] = grid_data.forecast_area
            return_data['grids'] = grids
            return return_data
        else:
            error = f'invalid range {data[0]} at index {index+9}'
            error_obj = weather_forecast_logs.objects.create(message=error)
            return False

    @classmethod
    def day_forecast_code(cls, relation_char):
        if ":" in relation_char:
            relation_char = relation_char.replace(":", "-").replace(" ", "").upper()

        if weather_codes.objects.filter(relation_in_char=relation_char).exists():
            code_data = weather_codes.objects.get(relation_in_char=relation_char)
            return code_data.code
        else:
            error = f' weather code with this {relation_char} not exist'
            error_obj = weather_forecast_logs.objects.create(message=error)
            return False

    @staticmethod
    def create_temp_data(start_date, grid_id, forecast_area, day_1, day_2="null", day_3="null", day_4="null",
                         day_5="null", day_6="null", num_of_days="00"):
        weather_send_temp_packet.objects.create(
            start_date=start_date,
            grid_id=grid_id,
            day_1=day_1,
            day_2=day_2,
            day_3=day_3,
            day_4=day_4,
            day_5=day_5,
            day_6=day_6,
            num_of_day=num_of_days,
            forecast_area=forecast_area
        )


    @classmethod
    def csv_read(cls, file):
        df = pd.read_csv(file, skiprows=[i for i in range(0, 8)], header=None, )
        error_messages = []
        try:
            null_mask = df.isnull()
            null_locations = null_mask.stack()
            for index, value in null_locations.iteritems():
                if value:
                    row, column = index
                    d = f"Null value found at row number {row + 9} and column name {column + 1}"
                    error_messages.append(d)

        except Exception as e:
            print(e)
        if error_messages:
            for message in error_messages:
                weather_forecast_logs.objects.create(message=message)


        def check_element(x):
            if pd.isnull(x):
                return False
            else:
                return (':' in x) or ('-' in x)


        increment_1 = 9
        increment_2 = 1
        result = df.applymap(check_element)

        a = result.iloc[1:][~result.iloc[1:]].stack().index.tolist()
        new_lst = [[t[0] + increment_1, t[1] + increment_2] for t in a]

        for idx, error in enumerate(new_lst):
            row, col = error
            error_a = weather_forecast_logs.objects.create(
                message=f'only : and - is accepted but Error  occurred at row {row} and column {col}')

        for i, r in df.iterrows():
            if r.isnull().any():
                continue
            if i == 0:
                cls.date_read(r)
                continue
            range_area_data = cls.Range_area(r,i)

            if range_area_data is False:
                continue
            grids = range_area_data['grids']
            forecast_area = range_area_data['forecast_area']
            # day code

            day1 = cls.day_forecast_code(relation_char=r[1])
            try:
                day2 = cls.day_forecast_code(relation_char=r[2])
            except:
                day2 = ""
            try:
                day3 = cls.day_forecast_code(relation_char=r[3])
            except:
                day3 = ""
            try:
                day4 = cls.day_forecast_code(relation_char=r[4])
            except:
                day4 = ""
            try:
             day5 = cls.day_forecast_code(relation_char=r[5])
            except:
                day5 = ""
            try:
               day6 = cls.day_forecast_code(relation_char=r[6])
            except:
                day6 = ""
            if False in [grids, forecast_area]:
                continue

            for grid in grids:
                cls.create_temp_data(start_date=cls.start_date, grid_id=grid, forecast_area=forecast_area, day_1=day1,
                                     day_2=day2, day_3=day3, day_4=day4, day_5=day5, day_6=day6, num_of_days="0"+str(len(df.columns)-1))

        # packet
        w_all_data = weather_send_temp_packet.objects.all()
        data = []
        for i in w_all_data:
            packet = f"#@92{i.start_date}{i.grid_id}{i.num_of_day}{i.forecast_area}{i.day_1}{i.day_2}{i.day_3}{i.day_4}{i.day_5}{i.day_6}@#"
            data.append({
                "start_date": i.start_date,
                "grid_id": i.grid_id,
                "num_of_day": i.num_of_day,
                "packet": packet,
                "day_1": i.day_1,
                "day_2": i.day_2,
                "day_3": i.day_3,
                "day_4": i.day_4,
                "day_5": i.day_5,
                "day_6": i.day_6,
                "forecast_area": i.forecast_area,
                "id": i.id
            })
            i.delete()

        return data


weather_obj = weather_forecast()




