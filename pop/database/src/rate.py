import pandas as pd
from utils.utils import BaseWorker
from pitch_extraction import intensity_df
from utils.utils_transform import to_doc
import numpy as np

class Rate:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.min_duration = self.df['Duration'].min()
        self.max_duration = self.df['Duration'].max()

    def calculate_coeff(self) -> float:
        return 100 / (self.max_duration - self.min_duration)

    def calculate_relative_duration(self) -> pd.DataFrame:
        coeff = self.calculate_coeff()
        self.df['Duration (R)'] = self.df['Duration'].apply(lambda x: int(coeff * (x - self.min_duration)))
        self.df['Duration (R) description'] = self.df['Duration (R)'].apply(BaseWorker.provide_description)
        return self.df

    def calculate_mean_syllable_duration(self) -> float:
        return self.df['Duration'].mean()

    def calculate_mean_syllable_duration_description(self) -> str:
        mean_duration = self.calculate_mean_syllable_duration()
        coeff = self.calculate_coeff()
        relative_mean = int(coeff * (mean_duration - self.min_duration))
        return BaseWorker.provide_description(relative_mean)

    def calculate_duration_ratios(self) -> pd.DataFrame:
        # Получаем значения Duration
        durations = self.df['Duration'].values
        syllables = self.df['Syllable'].values
        # Создаем пустой список для хранения результатов
        ratios = []
        # Вычисляем соотношения только для верхнего треугольника матрицы
        for i in range(len(syllables)):
            for j in range(i + 1, len(syllables)):
                ratio = durations[i] / durations[j]
                ratios.append({
                    'Syllable': syllables[i],
                    'Compared_to': syllables[j],
                    'Ratio': round(ratio, 2),
                    'Description': f"{syllables[i]}/{syllables[j]}"
                })
        # Создаем датафрейм из списка словарей
        ratio_df = pd.DataFrame(ratios)
        return ratio_df

    def process_data(self):
        self.calculate_relative_duration()
        mean_duration = self.calculate_mean_syllable_duration()
        mean_description = self.calculate_mean_syllable_duration_description()

        result_df = self.df[['Syllable', 'Duration', 'Duration (R)', 'Duration (R) description']].copy()
        result_df['Mean Syllable Duration'] = mean_duration
        result_df['Mean Syllable Duration Description'] = mean_description

        # Вычисляем соотношения длительностей
        ratios_df = self.calculate_duration_ratios()

        return result_df, ratios_df


rate = Rate(intensity_df)
processed_df, ratios_df = rate.process_data()

