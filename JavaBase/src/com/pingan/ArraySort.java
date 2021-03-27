package com.pingan;

/**
 * @author zhangjian
 * @date 2020-01-15 21:34
 * 数组的排序：选择排序（数组中第一个元素与之后的每一个元素都进行比较）
 * 冒泡排序（数组中相邻的元素进行比较）
 * 规则：比较大小，位置交换
 */
public class BubbleSort {
    //程序的主入口
    public static void main(String[] args) {

        int[] arr = {1, 45, 6, 745, 451, 235};
        //调用选择排序
        bubbleSort(arr);
        //打印数组
        printArray(arr);

    }

    /**
     *
     * @param arr:输入的待排序的数组
     */
    public static void bubbleSort(int[] arr) {
        for (int i = 0; i < arr.length-1; i++) {
            //内循环，每次循环的次数都在减少
            for (int j = i + 1; j < arr.length; j++) {
                //如果前一个元素比后一个元素要大
                if (arr[i] > arr[j]) {
                    //数组进行换位
                    int temp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = temp;
                }
            }
            
        }

    }

    public static void printArray(int[] arr) {
        //输出一半中括号,不要换行打印
        System.out.print("[");
        //对数组进行遍历
        for(int i = 0 ; i < arr.length ; i++){
            //判断遍历到的元素,是不是数组的最后一个元素
            //如何判断 循环变量 到达 length-1
            if( i == arr.length-1 ){
                //输出数组的元素和]
                System.out.print(arr[i]+"]");
            } else {
                //不是数组的最后一个元素,输出数组元素和逗号
                System.out.print(arr[i]+",");
            }
        }
        System.out.println();
    }
}
