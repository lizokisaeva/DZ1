# -*- coding: utf-8 -*-
"""DZ2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uTgDSWDGivWnCf1flhnuGUYXgwiWPp2l

# Домашнее задание №2

Импорт необходимых пакетов и классов
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.formula.api import ols

from google.colab import drive
drive.mount('/content/gdrive')

"""Загрузка данных"""

rlms_hse = '/content/gdrive/MyDrive/Colab Notebooks/rlms_hse.dta'
df = pd.read_stata(rlms_hse, convert_categoricals = False) 
df.head(3)

"""Переменные из датафрейма, которые будем использовать:
* u_age - количество полных лет;
* uh5   - пол респондента;
* um1   - вес в кг;
* um2   - рост в см;
* region - регион.
"""

data =  df[['u_age', 'uh5', 'um1', 'um2', 'region']]
data = data.rename(columns = {'u_age' : 'age', 'uh5': 'gender', 'um1' : 'weight', 'um2' : 'height'})
data.head()

"""Заменим большие значения на NaN"""

new_data = data.replace([99999997, 99999998, 99999999, 100000000], np.nan)
new_data.head()

"""Удалим наблюдения с отсутсвующими значениями"""

new_data = new_data.dropna()

new_data.info()

"""## Вариант 1:
* регион - 138
"""

my_data = new_data.loc[lambda new_data: new_data['region'] == 138].copy()
my_data.head(3)

my_data.loc[my_data.gender == 1, 'gender'] = 'male'
my_data.loc[my_data.gender == 2, 'gender'] = 'female'
my_data.head(3)

"""### Задание 1 - построить модель линейной регрессии для зависимости веса респондента от его роста (для респондентов всех возрастов, мужского и женского пола)

Преобразование данных в формат ndarray
"""

weight = my_data[['weight']].to_numpy()
height = my_data[['height']].to_numpy()

height = height.reshape(-1, 1)
height.shape

"""Использование библиотеки sklearn"""

model = LinearRegression()

model.fit(height, weight)

"""Коэффициенты детерминации:"""

r_sq = model.score(height, weight)
print('Коэффициент детерминации:', round(r_sq, 6))

# Количество наблюдений
n = weight.shape[0]

# Количество зависимых переменных (предикторов)
p = 1

adj_r_sq = 1 - (1 - r_sq) * (n - 1) / (n - p - 1)
print('Скорректированный коэффициент детерминации:', round(adj_r_sq, 6))

"""Использование библиотеки statsmodels"""

X = sm.add_constant(height)
y = weight
est = sm.OLS(y, X)
est2 = est.fit()
print(est2.summary())

"""Модель для респондентов:
$$weight = -67,2192 + 0,8366 \cdot height$$  
"""

A = np.identity(len(est2.params))
A = A[1:,:]
print(f"F-тест для модели: {est2.f_test(A)}")

"""Поскольку p-значение приблизительно равно нулю, мы отвергаем нулевую гипотезу (модель не является значимой). Другими словами, есть данные, свидетельствующие о наличии линейной зависимости между весом и ростом респондентов.

Визуализация линейной регрессионной модели:
"""

sns.set_style('whitegrid')
sns.lmplot(x ='height', y ='weight', data = my_data, 
           hue ='gender', markers = ['o', 'x'])

"""### Задание 2 - построить модель линейной регрессии для зависимости веса респондента от его роста отдельно для мальчиков, девочек, мужчин и женщин

Данные для линейной регрессии

*   для мальчиков - b_data
*   для девочек - g_data
* для мужчин - m_data
* для женщин - w_data
"""

man_data = my_data.loc[lambda my_data: my_data['gender'] == 'male']
woman_data = my_data.loc[lambda my_data: my_data['gender'] == 'female']

b_data = man_data.loc[lambda man_data: man_data['age'] < 18]
g_data = woman_data.loc[lambda woman_data: woman_data['age'] < 18]
m_data = man_data.loc[lambda man_data: man_data['age'] >= 18]
w_data = woman_data.loc[lambda woman_data: woman_data['age'] >= 18]

weight_b = b_data[['weight']].to_numpy()
height_b = b_data[['height']].to_numpy()
weight_g = g_data[['weight']].to_numpy()
height_g = g_data[['height']].to_numpy()
weight_m = m_data[['weight']].to_numpy()
height_m = m_data[['height']].to_numpy()
weight_w = w_data[['weight']].to_numpy()
height_w = w_data[['height']].to_numpy()

height_b = height_b.reshape(-1, 1)
height_b.shape
height_g = height_g.reshape(-1, 1)
height_g.shape
height_m = height_m.reshape(-1, 1)
height_m.shape
height_w = height_w.reshape(-1, 1)
height_w.shape

model_b = LinearRegression()
model_b.fit(height_b, weight_b)

model_g = LinearRegression()
model_g.fit(height_g, weight_g)

model_m = LinearRegression()
model_m.fit(height_m, weight_m)

model_w = LinearRegression()
model_w.fit(height_w, weight_w)

r_sq_b = model_b.score(height_b, weight_b)
r_sq_g = model_g.score(height_g, weight_g)
r_sq_m = model_m.score(height_m, weight_m)
r_sq_w = model_w.score(height_w, weight_w)
print(f"Коэффициент детерминации для мальчиков: {round(r_sq_b, 6)}, для девочек: {round(r_sq_g, 6)}, \
 для мужчин: {round(r_sq_m, 6)}, для женщин: {round(r_sq_w, 6)}")

n_b = weight_b.shape[0]
n_g = weight_g.shape[0]
n_m = weight_m.shape[0]
n_w = weight_w.shape[0]

adj_r_sq_b = 1 - (1 - r_sq_b) * (n_b - 1) / (n_b - p - 1)
adj_r_sq_g = 1 - (1 - r_sq_g) * (n_g - 1) / (n_g - p - 1)
adj_r_sq_m = 1 - (1 - r_sq_m) * (n_m - 1) / (n_m - p - 1)
adj_r_sq_w = 1 - (1 - r_sq_w) * (n_w - 1) / (n_w - p - 1)
print(f"Скорректированный коэффициент детерминации для мальчиков: {round(adj_r_sq_b, 6)}, \
 для девочек: {round(adj_r_sq_g, 6)}, для мужчин: {round(adj_r_sq_m, 6)}, для женщин: {round(adj_r_sq_w, 6)}")

X_b = sm.add_constant(height_b)
y_b = weight_b
est_b = sm.OLS(y_b, X_b).fit()
B = np.identity(len(est_b.params))
B = B[1:,:]
print(f"F-тест для модели мальчиков: {est_b.f_test(B)}")

X_g = sm.add_constant(height_g)
y_g = weight_g
est_g = sm.OLS(y_g, X_g).fit()
G = np.identity(len(est_g.params))
G = G[1:,:]
print(f"F-тест для модели девочек: {est_g.f_test(G)}")

X_m = sm.add_constant(height_m)
y_m = weight_m
est_m = sm.OLS(y_m, X_m).fit()
M = np.identity(len(est_m.params))
M = M[1:,:]
print(f"F-тест для модели мужчин: {est_m.f_test(M)}")

X_w = sm.add_constant(height_w)
y_w = weight_w
est_w = sm.OLS(y_w, X_w).fit()
W = np.identity(len(est_w.params))
W = W[1:,:]
print(f"F-тест для модели женщин: {est_w.f_test(W)}")

"""Из полученных выше p-значений для различных моделей можно сделать вывод, что мы отвергаем нулевую гипотезу (поскольку p-значение во всех случаях приблизительно равно нулю при уровне значимости 5%). Таким образом, линейные зависимости между весом и ростом отдельно для мальчиков, девочек, мужчин и женщин существуют.

Сравним значения коэффициентов детерминации и скоректированных коэффициентов детерминации для всех моделей (п.1 и п.2):
"""

r_sq_all = [r_sq, r_sq_b, r_sq_g, r_sq_m, r_sq_w]
adj_r_sq_all = [adj_r_sq, adj_r_sq_b, adj_r_sq_g, adj_r_sq_m, adj_r_sq_w]
df = pd.DataFrame({'Коэффициент детерминации': r_sq_all, 'Скорректированный коэффициент детерминации': adj_r_sq_all})
df2 = df.rename(index={0: 'Для всех', 1: 'Для мальчиков', 2: 'Для девочек', 3: 'Для мужчин', 4: 'Для женщин'})
df2

fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize=(12,14))
sns.regplot(x = 'height', y = 'weight', data = b_data, color = "deepskyblue", ax = axes[0,0])
sns.regplot(x = 'height', y = 'weight', data = g_data, color = "violet", ax = axes[0,1])
sns.regplot(x ='height', y ='weight', data = m_data, color = "darkblue", ax = axes[1,0])
sns.regplot(x ='height', y ='weight', data = w_data, color = "firebrick", ax = axes[1,1])
axes[0,0].set_title("Мальчики")
axes[0,1].set_title("Девочки")
axes[1,0].set_title("Мужчины")
axes[1,1].set_title("Женщины")

"""### Задание 3 - сделать вывод о качестве каждой из 5 построенных моделей

Коэффициент детерминации для модели с константой принимает значения от 0 до 1. Чем ближе значение коэффициента к 1, тем сильнее зависимость. При оценке регрессионных моделей это интерпретируется как соответствие модели данным. Для приемлемых моделей предполагается, что коэффициент детерминации должен быть хотя бы не меньше 50%. Модели с коэффициентом детерминации выше 80% можно признать достаточно хорошими. Равенство коэффициента детерминации единице означает, что объясняемая переменная в точности описывается рассматриваемой моделью.
"""

df2

"""Проанализировав таблицу сравнения коэффициентов детерминации, можно сделать следующий вывод:

* Модель 1 (все респонденты) имеет коэффициент детерминации 53%, что является приемлемым, и в принципе, такая модель может быть использована на практике.
* Модели для мальчиков и для девочек имеют коэффициенты детерминации 85% и 78%, что является очень хорошим результатом, и такие модели применимы на практике.
* Модели для мужчин и женщин имеют коэффициенты детерминации 9% и 1%, что говорит нам о том, что в данных моделях нет линейной связи между весом и ростом, и такие модели не могут быть использованы на практике.

### Задание 4 - включить в модель ещё один "предиктор" - возраст, и построить 3 модели (для мужчин и женщин, только для мужчин, только для женщин) зависимости веса респондента от его роста

#### Включение возраста как непрерывную переменную
"""

X_age = my_data[['age', 'height']]
X_age = sm.add_constant(X_age)
y_age = my_data[['weight']]
est_with_age = sm.OLS(y_age, X_age).fit()

X_age_m = man_data[['age', 'height']]
X_age_m = sm.add_constant(X_age_m)
y_age_m = man_data[['weight']]
est_with_age_m = sm.OLS(y_age_m, X_age_m).fit()

X_age_w = woman_data[['age', 'height']]
X_age_w = sm.add_constant(X_age_w)
y_age_w = woman_data[['weight']]
est_with_age_w = sm.OLS(y_age_w, X_age_w).fit()

E = np.identity(len(est_with_age.params))
E = E[1:,:]
print(f"F-тест для модели мужчин и женщин: {est_with_age.f_test(E)}")

N = np.identity(len(est_with_age_m.params))
N = N[1:,:]
print(f"F-тест для модели мужчин: {est_with_age_m.f_test(N)}")

F = np.identity(len(est_with_age_w.params))
F = F[1:,:]
print(f"F-тест для модели женщин: {est_with_age_w.f_test(F)}")

"""Поскольку во всех моделях p-значение приблизительно равно нулю, мы отвергаем нулевую гипотезу (модель не является значимой). Линейная зависимость между ростом, возрастом и весом респондентов есть."""

print(f"Коэффициент детерминации для всех: {round(est_with_age.rsquared, 6)}, \
 для мужчин: {round(est_with_age_m.rsquared, 6)}, для женщин {round(est_with_age_w.rsquared, 6)}")

print(f"Скорректированный коэффициент детерминации для всех: {round(est_with_age.rsquared_adj, 6)}, \
 для мужчин: {round(est_with_age_m.rsquared_adj, 6)}, для женщин {round(est_with_age_w.rsquared_adj, 6)}")

"""Проанализировав коэффициенты детерминации моделей, можно сделать вывод, что,  в принципе, данные модели могут быть использованы на практике. Самая точная модель - модель для мужчин (коэффициент детерминации - 67%).

#### Включение возраста как категориальную переменную

##### Модель для мужчин и женщин
"""

age_data = my_data.copy()
age_data.loc[age_data.age < 18, 'age_group'] = 'child'
age_data.loc[age_data.age >= 18, 'age_group'] = 'adult'
age_data.head(3)

"""Учтем категориальную переменную "возраст" в свободном члене:"""

est_with_gender_intercept = \
  ols('weight ~ C(age_group) + height', data = age_data).fit()
print(est_with_gender_intercept.summary())

"""Модель для взрослых (мужчин и женщин):
$$weight = -25,0628 + 0,5979 \cdot height$$  
Модель для детей (мальчиков и девочек):  
$$weight = (-25,0628 - 19,8517) + 0,5979 \cdot height$$

##### Модель только для мужчин
"""

m_age_data = age_data.loc[lambda age_data: age_data['gender'] == 'male']

"""Учтем категориальную переменную "возраст" в угловом коэффициенте:"""

est_with_gender_slope = \
  ols('weight ~ C(age_group) : height', data = m_age_data).fit()
print(est_with_gender_slope.summary())

"""Модель для взрослых (мужчин):
$$weight = -44,2357 + 0,7206 \cdot height$$  
Модель для детей (мальчиков):  
$$weight = -44,2357 + 0,5951 \cdot height$$

##### Модель только для женщин
"""

w_age_data = age_data.loc[lambda age_data: age_data['gender'] == 'female']

"""Учтем категориальную переменную "возраст" в свободном члене и угловом коэффициенте:"""

est_with_gender_intercept_and_slope = \
  ols('weight ~ C(age_group) * height', data = w_age_data).fit()
print(est_with_gender_intercept_and_slope.summary())

"""Модель для взрослых (женщин):
$$weight = 22.0819 + 0,2992 \cdot height$$  
Модель для детей (девочек):   
$$weight = (22.0819 - 57.3362) + (0,2992 + 0,2245) \cdot height$$

Поскольку во всех моделях p-значение приблизительно равно нулю, мы отвергаем нулевую гипотезу (модель не является значимой). В данном случае линейная зависимость между ростом, возрастом и весом респондентов также есть.

Коэффициенты детерминации моделей следующие:
*   для мужчин и женщин: 60%
*   только для мужчин: 70%
*   только для женщин: 50%

### Задание 5 - для моделей, построенных в задании 2, вычислить средний (по региону) рост мальчиков, девочек, мужчин, женщин и уменьшить его на 10 см. С использованием моделей линейной регрессии спрогнозировать 4 значения веса для средних значений роста, уменьшенных на 10 см
"""

print(f"Средний рост \n-мальчиков: {b_data.height.mean()} \n-девочек: {g_data.height.mean()} \
\n-мужчин: {m_data.height.mean()} \n-женщин: {w_data.height.mean()}")

"""Уменьшим рост на 10 см"""

height_b_10 = int(b_data.height.mean()) - 10
height_g_10 = int(g_data.height.mean()) - 10
height_m_10 = int(m_data.height.mean()) - 10
height_w_10 = int(w_data.height.mean()) - 10

"""Прогнозирование с помощью встроенной функции:"""

x_pred_b = np.array(height_b_10)
x_pred_b = x_pred_b.reshape(-1, 1)
y_pred_b_auto = model_b.predict(x_pred_b)

x_pred_g = np.array(height_g_10)
x_pred_g = x_pred_g.reshape(-1, 1)
y_pred_g_auto = model_g.predict(x_pred_g)

x_pred_m = np.array(height_m_10)
x_pred_m = x_pred_m.reshape(-1, 1)
y_pred_m_auto = model_m.predict(x_pred_m)

x_pred_w = np.array(height_w_10)
x_pred_w = x_pred_w.reshape(-1, 1)
y_pred_w_auto = model_w.predict(x_pred_w)

print(f"Спрогнозированные значения веса \n-для мальчиков: {y_pred_b_auto} \n-для девочек: {y_pred_g_auto} \
\n-для мужчин: {y_pred_m_auto} \n-для женщин: {y_pred_w_auto}")