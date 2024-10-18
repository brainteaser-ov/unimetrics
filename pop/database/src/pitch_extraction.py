import os
import parselmouth
import pandas as pd

class MainData:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def get_duration(self):
        sound = parselmouth.Sound(self.audio_file)
        return sound.duration

    def analyze_pitch(self):
        pitch_data = []
        for file in self.audio_file:
            sound = parselmouth.Sound(file)
            pitch = sound.to_pitch()
            pitch_values = pitch.selected_array['frequency']
            filtered_pitch = list(filter(lambda x: x != 0, pitch_values))

            if filtered_pitch:
                pitch_info = {
                    "Syllable": os.path.splitext(os.path.basename(file))[0],
                    "Min pitch": int(min(filtered_pitch)),
                    "Max pitch": int(max(filtered_pitch)),
                    "Start pitch": int(next((x for x in pitch_values if x != 0), 0)),
                    "End pitch": int(next((x for x in reversed(pitch_values) if x != 0), 0)),
                    "Mean pitch": int(sum(filtered_pitch) / len(filtered_pitch)),
                    "Duration": round(self.get_duration(), 3)
                }
            else:
                pitch_info = {
                    "Syllable": os.path.splitext(os.path.basename(file))[0],
                    "Min pitch": 0,
                    "Max pitch": 0,
                    "Start pitch": 0,
                    "End pitch": 0,
                    "Mean pitch": 0,
                    "Duration": round(self.get_duration(), 3)
                }
            pitch_data.append(pitch_info)

        return pd.DataFrame(pitch_data)

    def analyze_intensity(self):
        intensity_data = []
        for file in self.audio_file:
            sound = parselmouth.Sound(file)
            intensity = sound.to_intensity()
            intensity_values = intensity.values[0]

            intensity_info = {
                "Syllable": os.path.splitext(os.path.basename(file))[0],
                "Min intensity": int(min(filter(lambda x: x > 0, intensity_values))),
                "Max intensity": int(max(intensity_values)),
                "Start intensity": int(next((x for x in intensity_values if x > 0), 0)),
                "End intensity": int(intensity_values[-1]),
                "Mean intensity": int(sum(intensity_values) / len(intensity_values)),
                "Duration": round(self.get_duration(), 3)
            }
            intensity_data.append(intensity_info)

        return pd.DataFrame(intensity_data)

    def get_datasets(self):
        pitch_df = self.analyze_pitch()
        intensity_df = self.analyze_intensity()
        return pitch_df, intensity_df


# data = MainData(audio_f)
# pitch_df, intensity_df = data.get_datasets()

