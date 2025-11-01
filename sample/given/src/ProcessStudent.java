
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author PC
 */
public class ProcessStudent {
    public void sortStudent(List<Student> l){
        Collections.sort(l);
       
    }
    public List<Student> find_by_partial_name(List<Student> l,String letter){
        ArrayList<Student> filteredL = new ArrayList();
        for (Student s : l) {
            if (s.name.startsWith(letter)) {
                filteredL.add(s);
            }
        }
        return filteredL;
    }
    public List<Student> find_higher_gpa(List<Student> l,int gpa){
        ArrayList<Student> filteredL = new ArrayList();
        for (Student s : l) {
            if (s.gpa > gpa) {
                filteredL.add(s);
            }
        }
        return filteredL;
    }
}
