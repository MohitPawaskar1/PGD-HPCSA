import java.util.Arrays;

class Arrays_Operation {
    public static void main(String[] args) {
        
    int[] marks = new int[3];
    marks[0] = 97;
    marks[1] = 98;
    marks[2] = 95;

    System.out.println("Mark List      : "+marks[0]);
    System.out.println("Lenght of Array: "+marks.length);
    Arrays.sort(marks);
    System.out.println("Sorted Array   : "+marks[0]);
    }
}
