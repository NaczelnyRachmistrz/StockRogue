
class StrategyData():

    def __init__(self, number_of_past_days, alpha, gamma, company_name, company_data):
        self.number_of_past_days = number_of_past_days
        self.alpha = alpha
        self.beta = 1.0 - alpha
        self.gamma = gamma
        self.company_name = company_name
        self.company_data = company_data
        self.sum_volume = self.sum_volume()

    def sum_volume(self):
        result = 0
        for idx, day in enumerate(self.company_data):
            if idx >= self.number_of_past_days:
                break
            result += day['obrot']
        return result

    def predict_future_average_name_value(self, name):
        result = 0.0
        gamma_acc = self.beta
        gamma_max = pow(self.gamma, self.number_of_past_days)
        if gamma_max == 1.0 or gamma_max == 0.0:
            gamma_factor = 1 / self.number_of_past_days
        else:
            gamma_factor = (1 - self.gamma) / (1 - gamma_max)

        for _, day in zip(range(self.number_of_past_days), self.company_data):
            result += day[name] * (self.alpha * (day['obrot'] / self.sum_volume) +
                                   gamma_acc * gamma_factor)
            gamma_acc *= self.gamma

        return result
