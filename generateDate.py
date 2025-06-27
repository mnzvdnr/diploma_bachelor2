from datetime import datetime, timedelta
import random

#from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, text, MetaData, Table, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import select
import load_config
from load_config import Data, Purchase,PurchaseList,Product, ProductType, ProductSize,ProductGender
from datetime import datetime
import numpy as np
import statistics as stat
import os
import matplotlib.pyplot as plt
import pandas as pd

from pmdarima import auto_arima

from datetime import datetime, timedelta
from statsmodels.tsa.stattools import acf

import numpy as np
from pmdarima import auto_arima

from statsmodels.graphics.tsaplots import plot_acf


from pmdarima import auto_arima


from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import arma_order_select_ic


class calculate():
    Data = Data()
    def __init__(self):
        self.start_date = None
        self.end_date = datetime.now()
        self.category = None #None-название товаров, 1-тип товаров, 2-размер, 3-гендер
        self.period = 1 #1-месяца, 2-сезоны, None - без периода
        self.bool_date = False #true- учитывать период , false-не учитывать период

    def ABC(self):
        if self.bool_date==True: # расчёт по периоду
            purchases = Data.session.query(Purchase).filter(Purchase.date_order >= self.start_date, Purchase.date_order <= self.end_date).all()
            purchases_id = [i.id for i in purchases]
            purchaseList = Data.session.query(PurchaseList).filter(PurchaseList.id_purchase.in_(purchases_id)).all()
        else: #расчёт по всем продажам
            purchaseList = Data.session.query(PurchaseList).all()
        products = Data.session.query(Product).all()
        all_sum=0
        #считаем выручку
        for purchas_product in purchaseList:
            all_sum += [i.price*purchas_product.count_product for i in products if i.id == purchas_product.id_product][0]

        #считаем выручку по каждому отдельному товару
        if self.category==None:
            sum_products = {i.name: 0 for i in products}
            for product in products:
                for purchas_product in purchaseList:
                    if purchas_product.id_product==product.id:
                        sum_products[product.name]+=product.price*purchas_product.count_product
        if self.category == 1: #по типу товара
            productType = Data.session.query(ProductType).all()
            sum_products = {i.name: 0 for i in productType}
            for type in productType:
                for product in products:
                    if product.type == type.id:
                        for purchas_product in purchaseList:
                            if purchas_product.id_product==product.id:
                                sum_products[type.name]+=product.price*purchas_product.count_product
        if self.category == 2: #по размнру товара
            productSize = Data.session.query(ProductSize).all()
            sum_products = {i.name: 0 for i in productSize}
            for type in productSize:
                for product in products:
                    if product.size == type.id:
                        for purchas_product in purchaseList:
                            if purchas_product.id_product==product.id:
                                sum_products[type.name]+=product.price*purchas_product.count_product
        if self.category == 3: #по принадложности к гендеру
            productGender = Data.session.query(ProductGender).all()
            sum_products = {i.name: 0 for i in productGender}
            for type in productGender:
                for product in products:
                    if product.gender == type.id:
                        for purchas_product in purchaseList:
                            if purchas_product.id_product==product.id:
                                sum_products[type.name]+=product.price*purchas_product.count_product
        for i in sum_products.values():
            round(i, 2)
        print(sum_products)
        self.draw_ABC(sum_products)
        #сортируем выручку
        sorted_dict = {k: v for k, v in sorted(sum_products.items(), key=lambda item: item[1], reverse=True)}
        sum_products=sorted_dict
        #вклад товара в общую прибыль
        percent_sum_products={}
        for key, value in sum_products.items():
            percent_sum_products[key]=(value/all_sum)*100
        print("ВТвОП",percent_sum_products)
        #накопительный вклад товара
        n_sum_products={}
        term =0
        for key, value in percent_sum_products.items():
            term  += value
            n_sum_products[key]=term
        print("НЭ",n_sum_products)
        #разбиваем на категории ABC
        ABC = {'A':[],'B':[], 'C':[]}
        for key, value in n_sum_products.items():
            if value<=80:
                ABC['A'].append(key)
            elif value<95 and value>80:
                ABC['B'].append(key)
            else:
                ABC['C'].append(key)
        print(ABC)
        print("Выручка", all_sum)
        print("СпП",sum_products)
        sum=0
        for i in sum_products.values():
            sum+=i
        print("СВП", sum)
        self.save_to_excel(ABC, 'ABC')
        return "ABC"
    def viruchka_kat(self):
        if self.bool_date==True: #расчёт по периоду
            purchases = Data.session.query(Purchase).filter(Purchase.date_order >= self.start_date, Purchase.date_order <= self.end_date).all()
            purchases_id = [i.id for i in purchases]
            purchaseList = Data.session.query(PurchaseList).filter(PurchaseList.id_purchase.in_(purchases_id)).all()
        else: # расчёт по всем продажам
            purchases = Data.session.query(Purchase).all()
            purchaseList = Data.session.query(PurchaseList).all()
        products = Data.session.query(Product).all()
        if self.period==None:
            if self.category==None: #по названию товара
                productsDict = {i.name:0 for i in products}
                for purchase_product in purchaseList:
                    for product in products:
                        if purchase_product.id_product == product.id:
                            productsDict[product.name]+=product.price*purchase_product.count_product
            elif self.category==1:# по типу товара
                productType = Data.session.query(ProductType).all()
                productsDict = {i.name: 0 for i in productType}
                for purchase_product in purchaseList:
                    for product in products:
                        if purchase_product.id_product == product.id:
                            for type in productType:
                                if product.type == type.id:
                                    productsDict[type.name]+=product.price*purchase_product.count_product
            if self.category == 2: #по размнру товара
                productSize = Data.session.query(ProductSize).all()
                productsDict = {i.name: 0 for i in productSize}
                for purchase_product in purchaseList:
                    for product in products:
                        if purchase_product.id_product == product.id:
                            for size in productSize:
                                if product.size == size.id:
                                    productsDict[size.name] += product.price * purchase_product.count_product
            if self.category == 3: #по принадложности к гендеру
                productGender = Data.session.query(ProductGender).all()
                productsDict = {i.name: 0 for i in productGender}
                for purchase_product in purchaseList:
                    for product in products:
                        if purchase_product.id_product == product.id:
                            for gender in productGender:
                                if product.gender == gender.id:
                                    productsDict[gender.name] += product.price * purchase_product.count_product
            print(productsDict)
            self.save_to_excel_general(productsDict)
            return
        if self.period == 2:
            periods = {'зима': [], 'весна': [], 'лето': [], 'осень': []}
            for purchase in purchases:
                if purchase.date_order.month in [12, 1, 2]:
                    periods['зима'].append(purchase.id)
                elif purchase.date_order.month in [3, 4, 5]:
                    periods['весна'].append(purchase.id)
                elif purchase.date_order.month in [6, 7, 8]:
                    periods['лето'].append(purchase.id)
                elif purchase.date_order.month in [9, 10, 11]:
                    periods['осень'].append(purchase.id)
        # по месяцам
        if self.period == 1:
            periods = {i: [] for i in range(1, 13)}
            for i in purchases:
                for month in periods.keys():
                    if i.date_order.month == month:
                        periods[month].append(i.id)
        # по названию товара
        if self.category == None:
            # по месяцам
            if self.period == 1:
                periods_product = {i: {i.name: 0 for i in products} for i in range(1, 13)}
            # по сезону
            if self.period == 2:
                periods_product = {'зима': {i.name: 0 for i in products}, 'весна': {i.name: 0 for i in products},
                                   'лето': {i.name: 0 for i in products}, 'осень': {i.name: 0 for i in products}}
            for month, purchase_ids in periods.items():
                for pList in purchaseList:
                    if pList.id_purchase in purchase_ids:
                        for product in products:
                            if product.id == pList.id_product:
                                periods_product[month][product.name] += product.price * pList.count_product
            for month, array in periods_product.items():
                for i in array.values():
                    round(i, 2)
            print(periods_product)
            self.save_to_excel_general(periods_product)
            # по месяцам
            if self.period == 1:
                product_array = {k: [] for k, v in periods_product[1].items()}
            # по сезону
            if self.period == 2:
                product_array = {k: [] for k, v in periods_product['зима'].items()}
            for key, value in periods_product.items():
                for key2, value2 in value.items():
                    product_array[key2].append(value2)
        if self.category == 1:
            productType = Data.session.query(ProductType).all()
            # по сезонам
            if self.period == 2:
                periods_product = {'зима': {i.name: 0 for i in productType}, 'весна': {i.name: 0 for i in productType},
                                   'лето': {i.name: 0 for i in productType}, 'осень': {i.name: 0 for i in productType}}
            # по месяцам
            if self.period == 1:
                periods_product = {j: {i.name: 0 for i in productType} for j in range(1, 13)}
            for month, purchase_ids in periods.items():
                for pList in purchaseList:
                    if pList.id_purchase in purchase_ids:
                        for product in products:
                            if product.id == pList.id_product:
                                for i in productType:
                                    if i.id == product.type:
                                        periods_product[month][i.name] += product.price * pList.count_product
            for month, array in periods_product.items():
                for i in array.values():
                    round(i, 2)
            print(periods_product)
            self.save_to_excel_general(product_array)

    def viruchka(self):
        if self.bool_date==True: # расчёт по периоду
            purchases = Data.session.query(Purchase).filter(Purchase.date_order >= self.start_date, Purchase.date_order <= self.end_date).all()
            purchases_id = [i.id for i in purchases]
            purchaseList = Data.session.query(PurchaseList).filter(PurchaseList.id_purchase.in_(purchases_id)).all()
        else: # расчёт по всем продажам
            purchases = Data.session.query(Purchase).all()
            purchaseList = Data.session.query(PurchaseList).all()
        products = Data.session.query(Product).all()

        all_sum = 0
        # считаем выручку
        for purchas_product in purchaseList:
            all_sum += [i.price * purchas_product.count_product for i in products if i.id == purchas_product.id_product][0]
        discount_sum=0
        for purchase in purchases:
            if purchase.discount!=None:
                chek_sum=0
                for purchas_product in purchaseList:
                    if purchase.id == purchas_product.id_purchase:
                        chek_sum+=[i.price * purchas_product.count_product for i in products if i.id == purchas_product.id_product][0]
                discount = chek_sum*purchase.discount/100
                discount_sum+=discount
        self.draw_viruchka(int(all_sum), int(discount_sum))
        print(all_sum)
        print(discount_sum)
        print(all_sum-discount_sum)
        print(discount_sum*100/all_sum)

    def XYZ(self):
        products = Data.session.query(Product).all()

        purchases = Data.session.query(Purchase).filter(Purchase.date_order >= datetime.now() - timedelta(days=365),
                                                        Purchase.date_order <= datetime.now()).all()
        purchases_id = [i.id for i in purchases]
        purchaseList = Data.session.query(PurchaseList).filter(PurchaseList.id_purchase.in_(purchases_id)).all()

        #по сезонам
        if self.period==2:
            periods = {'зима': [], 'весна': [], 'лето': [], 'осень': []}
            for purchase in purchases:
                if purchase.date_order.month in [12, 1, 2]:
                    periods['зима'].append(purchase.id)
                elif purchase.date_order.month in [3, 4, 5]:
                    periods['весна'].append(purchase.id)
                elif purchase.date_order.month in [6, 7, 8]:
                    periods['лето'].append(purchase.id)
                elif purchase.date_order.month in [9, 10, 11]:
                    periods['осень'].append(purchase.id)
            print(periods)
        #по месяцам
        if self.period==1:
            periods = {i: [] for i in range(1, 13)}
            for i in purchases:
                for month in periods.keys():
                    if i.date_order.month == month:
                        periods[month].append(i.id)
            print(periods)
        #по названию товара
        if self.category==None:
            #по месяцам
            if self.period==1:
                periods_product = {i: {i.name: 0 for i in products} for i in range(1, 13)}
            #по сезону
            if self.period==2:
                periods_product ={'зима': {i.name: 0 for i in products}, 'весна': {i.name: 0 for i in products},
                                         'лето': {i.name: 0 for i in products}, 'осень': {i.name: 0 for i in products}}
            print(periods_product)
            for month, purchase_ids in periods.items():
                for pList in purchaseList:
                    if pList.id_purchase in purchase_ids:
                        for product in products:
                            if product.id ==pList.id_product:
                                periods_product[month][product.name]+=product.price * pList.count_product
            for month, array in periods_product.items():
                for i in array.values():
                    round(i,2)
            print(periods_product)
            self.draw_XYZ(periods_product)
            #по месяцам
            if self.period==1:
                product_array = {k: [] for k, v in periods_product[1].items()}
            #по сезону
            if self.period==2:
                product_array = {k: [] for k, v in periods_product['зима'].items()}
            for key, value in periods_product.items():
                    for key2, value2 in value.items():
                        product_array[key2].append(value2)
            print(product_array)


        if self.category==1:
            productType = Data.session.query(ProductType).all()
            #по сезонам
            if self.period==2:
                periods_product = {'зима': {i.name: 0 for i in productType}, 'весна': {i.name: 0 for i in productType},
                                       'лето': {i.name: 0 for i in productType}, 'осень': {i.name: 0 for i in productType}}
            #по месяцам
            if self.period==1:
                periods_product = {j: {i.name: 0 for i in productType} for j in range(1, 13)}
            print(periods_product)
            for month, purchase_ids in periods.items():
                for pList in purchaseList:
                    if pList.id_purchase in purchase_ids:
                        for product in products:
                            if product.id == pList.id_product:
                                for i in productType:
                                    if i.id == product.type:
                                        periods_product[month][i.name] += product.price * pList.count_product
            for month, array in periods_product.items():
                for i in array.values():
                    round(i,2)
            print(periods_product)
            self.draw_XYZ(periods_product)
            #по месяцам
            if self.period==1:
                product_array = {k: [] for k, v in periods_product[1].items()}
            #по сезонам
            if self.period==2:
                product_array = {k: [] for k, v in periods_product['зима'].items()}
            for key, value in periods_product.items():
                for key2, value2 in value.items():
                    product_array[key2].append(value2)
            print(product_array)


        # проводим XYZ анализ
        kof_var = {}
        for key, value in product_array.items():
            kof_var[key] = stat.stdev(value) / stat.mean(value) * 100
        print(kof_var.values())  # коэффиценты вариации
        sr_kof_var = stat.mean(kof_var.values())
        print(sr_kof_var)  # среднее значение вариации
        XYZ = {'X':[], 'Y':[], 'Z':[]}
        for key, value in kof_var.items():
            if value < 0.45 * sr_kof_var:
                XYZ['X'].append(key)
            elif 0.45 * sr_kof_var <= value and value < 0.55 * sr_kof_var:
                XYZ['Y'].append(key)
            elif value >= 0.55 * sr_kof_var:
                XYZ['Z'].append(key)
        print(XYZ)
        self.save_to_excel(XYZ, f"XYZ_{str(self.period)}_{str(self.category)}")

        return f"XYZ_{str(self.period)}_{str(self.category)}"

    def draw_XYZ(self, data):
        if self.period == 1:
            categories = [i for i in data[1].keys()]
        elif self.period == 2:
            categories = [i for i in data["зима"].keys()]

        if not os.path.exists(f"XYZ_{str(self.period)}_{str(self.category)}"):
            os.makedirs(f"XYZ_{str(self.period)}_{str(self.category)}")

        for category in categories:
            values = [data[season][category] for season in data]

            plt.figure(figsize=(10, 6))
            plt.bar(data.keys(), values, color='skyblue')

            if self.period == 1:
                plt.xlabel('Месяц')
            elif self.period == 2:
                plt.xlabel('Время года')

            plt.ylabel('Сумма продаж')
            if self.bool_date==False:
                plt.title(f'Продажи по "{category}"')
            else:
                plt.title(f'Сумма продаж по "{category}" за период с {self.start_date.date()} по {self.end_date.date()}')
            #plt.grid(True)  # Добавляем сетку на график
            #plt.xticks(rotation=45)  # Поворачиваем подписи оси X на 45 градусов для лучшей читаемости

            # Сохраняем текущий график в папку "XYZ"
            filename = os.path.join(f"XYZ_{str(self.period)}_{str(self.category)}", f"{category}_plot.png")
            plt.savefig(filename, dpi=60)
            plt.close()  # Закрываем текущий график

    def draw_ABC(self, dictionary ):
        output_folder = 'ABC'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        keys = list(dictionary.keys())
        values = list(dictionary.values())

        plt.figure(figsize=(10, 6))
        plt.barh(keys, values, color='skyblue')
        plt.xlabel('Значения')
        plt.ylabel('Ключи')
        if self.bool_date == False:
            plt.title('Сумма продаж')
        else:
            plt.title(f'Сумма продаж за период с {self.start_date.date()} по {self.end_date.date()}')
        plt.tight_layout()

        output_path = os.path.join(output_folder, 'viruchka.png')
        plt.savefig(output_path)
        plt.close()

    def save_to_excel(self, data, filename):
        # Создаем DataFrame из словаря
        df = pd.DataFrame([(category, item) for category, items in data.items() for item in items],
                          columns=['Категория', 'Элемент'])

        # Создаем папку "abc", если она не существует
        if not os.path.exists(filename):
            os.makedirs(filename)

        # Путь к файлу Excel в папке "abc"
        filepath = os.path.join(filename, f'{filename}.xlsx')

        # Сохраняем DataFrame в файл Excel
        df.to_excel(filepath, index=False)

    def save_to_excel_general(self, data):
        filename='general'
        if self.period==None:
            df = pd.DataFrame.from_dict(data, orient='index', columns=['Выручка'])
            total_revenue = df['Выручка'].sum()
            df.loc['Общая выручка'] = total_revenue
        else:
            # Создаем DataFrame из словаря
            df = pd.DataFrame(data)

            # Добавляем столбец с суммой по строкам
            df['Сумма'] = df.sum(axis=1)
            # Добавляем строку с названием "Общая выручка" и значениями сумм по столбцам
            total_revenue = df.sum(axis=0)
            df.loc['Общая выручка'] = total_revenue

        # Сохраняем DataFrame в файл формата xlsx
        # Путь к файлу Excel в папке "abc"
        filepath = os.path.join(filename, f'{filename}.xlsx')

        # Сохраняем DataFrame в файл Excel
        df.to_excel(filepath, index=True)

    def draw_viruchka(self, all_sum, discount_sum):
        # Вычисляем значения для графика
        revenue = all_sum - discount_sum
        discount_percentage = (discount_sum * 100) / all_sum

        # Подготовка данных для кругового графика
        labels = [f'Выручка = {revenue}', f'Скидка = {discount_sum}']
        sizes = [revenue, discount_sum]
        colors = ['#4CAF50', '#FF5733']
        explode = (0.1, 0)  # Выделим "выручку" немного

        # Построение кругового графика
        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=140)

        # Настройки для более красивого отображения
        ax.axis('equal')  # Равные оси для кругового графика

        # Отображаем круговой график
        plt.title(f'Общее значение {all_sum}')

        output_folder = 'general'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = os.path.join(output_folder, 'viruchka.png')
        plt.savefig(output_path)
        plt.close()

    def Prognoz(self):
        products = Data.session.query(Product).all()

        purchases = Data.session.query(Purchase).filter(Purchase.date_order >= datetime.now() - timedelta(days=1095),
                                                        Purchase.date_order <= datetime.now()).all()
        purchases_id = [i.id for i in purchases]
        purchaseList = Data.session.query(PurchaseList).filter(PurchaseList.id_purchase.in_(purchases_id)).all()

        end_date = datetime.now()
        start_date = end_date - timedelta(days=1095)
        """ Генерирует словарь с ключами в формате 'год-месяц' от start_date до end_date. """
        # Создаем диапазон месяцев
        months_range = pd.date_range(start=start_date, end=end_date, freq='MS')
        # Инициализируем словарь с пустыми списками
        periods = {month.strftime('%Y-%m'): [] for month in months_range}
        for j in purchases:
            for month in periods.keys():
                if j.date_order.strftime('%Y-%m') == month:
                    periods[month].append(j.id)

        periods_product = {month.strftime('%Y-%m'): {i.name: 0 for i in products} for month in months_range}

        for month, purchase_ids in periods.items():
            for pList in purchaseList:
                if pList.id_purchase in purchase_ids:
                    for product in products:
                        if product.id == pList.id_product:
                            periods_product[month][product.name] += 1 * pList.count_product

        for month, array in periods_product.items():
            for j in array.values():
                round(j, 2)

        print(periods_product)
        sales_dict = periods_product
        data = self.collect_and_prepare_data(sales_dict)
        names = {i.name:0 for i in products}
        for product in names.keys():
            product_series = data[product]
            m = self.estimate_seasonality(product_series)
            model = self.fit_sarima_model(product_series, m)
            forecast = self.forecast_sales(model, 12)
            print(forecast)
            forecast_date = dict(zip(forecast.index, forecast.values))
            self.save_forecast_and_plot(forecast_date, product)
        return 'prognoz'



    def collect_and_prepare_data(self, sales_dict):
        df = pd.DataFrame(sales_dict).T
        df.index = pd.to_datetime(df.index, format='%Y-%m')  # Преобразование индекса в datetime
        return df

    # def collect_data(self, purchases, products):
    #     sales_dict = {}
    #     for product in products:
    #         sales_dict[product.name] = {}
    #         for purchase in purchases:
    #             month_key = purchase.date_order.strftime('%Y-%m')
    #             if month_key not in sales_dict[product.name]:
    #                 sales_dict[product.name][month_key] = 0
    #             sales_dict[product.name][month_key] += 1
    #     return sales_dict

    # def analyze_series(self, series):
    #     plot_acf(series.dropna(), lags=40)
    #     plt.show()

    def estimate_seasonality(self, series, max_lag=24):
        acf_vals = acf(series.dropna(), nlags=max_lag, fft=True)
        seasonal_lags = np.argsort(-np.abs(acf_vals))[1:]
        for lag in seasonal_lags:
            if acf_vals[lag] > 0.3:
                return lag
        return 12  # Default to 12 if no significant seasonality is detected

    def fit_sarima_model(self, series, seasonal_periods):
        model = auto_arima(series.dropna(), start_p=1, start_q=1,
                           max_p=5, max_q=5, m=seasonal_periods,
                           seasonal=True, stepwise=True, suppress_warnings=True,
                           D=1, trace=True)
        print(model.summary())
        return model

    def forecast_sales(self, model, periods):
        forecast = model.predict(n_periods=periods)
        return forecast

    def save_forecast_and_plot(self, data, name):
        folder_path = 'prognoz'
        excel_file = f'{name}.xlsx'
        plot_file = f'{name}.png'
        """
        Сохраняет прогнозные данные в Excel и график продаж в указанную папку.

        :param data: dict или pandas.Series с прогнозными данными
        :param folder_path: str, путь к папке для сохранения файлов
        :param excel_file: str, имя файла Excel для сохранения данных
        :param plot_file: str, имя файла для сохранения графика
        """
        # Создание папки, если она не существует
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Обработка данных
        if isinstance(data, dict):
            data = pd.Series(data)

        # Сохранение данных в Excel
        data.to_excel(os.path.join(folder_path, excel_file), index=True)

        # Создание графика
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data.values, marker='o', linestyle='-', color='b')
        plt.title('Прогноз продаж')
        plt.xlabel('Дата')
        plt.ylabel('Продажи')
        plt.grid(True)
        plt.savefig(os.path.join(folder_path, plot_file))
        plt.close()


# c = calculate()
# # c.bool_date=True
# # c.start_date = datetime(2023, 4, 3)
# # c.end_date = datetime.now()
# # c.period=2
# # c.viruchka_kat()
# c.Prognoz()
#
# c.XYZ()
# # c.viruchka()
# #c.viruchka_kat()
# Data.session.close()






