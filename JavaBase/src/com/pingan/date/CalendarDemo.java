package com.pingan;

import java.util.Calendar;

/**
 * @author zhangjian
 * @date 2020-02-04 19:16
 */
public class CalendarDemo {
    public static void main(String[] args) {
        function();
    }

    /**
     * Calendar类的get方法
     * 获取日历字段的值
     * int get(int)
     * 参数int，获取的哪个日历字段
     * 返回值，表示日历字段的具体数值
     */
    public static void function() {
        Calendar c = Calendar.getInstance();
        System.out.println(c);
        //获取年份
        int year = c.get(Calendar.YEAR);
        //获取月份
        int month = c.get(Calendar.MONTH) + 1;
        //获取天数
        int day = c.get(Calendar.DAY_OF_MONTH);
        System.out.println(year+"年"+month+"月"+day+"日");

    }
}
