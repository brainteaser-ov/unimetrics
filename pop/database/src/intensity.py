from .utils import BaseWorker
import pandas as pd
import numpy as np
# from pitch_extraction import intensity_df


class Loudness():
    def __init__(self, df: pd.DataFrame, min_intensity: float, max_intensity: float):
        self.df = df
        self.min_intensity = min_intensity
        self.max_intensity = max_intensity

    def calculate_coeff(self) -> float:
        return round((100 / (self.max_intensity - self.min_intensity)), 3)

    def calculate_levels(self) -> pd.DataFrame:
        coeff = self.calculate_coeff()
        intensity_columns = ['Max intensity', 'Start intensity', 'End intensity', 'Mean intensity']

        for col in intensity_columns:
            new_col_name = f'{col} (R)'
            self.df[new_col_name] = self.df[col].apply(lambda x: int(coeff * (x - self.min_intensity)))
            self.df[f'{new_col_name} description'] = self.df[new_col_name].apply(BaseWorker.provide_description)

        return self.df

    def calculate_intensity_speed(self) -> pd.DataFrame:
        self.df['Intensity Speed'] = abs(
            round((self.df['End intensity'] - self.df['Start intensity']) / self.df['Duration'], 3))
        return self.df

    def calculate_intensity_ratios(self) -> pd.DataFrame:
        # Получаем значения Mean intensity
        mean_intensities = self.df['Mean intensity'].values
        syllables = self.df['Syllable'].values
        # Создаем пустой список для хранения результатов
        ratios = []
        # Вычисляем соотношения только для верхнего треугольника матрицы
        for i in range(len(syllables)):
            for j in range(i + 1, len(syllables)):
                ratio = mean_intensities[i] / mean_intensities[j]
                ratios.append({
                    'Syllable': syllables[i],
                    'Compared_to': syllables[j],
                    'Ratio': round(ratio, 2),
                    'Description': f"{syllables[i]}/{syllables[j]}"
                })
        # Создаем датафрейм из списка словарей
        ratio_df = pd.DataFrame(ratios)
        return ratio_df

    def calculate_statistics(self) -> pd.DataFrame:
        self.df['Intensity variance'] = round(self.df['Mean intensity'].var(), 3)
        self.df['Intensity mean'] = round(self.df['Mean intensity'].mean(), 3)
        return self.df

    def process_data(self) -> tuple:
        self.calculate_levels()
        self.calculate_statistics()
        self.calculate_intensity_speed()
        intensity_ratios = self.calculate_intensity_ratios()
        return self.df, intensity_ratios


# loudness = Loudness(intensity_df, min_intensity=20, max_intensity=100)
# processed_df, intensity_ratios_df = loudness.process_data()



