import pandas as pd

from taskapp.models import avalanche_axis, avalanche_grid


def log_message_generator(row, index):
    if str(row[1]) == "nan":
        return f"Empty axis title at {index}"
    elif str(row[2])== "nan":
        return f"Empty axis id at {index}"
    elif str(row[3]) == "nan":
        return f"Empty AOR at {index}"
    elif str(row[4]) == "nan":
        return f"Empty grids at {index}"

    elif str(row[5]) == "nan":
        return f"Empty AFG code at {index}"

    return ""


def axis_add_csv(file):
    # try:
    df = pd.read_csv(file, dtype=str, header=None, skiprows=[0])
    response_data = []
    for index, row in df.iterrows():
        status = True
        message = []
        axis_title = str(row[1])
        axis_id = str(row[2])
        aor = str(row[3])
        grids = str(row[4])
        axis_code_afg = str(row[5])

        if str(axis_title) != 'nan' and str(axis_id) != 'nan' and str(aor) != 'nan' and str(grids) != 'nan' and str(
                axis_code_afg) != 'nan':
            if avalanche_axis.objects.filter(avalanche_axis__iexact=axis_title).exists():
                message.append(f'the Avalanche_Axis  {axis_title} is already exists <br>')
                status = False

            if avalanche_axis.objects.filter(avalanche_axis_code=axis_id).exists():
                message.append(f'the avalanche_axis_code  {axis_id} is already exists <br>')
                status = False
            else:

                if axis_id.isnumeric() == False:
                    message.append(f'the axis_id  {axis_id}  not a numeric <br>')
                    status = False
                if len(axis_id) != 3:
                    message.append(f'the axis_id  {axis_id}  length must  be equal to 3 <br>')
                    status = False

            try:
                grid = list(grids.split(","))
            except Exception as e:
                print(e)

            if ' ' in grid:
                message.append(f"invalid grids at has a  space <br>")
                status = False
            else:
                temp = []
                for i in grid:
                    if grid.count(i) > 1:
                        if i not in temp:
                            temp.append(i)
                            message.append(f"  grids {i} has already exist <br>")
                            status = False

                    if len(i) != 4:
                        message.append(f'the grids  {grids}  length must  be equal to 4 <br>')
                        status = False

                    if i.isnumeric() == False:
                        message.append(f'the grids  {grids}  not numeric value <br>')
                        status = False

            if avalanche_axis.objects.filter(axis_code_afg=axis_code_afg).exists():
                message.append(f'the axis_code_afg  {axis_code_afg} is already exists <br>')

            else:
                if axis_code_afg.isnumeric() == False:
                    message.append(f'the axis_code_afg  {axis_code_afg} is already exists <br>')

        try:
            print(grids)
            avalanche_axis.objects.create(
                    avalanche_axis=axis_title,
                    avalanche_axis_code=axis_id,
                    aor=aor,
                    grids=grids,
                    axis_code_afg=axis_code_afg
                )
            try:
                for g in list(grids.split(",")):
                    avalanche_grid.objects.create(
                        grid_id=g
                    )
            except:
                pass
        except Exception as e:
            message.append(str(e))

        response_data.append({
            "id": index,
            "axis_title": axis_title,
            "axis_id": axis_id,
            "aor": aor,
            "grids": grids,
            "axis_code_afg": axis_code_afg,
            "message": message
        })

    return response_data



