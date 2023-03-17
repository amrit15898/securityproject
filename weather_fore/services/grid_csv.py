from weather_fore.models import weather_grids, Grids
import pandas as pd


class Grid_csv:
    @classmethod
    def grid_name_read(cls, row, index, message):
        name = row[1]
        status = True

        if weather_grids.objects.filter(name__iexact=name).exists():
            message.append(f'name {name} is on that index  {index + 1} is alredy exist  ')

            status = False

        return name, status

    @classmethod
    def sect_id_read(cls, row, index, message):
        sect_id = row[2]

        status = True
        if isinstance(sect_id, float) == False:
            message.append(f'sect_id {sect_id} is on that index  {index + 1} is not float value  ')
            status = False

        elif weather_grids.objects.filter(sect_id=sect_id).exists():

            message.append(f'sect_id {sect_id} is on that index  {index + 1} is alredy exist  ')
            status = False
        return sect_id, status

    @classmethod
    def read_forecast_area(cls, row, index, message):
        forecast_area = row[3]

        status = True

        if isinstance(forecast_area, int) == False:
            message.append(f'forecast_area {forecast_area} is on that index  {index + 1} is not int value  ')
            status = False

        elif weather_grids.objects.filter(forecast_area=forecast_area).exists():

            message.append(f'forecast_area {forecast_area} is on that index  {index + 1} is alredy exist  ')
            status = False

        if len(str(forecast_area)) == 2:
            forecast_area = "0"+str(forecast_area)
        elif len(str(forecast_area)) == 1:
            forecast_area = "00"+str(forecast_area)
        return forecast_area, status

    @classmethod
    def read_natsat_grid(cls, row, index, message):
        status = True
        grid = row[4]
        grid_data = grid.split(',')
        grid_lis = []
        grid_len = []
        grid_int = []

        for i in grid_data:

            if i.isnumeric() == False and i != "":
                grid_int.append(i)
                status = False

            if len(i) != 4:
                grid_len.append(i)
                status = False

            if Grids.objects.filter(grid_id=i).exists():
                grid_lis.append(i)
                status = False

        if status is True:
            return grid, status
        else:
            data = ' '.join(grid_lis)
            message.append(f'Grid {data} is on that index {index+1} is already exist')

        if grid_len:
            gr_len = ' '.join(grid_len)
            message.append(f'Grid {gr_len} is on not equal to 4 at index {index + 1} or invalid format')

        if grid_int:
            gr_int = ' '.join(grid_int)
            message.append(f'Grid {gr_int} invalid(integer required)')

        return grid, status

    @classmethod
    def file_read(cls, file):
        df = pd.read_csv(file, header=None, skiprows=[0])
        response_data = []

        for index, row in df.iterrows():

            message = []
            name, name_status = cls.grid_name_read(row, index, message)
            sect_id, sect_id_status = cls.sect_id_read(row, index, message)
            forecast_area, forecast_area_status = cls.read_forecast_area(row, index, message)
            grids, grids_status = cls.read_natsat_grid(row, index, message)

            if name_status and sect_id and forecast_area_status and grids_status == True:
                grid_obj = []
                grid_data = grids.split(',')
                for i in grid_data:
                    obj = Grids.objects.create(grid_id=i)
                    grid_obj.append(obj)

                weather_grids_obj = weather_grids.objects.create(name=name, sect_id=sect_id,
                                                                 forecast_area=forecast_area)
                weather_grids_obj.natsat_grids.set(grid_obj)
                weather_grids_obj.save()

            response_data.append({
                "id": index,
                "name": name,
                "sect_id": sect_id,
                "forecast_area": forecast_area,
                "grids": grids,
                "message": message

            })


        return response_data


grid_csv = Grid_csv()

