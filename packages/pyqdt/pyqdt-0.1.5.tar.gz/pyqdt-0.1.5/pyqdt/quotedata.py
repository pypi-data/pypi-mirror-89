# -*- coding: utf-8 -*-

import os

import math
import numpy
import pandas

from functools import lru_cache
from .common import *

from dateutil.parser import parse


class QuoteData:
    _data_path = None
    _options = None

    def __init__(self, data_path):
        """本地行情数据类

        参数:
            data_path: 数据路径

        """
        if not data_path or not os.path.exists(data_path):
            raise Exception('the DATA_PATH is not exists.')
        self._data_path = data_path
        self._options = {
            # 'cache_max_num': 16
        }

    @lru_cache(maxsize=None, typed=True)
    def _fetch_data(self, filename, date_columns=None):
        """获取数据

        参数:
            filename: 数据文件名
            dtype: 字段类型
            parse_dates: 日期字段

        返回值: DataFrame

        """

        data_file = os.path.join(self._data_path, filename)
        if not os.path.exists(data_file):
            return

        result = None
        extname = os.path.splitext(filename)[-1][1:].lower()
        if extname == 'csv':
            if not date_columns:
                parse_dates = False
            elif type(date_columns) is list:
                parse_dates = date_columns
            elif type(date_columns) is tuple:
                parse_dates = list(date_columns)
            elif type(date_columns) is str:
                parse_dates = [date_columns]
            else:
                raise ValueError('date_columns is error.')
            result = pandas.read_csv(data_file, dtype={'code': str}, parse_dates=parse_dates)
        elif extname == 'txt':
            with open(data_file, 'r') as f:
                result = f.readlines()
        return result

    def get_option(self, name):
        """获取可选项

        参数:
            name: 可选项名

        返回值: 可选项值

        """

        if name in self._options:
            return self._options[name]
        else:
            raise Exception('option %s is invalid.')

    def set_option(self, name, value):
        """设置可选项

        参数:
            name: 可选项名
            value: 可选项值

        """

        if name in self._options:
            self._options[name] = value
        else:
            raise Exception('option %s is invalid.')

    def execute_rehabilitation(self, data, fq='pre', fq_vol=False, columns=None) -> pandas.DataFrame:
        """执行复权操作

        复权逻辑：
            data 为 DataFrame 行情数据，基中 datetime 作为时间字段识别出 start_date 和 end_date
            当 fq == 'pre' 时，复权参考日为 end_date
            当 fq == 'post' 时，复权参考日为 start_date
            当 除权除息日 <= 复权参考日 时，所有 < 除权除息日 的数据进行前复权
            当 除权除息日 > 复权参考日 时，所有 >= 除权除息日 的数据进行后复权

        参数:
            data: 输入数据
            fq: 复权方式或日期
            fq_vol: 是否复权成交量：默认值 False
            columns: 需要复权的字段列表

        返回值: 输出数据

        """
        default_cols_px = ['open', 'close', 'high', 'low', 'pre_close', 'high_limit', 'low_limit']
        default_cols_vm = ['volume']

        df = data
        if not fq or len(df) == 0:
            return df
        if not columns:
            columns = df.columns

        security = list(set(df['code'].tolist()))
        start_date = min(df['datetime']).strftime('%Y-%m-%d')
        end_date = max(df['datetime']).strftime('%Y-%m-%d')

        if fq == 'pre':
            ts_ref = pandas.Timestamp(time.strftime('%Y-%m-%d', formatter_st(end_date)))
        elif fq == 'post':
            ts_ref = pandas.Timestamp(time.strftime('%Y-%m-%d', formatter_st(start_date)))
        else:
            ts_ref = pandas.Timestamp(time.strftime('%Y-%m-%d', formatter_st(fq)))

        xrxd = self.get_security_xrxd(security=security, start_date=start_date, end_date=end_date)
        if xrxd is None:
            return df

        fq_cols_px = [x for x in list(df.columns) if x in columns and x in default_cols_px]
        fq_cols_vm = [x for x in list(df.columns) if x in columns and x in default_cols_vm] if fq_vol else []
        if not fq_cols_px and not fq_cols_vm:
            return df
        for index, row in xrxd.iterrows():
            ts_date = pandas.Timestamp(row['date'])

            # print(row['code'], row['date'], r, v)
            r = 10 / (10 + (row['dividend_ratio'] if not math.isnan(row['dividend_ratio']) else 0) + (
                row['transfer_ratio'] if not math.isnan(row['transfer_ratio']) else 0))
            v = (row['bonus_ratio'] if not math.isnan(row['bonus_ratio']) else 0) / 10
            if fq_cols_px:
                n = self.get_price_precision(row['code'])
                if ts_date <= ts_ref:
                    c = df.loc[(df['code'] == row['code']) & (df['datetime'] < ts_date), fq_cols_px]
                    if len(c) > 0:
                        c = round((c - v) * r, n)
                        df.loc[(df['code'] == row['code']) & (df['datetime'] < ts_date), fq_cols_px] = c
                else:
                    c = df.loc[(df['code'] == row['code']) & (df['datetime'] >= ts_date), fq_cols_px]
                    if len(c) > 0:
                        c = round(c / r + v, n)
                        df.loc[(df['code'] == row['code']) & (df['datetime'] >= ts_date), fq_cols_px] = c
            if fq_cols_vm:
                if ts_date <= ts_ref:
                    c = df.loc[(df['code'] == row['code']) & (df['datetime'] < ts_date), fq_cols_vm]
                    if len(c) > 0:
                        c = round(c / r)
                        df.loc[(df['code'] == row['code']) & (df['datetime'] < ts_date), fq_cols_vm] = c
                else:
                    c = df.loc[(df['code'] == row['code']) & (df['datetime'] >= ts_date), fq_cols_vm]
                    if len(c) > 0:
                        c = round(c * r)
                        df.loc[(df['code'] == row['code']) & (df['datetime'] >= ts_date), fq_cols_vm] = c
        return df

    def get_price_precision(self, security) -> int:
        """获取价格精度

        参数:
            security: 字符串或列表

        返回值: 精度或精度列表

        """
        if type(security) is str:
            n = 2
            p = security.find('.')
            if p >= 0:
                code = security[:p]
                exch = security[p + 1:]
                if exch == 'SZ':
                    if code[0] == '1':
                        n = 3
                    elif code[0:3] == '399' or code[0:4] == '9000':
                        n = 4
                elif exch == 'SH':
                    if code[0] == '5':
                        n = 3
                    elif code[0:3] == '000' or code[0:4] == '1000':
                        n = 4
            return n
        elif type(security) is list:
            r = []
            for s in security:
                r.append(self.get_price_precision(s))
            return r

    def get_quote_date(self) -> time.struct_time:
        """获取行情日期

        返回值:
            最新行情日期

        """
        filename = 'ckvalid.txt'
        txt = self._fetch_data(filename)
        if not txt:
            raise Exception('fetch data from %s failed.' % filename)

        result = dict()
        for s in txt:
            s = s.strip()
            if not s:
                continue
            p = s.find('=')
            if p <= 0:
                continue
            k = s[0:p].strip()
            v = s[p + 1:].strip()
            if not k or not v:
                continue
            result[k] = v

        stime = result.get('last_date')
        if not stime:
            raise Exception('the quote_data not found.')
        last_date = time.strptime(stime, '%Y-%m-%d')
        tdays = self.get_trade_days(end_date=last_date, count=1)
        if not tdays:
            raise Exception('trade-days is empty.')
        return formatter_st(tdays[0])

    def get_trade_days(self, start_date=None, end_date=None, count=None) -> list:
        """获取交易日列表

        参数:
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一

        返回值:
            交易日列表；类型 [datetime.date]

        """

        start_date = formatter_st(start_date) if start_date else None
        end_date = formatter_st(end_date) if end_date else None
        dt_start = numpy.datetime64(
            datetime.datetime.fromtimestamp(time.mktime(start_date))) if start_date else None
        dt_end = numpy.datetime64(datetime.datetime.fromtimestamp(time.mktime(end_date))) if end_date else None

        filename = 'quote-tdays.csv'
        df = self._fetch_data(filename, date_columns='date')
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)

        result = df['date'].values
        if dt_start or dt_end or count:
            if not dt_end:
                dt_end = numpy.datetime64(datetime.date.today())
            if count and count > 0:
                result = result[numpy.where(result <= dt_end)][-count:]
            elif dt_start:
                result = result[numpy.where((result >= dt_start) & (result <= dt_end))]
        result = [datetime.date.fromtimestamp(x.astype(datetime.datetime) / 1e9) for x in result]
        return result

    def get_security_info(self, security=None, fields=None, types=None) -> pandas.DataFrame:
        """获取证券信息数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
            types: 获取证券类型；类型 字符串 list；默认值 stock；
                   可选值: 'stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof' 等；

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                display_name：中文名称
                name：缩写简称
                start_date：上市日期；类型 datetime.date
                end_date: 退市日期；类型 datetime.date；如没有退市为 2200-01-01
                type：证券类型；stock（股票）, index（指数），etf（ETF基金），fja（分级A），fjb（分级B）

        """
        security = formatter_list(security)
        fields = formatter_list(fields)
        types = formatter_list(types, 'stock')

        result = pandas.DataFrame()
        filename = 'quote-ctb.csv'
        df = self._fetch_data(filename, date_columns=('start_date', 'end_date'))
        df = df.copy()
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)
        if types:
            df = df[df['type'].isin(types)]
        if security:
            df = df[df['code'].isin(security)]
        if fields:
            cols_retain = ['code'] + fields
            cols_all = list(df.columns)
            cols_drop = [x for x in cols_all if x not in cols_retain]
            df.drop(columns=cols_drop, inplace=True)
        result = result.append(df, ignore_index=True)
        result.set_index('code', inplace=True)
        return result

    def get_security_xrxd(self, security, start_date=None, end_date=None, count=None) -> pandas.DataFrame:
        """获取证券除权除息数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一

        返回值:
            DataFrame 对象，包含字段：
                date: 实施日期
                code：证券代码
                dividend_ratio：送股比例，每 10 股送 X 股
                transfer_ratio：转赠比例，每 10 股转增 X 股
                bonus_ratio：派息比例，每 10 股派 X 元

        """
        security = formatter_list(security)
        if not security:
            raise ValueError('security need be provided.')

        filename = 'quote-xrxd.csv'
        df = self._fetch_data(filename, date_columns='date')
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)
        df = df.copy()
        df = df[df['code'].isin(security)]
        tdays = self.get_trade_days(start_date, end_date, count)
        df = df[df['date'].isin(tdays)]
        df.sort_values(['code', 'date'], axis=0, ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def get_quote_static(self, date=None, fields=None, exch=None) -> pandas.DataFrame:
        """获取静态行情数据

        参数:
            date: 行情日期；类型 str/struct_time/datetime.date/datetime.datetime; 默认值：最新行情日
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
                   可选值：'open','close','high','low','volume','money','high_limit','low_limit','pre_close','paused'
            exch: 交易所；默认值 ['SH', 'SZ']

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                datetime: 行情时间
                code：证券代码
                open：开盘价
                close：收盘价
                high：最高价
                low：最低价
                volume：成交量
                money：成交额
                high_limit：涨停价
                low_limit：跌停价
                pre_close：昨日收盘价
                paused：停牌标记

        """
        fields = formatter_list(fields)
        exch = formatter_list(exch, ['SH', 'SZ'])
        curr_date = formatter_st(date, self.get_quote_date())
        # print(curr_date)
        result = pandas.DataFrame()
        for x in exch:
            filename = os.path.join('static', x, time.strftime('%Y', curr_date),
                                    x + '_STATIC_' + time.strftime('%Y%m%d', curr_date) + '.csv')
            df = self._fetch_data(filename, date_columns='datetime')
            if df is None:
                continue
            df = df.copy()
            df['code'] = df['code'] + '.' + x
            if fields:
                cols_retain = ['datetime', 'code'] + fields
                cols_all = list(df.columns)
                cols_drop = [x for x in cols_all if x not in cols_retain]
                df.drop(columns=cols_drop, inplace=True)
            result = result.append(df, ignore_index=True)
        # print(result)
        return result

    def get_quote_kdata(self, security, period='day', fq='pre', fq_vol=False, fields=None, start_date=None,
                        end_date=None, count=None):
        """获取K线数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            period: 周期，默认值 day，支持 day, week, mon, season, year, mnX
                    mnX 代表 X 分钟K线数据，如 mn1，mn5, mn15, mn30, mn60 等
            fq: 复权方式；默认值 'pre'；'pre' 前复权, 'post' 后复权，None 不复权，复权日期
            fq_vol: 是否复权成交量：默认值 False
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
                   可选值：'open','close','high','low','volume','money'
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                datetime: 行情时间
                code：证券代码
                open：开盘价
                close：收盘价
                high：最高价
                low：最低价
                volume：成交量
                money：成交额

        """

        # 参数格式标准化
        security = formatter_list(security)
        fields = formatter_list(fields, ['open', 'close', 'high', 'low', 'volume', 'money'])
        start_date = formatter_st(start_date) if start_date else None
        end_date = formatter_st(end_date, time.localtime())
        if not start_date and not count:
            raise ValueError('start_date or count must to be set.')
        elif start_date and count:
            raise ValueError('start_date and count cannot be set both.')

        # 对周期进行分析，获得周期基类，day / mn1
        if period in ['day', 'daily', 'week', 'mon', 'month', 'season', 'year']:
            period_type = 'day'
            period_step = 0
        elif period[-1] == 'm' and period[:-1].isdecimal():
            period_type = 'mn1'
            period_step = int(period[:-1])
        elif period[0:2] == 'mn' and period[2:].isdecimal():
            period_type = 'mn1'
            period_step = int(period[2:])
        else:
            raise Exception('period is invalid.')


        # 针对设置 count，且周期基类为 day 的非单日周期，将 count 转换为 start_date 处理
        if count and period_type == 'day' and period not in ['day', 'daily']:
            if period == 'week':
                trade_list = self.get_trade_days(count=count * 5)
                week_maps = [x.isocalendar()[0] * 100 + x.isocalendar()[1] for x in trade_list]
                week_list = list(set(week_maps))
                week_list.sort()
                w = week_list[-count]
                start_date = trade_list[week_maps.index(w)].timetuple()
            elif period in ['mon', 'month']:
                y = end_date.tm_year
                m = end_date.tm_mon + 1 - count
                while m <= 0:
                    y -= 1
                    m += 12
                start_date = datetime.datetime(y, m, 1).timetuple()
            elif period == 'season':
                y = end_date.tm_year
                s = (end_date.tm_mon - 1) // 3 + 1 - count
                while s < 0:
                    y -= 1
                    s += 4
                start_date = datetime.datetime(y, s * 3 + 1, 1).timetuple()
            elif period == 'year':
                y = end_date.tm_year + 1 - count
                start_date = datetime.datetime(y, 1, 1).timetuple()
            count = None

        # 需保留的列清单
        cols_retain = ['datetime', 'code'] + fields

        # 获取模式分析：是否从静态数据合成 mode_static
        mode_static = False
        prep_count = None
        if count:
            if period in ['day', 'daily']:
                prep_count = count
            elif period_type == 'mn1':
                prep_count = count * period_step
        if period_type == 'day':
            if prep_count:
                evaluate_days = prep_count
            elif start_date:
                evaluate_days = int((time.mktime(end_date) - time.mktime(start_date)) / 86400 * 5 / 7)
            else:
                evaluate_days = None
            if evaluate_days < len(security):
                mode_static = True
        result = pandas.DataFrame()
        if mode_static:
            # 从静态文件获取数据
            count = None
            trade_list = self.get_trade_days(start_date, end_date, prep_count)
            for x in trade_list:
                df = self.get_quote_static(x)
                df = df[df['code'].isin(security)]
                df = self.execute_rehabilitation(df, fq, fq_vol, cols_retain)
                result = result.append(df, ignore_index=True)
            cols_all = list(result.columns)
            cols_all.insert(0, cols_all.pop(cols_all.index('code')))
            result = result[cols_all]
            result.sort_values(['code', 'datetime'], axis=0, ascending=True, inplace=True)
            result.reset_index(drop=True, inplace=True)
        else:
            # 从K线文件获取数据
            dt_start = numpy.datetime64(
                datetime.datetime.fromtimestamp(time.mktime(start_date))) if start_date else None
            dt_end = numpy.datetime64(datetime.datetime.fromtimestamp(time.mktime(end_date)))
            for x in security:
                p = x.find('.')
                if p < 0:
                    continue
                sec_code = x[0:p]
                exc_code = x[p + 1:]
                filename = os.path.join(period_type, exc_code, exc_code + '_' + period_type.upper()
                                        + '_' + sec_code + '.csv')
                df = self._fetch_data(filename, date_columns='datetime')
                if df is None:
                    continue
                df = df.copy()
                if not prep_count:
                    df = df[(df['datetime'] >= dt_start) & (df['datetime'] <= dt_end)]
                else:
                    df = df[df['datetime'] <= dt_end][-prep_count:]
                df.insert(loc=0, column='code', value=sec_code + '.' + exc_code)
                df = self.execute_rehabilitation(df, fq, fq_vol, cols_retain)
                result = result.append(df, ignore_index=True)

        # 多周期分组聚合
        agg_need = True
        if period == 'year':
            result['period'] = result['datetime'].apply(lambda x: x.year)
        elif period == 'season':
            result['period'] = result['datetime'].apply(lambda x: '%dq%d' % (x.year, (x.month - 1) // 3 + 1))
        elif period == 'mon':
            result['period'] = result['datetime'].apply(lambda x: x.year * 100 + x.month)
        elif period == 'week':
            result['period'] = result['datetime'].apply(lambda x: '%dw%02d' % x.isocalendar()[:2])
        elif period_type == 'mn1' and period != 'mn1':
            m = [570, 660]
            n = period_step
            result['period'] = result['datetime'].apply(lambda x: '%d%02d%02dt%04d' % (
                x.year, x.month, x.day, ((x.hour * 60 + x.minute - 1 - m[0 if x.hour < 12 else 1]) // n + 1) * n))
        else:
            agg_need = False
        if agg_need:
            agg_dict = {'datetime': 'last', 'open': 'first', 'close': 'last', 'high': 'max', 'low': 'min',
                        'volume': 'sum',
                        'money': 'sum'}
            for k in [x for x in agg_dict.keys() if x not in cols_retain]:
                del agg_dict[k]
            result = result.groupby(['code', 'period']).agg(agg_dict)
            result.reset_index(inplace=True)
            result.drop(columns='period', inplace=True)

        # 移除非选定列
        cols_all = list(result.columns)
        cols_drop = [x for x in cols_all if x not in cols_retain]
        if cols_drop:
            result.drop(columns=cols_drop, inplace=True)

        # 重建索引
        result.reset_index(drop=True, inplace=True)

        return result
