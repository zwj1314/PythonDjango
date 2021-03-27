package cn.edu360.spark

import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

/**
 * @author zhangjian
 * @date 2021-02-15 17:18
 * 根据日志计算最受欢迎的老师
 */
object FavTeacher {
  def main(args: Array[String]): Unit = {

    //定义spark上下文
    val conf = new SparkConf().setAppName("FavTeacher").setMaster("local[4]")
    val sc = new SparkContext(conf)

    //指定从哪里读取数据
    val lines: RDD[String] = sc.textFile(args(0))

    //整理数据
    val teacherAndOne = lines.map(line => { 
      val index = line.lastIndexOf("/")
      val teacher = line.substring(index + 1)
      (teacher, 1)
    })

    //聚合
    val reduced: RDD[(String, Int)] = teacherAndOne.reduceByKey(_ + _)
    //排序
    val sorted = reduced.sortBy(_._2, false)
    //触发action
    val result: Array[(String, Int)] = sorted.collect()

    //打印
    print(result.toBuffer)

    sc.stop()



  }

}
