# import pandas as pd
# from pitch_extraction import MainData
# from frequency import Frequency
# from intensity import Loudness
# from rate import Rate
#
# audio_f = '/Users/oksanagoncarova/Desktop/Новая папка/r_r_split'
#
# def process_data():
#     data = MainData(audio_f)
#     pitch_df, intensity_df = data.get_datasets()
#
#     # Вызов класса Frequency
#     frequency = Frequency(min_value=80, max_value=500, dataset=pitch_df)
#     pitch_df, pitch_ratios = frequency.process_data()
#
#     # Вызов класса Loudness
#     loudness = Loudness(intensity_df, min_intensity=40, max_intensity=130)
#     intensity_df, intensity_ratios = loudness.process_data()
#
#     # Вызов класса Rate
#     rate = Rate(intensity_df)
#     rate_df, rate_ratios = rate.process_data()
#
#     # Объединение результатов в один Excel-файл
#     with pd.ExcelWriter('final_results.xlsx') as writer:
#         pitch_df.to_excel(writer, sheet_name='Pitch', index=False)
#         pitch_ratios.to_excel(writer, sheet_name='Pitch Ratios', index=False)
#         intensity_df.to_excel(writer, sheet_name='Intensity', index=False)
#         intensity_ratios.to_excel(writer, sheet_name='Intensity Ratios', index=False)
#         rate_df.to_excel(writer, sheet_name='Rate', index=False)
#         rate_ratios.to_excel(writer, sheet_name='Rate Ratios', index=False)
#
#     # # Сохранение отдельных документов .doc
#     # to_doc(pitch_df, 'final_pitch.doc')
#     # to_doc(pitch_ratios, 'pitch_ratio.doc')
#     # to_doc(intensity_df, 'final_intensity.doc')
#     # to_doc(intensity_ratios, 'intensity_ratios.doc')
#     # to_doc(rate_df, 'rate.doc')
#     # to_doc(rate_ratios, 'rate_ratio.doc')
#
#
# process_data()
