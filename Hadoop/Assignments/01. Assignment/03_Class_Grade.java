// 3. Class Grades Analyzer
// Write a Java program that stores the grades of 5 students in an array (e.g., int[] grades = {88, 76,
// 95, 100, 67};).
// • Calculate and print the average grade for the class.
// • Find and print the highest grade in the array.
// • Find and print the lowest grade in the array.



class Grades {
    public static void main(String[] args) {
        int[] grades = {88, 76, 95, 100, 67};
        double avg = 0;
        int sum = 0;
        int total_stud = grades.length;
        int highest = grades[0];
        int lowest = grades[0];

        for (int i=0; i < grades.length; i++){
            sum = sum + grades[i];
        }
        avg = sum / total_stud;
        System.out.println("Average of the Class: "+avg);

        for (int i=0; i < grades.length; i++){
            if (highest < grades[i]){
                highest = grades[i];
            }
        
        }
        System.out.println("The Highest Grade in Class: "+highest);


        for (int i=0; i < grades.length; i++){
            if (lowest > grades[i]){
                lowest = grades[i];
            }
        
        }
        System.out.println("The Lowest Grade in Class: "+lowest);

    }
}