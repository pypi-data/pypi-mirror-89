#! -*- coding: utf8 -*-
import itertools
import re

from rich import print
from rich.columns import Columns
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

from .main import GetMovies
from .const import WEEK

def transferWeekDay(d):
    return d[:-2] + WEEK.get(d[-2], '') + d[-1:]

def generateTime(date, time):
    time = list(map(lambda x: ['', x], time))
    time[0][0] = transferWeekDay(date)
    return time

def create_row(table, data):
    for i in data: table.add_row(*i)


def main():
    movies = GetMovies()
    data = list()
    for m in movies:
        for i in range(len(m.get('title', ''))-1, -1, -1):
            if re.match(r'[A-Za-z 0-9-]', m.get('title')[i]):
                continue
            m['title'] = m.get('title')[:i+1] + '\n' + m.get('title')[i+1:]
            break
        table = Table(title=m.get('title'), min_width=len(m.get('title')))
        table.add_column('Date', style="cyan", no_wrap=True, justify="right")
        table.add_column('Time', style="magenta")

        for v in m.get('time', dict()).items():
            for d in generateTime(*v): table.add_row(*d)

        data.append(table)
    console = Console()
    console.print(Columns(data))

if __name__ == '__main__':
    main()
