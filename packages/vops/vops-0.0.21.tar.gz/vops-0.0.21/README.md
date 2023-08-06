# Vops
This python project uses data from yahoo finance to graph option profit-loss diagrams.

Note: any examples used here are outdated because the option contracts have expired.

## Installing
Installing with pip:
```bash
pip install vops
```

## Usage
Simple program graphing a long call option:
```python
from vops import scraping
from vops import graphing

optionObj = scraping.scrapeCallOptions('TSLA')

graphing.graphLongCall(optionObj, 'TSLA201224C00020000')
```
Graphing both short and long positions on a call option:
```python
optionObj = scraping.scrapeCallOptions('TSLA')

graphing.graphCalls(optionObj, 'TSLA201224C00020000')
```

Exporting graphs to a png:
```python
graphing.graphCalls(optionObj, 'TSLA201224C00020000', export = True)
```

Output:

![plot](./res/options.png)

## Todo

* Update resource files
* Add axis labels to all graphs
* Create method for graphing long and short put options simultaneously
* Merge call/put options chains
