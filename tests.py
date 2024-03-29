from unittest import TestCase

from pydantic import ValidationError

from calculate_deposit import calculate_deposit
from dto import PostDepositInput


class TestValidatePostDepositInput(TestCase):

    def test_valid(self):
        date_ = ['01.01.2000', '31.01.2020', '29.02.2020', '15.06.2022', '31.12.2021']
        periods = [1, 60, 11, 24, 37]
        amount = [10000, 10001, 300000, 1500000, 3000000]
        rate = [1, 8, 2, 4, 6]

        for i in range(5):
            input_ = PostDepositInput(
                **{'date': date_[i], 'periods': periods[i], 'amount': amount[i], 'rate': rate[i]}
            )
            assert input_.date_ == date_[i] and input_.periods == periods[i] \
                   and input_.amount == amount[i] and input_.rate == rate[i]

    def test_invalid(self):
        input_dicts = {
            'date': ['01.01.56786', '50.01.2020', '12.30.2020', '15/06/2022', '31-12-2021'],
            'periods': [0, -2, 61, 0.5, 1000],
            'amount': [9999, -10001, 3000001, 0, 300000000],
            'rate': [0.5, -3, 0, 8.01, 10]
        }

        for key, values in input_dicts.items():
            for value in values:
                with self.assertRaises(ValidationError):
                    print(key, value)
                    PostDepositInput(
                        **({
                            'date': '05.10.2023',
                            'periods': 10,
                            'amount': 20000,
                            'rate': 4
                        } | {key: value})
                    )


class TestCalculateDeposit(TestCase):

    def test_periods_1(self):
        inputs = [
            {'date': '01.01.2001', 'periods': 1, 'amount': 10000, 'rate': 1},
            {'date': '31.01.2001', 'periods': 6, 'amount': 100000, 'rate': 3},
            {'date': '28.02.2001', 'periods': 12, 'amount': 100005, 'rate': 5},
            {'date': '30.04.2001', 'periods': 13, 'amount': 50000, 'rate': 7},
            {'date': '15.05.2003', 'periods': 24, 'amount': 11000, 'rate': 2}
        ]
        outputs = [
            {'01.01.2001': 10008.33},
            {
                '31.01.2001': 100250.0, '28.02.2001': 100500.63, '31.03.2001': 100751.88,
                '30.04.2001': 101003.76, '31.05.2001': 101256.27, '30.06.2001': 101509.41
            },
            {
                '28.02.2001': 100421.69, '28.03.2001': 100840.11, '28.04.2001': 101260.28,
                '28.05.2001': 101682.2, '28.06.2001': 102105.87, '28.07.2001': 102531.31,
                '28.08.2001': 102958.53, '28.09.2001': 103387.52, '28.10.2001': 103818.3,
                '28.11.2001': 104250.88, '28.12.2001': 104685.26, '28.01.2002': 105121.45
            },
            {
                '30.04.2001': 50291.67, '30.05.2001': 50585.03, '30.06.2001': 50880.11,
                '30.07.2001': 51176.91, '30.08.2001': 51475.45, '30.09.2001': 51775.72,
                '30.10.2001': 52077.75, '30.11.2001': 52381.53, '30.12.2001': 52687.09,
                '30.01.2002': 52994.43, '28.02.2002': 53303.57, '30.03.2002': 53614.5,
                '30.04.2002': 53927.26
            },
            {
                '15.05.2003': 11018.33, '15.06.2003': 11036.7, '15.07.2003': 11055.09,
                '15.08.2003': 11073.52, '15.09.2003': 11091.97, '15.10.2003': 11110.46,
                '15.11.2003': 11128.98, '15.12.2003': 11147.53, '15.01.2004': 11166.1,
                '15.02.2004': 11184.71, '15.03.2004': 11203.36, '15.04.2004': 11222.03,
                '15.05.2004': 11240.73, '15.06.2004': 11259.47, '15.07.2004': 11278.23,
                '15.08.2004': 11297.03, '15.09.2004': 11315.86, '15.10.2004': 11334.72,
                '15.11.2004': 11353.61, '15.12.2004': 11372.53, '15.01.2005': 11391.48,
                '15.02.2005': 11410.47, '15.03.2005': 11429.49, '15.04.2005': 11448.54
            }
        ]
        for i in range(5):
            a = calculate_deposit(PostDepositInput(**inputs[i])).model_dump()
            print(a)
            assert a == outputs[i]
