package cn.edu360.spark

import org.apache.spark.broadcast.Broadcast
import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

import java.sql.{Connection, DriverManager, PreparedStatement}

/**
 * @author zhangjian
 * @date 2021-03-27 12:41
 */
object IpLocation2 {
  def main(args: Array[String]): Unit = {
    val conf: SparkConf = new SparkConf().setAppName("IpLocation2").setMaster("local[4]")
    val sc: SparkContext = new SparkContext(conf)

    //读取hdfs上的ip规则，由于文件分布在不同的集群节点上，每个节点是部分数据，需要整合成完整的ip规则数据
    val rulesLines: RDD[String] = sc.textFile(args(0))

    // 整理ip规则
    val ipRulesRDD: RDD[(Long, Long, String)] = rulesLines.map(line => {
      val fields: Array[String] = line.split("[|]")
      val startNum: Long = fields(2).toLong
      val endNum: Long = fields(3).toLong
      val province: String = fields(6)
      (startNum, endNum, province)
    })

    //收集数据到Driver端中，然后再广播到Executor中
    val rulesInDriver: Array[(Long, Long, String)] = ipRulesRDD.collect()

    //将Driver端的数据广播到Executor中
    val broadcastRef: Broadcast[Array[(Long, Long, String)]] = sc.broadcast(rulesInDriver)

    // 创建RDD，读取访问日志
    val accessLines: RDD[String] = sc.textFile(args(1))

    // 整理数据，对rdd进行操作就是对rdd的分区进行操作，每个分区生成一个task任务
    val provinceAndOne: RDD[(String, Int)] = accessLines.map(log=>{

      // 对log日志的每一行进行切分
      val fields: Array[String] = log.split("[|]")

      val ip: String = fields(1)
      //将ip地址转换为十进制
      val ipNum: Long = Utils.ip2Long(ip)
      // 进行二分法查找，通过Driver端的引用获取到Executor中的广播变量
      // 该函数的代码是在Executor中执行，通过广播变量的引用就可以拿到Executor中的广播的规则
      val rulesInExecutor: Array[(Long, Long, String)] = broadcastRef.value
      // 查找
      var province = "未知"
      val index: Int = Utils.binarySearch(rulesInExecutor, ipNum)
      if (index != -1){
        province = rulesInExecutor(index)._3
      }
      // 根据省份来计数
      (province, 1)

    }

    )

    // 聚合
    // val sum=(x:Int, y:Int)=> x+y
    val reduced: RDD[(String, Int)] = provinceAndOne.reduceByKey(_ + _)

//    // 将结果打印
//    val result: Array[(String, Int)] = reduced.collect()
//    print(result.toBuffer)
    // 数据写入到MySQL中
    // 一次拿出一个分区的数据，一个分区用一个jdbc链接，再将一个分区的数据写完成后再建立链接，减少资源的消耗。
    // 将方法转为函数reduced.foreachPartition(Utils.data2Mysql _)
    reduced.foreachPartition(it=>{Utils.data2Mysql(it)})

    sc.stop()


  }

}
