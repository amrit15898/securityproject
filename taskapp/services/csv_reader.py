from datetime import datetime
import pandas as pd
from taskapp.models import avalanche_axis_temporary_data, avalanche_message_logs, avalanche_axis
from taskapp.services.avalanche_forecast import avalanche_forecaster_packet_one, avalanche_forecaster_message_two
from django.shortcuts import redirect



csv_reader_kwargs = {"invalid": False, "message": ""}

class Avalanche_file_send(object):

    @staticmethod
    def axis_code_afg_grids(afg):
        if avalanche_axis.objects.filter(axis_code_afg=afg).exists():
            data = avalanche_axis.objects.get(axis_code_afg=afg)
            grids = list(data.grids.split(","))
            context = {
                "grids": grids,
                "avalanche_axis_id": data.avalanche_axis_code
            }
            return context
        else:
            avalanche_message_logs.objects.create(message=f"invalid avalanche afc {afg}")
            return False

    @staticmethod
    def avalanche_temp(grid, date, axis_id, axis_code, outlook):

        if avalanche_axis_temporary_data.objects.filter(grid_id=grid).exists():
            grid_data = avalanche_axis_temporary_data.objects.get(grid_id=grid)
            axis_ids = grid_data.avalanche_axis
            avalanche_code = grid_data.avalanche_code
            axis_ids[f'axis{len(axis_ids)+1}'] = axis_id
            avalanche_code[f'forecast{len(avalanche_code)+1}'] = axis_code
            if grid_data.no_of_axis == 15:
                avalanche_message_logs.objects.create(message=f"{grid_data.grid_id} more than 15 axis in this grid")
                grid_data.delete()
            else:
                grid_data.avalanche_axis = axis_ids
                grid_data.avalanche_code = avalanche_code
                grid_data.no_of_axis = grid_data.no_of_axis + 1
                grid_data.save()

        else:
            avalanche_axis_temporary_data.objects.create(
                date=date,
                grid_id=grid,
                no_of_axis=1,
                avalanche_axis={"axis1": axis_id},
                avalanche_code={"forecast1": axis_code},
                outlook=outlook
            )

    @staticmethod
    def create_log_message(message):
        avalanche_message_logs.objects.create(message=message)

    @classmethod
    def read_excel_code(cls, row):
        code = str(row[2])
        if code == "nan" or code == "":
            cls.create_log_message(f"invalid avalanche axis code at afg {row[0]}")
        elif int(row[2]) > 5:
            cls.create_log_message(f"avalanche axis code is greater than 5 at afg {row[0]}")
        else:
            return code

    @classmethod
    def read_excel_date(cls, row):
        try:
            date = row[1]
            return date
        except Exception:
            cls.create_log_message(f"avalanche axis code missing of afc no {row[0]}")
            return ''

    @classmethod
    def read_excel_aft(cls, row):
        try:
            afc = row[0]
            return afc
        except Exception as e:
            cls.create_log_message(f"avalanche axis code missing of afc no {row[0]}")
            return ''

    @classmethod
    def read_excel_outlook(cls, row):
        outlook = str(row[3])
        if outlook == "nan" or outlook == "":
            cls.create_log_message(f"avalanche outlook missing of afc no {row[0]}")
        else:
            return outlook
    def read_my_csv(self, file):
        try:
            df = pd.read_csv(file, header=None)
            for index, row in df.iterrows():
                # print(row[0], row[1], row[2])
                try:
                    afc = self.read_excel_aft(row)
                    axis_date = self.read_excel_date(row)
                    axis_code = self.read_excel_code(row)
                    outlook = self.read_excel_outlook(row)
                    # print(afc,axis_code,axis_date, outlook)
                    try:
                        sample_list = [afc, axis_code, axis_date, outlook]
                        if "nan" in sample_list or "" in sample_list or None in sample_list:
                            continue
                    except Exception as e:
                        print(e, "here")

                    afg_data = self.axis_code_afg_grids(afc)
                    if afg_data is False:
                        continue
                    for i in afg_data['grids']:
                        self.avalanche_temp(
                            grid=i,
                            date=axis_date,
                            axis_id=afg_data["avalanche_axis_id"],
                            axis_code=axis_code,
                            outlook=outlook
                        )
                except Exception as e:
                    csv_reader_kwargs["invalid"] = True
                    return csv_reader_kwargs

            all_temp_data = avalanche_axis_temporary_data.objects.all()
            response_data = []
            for i in all_temp_data:
                current_date = datetime.strptime(i.date, "%d-%m-%Y").date()
                format_date = datetime.strftime(current_date, "%d%m%y")
                packet = avalanche_forecaster_packet_one(
                    start_date=format_date,
                    grid_id=i.grid_id,
                    num_axis=i.no_of_axis,
                    axis_ids=list(i.avalanche_axis.values()),
                    forecast_codes=list(i.avalanche_code.values()),
                )

                message_two_packet = avalanche_forecaster_message_two(
                    start_date=format_date,
                    grid_id=i.grid_id,
                    outlook=i.outlook
                )
                response_data.append({
                    "id": i.id,
                    "date": format_date,
                    "grid_id": i.grid_id,
                    "no_of_axis": i.no_of_axis,
                    "avalanche_axis": list(i.avalanche_axis.values()),
                    "avalanche_code": list(i.avalanche_code.values()),
                    "packet": packet,
                    "packet2": message_two_packet,
                    "outlook": i.outlook
                })

                i.delete()


        except Exception as e:
            print("here")
            return e
        return response_data



csv_reader = Avalanche_file_send()








































# rest api
# class Avalanche_file_send(generics.CreateAPIView):
#     serializer_class = AvalancheUpload
#     permission_classes = [AllowAny]
#
#     @staticmethod
#     def axis_code_afg_grids(afg):
#         if avalanche_axis.objects.filter(axis_code_afg=afg).exists():
#             data = avalanche_axis.objects.get(axis_code_afg=afg)
#             grids = list(data.grids.split(","))
#             context = {
#                 "grids": grids,
#                 "avalanche_axis_id": data.avalanche_axis_code
#             }
#             return context
#         else:
#             avalanche_message_logs.objects.create(message=f"invalid avalanche afc {afg}")
#             return False
#
#     @staticmethod
#     def avalanche_temp(grid, date, axis_id, axis_code):
#
#         if avalanche_axis_temporary_data.objects.filter(grid_id=grid).exists():
#             grid_data = avalanche_axis_temporary_data.objects.get(grid_id=grid)
#             axis_ids = grid_data.avalanche_axis
#             avalanche_code = grid_data.avalanche_code
#             axis_ids[f'axis{len(axis_ids)+1}'] = axis_id
#             avalanche_code[f'forecast{len(avalanche_code)+1}'] = axis_code
#             grid_data.avalanche_axis = axis_ids
#             grid_data.avalanche_code = avalanche_code
#             grid_data.no_of_axis = grid_data.no_of_axis +1
#             grid_data.save()
#
#         else:
#             avalanche_axis_temporary_data.objects.create(
#                 date=date,
#                 grid_id=grid,
#                 no_of_axis=1,
#                 avalanche_axis={"axis1": axis_id},
#                 avalanche_code={"forecast1": axis_code},
#             )
#
#     @staticmethod
#     def create_log_message(message):
#         avalanche_message_logs.objects.create(message=message)
#
#     @classmethod
#     def read_excel_code(cls, row):
#         try:
#             id = row[2]
#             return id
#         except Exception as e:
#             cls.create_log_message(f"avalanche axis date missing of afc no {row[0]}")
#             return None
#
#     @classmethod
#     def read_excel_date(cls, row):
#         try:
#             date = row[1]
#             return date
#         except Exception as e:
#             cls.create_log_message(f"avalanche axis code missing of afc no {row[0]}")
#             return None
#
#     @classmethod
#     def read_excel_aft(cls, row):
#         try:
#             afc = row[0]
#             return afc
#         except Exception as e:
#             cls.create_log_message(f"avalanche axis code missing of afc no {row[0]}")
#             return None
#
#     def post(self, request, *args, **kwargs):
#         data = AvalancheUpload(data=request.data)
#         if data.is_valid(raise_exception=True):
#             file = data.validated_data['file']
#
#             try:
#                 df = pd.read_excel(file, header=None)
#                 for index, row in df.iterrows():
#                     # print(row[0], row[1], row[2])
#                     try:
#                         afc = self.read_excel_aft(row)
#                         axis_date = self.read_excel_date(row)
#                         axis_code = self.read_excel_code(row)
#                         if afc is None or axis_date is None or axis_code is None:
#                             continue
#
#                         afg_data = self.axis_code_afg_grids(afc)
#                         for i in afg_data['grids']:
#                             self.avalanche_temp(
#                                 grid=i,
#                                 date=axis_date,
#                                 axis_id=afg_data["avalanche_axis_id"],
#                                 axis_code=axis_code
#                             )
#                     except Exception as e:
#                         print(e)
#                 all_temp_data = avalanche_axis_temporary_data.objects.all()
#                 response_data = []
#                 for i in all_temp_data:
#                     current_date = datetime.strptime(i.date, "%d-%m-%Y").date()
#                     format_date = datetime.strftime(current_date, "%d%m%y")
#
#                     response_data.append({
#                         "id": i.id,
#                         "date": format_date,
#                         "grid_id": i.grid_id,
#                         "no_of_axis": i.no_of_axis,
#                         "avalanche_axis": list(i.avalanche_axis.values()),
#                         "avalanche_code": i.avalanche_code.values()
#                     })
#                     i.delete()
#
#
#             except Exception as e:
#                 print(e)
#                 return Response({"status": "invalid file"}, status=status.HTTP_404_NOT_FOUND)
#             return Response(response_data, status=status.HTTP_201_CREATED)
#
#
