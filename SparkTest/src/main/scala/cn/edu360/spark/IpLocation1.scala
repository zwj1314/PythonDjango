package cn.edu360.spark

import org.apache.spark.broadcast.Broadcast
import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

/**
 * @author zhangjian
 * @date 2021-03-27 12:41
 */
object IpLocation1 {
  def main(args: Array[String]): Unit = {
    val conf: SparkConf = new SparkConf().setAppName("IpLocation1").setMaster("local[4]")
    val sc: SparkContext = new SparkContext(conf)

    //在Driver端获取到全部的ip规则数据（全部的ip规则数据在某一台机器上，跟driver在同一台机器上）
    // 全部的ip规则在Driver端，在driver的内存中
    val rules: Array[(Long, Long, String)] = Utils.parseRule(args(0))

    //将Driver端的数据广播到Executor中

    //调用sc上的广播方法
    //广播变量的引用（还在Driver端）
    val broadcastRef: Broadcast[Array[(Long, Long, String)]] = sc.broadcast(rules)

    // 创建RDD，读取访问日志
    val accessLines: RDD[String] = sc.textFile(args(1))

    // 这个函数在Driver定义的
    val func = (line: String) => {
      val fields: Array[String] = line.split("[|]")
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

    // 整理数据，对rdd进行操作就是对rdd的分区进行操作，每个分区生成一个task任务
    val provinceAndOne: RDD[(String, Int)] = accessLines.map(func)

    // 聚合
    // val sum=(x:Int, y:Int)=> x+y
    val reduced: RDD[(String, Int)] = provinceAndOne.reduceByKey(_ + _)

    // 将结果打印
    val result: Array[(String, Int)] = reduced.collect()
    print(result.toBuffer)

    sc.stop()


  }

}
