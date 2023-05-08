


class Percentages:

    activate_percentages = True

    @staticmethod
    def ovw_as_percentage(df_ovw, name):
        if Percentages.activate_percentages == True:

            df_ovw[name] = [str(round(100 * x / 5, 2)) + '%' for x in df_ovw[name].to_list()]