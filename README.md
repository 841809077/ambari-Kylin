# ambari-Kylin
Ambari集成Apache Kylin服务

---

> 参考 cas-bigdatalab提交的ambari-kylin-service项目
> 项目地址: https://github.com/cas-bigdatalab/ambari-kylin-service.git
>
> 感谢大佬提供了ambari集成Kylin服务的思路。

---

> 加群

这个项目开源了一段时间了，有不少人已经在用了，大部分朋友都已经搭建成功。如果您在使用过程中遇到任何问题，可扫描下方二维码关注公众号或者加我好友，回复【加群】，群内有不少已经搭建成功的小伙伴。

  ![](https://841809077.github.io/img/qrcode.png)

---

> 概述

目前上传至ambari-Kylin上的有两个版本，一个是**HDP2.6与Kylin2.5.1**集成使用的一版；一个是**HDP3.0与Kylin2.6.0**集成使用的一版。

上传至github上的仅支持服务的基本使用，如正常启停，超链接`Kylin Web UI`功能。

但是像服务的**启停顺序**和服务的**自定义告警**没有上传至此，需要微信关注公众号**大数据实战演练**，也可扫描底部二维码，回复**ambari-kylin**关键词获取云盘链接。云盘链接不仅有**两个集成kylin服务的完整版**，还有脚本中用到的**kylin与nginx的源码**。

可能有人会想，为什么要这么麻烦？！**原因很简单，我的公众号刚刚起步，现在我将耗费了好几天整理出来的心血免费贡献给有需要的人，我就想让大家多多关注我的公众号而已，或者通过公众号还可以交个朋友。内容都是干货，排版也很精美，并且里面的私信都会很快回复大家的！**

**ambari-kylin部署过程中有什么困难的话，也可以通过微信公众号来联系我。**

> 使用该项目的前提条件

1. **ambari主节点**上安装`httpd`服务并开启，**将Kylin和Nginx的源码包**放到`/var/www/html/kylin`目录下。（源码包不需要解压。由于源码包太大，`github`上传不了，请到文章底部关注**我的微信公众号**，回复**ambari-kylin**获取云盘链接。也感谢您的关注！）
2. 在`ambari`集群**各主机**已安装`wget`命令
3. **hdp-2.6-kylin-2.5.1**适配`CentOS-7 64`位系统，`CentOS-6 64`位系统（使用`CentOS-6`系统，启动`nginx`时可能会报错，**下文会粘出解决方法**）；**hdp-3.0-kylin-2.6.0**仅适配于`CentOS-7 64`位系统。其他系统没有测试。
4. 适配于**ambari2.6 + hdp 2.6.4.0-91** 和 **ambari2.7 + hdp 3.0.1.0-187**，请根据需要选取使用版本。

---

> hdp-2.6-kylin-2.5.1部署步骤：

1. 将Kylin和Nginx的源码包放到Ambari主节点的`/var/www/html/kylin`中，不需要解压。

2. 这里我选择的stack版本是`2.6`，在Ambari主节点上执行一下命令：

   ```shell
   git clone https://github.com/841809077/ambari-Kylin.git
   cp -r ambari-Kylin/hdp-2.6-kylin-2.5.1/KYLIN/ /var/lib/ambari-server/resources/stacks/HDP/2.6/services
   ```

   最终如图所示：

   ![](https://cdn.jsdelivr.net/gh/841809077/blog-img/20190101/20190124234507.jpg)

3. 重启ambari：`ambari-server restart`

> hdp-3.0-kylin-2.6.0部署步骤：

1. 将Kylin和Nginx的源码包放到Ambari主节点的`/var/www/html/kylin`中，不需要解压。

2. 这里我选择的stack版本是`3.0`，在Ambari主节点上执行一下命令：

   ```shell
   git clone https://github.com/841809077/ambari-Kylin.git
   cp -r ambari-Kylin/hdp-3.0-kylin-2.6.0/KYLIN/ /var/lib/ambari-server/resources/stacks/HDP/3.0/services
   ```

   最终如图所示：

   ![](https://cdn.jsdelivr.net/gh/841809077/blog-img/20190301/20190312220020.jpg)

3. 重启ambari：`ambari-server restart`

---

> Kylin部署方式

目前采用的`Kylin`部署集群方式相对来说简单，只需要增加`Kylin`的节点数，因为`Kylin`的元数据（`Metadata`）是存储在`HBase`中，只需要在`Kylin`中配置，让`Kylin`的每个节点都能访问同一个`Metadata`表就形成了`Kylin`集群（`kylin.metadata.url` 值相同）。并且`Kylin`集群中只有一个`Kylin`实例运行任务引擎（`kylin.server.mode＝all`)，其它`Kylin`实例都是查询引擎(`kylin.server.mode=query`)模式。
为了实现负载均衡，即将不同用户的访问请求通过`Load Balancer`（负载均衡器）（比如`lvs，nginx`等）分发到每个`Kylin`节点，保证`Kylin`集群负载均衡。对于负载均衡器可以启用`SSL`加密，安装防火墙，对外部用户只用暴露负载均衡器的地址和端口号，这样也保证`Kylin`系统对外部来说是隔离的。
我们的生产环境中使用的`LB`是`nginx`，用户通过`LB`的地址访问`Kylin`时，`LB`将请求通过负载均衡调度算法分发到`Kylin`集群的某一个节点，不会出现单点问题，同时如果某一个`Kylin`节点挂掉了，也不会影响用户的分析。
这种方式也不是完美的，但是比较好配置，一般场景下是可以满足的。

---

> 该项目修改如下：

1. Kylin和Nginx源码修改

   - 修改了Kylin的日志输出为`/var/log/kylin/`目录下

   - 修改Nginx的日志输出为`/var/log/nginx/目录下`

   - 修改Nginx的pid文件路径为：`/var/run/nginx/nginx.pid`
2. 完善脚本逻辑，优化代码。
3. 增加并修改`kylin.xml`和`nginx.xml`文件内容
4. 实现在`ambari web UI`修改配置项，保存后**提示重启**功能
5. 由于`80`端口与`httpd`端口冲突，所以修改Nginx的端口为`81`
6. **解决**nginx负载均衡后，需要刷新页面，重复登陆才可以访问到实时数据的**问题**，实现`session`会话持久性

---

> 项目逻辑说明

1. 通过`wget`命令在主节点的本地仓库中下载`Kylin`和`Nginx`的源码，源码安装路径分别为：`/usr/hdp/2.6.4.0-91(或3.0.1.0-187)/kylin`和`/usr/hdp/2.6.4.0-91(或3.0.1.0-187)/nginx`。不要修改nginx的安装目录，否则启动nginx会报错。**如果需要更改nginx的安装目录，需要重新编译nginx源码。**
2. 通过该服务脚本能够成功部署Kylin集群，**三台主机：一个all模式，两个query模式，nginx节点可安装在任意一台节点上。**
3. **不足或需要注意的地方：** **选择Kylin slave的时候，Kylin all所在节点上不能安装Kylin Query，这里在ambari界面上没有做限制。要注意**。最终实现效果就是**每个节点上都有Kylin服务，只不过模式不同，分工不同。**

---

> 效果图

**HDP3.0-kylin2.5.1：**

![](https://cdn.jsdelivr.net/gh/841809077/blog-img/20181110/20181214222045.jpg)

![](https://cdn.jsdelivr.net/gh/841809077/blog-img/20181110/20181214223927.png)

![](https://cdn.jsdelivr.net/gh/841809077/blog-img/20181110/20181213234222.jpg)

**HDP3.0-kylin2.6.0：**

![](https://cdn.jsdelivr.net/gh/841809077/blog-img/20190301/20190312220225.jpg)

![](https://cdn.jsdelivr.net/gh/841809077/blog-img/20190301/20190312220751.jpg)

---

> nginx在CentOS-6 64位系统启动失败问题解决方案

[点击这里获取解决方案](https://841809077.github.io/2018/05/21/Nginx%E5%AE%89%E8%A3%85%E9%85%8D%E7%BD%AE.html#5-ngnix%E5%9C%A8CentOS-6%E7%B3%BB%E7%BB%9F%E5%90%AF%E5%8A%A8%E6%8A%A5%E9%94%99)

---

> 还拥有的功能

1. Kylin服务默认配置依赖于hdfs，mapreduce，hive，hbase组件，如何定义ambari集群各服务组件的起停顺序，使Kylin服务组件在hdfs，mapreduce，hive，hbase组件之后启动呢，这是一个知识点。
2. 添加告警设置，如果某节点的Kylin端口挂掉了，给与用户报警展示。

---
kylin + nginx 源码包太大，gitgub上传不了，并且**上述还拥有的功能已经实现**，如果有需要的可以**私信我的公众号**：回复**ambari-kylin**获取云盘链接，里面有**整个源码包和自定义Kylin安装服务脚本完整版（HDP2.6+与HDP3.0+均支持Kylin集成）**。

上述功能如果感兴趣的，可以**微信搜索公众号私聊我：大数据实战演练**或者**扫描下方二维码关注**即可：

![](https://cdn.jsdelivr.net/gh/841809077/blog-img/20181110/20181213235322.png)	
