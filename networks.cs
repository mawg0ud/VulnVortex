using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Collections;


namespace University
{
    class networks
    {

string University;
string Student;
int ID;
string Faculty;
string n,id;
     
      public static void Main()
       {
          
        string path = "C:\\University.txt";


        // "Delete" if there is a duplicate file
        if (File.Exists(@"C:\\University.txt"))
           {
            File.Delete(@"C:\\University.txt");
           }


        // Create (University) file
        using (FileStream uni = File.Create(@"C:\\University.txt"))
        {

       // Insert variable records
        
        void ReadData ()
            {
            
            Console.Write("Please, Enter student name: ");
            n = Console.ReadLine();;
            Console.Write(" Please, Enter student ID: ");
            id = Console.ReadLine();
            {
           Console.WriteLine(n); 
           Console.WriteLine(id);
           Console.ReadLine();
            };


         // Insert fixed records
            FileStream uni1 = new FileStream(@"C:\\University.txt", FileMode.Open, FileAccess.Write);
            StreamWriter writer = new StreamWriter(uni1);
            writer.Write("Ahmed,12569,ICS");
            writer.Write("karim,11467,Engineering");
            writer.Write("Emad,17830,Pharmacy");
            writer.Write("Abd-Allah,15456,Mass Communication");
            writer.Write("Omar,19008,Engineering");
            writer.Write("Samer,15321,Business");
            writer.Write("Mostafa,14327,Dentistry");
            writer.Write("Nasr,87344,Dentistry");
            writer.Write("Zeyad,99786,Mass Communication");
            writer.Write("Ali,90804,Nursing");
            writer.Close();


        // Open the stream and read waht in it
        using (StreamReader uni2 = File.OpenText(@"C:\\University.txt"))
        {
            string student = "";
            while ((student = uni2.ReadLine()) != null)
            {
                Console.WriteLine(uni1);
            }
        }


        // Adding 3 students records
        using(var fileStream = File.Open(@"C:\\University.txt", FileMode.Open, FileAccess.Write))
        {
            using (StreamWriter uni3 = new StreamWriter(@"C:\\University.txt", true))
            {
              writer.Write("Noran,78543,Dentistry");
              writer.Write("Rawan,98007,Mass Communication");
              writer.Write("Mohamed,12342,Engineering");
              writer.Close();
            }


        // Updating student record
         ArrayList ICS = new ArrayList();
            string filename = "@C:\\University.txt";
            using (StreamWriter uni5 = new StreamWriter(University))
            {
                int lineCount = 1;
 
                foreach (String uni6 in ICS)
                {
                    if (lineCount % 6 == 0)
                        uni5.WriteLine("Student information is not available");
                    else
                        uni5.WriteLine(uni1);
 
                    ++lineCount;
                }
                uni5.Close();
            }


        //Deleting student record
            List<string>
            studentlist=File.ReadAllLines(University).ToList();
            string firstItem = studentlist[0];
            studentlist.RemoveAt(0);
            File.WriteAllLines(filename, studentlist.ToArray());






        //Reclaiming Space







        //Primary Index
              // private void CreateIndex(string student, string id, bool unique = false)
               //{
               //Database.ExecuteSqlCommand(String.Format("create first primary index)", 
               //unique ? "UNIQUE" : "",
               //id,
               //student.Replace(",","_"),
               //student));
               } 








        //Secondary Index









        //Serialization






       

    }
}