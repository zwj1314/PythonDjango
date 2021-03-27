package cn.edu360.sparkstream

import org.apache.spark.streaming.dstream.{DStream, ReceiverInputDStream}
import org.apache.spark.streaming.{Milliseconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

/**
 * @author zhangjian
 * @date 2021-03-27 21:27
 */
object StreamingWordCount {
  def main(args: Array[String]): Unit = {

    // 离线任务是创建SparkContext，现在要实现实时计算，用StreamingContext。local后面的数字代表着线程的个数*代表多线程
    val conf: SparkConf = new SparkConf().setAppName("SteamingWordCount").setMaster("local[2]")
    val sc: SparkContext = new SparkContext(conf)

    // StreamingContext是对SparkContext的包装，包装了一层实现了实时功能
    // 第二个参数是小批次产生的时间间隔
    val ssc: StreamingContext = new StreamingContext(sc, Milliseconds(5000))

    // 有了StreamingContext，就可以创建StreamingContext的抽象DStream
    // 从一个socket端口中读取数据
    val lines: ReceiverInputDStream[String] = ssc.socketTextStream("192.168.3.26", 8888)
    // 对DStream进行操作，操作这个抽象就像操作一个本地集合
    val words: DStream[String] = lines.flatMap(_.split(" "))
    // 单词和1组合在一起
    val wordAndOne: DStream[(String, Int)] = words.map((_, 1))
    // 聚合
    val result: DStream[(String, Int)] = wordAndOne.reduceByKey(_ + _)

    // 打印结果
    result.print()

    // 启动SparkStreaming程序
    ssc.start()

    // 等待程序退出
    ssc.awaitTermination()

  }

}
