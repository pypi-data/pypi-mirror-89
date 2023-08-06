# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cnholiday']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cnholiday',
    'version': '0.2.0',
    'description': '查询某天是否放假',
    'long_description': '# CNHoliday: 查询某天是否放假\n\n数据来源:\n\n| 年份 | 出处                                                                                                             |\n| :--: | ---------------------------------------------------------------------------------------------------------------- |\n| 2019 | [国务院办公厅关于 2019 年部分节假日安排的通知](http://www.gov.cn/zhengce/content/2018-12/06/content_5346276.htm) |\n| 2020 | [国务院办公厅关于 2020 年部分节假日安排的通知](http://www.gov.cn/zhengce/content/2019-11/21/content_5454164.htm) |\n| 2021 | [国务院办公厅关于 2021 年部分节假日安排的通知](http://www.gov.cn/zhengce/content/2020-11/25/content_5564127.htm) |\n\n安装：\n\n```sh\n# 不依赖第三方包库\npip install cnholiday\n```\n\n用法：\n\n```python\n>>> from datetime import datetime\n>>>\n>>> from cnholiday import CNHoliday\n>>>\n>>>\n>>> cnholiday = CNHoliday()\n>>> _day = datetime(2019, 10, 1)\n>>> print(cnholiday.check(_day))\nTrue\n>>> print(cnholiday.check_shift(_day))\nTrue\n>>> print(cnholiday.check_shift(_day, shift=2))\nTrue\n>>> print(cnholiday.check_shift(_day, shift=3))\nTrue\n```\n\n---\n\n相关项目：\n\n- GitHub 上有另一个同名项目 <https://github.com/valaxy/cnholiday>\n',
    'author': 'ringsaturn',
    'author_email': 'ringsaturn.me@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ringsaturn/cnholiday',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
