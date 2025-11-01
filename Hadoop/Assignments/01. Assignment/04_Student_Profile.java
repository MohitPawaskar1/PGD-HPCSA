// 4. Student Profile
// Create a Student class with the following attributes (fields):
// • String name
// • int studentID
// • double gpa

// The class should also have a method:
// • void displayProfile(): This method prints all the student's information to the console in a
// clean format.
// In your main method, create two different Student objects, set their attributes, and call the
// displayProfile() method for each one.


class Student {
    String name;
    int studentID;
    double gpa;

    Student (String n, int studID, double gpaa){
        name = n;
        studentID = studID;
        gpa = gpaa;

    }

    void displayProfile() {
        System.out.println("Student's Profile");
        System.out.println("---------------------------");
        System.out.println("Student Name: "+name);
        System.out.println("Student ID  : "+studentID);
        System.out.println("Student GPA : "+gpa);
        System.err.println("");

    }
}


class Profile {

    public static void main(String[] args) {
    
    Student s1 = new Student("Soham", 7021, 9.0);
    Student s2 = new Student("Mohit", 7012, 6.86);
    Student s3 = new Student("Yogesh", 7011, 9.9);
    Student s4 = new Student("Ajinkya", 7002, 8.5);
    s1.displayProfile();
    s2.displayProfile();
    s3.displayProfile();
    s4.displayProfile();
    
    }




}