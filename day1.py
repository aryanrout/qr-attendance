# # variable is  memory loaction 
# # typecasting 
# a=34

# print(a)
# print(type(a))
# b="34"

# print(b)
# print(type(b))
# # convert b to int 
# c=int(b)
# print(c)
# print(type(c))
# # user input 
# a=int(input("enter a number "))
# b=int(input("enter a number "))

# print (a+b)

# a=int(input("enter a number "))
# b=int(input("enter a number "))


# print (a+b)

# #escape sequences 
"""print("hello wolrd",'aryan' ,sep=",,")
print("hello wolrd",'aryan' ,end="..")
print("aryan")"""



#operator (repl:read evaluate ptint loop )
#arithmetic operation(+,-,*,%,//(floor divsion double),/)
#comparssion operator(give result in boolean form (!=,==,<,>,<=,>=))
#logical operator(used to perform operation on booolean basically for two boolean argument (and, or ,not) not: Python me not operator ek logical operator hai jo kisi condition ka ulta (opposite) karta hai.)
     # t and t is t               t or t is t          x=true
     # f and f is f               f or t is t          print (not x) o/p :false
     # f and t is f               f or f is f
#assiment operator (=,+=,-=,/=,*= **=(exponsial means powwer to))
#mebmership operator (in,not in)
#indetity operator (is ,is not)
      

#if else stateement if-else statements in programming to make decisions based on certain conditions.
"""age=int(input("eneter yout age "))
if(age>18):
    print("yes you can drive")
elif(age==18):
 print("yes you can drive")
else:
    print("no you can not drive")"""
#match  similar to switch case new version 3.1.0
"""a=int(input("enter a number between 1-10:"))
match a:
    case 1:
        print("you won a trip to chichago")
    case 3:
        print("you won a cricket kit")
    case 7:
        print("better luck next time")
    case _:
      print("your luck is too bad")"""

#for loop :We use a for loop to repeat a block of code a specific number of times.
#range fuction  goes from 1 to n-1 for example range (1,6) so it will go 1 to n-1 where n is 6
"""for i in range (1,6):
  print (i)"""

#printing tabke of 5 
"""for i in range (1,11):
    print(5*(i))
# printing satr
for i in range (1,6):
         
         print("*"*i)
"""

#while loop 
i=1
while i<6:
    print(i*("*"))
    i=i+1


    
 
  
a='7'
b='3'
print(a*int(b))