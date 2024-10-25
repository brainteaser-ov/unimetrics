import os
import pandas as pd
import parselmouth
from parselmouth.praat import call
from textgrid import TextGrid
from .utils_vowels import SoundSample

# class FormantExtractor:
#     def __init__(self, directory):
#         self.directory = directory

class FormantExtractor():
    def __init__(self, audio_file_path, textgrid_file_path):
        self.audio_file_path = audio_file_path
        self.textgrid_file_path = textgrid_file_path

    def extract_formants(self):
        data = []  # To store the results

        # Get all the .wav files in the directory
        wav_files = self.audio_file_path

        for wav_file in wav_files:
            base_name = os.path.splitext(wav_file)[0]  # File name without extension
            wav_path = self.audio_file_path
            textgrid_path = self.textgrid_file_path

            if not os.path.exists(self.textgrid_file_path):
                print(f"No TextGrid file found for {wav_file}, skipping.")
                continue

            # Load the TextGrid file using 'textgrid'
            try:
                tg = TextGrid.fromFile(self.textgrid_file_path)
            except Exception as e:
                print(f"Error reading TextGrid file {self.textgrid_file_path}: {e}")
                continue

            # Find the tier named 'sound'
            sound_tier = tg.getFirst('sound')
            if sound_tier is None:
                print(f"No 'sound' tier found in {self.textgrid_file_path}, skipping.")
                continue

            # Load the .wav file using 'parselmouth'
            snd = parselmouth.Sound(wav_path)

            # Process each interval in the 'sound' tier
            for interval in sound_tier:
                label = interval.mark.strip()
                if label != '':
                    start_time = interval.minTime
                    end_time = interval.maxTime
                    duration = end_time - start_time  # Calculate duration

                    # Extract the segment corresponding to the interval
                    segment = snd.extract_part(from_time=start_time, to_time=end_time, preserve_times=False)

                    # Compute formants using Praat's algorithms via parselmouth
                    formant = call(segment, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)

                    # Get formant values at the midpoint of the segment
                    t = segment.duration / 2.0
                    f1 = call(formant, "Get value at time", 1, t, 'Hertz', 'Linear')
                    f2 = call(formant, "Get value at time", 2, t, 'Hertz', 'Linear')
                    f3 = call(formant, "Get value at time", 3, t, 'Hertz', 'Linear')

                    # Append the data, including Duration and File Name
                    data.append({
                        'File Name': base_name,
                        'Sound Name': label,
                        'Duration': duration,
                        'F1': f1,
                        'F2': f2,
                        'F3': f3
                    })

        # Save the data to a DataFrame
        df = pd.DataFrame(data)
        return df

class FormantAnalyser():
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def process_data(self):
        # Process the dataframe, adding new columns, comparing formant values with reference
        self.formant_reference()
        self.calculate_percent_duration()
        df = self.add_columns()
        return df

    def formant_reference(self):
        transcription = []
        for index, row in self.dataframe.iterrows():
            if row['Sound Name'] in SoundSample.consonants:
                transcription.append('consonant')
            else:
                f1 = row['F1']
                f2 = row['F2']
                matched = False
                for vowel, v_f1, v_f2 in SoundSample.formant_reference_table:
                    if v_f1 - 100 <= f1 <= v_f1 + 100 and v_f2 - 100 <= f2 <= v_f2 + 100:
                        transcription.append(vowel)
                        matched = True
                        break
                if not matched:
                    transcription.append('unknown')

        self.dataframe['Transcription'] = transcription
        return self.dataframe

    def calculate_percent_duration(self):
        df = self.formant_reference()
        # Sum the total duration for each file
        total_durations = df.groupby('File Name')['Duration'].sum().reset_index()
        total_durations.rename(columns={'Duration': 'Total_duration'}, inplace=True)

        # Initialize the Percent_duration column
        df['Percent_duration'] = 0.0

        # For each row in the original DataFrame
        for index, row in df.iterrows():
            filename = row['File Name']
            vowel_duration = row['Duration']

            # Calculate the total duration for the given file
            total_duration = df[df['File Name'] == filename]['Duration'].sum()

            # Calculate the percentage
            percent_duration = round(vowel_duration / total_duration * 100, 3)

            # Assign the percentage to the DataFrame directly
            df.at[index, 'Percent_duration'] = percent_duration

        # Merge with total durations
        result_df = pd.merge(df, total_durations, on='File Name', how='left')

        return result_df


    def add_columns(self):
        # Add new columns to the dataframe
        df = self.calculate_percent_duration()

        # Calculate R1, R2, and R3
        def calculate_R3(row):
            if row['Transcription'] != 'consonant':
                return row['F3'] / row['F1']
            return None

        def calculate_R2(row):
            if row['Transcription'] != 'consonant':
                return row['F3'] / row['F2']
            return None

        def calculate_R1(row):
            if row['Transcription'] != 'consonant':
                return row['F2'] / row['F1']
            return None

        df['R1'] = df.apply(calculate_R1, axis=1)
        df['R2'] = df.apply(calculate_R2, axis=1)
        df['R3'] = df.apply(calculate_R3, axis=1)

        return df

class FormantDataframe():
    def __init__(self, audio_file_path, textgrid_file_path):
        self.audio_file_path = audio_file_path
        self.textgrid_file_path = textgrid_file_path

    def write_to_excel(self, excel_filename='formant_analysis.xlsx'):
        extractor = FormantExtractor(self.audio_file_path, self.textgrid_file_path)
        # print(extractor)
        dataframe = extractor.extract_formants()
        analyser = FormantAnalyser(dataframe)
        df = analyser.process_data()
        return df
        # # Сохраняем результирующий файл в той же директории, что и аудиофайл
        # output_folder = os.path.dirname(self.audio_file_path)
        # output_path = os.path.join(output_folder, excel_filename)
        # df.to_excel(output_path, index=False)
        # print(f"Formant analysis saved to {output_path}")

#
# class FormantDataframe():
#     def __init__(self, folder_path):
#         self.folder_path = folder_path
#
#     def write_to_excel(self, excel_filename='formant_analysis.xlsx'):
#         extractor = FormantExtractor(self.folder_path)
#         print(extractor)
#         dataframe = extractor.extract_formants()
#         analyser = FormantAnalyser(dataframe)
#         df = analyser.process_data()
#         output_path = os.path.join(self.folder_path, excel_filename)
#         df.to_excel(output_path, index=False)
#         print(f"Formant analysis saved to {output_path}")


