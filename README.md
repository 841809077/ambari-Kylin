# ambari-Kylin
Ambari集成Apache Kylin服务

---

> 参考 cas-bigdatalab提交的ambari-kylin-service项目
> 项目地址: https://github.com/cas-bigdatalab/ambari-kylin-service.git
>
> 感谢这位前辈提供了ambari集成Kylin服务的思路。

---

> 使用该项目的前提条件

1. **ambari主节点**上安装`httpd`服务并开启，将代码的`resource_package`文件目录下的**tar包**放到`/var/www/html/kylin`目录下
2. 在ambari集群**各主机**已安装`wget`命令
3. 适配CentOS-7 64位系统，CentOS-6 64位系统（使用该系统，启动nginx时可能会报错，下文会粘出解决方法），其他系统没有测试
4. 适配于ambari2.6 + hdp 2.6.4.0-91，ambari2.7（待适配）
5. 版本说明：Kylin 5.2.1 + Nginx 1.8.1

---

> Kylin部署方式

目前采用的Kylin部署集群方式相对来说简单，只需要增加Kylin的节点数，因为Kylin的元数据（Metadata）是存储在HBase中，只需要在Kylin中配置，让Kylin的每个节点都能访问同一个Metadata表就形成了Kylin集群（kylin.metadata.url 值相同）。并且Kylin集群中只有一个Kylin实例运行任务引擎（kylin.server.mode＝all)，其它Kylin实例都是查询引擎(kylin.server.mode=query)模式。
为了实现负载均衡，即将不同用户的访问请求通过Load Balancer（负载均衡器）（比如lvs，nginx等）分发到每个Kylin节点，保证Kylin集群负载均衡。对于负载均衡器可以启用SSL加密，安装防火墙，对外部用户只用暴露负载均衡器的地址和端口号，这样也保证Kylin系统对外部来说是隔离的。
我们的生产环境中使用的LB是nginx，用户通过LB的地址访问Kylin时，LB将请求通过负载均衡调度算法分发到Kylin集群的某一个节点，不会出现单点问题，同时如果某一个Kylin节点挂掉了，也不会影响用户的分析。
这种方式也不是完美的，但是比较好配置，一般场景下是可以满足的。

---

> 该项目修改如下：

1. Kylin和Nginx源码修改

   - 修改了Kylin的日志输出为`/var/log/kylin/`目录下

   - 修改Nginx的日志输出为`/var/log/nginx/目录下`

   - 修改Nginx的pid文件路径为：`/var/run/nginx/nginx.pid`
2. 完善脚本逻辑，优化代码，去除`env.rc.j2`文件。
3. 增加并修改`kylin.xml`和`nginx.xml`文件内容
4. 实现在ambari web UI修改配置项，保存后**提示重启**功能
5. 由于`80`端口与`httpd`端口冲突，所以修改Nginx的端口为`81`
6. 解决nginx负载均衡后，需要刷新页面，重复登陆才可以访问到实时数据，实现`session`会话持久性

---

> 项目逻辑说明

1. 通过`wget`命令在主节点的本地仓库中下载`Kylin`和`Nginx`的源码，安装路径分别为：`/usr/hdp/2.6.4.0-91/kylin`和`/usr/hdp/2.6.4.0-91/nginx`。不要修改nginx的安装目录，否则启动nginx会报错，需要重新编译nginx源码
2. 通过该服务脚本能够成功部署Kylin集群，三台主机：一个all模式，两个query模式，nginx节点可安装在任意一台节点上。
3. **不足：** 选择Kylin slave的时候，Kylin all所在节点上不能安装Kylin Query了，这里没有做限制。要注意。最终实现效果就是每个节点上都有Kylin服务，只不过模式不同，分工不同。

---

> 效果图

![](https://raw.githubusercontent.com/841809077/blog-img/master/20181110/20181214222045.jpg)

![](https://raw.githubusercontent.com/841809077/blog-img/master/20181110/20181214223927.png)

![](https://raw.githubusercontent.com/841809077/blog-img/master/20181110/20181213234222.jpg)

---

> nginx在CentOS-6 64位系统启动失败问题解决方案

待整理

---

> 还拥有的功能

1. Kylin服务依赖于hdfs，mapreduce，hive，hbase组件，如何定义ambari集群各服务组件的起停顺序，使Kylin服务组件在hdfs，mapreduce，hive，hbase组件之后启动呢，这是一个知识点
2. 添加告警设置，如果某节点的Kylin端口挂掉了，给与用户报警展示

---

上述功能如果感兴趣的，可以**微信搜索公众号私聊我：大数据实战演练**或者**扫描下方二维码关注**即可：

![](https://raw.githubusercontent.com/841809077/blog-img/master/20181110/20181213235322.png)	




