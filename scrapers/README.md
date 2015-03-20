In general, move to a project directory and use the standard scrapy
command-line tools. The input arguments (specified by -a switch)
depend on spiders.

```
$ cd subproject
$ scrapy crawl spider_name -a 'kwarg1=val1' -a 'kwarg2=val2'
```
