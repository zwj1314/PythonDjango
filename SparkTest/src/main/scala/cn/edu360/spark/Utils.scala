package cn.edu360.spark

import java.sql.{Connection, DriverManager, PreparedStatement}
import scala.io.{BufferedSource, Source}

/**
 * @author zhangjian
 * @date 2021-03-19 23:12
 */
object Utils {

  //将ip地址转化为十进制
  def ip2Long(ip: String): Long = {
    val fragments: Array[String] = ip.split("[.]")
    var ipNum = 0L
    for (i <- 0 until fragments.length ){
      ipNum = fragments(i).toLong | ipNum << 8L
    }
    ipNum
  }

  //解析ip的规则，解析出起始ip地址和结束ip地址对应的十进制以及省份信息
  def parseRule(path: String): Array[(Long, Long, String)] = {
    // 读取数据文件
    val bf: BufferedSource = Source.fromFile(path)
    // 得到文件的每一行数据
    val lines: Iterator[String] = bf.getLines()
    // 对scala的迭代器进行操作
    val rules: Array[(Long, Long, String)] = lines.map(line => {
      val fileds: Array[String] = line.split("[|]")
      val startNum: Long = fileds(2).toLong
      val endNum: Long = fileds(3).toLong
      val province: String = fileds(6)
      (startNum, endNum, province)
    }
      // 加载到内存中
    ).toArray
    rules

  }

  // 定义二分查找法，输入的是数组和要匹配的ip地址，返回的是对应的位置索引
  def binarySearch(lines: Array[(Long, Long, String)], ip: Long) : Int = {
    var low = 0
    var high = lines.length - 1
    while (low <= high){
      val middle = (low + high) / 2
      if ((ip >= lines(middle)._1) && (ip <= lines(middle)._2)) {
        return middle
      }
      if (ip < lines(middle)._1) {
        high = middle - 1
      } else {
        low = middle + 1
      }
    }
    -1
  }

  def data2Mysql(it: Iterator[(String, Int)]): Unit ={
    val conn: Connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/bigdata", "root", "abcd1234")
    val pstm: PreparedStatement = conn.prepareStatement("insert into access_log values (?, ?)")
    // 将分区中的每一条数据拿出来
    it.foreach(tp=>{
    pstm.setString(1, tp._1)
    pstm.setInt(2, tp._2)
    pstm.executeUpdate()
  })
    pstm.close()
    conn.close()
  }

  def main(args: Array[String]): Unit = {

    // 数据放入内存中
    val rules: Array[(Long, Long, String)] = parseRule("/Users/zhangjian/Downloads/ip.txt")
    // 将ip地址转为十进制
    val ipNum: Long = ip2Long("111.198.38.185")
    // 二分查找
    val index: Int = binarySearch(rules, ipNum)
    // 根据返回的索引到rules中找到对应的省份信息
    val province: String = rules(index)._3

    print(province)
  }

}
