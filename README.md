# CM Real time GRAPH
RealTime Cable Modem Graph for Docsis cable modems

>Displaying current docsis information about the customer or cable modem is always something you must have an option to look at. This is a real time CM graph running for 5 minutes and refreshing after 10 seconds. It is displaying the following information:

- Downstream Signal
- Downstream Signal To Noise Ratio
- Downstream Micro Reflections
- Downstream Codeword Error Ratio
- Downstream Forward Erorr Correction
- Upstream Signal
- Upstream Signal To Noise Ratio
- Upstream Cable Modem RX Power
- Upstream Codeword Error Ratio
- Upstream Forward Erorr Correction
- Current Traffic On Cable Interface

***Dashboard***
![Dashboard](https://raw.githubusercontent.com/l-n-monitoring/CM-RT-GRAPH/master/images/screencapture-localhost-3333-d-6gm-OtWWk-rt-cm-graph-2019-05-20-15_58_40.png)()

**Prerequirements**
- <a href="https://docs.influxdata.com/influxdb/v1.7/introduction/installation/">InfluxDB</a>
- <a href="https://docs.influxdata.com/telegraf/v1.10/introduction/installation/">Telegraf</a>
- <a href="https://grafana.com/docs/installation/">Grafana</a>
- net-snmp
- <a href="https://pypi.org/project/puresnmp/">puresnmp</a> (pip3 install puresnmp)

**Installation**
```
cd /opt
git clone https://github.com/l-n-monitoring/CM-RT-GRAPH.git

```
```

```
