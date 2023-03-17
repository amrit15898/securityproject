import pandas as pd
from weather_fore.models import weather_codes

errors = []
def forcast_name(row):
    check_forecast = weather_codes.objects.filter(forecast=row[0])
    if check_forecast.exists():
        msg = f"forcast name already exits {row[0]}"
        errors.append(msg)
        return False

    return row[0]


def check_code(row):
    check_len = row[1]
    if str(check_len) == "nan":
        return False
    elif type(check_len) == str:
        msg = "character are not allowed"
        errors.append(msg)
        return False
    elif check_len >= 10:
        msg = "code only one digit required"
        errors.append(msg)
        return False
    elif check_len == 0:
        msg = "code zero not required"
        errors.append(msg)


    code = str(int(row[1]))
    if len(code) > 2:
        errors.append("invalid code")
    elif len(code) < 2:
        code = "0" + code

    if weather_codes.objects.filter(code=code).exists():
        msg = f"forecast code already exists {code}"
        errors.append(msg)
        return False

    return code



def relation_in_char(row):
    check_len = row[2]
    if str(check_len) == "nan":
        return False
    relation = weather_codes.objects.filter(relation_in_char=row[2])
    if relation.exists():
        msg = f"relation in char already exits {row[2]}"
        errors.append(msg)
        return False
    return row[2]


def check_intensity(row):
    intensity = weather_codes.objects.filter(intensity=row[3])
    if intensity.exists():
        msg = f"intensity already exits {row[3]}"
        errors.append(msg)
        return False
    return row[3]


def check_legend(row):
    legend = weather_codes.objects.filter(legend=row[4])
    if legend.exists():
        msg = f"legend already exits {row[4]}"
        errors.append(msg)
        return False
    return row[4]





def weather_code_csv(excel):
        fields = [0, 1, 2, 3, 4, 5]
        read_files = pd.read_csv(excel, usecols=fields)
        response_data = []
        for index, row in read_files.iterrows():
            name = forcast_name(row)
            code = check_code(row)
            relation = relation_in_char(row)
            legend = check_legend(row)
            row_list = [str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])]
            if "NaN" == str(row[0]) or "nan" == str(row[0]) or False in row_list:
                continue
            elif False in [name, code, relation, legend]:
                response_data.append({
                    "id": index,
                    "forecast": row[0],
                    "code": code,
                    "relation": row[2],
                    "intensity": row[3],
                    "area": '' if "NaN" == str(row[4]) or "nan" == str(row[4]) else row[4],
                    "legend": row[5],
                    "error": str(errors).replace('[', "").replace(']', '').replace("'", "").replace(",", "<br>"),
                })
                errors.clear()
                continue
            else:
                weather_codes.objects.create(
                    forecast=row[0],
                    code=code,
                    relation_in_char=row[2],
                    intensity=row[3],
                    area='' if "NaN" == str(row[4]) or "nan" == str(row[4]) else row[4],
                    legend=row[5]
                )
                response_data.append({
                    "id": index,
                    "forecast": row[0],
                    "code": code,
                    "relation": row[2],
                    "intensity": row[3],
                    "area": '' if "NaN" == str(row[4]) or "nan" == str(row[4]) else row[4],
                    "legend": row[5],
                    "error": "",
                })
        return response_data

