# Monitor and auto execute single script after modify

support go, python, c++, c.
filename endswith .py .c .cpp .go
extend other.
Support django reload server when template change.

[zh_cn] 自动执行修改后的脚本

## install

```bash
pip install seeing
```

## use

```bash
seeing -f hello.py
seeing -s 3 -f hello.go  # execute script after hello.go modified 3 seconds.
seeing -f hello.cpp      # it will run g++ hello.cpp && ./a.out
seeing -f hello.c        # same as cpp

# reload django devlop server
pip install gunicorn
seeing -c gunicorn project_name.wsgi
```

## extend other

```bash
seeing -c sh hello.sh
seeing -c open hello.html
seeing -c node hello.js
seeing -c scrapy spider.py
```
