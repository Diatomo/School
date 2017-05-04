


#file: donations
#BEGIN{printf("%s", ". *** CAMPAIGN 2016 ***\n")
#printf("%s", ". CONTRIBUTION REPORT Q1\n")
BEGIN {
  #print("----------------------------------------------------------------------------------------------------------------------")
  printf("%s %s %s %s %s %s\n", "NAME", "PHONE-NUMBER", "Jan|", "Feb|", "Mar|", "Total-Donated\n")
  #print("----------------------------------------------------------------------------------------------------------------------")}
  max = 0
  min = 1000}
{sum = $3 + $4 + $5
  printf("%s %s %d %d %d %d\n", $1, $2, $3, $4, $5, sum)
  janTotal += $3
  febTotal += $4
  marTotal += $5
  grandTotal += sum
  for (j = 3; j < NF; j++){
    min = (min < $j) ? min : $j
    max = (max > $j) ? max : $j
  }
}
END{
  #print("----------------------------------------------------------------------------------------------------------------------\n")
  #print("----------------------------------------------------------------------------------------------------------------------\n")
  printf("%s %s %d %d %d %d\n"," - ", " - ", janTotal, febTotal, marTotal, grandTotal)
  print("\nSummary:")
  monthMax = janTotal
  if (monthMax < febTotal){
    monthMax = febTotal
    }
  if (monthMax < marTotal){
    monthMax = marTotal
  }
  printf("Total-received-this-quarter: %.2f\n",grandTotal)
  print(" \n")
  printf("Best-month: %.2f\n", monthMax)  #findMax
  printf("Number-of-contributors: %d\n", NR)
  printf("Highest-Contribution: %.2f\n", max)#findMax #name
  printf("Lowest-contribution: %.2f\n", min)#minimum
  print("\n")
  grandTotal = grandTotal / 12
  printf("Average-total-donation %.2f\n", grandTotal)#average
  }

