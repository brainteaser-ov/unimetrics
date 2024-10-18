from .utils import BaseWorker
import pandas as pd
# from pitch_extraction import pitch_df


class Frequency:
    def __init__(self, min_value: int, max_value: int, dataset: pd.DataFrame):
        self.min_value = min_value
        self.max_value = max_value
        self.dataset = dataset

    def calculate_coeff(self):
        return round((100 / BaseWorker.calculate(self.max_value, self.min_value)), 2)

    def calculate_range_register(self, df):
        # Проверяем наличие столбца 'Mean pitch (PT)'
        if 'Mean pitch (PT)' not in df.columns:
            raise ValueError("Столбец 'Mean pitch (PT)' не найден в датасете")
        # Находим максимальное и минимальное значения
        max_value = df['Mean pitch (PT)'].max()
        min_value = df['Mean pitch (PT)'].min()
        register = [BaseWorker.provide_register(max_value), BaseWorker.provide_register(min_value)]
        return [BaseWorker.provide_range_description(int(max_value - min_value)),
                BaseWorker.find_register(register)]

    def calculate_levels(self) -> pd.DataFrame:
        # Создаем копию входного датасета
        new_dataset = self.dataset.copy()
        # Список колонок для обработки
        pitch_columns = ['Start pitch', 'End pitch', 'Min pitch', 'Max pitch', 'Mean pitch']

        # Функция для обработки каждого значения
        def process_pitch(value):
            rel_pitch = BaseWorker.calculate(value, self.min_value)
            return round(self.calculate_coeff() * rel_pitch, 2)
        # Применяем обработку к каждой колонке
        for column in pitch_columns:
            new_column_name = f'{column} (PT)'
            new_dataset[new_column_name] = new_dataset[column].apply(process_pitch)
        # columns_to_drop = ['Min pitch', 'Max pitch', 'Start pitch', 'End pitch', 'Mean pitch']
        # new_dataset = new_dataset.drop(columns=columns_to_drop)
        return new_dataset

    def calculate_pitch_ratios(self, df):
        # Получаем значения Mean pitch
        mean_pitches = df['Mean pitch (PT)'].values
        syllables = df['Syllable'].values
        # Создаем пустой список для хранения результатов
        ratios = []
        # Вычисляем соотношения только для верхнего треугольника матрицы
        for i in range(len(syllables)):
            for j in range(i + 1, len(syllables)):
                ratio = mean_pitches[i] / mean_pitches[j]
                ratios.append({
                    'Syllable': syllables[i],
                    'Compared_to': syllables[j],
                    'Ratio': round(ratio, 2),
                    'Description': f"{syllables[i]}/{syllables[j]}"
                })
        # Создаем датафрейм из списка словарей
        ratio_df = pd.DataFrame(ratios)
        return ratio_df

    def calculate_intervals(self, dataset):
        # Создаем новый столбец 'Interval' в датасете
        dataset['Interval (PT)'] = ''
        for i, row in dataset.iterrows():
            start_pitch = row['Start pitch (PT)']
            end_pitch = row['End pitch (PT)']
            min_pitch = row['Min pitch (PT)']
            max_pitch = row['Max pitch (PT)']
            if start_pitch > end_pitch:
                # Рассчитываем интервал понижения
                int_fall = abs(((max_pitch - min_pitch) / min_pitch) * 100)
                interval_type = 'int_fall'
                interval_value = int_fall
            else:
                # Рассчитываем интервал повышения
                int_rise = abs(((max_pitch - min_pitch) / max_pitch) * 100)
                interval_type = 'int_rise'
                interval_value = int_rise
            # Записываем результат в столбец 'Speed'
            dataset.at[i, 'Interval (PT)'] = f"{interval_value:.2f} {interval_type}"
        return dataset

    def calculate_pitch_speed(self, df):
        required_columns = ['Syllable', 'Start pitch (PT)', 'End pitch (PT)', 'Duration']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Столбец '{col}' не найден в датасете")
        # Функция для расчета скорости изменения тона
        def calculate_speed(row):
            start_pitch = row['Start pitch (PT)']
            end_pitch = row['End pitch (PT)']
            duration = row['Duration']
            # Проверка на нулевую длительность во избежание деления на ноль
            if duration == 0:
                return 0
            # Расчет скорости как производной (изменение высоты тона / время)
            speed = abs((end_pitch - start_pitch) / duration)
            return round(speed, 2)

        # Применяем функцию к каждой строке и создаем новый столбец 'Speed'
        df['Speed (PT)'] = df.apply(calculate_speed, axis=1)
        # Добавляем единицу измерения к значениям скорости
        df['Speed (PT)'] = df['Speed (PT)'].apply(lambda x: f"{x} PT/s")

        return df

    def add_descriptions(self, df):
        columns_to_describe = ['Mean pitch (PT)', 'Max pitch (PT)', 'Min pitch (PT)',
                               'Start pitch (PT)', 'End pitch (PT)']
        for col in columns_to_describe:
            if col in df.columns:
                new_col_name = f"{col} Description"
                df[new_col_name] = df[col].apply(BaseWorker.provide_description)
            else:
                raise ValueError(f"Столбец '{col}' не найден в датасете")
        return df

    def process_data(self):
        # Рассчитываем уровни
        df = self.calculate_levels()
        data = self.calculate_pitch_ratios(df)
        # Рассчитываем интервалы
        df = self.calculate_intervals(df)
        # Рассчитываем скорость изменения тона
        df = self.calculate_pitch_speed(df)
        # Выбираем только нужные столбцы
        columns_to_keep = ['Syllable', 'Duration', 'Mean pitch', 'Max pitch',
                           'Min pitch', 'Start pitch', 'End pitch',
                           'Mean pitch (PT)', 'Max pitch (PT)',
                           'Min pitch (PT)', 'Start pitch (PT)', 'End pitch (PT)',
                           'Interval (PT)', 'Speed (PT)']

        # Проверяем наличие всех необходимых столбцов
        for col in columns_to_keep:
            if col not in df.columns:
                raise ValueError(f"Столбец '{col}' не найден в датасете")
        df = df[columns_to_keep].copy()
        df = self.add_descriptions(df)
        return df, data


# frequency = Frequency(min_value=80, max_value=500, dataset=pitch_df)
# result_df, data = frequency.process_data()

