package com.pingan;

/**
 * @author zhangjian
 * @date 2020-01-29 17:29
 * 员工抽象类，
 */
public abstract class AbstractEmployee {

    private String name;

    private String id;

    /**
     * 定义抽象工作方法
     */
    public abstract void work();

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}
