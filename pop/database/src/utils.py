from abc import ABC, abstractmethod
from typing import Any, List

import numpy as np


class Parameters(ABC):
    def __init__(self, syllables_list: List[float]):
        self.syllables_list = syllables_list

    @abstractmethod
    def calculate_coeff(self):
        pass

    @abstractmethod
    def calculate_mean(self):
        pass

    @abstractmethod
    def calculate_corr(self):
        pass

    @abstractmethod
    def calculate_nuclear(self):
        pass

    @abstractmethod
    def calculate_stressed(self):
        pass


class Calculation(Parameters, ABC):
    def __init__(self, syllables_list: List[float]):
        super().__init__(syllables_list)

    def calculate_mean(self):
        return sum(self.syllables_list) / len(self.syllables_list) * self.calculate_coeff()


class BaseWorker:

    @staticmethod
    def provide_description(value: Any) -> str:
        if 0 <= value <= 16:
            return f"ЭН: {value}"
        elif 17 <= value <= 33:
            return f"Н: {value}"
        elif 34 <= value <= 50:
            return f"СН: {value}"
        elif 51 <= value <= 67:
            return f"СВ: {value}"
        elif 68 <= value <= 84:
            return f"В: {value}"
        elif 85 <= value:
            return f"ЭВ: {value}"

    @staticmethod
    def provide_range_description(value: Any) -> str:
        if 0 <= value <= 16:
            return f"Мал: {value}"
        elif 17 <= value <= 33:
            return f"Уз: {value}"
        elif 34 <= value <= 50:
            return f"СУ: {value}"
        elif 51 <= value <= 67:
            return f"Ср: {value}"
        elif 68 <= value <= 84:
            return f"Расшир: {value}"
        elif 85 <= value:
            return f"Шир: {value}"

    @staticmethod
    def get_dictionary():
        tone_dict = {
            1.059: 1,
            1.122: 2,
            1.188: 3,
            1.258: 4,
            1.331: 5,
            1.411: 6,
            1.494: 7,
            1.582: 8,
            1.675: 9,
            1.744: 10,
            1.879: 11,
            2: 12,
            2.118: 13,
            2.234: 14,
            2.357: 15,
            2.596: 16,
            2.749: 17,
            2.911: 18,
            3.266: 20,
            3.439: 21,
            3.642: 22,
            3.857: 23,
            4: 24,
            4.236: 25,
            4.586: 26,
            4.857: 27,
            5.144: 28,
            5.447: 29,
            5.748: 30,
            6.1: 31,
            6.446: 32,
            6.826: 33,
            7.229: 34,
            7.965: 35,
            9: 36
        }
        return tone_dict

    @staticmethod
    def unpack_list(result: Any):
        row = []
        for i in range(len(result)):
            if 0 <= result[i] <= 1.3:
                row.append(['Мин', result[i]])
            if 1.4 <= result[i] <= 1.5:
                row.append(["Сл", result[i]])
            if 1.6 <= result[i] <= 1.9:
                row.append(["Ср", result[i]])
            if 2 <= result[i] <= 3:
                row.append(["Ярк", result[i]])
            if result[i] >= 3.1:
                row.append(["Макс", result[i]])
        return row

    @staticmethod
    def provide_register(value: Any) -> int:
        if 0 <= value <= 16:
            # print(f"НУн: {value};")
            return 1
        elif 17 <= value <= 33:
            # print(f"НУв: {value};")
            return 2
        elif 34 <= value <= 50:
            # print(f"СУн: {value};")
            return 3
        elif 51 <= value <= 67:
            # print(f"СУв: {value};")
            return 4
        elif 68 <= value <= 84:
            # print(f"ВУн: {value};")
            return 5
        elif 85 <= value <= 100:
            # print(f"Вув: {value};")
            return 6
        else:
            return "Неверное значение"

    @staticmethod
    def find_register(result: Any) -> str:
        if result[0] == 6 and result[1] == 5:
            print(f"ВУ: {(result[0], result[1])}")
            return f"ВУ"
        if result[0] == 6 and result[1] == 4:
            print(f"ВШвв: {(result[0], result[1])}")
            return f"ВШвв"
        if result[0] == 6 and result[1] == 3:
            print(f"ВШ: {(result[0], result[1])}")
            return f"ВШ"
        if result[0] == 6 and result[1] == 2:
            print(f"Пвв: {(result[0], result[1])}")
            return f"Пвв"
        if result[0] == 6 and result[1] == 1:
            print(f"П: {(result[0], result[1])}")
            return f"П"
        if result[0] == 5 and result[1] == 4:
            print(f"ВШнв: {(result[0], result[1])}")
            return f"ВШнв"
        if result[0] == 5 and result[1] == 3:
            print(f"ВШнн: {(result[0], result[1])}")
            return f"ВШнн"
        if result[0] == 5 and result[1] == 2:
            print(f"Пнв: {(result[0], result[1])}")
            return f"Пнв"
        if result[0] == 5 and result[1] == 1:
            print(f"Пнн: {(result[0], result[1])}")
            return f"Пнн"
        if result[0] == 4 and result[1] == 3:
            print(f"СУ: {(result[0], result[1])}")
            return f"СУ"
        if result[0] == 4 and result[1] == 2:
            print(f"СШвв: {(result[0], result[1])}")
            return f"СШвв"
        if result[0] == 4 and result[1] == 1:
            print(f"СШ: {(result[0], result[1])}")
            return f"СШ"
        if result[0] == 3 and result[1] == 2:
            print(f"СШнв: {(result[0], result[1])}")
            return f"СШнв"
        if result[0] == 3 and result[1] == 1:
            print(f"СШнн: {(result[0], result[1])}")
            return f"СШнн"
        if result[0] == 2 and result[1] == 1:
            print(f"НУ: {(result[0], result[1])}")
            return f"НУ"

        return "Неверное значение"

    @staticmethod
    def calculate(number1, number2) -> int:
        tone_dict = BaseWorker.get_dictionary()
        key = min(tone_dict.keys(), key=lambda x: abs(x - (number1 / number2)))
        value = tone_dict[key]
        return value

    @staticmethod
    def correlation(result):
        row = []
        for i in range(len(result) - 1):
            row.append(round((result[i] / result[i + 1]), 3))
        if len(result) > 2:
            row.append(round((result[0] / result[2]), 3))

        return row

    @staticmethod
    def round_list(result):
        rounded_result = []
        for value in result:
            rounded_value = round(value, 1)
            rounded_result.append(rounded_value)
        return rounded_result

    @staticmethod
    def variance(lst, coefficient):
        # Умножаем каждое число в списке на коэффициент
        multiplied_lst = [num * coefficient for num in lst]
        variance = np.var(multiplied_lst)
        return variance

    @staticmethod
    def std_deviation(lst, coefficient):
        multiplied_lst = [num * coefficient for num in lst]
        std_deviation = np.std(multiplied_lst)
        return std_deviation

    @staticmethod
    def plots(lst, coefficient):
        plot_lst = [num * coefficient for num in lst]

    @staticmethod
    def find_closest_key(dictionary, variable):
        closest_key = None
        min_difference = float('inf')

        for key in dictionary.keys():
            difference = abs(variable - key)
            if difference < min_difference:
                min_difference = difference
                closest_key = key

        return dictionary[closest_key]

