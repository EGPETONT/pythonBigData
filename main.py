# подключаем модуль для обработки данных
import pandas as pd
from io import StringIO
# # модули для работы с тепловыми картами
import seaborn as sns
import matplotlib.pyplot as plt

#путь к файлу
data_url = "biden_trump_tweets.csv"

df = pd.read_csv(
    data_url
)
# df = pd.read_csv(StringIO(data_url), header=[0,1])
# проверяем, что данные считались правильно
# для этого выводим первые 5 строк нашего датасета
print(df.head())

# объединяем события, которые произошли у каждого пользователя в одно и то же время
g = df.groupby(['hour_utc','minute_utc','username'])

# считаем количество твитов в каждой получившейся группе
tweet_cnt = g.id.nunique()
# для проверки выводим первые 5 строк обработанных данных
print(tweet_cnt.head())

# начинаем обработку данных с Джо Байдена
# получаем доступ к группе строк и столбцов,
# чтобы сформировать новый датасет для тепловой карты
jb_tweet_cnt = tweet_cnt.loc[:,:,'JoeBiden'].reset_index().pivot(index='hour_utc', columns='minute_utc', values='id')
# выводим фрагмент нового датасета для проверки


jb_tweet_cnt.fillna(0, inplace=True)
# Добавляем отсутствующие часы, если их нет в нашем датасете
jb_tweet_cnt = jb_tweet_cnt.reindex(range(0,24), axis=0, fill_value=0)
# Добавляем отсутствующие минуты и приводим всё к целым числам
jb_tweet_cnt = jb_tweet_cnt.reindex(range(0,60), axis=1, fill_value=0).astype(int)


print(jb_tweet_cnt.iloc[:10,:9])

# делаем то же самое для данных Дональда Трампа
dt_tweet_cnt = tweet_cnt.loc[:,:,'realDonaldTrump'].reset_index().pivot(index='hour_utc', columns='minute_utc', values='id')
dt_tweet_cnt.fillna(0, inplace=True)
dt_tweet_cnt = dt_tweet_cnt.reindex(range(0,24), axis=0, fill_value=0)
dt_tweet_cnt = dt_tweet_cnt.reindex(range(0,60), axis=1, fill_value=0).astype(int)
print(dt_tweet_cnt.iloc[:10,:9])