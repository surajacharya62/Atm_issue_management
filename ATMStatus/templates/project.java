


import java.util.Scanner; 

/**
 *
 * @author Prashant Ghimire|11702500
 */
 public class RopeCalculation
 {

     public void RemainingLengthOfRope()
     {
         System.out.print("Enter The 'Positive Integer' Number of Cut:");
         int rope= 100;
            int sum = 0, float remlen= 0.00;
                    Scanner cut= new Scanner(System.in);
                    int n= cut.nextInt();
                    for(in i=1;i<=n;i++)
                    {
                        
                        if(remlen >0)
                        {
                            remlen = rope / 2
                            sum += remlen
                            rope = remlen
                            System.out.println(" The length after "+i+"time cut is: "+ remlen+ " feet.");
                        }
                        else
                        {
                            
                            break;
                        }
                        

                    }
                        System.out.println(".The total javaremaining length after "+n+"time cut is: "+ remlen+ " feet.");
     }

 }

 public static class MainProgramam{

    public static void main(String[] args) {
        // Assign Value of Rope
        
        RopeCalculation obj = new RopeCalculation();
        
        System.out.println("The length of the rope is "+ rope +"feet.");
        System.out.println("");    
	while(1)   
	{
     System.out.print("Enter 1 for number of cut:");     
     System.out.print("Enter 2 for exit");
     System.out.print("Enter The 'Positive Integer' Number of Cut:");
        Scanner cut= new Scanner(System.in);
        int y= cut.nextInt();       
         switch (y) {
                    case 1:
                        obj.RemainingLengthOfRope();
                        
                    case 2:
                        exit();
                        
                    default:
                        MainProgramam.main();
                }
    }     

         
    
}
