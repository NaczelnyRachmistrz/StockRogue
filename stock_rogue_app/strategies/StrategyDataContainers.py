class StrategyData():
    def __init__(self,
                 company_name,
                 company_data,
                 number_of_past_days,
                 volume_importance_coefficient,
                 past_time_importance_coefficient):
        self.company_name = company_name
        self.company_data = company_data
        self.number_of_past_days = number_of_past_days
        self.volume_IC = volume_importance_coefficient
        self.time_IC = 1.0 - self.volume_IC
        self.past_time_IC = past_time_importance_coefficient

    def predict_future_average_name_value(self, name):
        return self.predict_future_average_name_value_volume_part(name) + \
               self.predict_future_average_name_value_time_part(name)

    def sum_volume(self):
        result = 0
        for idx, day in enumerate(self.company_data):
            if idx >= self.number_of_past_days:
                break
            result += day['obrot']
        return result

    def predict_future_average_name_value_volume_part(self, name):
        result = 0.0
        sum_volume = self.sum_volume()

        for _, day in zip(range(self.number_of_past_days), self.company_data):
            result += day[name] * (day['obrot'] / sum_volume)

        return result * self.volume_IC

    def predict_future_average_name_value_time_part(self, name):
        result = 0.0

        past_time_IC_acc = 1.0

        max_past_time_IC_acc = pow(self.past_time_IC, self.number_of_past_days)
        if max_past_time_IC_acc == 1.0:
            past_time_IC_acc = 1.0 / self.number_of_past_days
        else:
            past_time_IC_acc = (1.0 - self.past_time_IC) / (1.0 - max_past_time_IC_acc)

        for _, day in zip(range(self.number_of_past_days), self.company_data):
            result += day[name] * past_time_IC_acc
            past_time_IC_acc *= self.past_time_IC

        return result * self.time_IC
