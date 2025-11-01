/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author PC
 */
public class Student implements Comparable{
    public String id;
    public String name;
    public double gpa;
    
    public Student(){};
    public Student(String id,String name,double gpa){
        this.id = id;
        this.name=name;
        this.gpa=gpa;
    }
    @Override
    public int compareTo(Object other){
        Student o = (Student) other;

        int nameComparison = this.name.compareTo(o.name);
        if (nameComparison != 0) {
            return nameComparison;
        }

        
        return Double.compare(this.gpa, o.gpa);
    }
}
