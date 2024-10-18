# import pandas as pd
# from docx import Document
#
#
# def xsl_to_dataframe(file_path):
#     # Преобразование XSL в CSV
#     csv_file = file_path.replace('.xsl', '.csv')
#     xls = pd.read_excel(file_path)
#
#     xls.to_csv(csv_file, index=False)
#
#     # Создание датафрейма из данных CSV
#     df = pd.read_csv(csv_file)
#
#     return df
#
#
# def save_df_as_csv(df, csv_file_path):
#     # Сохранение датафрейма в файл CSV
#     df.to_csv(csv_file_path, index=False)
#
#
# def split_column_to_str_int(df, column_name):
#     df[f'{column_name}_str'] = ''
#     df[f'{column_name}_int'] = ''
#     df[column_name] = df[column_name].str.replace('[', '').str.replace(']', '').str.replace(',', '')
#     df[column_name] = df[column_name].str.replace("'", '')
#     # Проход по каждой строке столбца НФ/КФ_pitch
#     for index, row in df.iterrows():
#         # Разделение значения на две части
#         value_list = row[column_name].split(' ')
#         # Запись строковой части в столбец НФ/КФ_pitch_str
#         df.loc[index, f'{column_name}_str'] = value_list[0]
#         # Запись числовой части в столбец НФ/КФ_pitch_int
#         df.loc[index, f'{column_name}_int'] = (value_list[1])
#
#     df = df.drop([column_name], axis=1)
#     return df
#
#
# def interval_split(df, column_name):
#     df[f'{column_name}_str'] = ''
#     df[f'{column_name}_int'] = ''
#     df[column_name] = df[column_name].str.replace(':', '')
#     # Проход по каждой строке столбца НФ/КФ_pitch
#     for index, row in df.iterrows():
#         # Разделение значения на две части
#         value_list = row[column_name].split(' ')
#         # Запись строковой части в столбец НФ/КФ_pitch_str
#         df.loc[index, f'{column_name}_str'] = value_list[0]
#         # Запись числовой части в столбец НФ/КФ_pitch_int
#         df.loc[index, f'{column_name}_int'] = (value_list[1])
#
#     df = df.drop([column_name], axis=1)
#     return df
#
#
# def level_split(df, column):
#     df[f'{column}_start'] = ''
#     df[f'{column}_stressed'] = ''
#     df[f'{column}_end'] = ''
#     for index, row in df.iterrows():
#         if isinstance(row[column], list):
#             levels = row[column]
#             df.at[index, f'{column}_start'] = levels[0].strip()
#             df.at[index, f'{column}_stressed'] = levels[1].strip()
#             df.at[index, f'{column}_end'] = levels[2].strip()
#     df = df.drop([column], axis=1)
#     return df
#
#
# def range_split(df, column):
#     df['тональный диапазон'] = ''
#     df['регистр'] = ''
#     for index, row in df.iterrows():
#         if isinstance(row[column], list):
#             levels = row[column]
#             df.at[index, 'тональный диапазон'] = levels[0].strip()
#             df.at[index, 'регистр'] = levels[1].strip()
#
#     df = df.drop([column], axis=1)
#     return df
#
#
# def correlation_split(df, column):
#     df['НФ/ПУ_pitch'] = ''
#     df['ПУ/КФ_pitch'] = ''
#     df['НФ/КФ_pitch'] = ''
#     for index, row in df.iterrows():
#         if isinstance(row[column], list):
#             levels = row[column]
#             df.at[index, 'НФ/ПУ_pitch'] = str(levels[0]).strip()
#             df.at[index, 'ПУ/КФ_pitch'] = str(levels[1]).strip()
#             df.at[index, 'НФ/КФ_pitch'] = str(levels[2]).strip()
#     df = df.drop([column], axis=1)
#     return df
#
#
# def to_doc(data, filename):
#     doc = Document()
#
#     table = doc.add_table(data.shape[0] + 1, data.shape[1])
#     for i in range(data.shape[1]):
#         table.cell(0, i).text = data.columns[i]
#     for i in range(data.shape[0]):
#         for j in range(data.shape[1]):
#             table.cell(i + 1, j).text = str(data.values[i, j])
#
#     # Сохраняем документ
#     doc.save(filename + '.docx')
