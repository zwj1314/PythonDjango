package com.pingan;


import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * 对日期进行格式化（自定义）
 *
 * @author zhangjian
 * @date 2020-02-04 17:27
 */
public class SimpleDateFormatDemo {
    public static void main(String[] args) {
        function_2();
    }

    /**
     * 如何对日期格式化
     * 步骤：
     *  1、创建SimpleDateFormat对象
     *      在类构造方法中，写入字符串的日期格式(自己定义)
     *  2、SimpleDateFormat调用方法format对日期进行格式化
     *      String format(Date date)传递日期对象，返回字符串
     *
     *      日期模式
     *      yyyy 年份
     *      MM   月份
     *      dd   月中的天数
     *      HH   0-23小时
     *      mm   小时中的分钟
     *      ss   秒
     */
    public static void function() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy年MM月dd日HH点mm分钟ss秒");
        String date = sdf.format(new Date());
        System.out.println(date);

    }

    /**
     * DateFormat类方法 parse
     * 将字符串解析为日期对象
     * Date parse(String s) 字符串变成日期对象
     * 用户的输入转化成日期格式String =>> Date
     * Date ==> String format
     * 步骤：
     * 1、创建SimpleDateFormat对象
     *      构造方法中，指定日期格式
     * 2、子类对象，调用方法parse，传递String，返回Date
     *
     * 注意：时间和日期模式中的yyyy-MM-dd必须完全匹配才可以
     */
    public static void function_2(){
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        Date date = null;
        try {
            date = sdf.parse("2020-02-03");
        } catch (ParseException e) {
            e.printStackTrace();
        }
        System.out.println(date);
    }

}
