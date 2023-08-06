import math
print("Welcome to Py Academy")

for ch in range(1,100):

  what_subject = input("What subject may I help you with today?(Math/Physics) ")

    
  if what_subject == "math" or what_subject == "Math" or what_subject == "mathematics" or what_subject == "Mathematics":

    what_chap = input("What chapter may I help you with?(Progressions/Straight Lines(sl)/ Calculus)")

    if what_chap == "progressions" or what_chap == "Progressions":

      print("The topics involved along with their formulae are:")
      print('''For any Arithmetic Progression;
      a = first term of an AP, d = common difference of an AP
      nth term of an AP: a + (n-1)d
      Sum of n terms of an AP: n/2[2a + (n-1)d]

        Arithmetic Mean of two numbers 'a' and 'b';
        AM = [a+b]/2
        d = [b-a]/[n+1]

        For any Geometric Progression;
        a = first term of a GP, r = common ratio of GP
        nth term of a GP: ar^(n-1)
        Sum of n terms of GP: [a(r^n - 1)]/r-1

        Geometric Mean of two numbers 'a' and 'b';
        GM = (ab)^[1/2]
        r = (b/a)^[1/n+1]''')

      more_help=input("Do you need further assistance?(Yes/No) ")

      if more_help == "yes" or more_help == "Yes":
        ProgOrMean = (input("Do you want to find AM/GM or nth term/sum or insertion of AM/GM(ins)? "))

        if ProgOrMean == "nth term/sum" or ProgOrMean == "nth term/Sum":

          first_term = input("Enter First Term of the Progression: ")
          first_term = float(first_term)
          is_ap_or_gp = input("Is the Progression AP or GP?")
          is_ap_or_gp = str(is_ap_or_gp)

          if is_ap_or_gp == "AP" or is_ap_or_gp == "ap":
            common_difference = input("Enter Common Difference:")
            common_difference = float(common_difference)
            term = input("Enter the Term:")
            term = int(term)
            find_nth_term_or_sum = input("Do You Want to Find nth term or sum? ")
            find_nth_term_or_sum = str(find_nth_term_or_sum)

            if find_nth_term_or_sum == "nth term" or find_nth_term_or_sum == "nth Term":
              nth_term = first_term + ((term - 1) * common_difference)
              print("the nth Term is", nth_term)

            elif find_nth_term_or_sum == "sum" or find_nth_term_or_sum == "Sum":
              Sum = (term/2)*((2*first_term) + ((term-1)*common_difference))     
              print("The Sum is", Sum)
          else:
            common_ratio = input("Enter Common Ratio of GP:" )
            common_ratio = float(common_ratio)
            term = input("Enter nth Term of GP:")
            term = int(term)
            find_nth_term_or_sum = input("Do You Want to Find nth term or sum?")

            if find_nth_term_or_sum == "nth term" or find_nth_term_or_sum == "nth Term":
              nth_term = round(((first_term)*((common_ratio)**(term-1)),2)) 
              print("The nth Term is", nth_term)

            elif find_nth_term_or_sum == "sum" or find_nth_term_or_sum == "Sum":
              Sum = ((first_term*(1-common_ratio**term))/(1-common_ratio))   
              print("The Sum is", Sum)

        elif ProgOrMean == "AM/GM" or ProgOrMean == "am/gm":
          AM_GM = input("Do you want to find AM or GM?")

          if AM_GM == "AM" or AM_GM == "am":
            term_one = int(input("Enter one term:"))
            term_two = int(input("Enter second term:"))
            AM = (term_one + term_two)/2
            print("The AM is",AM)

          else:
            term_one = int(input("Enter one term:"))
            term_two = int(input("Enter second term:"))
            GM = (term_one*term_two)**(1/2)
            print("The GM is",GM)

        else:

          AMorGM = input("Insertion of AMs or GMs?")

          if AMorGM == "AM" or AMorGM == "AMs":
            a = int(input("Enter first term: "))
            b = int(input("Enter last term: "))
            n = int(input("Enter the number of terms you want to enter: "))
            d = (b-a)/(n+1)
            series = 0
            print("The AP thus formed is")

            for ch in range(0,n+2):
              Series = a + (d*ch)
              print(Series)

          else:
            
            a = int(input("Enter first term: "))
            b = int(input("Enter last term: "))
            n = int(input("Enter the number of terms you want to insert: "))
            r = (b/a)**(1/(n+1))
            series = 1
            print("The GP thus formed is")

            for ch in range(0,n+2):
              Series = a*(r**ch)
              print(Series)
              
    
    
    elif what_chap == 'straight lines' or what_chap == 'sl':

      print('''The topics involved along with their formulae are:
      General equation of a line is ax + by + c = 0.

      If equation of a line is of the form y = mx+c, then m is the slope of the line.


        Slope of a line given two points (a,b) and (c,d);
        (d-b)/(c-a) = (y-b)/(x-a).

        Angle(A) between two lines with slopes m and M ;
        tanA = (M-m)/(1+mM).''')

      more_help = input("Do you need further assistance?")

      if more_help == "yes" or more_help == "Yes":
                
        dist = input("Do you want to find the distance of a point from a line?")

        if dist == "yes" or dist == "Yes":

          y_coordinate = float(input("Enter y-coordinate of the point:"))
          x_coordinate = float(input("Enter x-coordinate of the point:"))
          coeff_y = float(input("Enter coefficient of y from the equation of the line:"))
          coeff_x = float(input("Enter coefficient of x from the equation of the line:"))
          constant = float(input("Enter constant term from the equation of the line:"))
          distance = round((y_coordinate*coeff_y + x_coordinate*coeff_x + constant)/((coeff_x**2) + (coeff_y**2))**(1/2),2)
          print("The perpendicular distance of the point from the line is",distance)

        else:
          coordinates_given = input("Are the coordinates of line given?")

          if coordinates_given == "yes" or coordinates_given == "Yes":
            y1 = float(input("Enter first y-coordinate:"))
            y2 = float(input("Enter second y-coordinate:"))
            x1 = float(input("Enter first x-coordinate:"))          
            x2 = float(input("Enter second x-coordinate:"))
            slope = ((y2-y1)/(x2-x1))
            print("The slope of the line is",slope)
            y_diff = y2-y1
            x_diff = x1-x2
            constant = (x1*(y1-y2) + y1*(x2-x1))
            angle = round(math.degrees(math.atan(slope)),2)
            print("The angle made by the line with the x-axis is",angle,"degrees")
            print("The equation of the line is",y_diff,"x +",x_diff,"y" "+",constant,"= 0")
            
            from matplotlib import pyplot as plt
            plt.plot([x1,x2],[y1,y2])
            plt.show()
                    
          else:
              
            slope = float(input("Enter slope of the line:"))
            y_int = float(input("Enter y-intercept of the line:"))
            print("The equation of the line is y =", slope,"x +", y_int)
            from matplotlib import pyplot as plt
            plt.plot([0,(-y_int/slope)],[y_int,0])
            plt.show()
            
    elif what_chap == 'c' or what_chap == 'Calculus':
      from sympy import *
      import matplotlib.pyplot as plt
      x = Symbol('x')
      y = Symbol('y')
      calc = input("Do you want to differentiate or integrate a function? (diff/int)")

      if calc == 'diff':
          f = input("Enter function to be differentiated :")
          print(diff(f,x))
              
      else:
          f = input("Enter function to be integrated :")
          print(integrate(f,x))
      continue
      


  elif what_subject == "physics" or what_subject == "Physics":
    what_chap = input("What chapter do you need help with, Projectile Motion(pm) or Circular Motion(cm)? ")

    if what_chap == "projectile motion" or what_chap == "Projectile Motion" or what_chap == "Projectile motion" or what_chap == "pm":

      x = float(input("Enter Initial Velocity(m/s):"))
      t = float(input("Enter Angle of Projection(degrees):"))
      y = math.radians(t)

      time_of_flight = ((x*(math.sin(y)))/5)
      print("Time of Flight is",time_of_flight,"seconds")

      horizontal_range = (((x**2)*(math.cos(y))*(math.sin(y)))/5)
      print("Horizontal Range of the Projectile is",horizontal_range,"meters")

      maximum_height = (((x**2)*((math.sin(y)**2)))/20)
      print("Maximum Height of the Projectile is",maximum_height,"meters")

      coeff_x = (5/(x*math.cos(y))**2)
      eqn = ('y =',math.tan(y),'x -',coeff_x,'x^2')
      print("The equation of the projectile is")
      print('y =',math.tan(y),'x -',coeff_x,'x^2')

    elif what_chap == "Circular Motion" or what_chap == "circular motion" or what_chap == "cm":
      find = input("What do you want to find, Angular Velocity(av), Angular Acceleration(aa)? ")

      if find == "angular velocity" or find == "Angular Velocity" or find == "av":
        accn_giv = input("Is the angular acceleration given?")

        if accn_giv == "Yes" or accn_giv == "yes":
          ang_accn = float(input("Enter the angular acceleration(in rad/s^2):"))
          ang_disp = float(input("Enter the angular displacement(in rad):"))
          ang_vel = (2*ang_accn*ang_disp)**(1/2)
          print("The angular velocity is",ang_vel,"rad/s")

        else:
          cent_accn = input("Is the centripetal acceleration given?")

          if cent_accn == "yes" or cent_accn == "Yes":
            cent_accn == float(input("Enter the centripetal acceleration(in m/s^2):"))
            radius = float(input("Enter the radius of circular motion(in m):"))
            vel = (cent_accn*radius)**(1/2)
            ang_vel = (vel/radius)
            print("The angular velocity is",ang_vel,"rad/s")

          else:
            lin_accn = float(input("Enter the linear acceleration(in m/s^2):"))
            radius = float(input("Enter the radius of circular motion(in m):"))
            ang_disp = float(input("Enter the angular displacement(in rad):"))
            ang_accn = lin_accn/radius
            ang_vel = (2*ang_accn*ang_disp)**(1/2)
            print("The angular velocity is",ang_vel,"rad/s")

      elif find == "angular acceleration" or find == "Angular Acceleration" or find == "aa":
        ang_vel = input("Is the angular velocity given?")

        if ang_vel == "Yes" or ang_vel == "yes":
          ang_vel = float(input("Enter the angular velocity(in rad/s):"))
          ang_disp = float(input("Enter the angular displacement(in rad):"))
          ang_accn = (ang_vel/(2*ang_disp))
            
        else:
          cent_accn = input("Is the centripetal acceleration given?")

          if cent_accn == "Yes" or cent_accn == "yes":
            cent_accn = float(input("Enter the centripetal acceleration(in m/s):"))
            accn = float(input("Enter net acceleration(in m/s^2):"))
            ang_accn = ((accn**2)-(cent_accn**2))**(1/2)
            print("The angular acceleration is",ang_accn)
  
  else:
    print("Please enter valid subject.")

  quiz = input("Would you like to take a small test based on what you have learnt? (y/n)")
  if quiz == "y" or quiz == "yes" or quiz == "Y":
    sub = input("What subject do you want to take the quiz on? (P/M)")
    if sub == "M" or sub == "m" or sub == "math":
      import random
      chp = input("What Math chapter would you like to take a test for: Progressions (pr) or Straight lines(sl): ")
      
      if chp == "Progressions" or chp == "progressions" or chp == "pr":
          num = random.randint(1,2)
          if num == 1:
              print("Q1) The 4 arithmetic means between 3 and 23 are: ")
              print("A) 5,9,11,13")
              print("B) 7,11,15,19")
              print("C) 5,11,15,22")
              print("D) 7,15,19,21")
              ans = input("Enter correct option: ")
              if ans == "B":
                print("Correct")
              else:
                print("Incorrect")
                  
              print()
              print("Q2) The GM of the numbers 3,(3^2),(3^3),...(3^n) is: ")
              print("A) 3^(2/n)")
              print("B) 3^((n+1)/2)")
              print("C) 3^(n/2)")
              print("D) 3^((n-1)/2)")
              ans = input("Enter correct option: ")
              if ans == "B":
                print("Correct")
              else:
                print("Incorrect")
                        
          else:
              print("Q1) The nth term of the series 3+10+17+... and 63+65+67+... are equal, then the value of n is?")
              print("A) 11")
              print("B) 12")
              print("C) 13")
              print("D) 15")
              ans = input("Enter correct option: ")
              if ans == "C":
                print("Correct")
              else:
                print("Incorrect")
              print()            
              print("Q2) The sum of few terms of any GP is 728, if common ratio is 3 and last term is 486, then first term of series will be?")
              print("A) 2")
              print("B) 1")
              print("C) 3")
              print("D) 4")
              ans = input("Enter correct option: ")
              if ans == "A":
                print("Correct")
              else:
                print("Incorrect")

      
      elif chp == "Straight lines" or chp == "sl" or chp == "straight lines":
          print("Q1) The equation of the line perpenicular to the line x/a - y/b = 1 and passing through the point at which it cuts x axis, is?")
          print("A) x/a + y/b + a/b = 0")
          print("B) x/b + y/a = b/a")
          print("C) x/b + y/a = 0")
          print("D) x/b + y/a = a/b")
          ans = input("Enter correct option: ")
          if ans == "A":
            print("Correct")
          else:
            print("Incorrect")
              
          print("Q2) Find the distance of the point (1,-1) from the line 12(x+6) = 5(y-2).")
          print("A) 4units")
          print("B) 8units")
          print("C) 6units")
          print("D) 5units")
          ans = input("Enter correct option: ")
          if ans == "D":
            print("Correct")
          else:
            print("Incorrect")

      else:
        print("Enter valid chapter")
        


    elif sub == "P" or sub == "p" or sub == "physics":
      chp = input("What physics chapter would you like to take the quiz for: Projectile Motion(pm) or Circular Motion(cm)?")
      if chp == "Projectile Motion" or chp == "pm":
        import random
        num = random.randint(1,2)

        if num == 1:
            
            print('''Question 1. A particle is projected at an angle 37 deg with the incline plane in upward direction with speed 10 m/s. The angle of inclination of plane is 53 deg. Then the maximum distance from the incline plane
            attained by the particle will be:
            A)3m
            B)4m
            C)5m
            D)0m''')
            ans1 = input('Enter answer:')
            if ans1 == 'A':
              print("Good job! That's the correct answer!")
            else:
              print('''That answer is incorrect.''')
                
            print('''Question 2. It was calculated that a shell when fired from a gun with a certain velocity and at an angle of elevation 5pi/36 rad should strike a given target in same horizontal plane. In actual practice, it was found that a hill just prevented the trajectory. At what angle of elevation should the gun be
                  fired to hit the target:
                  A)5pi/36 rad
                  B)11pi/36 rad
                  C)7pi/36 rad
                  D)13pi/36 rad''')
            ans2 = input('Enter answer:')
            if ans2 == 'D':
              print("Good job that's the correct answer")
            else:              
              print("Incorrect")
                
            
        else:
            
            print('''Question 1. A point mass is projected, making an acute angle with the horizontal. If the angle between velocity vector and acceleration vector g is theta at any time
                  t during the motion, then theta is given by:
                  A)0 < theta < 90
                  B)theta = 90
                  C)theta < 90
                  D)0 < theta < 180''')
            ans3 = input("Enter answer:")
            if ans3 == 'D':
              print("Good job! That's the correct answer.")
            else:
              print("Incorrect")

            print('''Question 2. What is the maximum speed of oblique projectile from the ground in the vertical plane passing through a point (30m,40m) and projection
                  point is taken as the origin (g = 10 m/s^2):
                  A)30 m/s
                  B)20m/s
                  C)10root5 m/s
                  D)50 m/s''')
            ans4 = input("Enter answer:")
            if ans4 == "A":
              print("Good job! That answer's correct!")
            else:
              print("Incorrect")
      
      else:
        import random
        num = random.randint(1,2)
        if num == 1:
          print('''Question 1. The maximum velocity with which a car driver must traverse a flat curve of radius 150m, coeff of friction 0.6 to avoid skidding
          A)60 m/s
          B)30 m/s
          C)15 m/s
          D)25 m/s''' )
          ans5 = input("Enter your answer:")
          if ans5 == "B":          
            print("Good job! That's the correct answer!")
          else:            
            print("Incorrect")
          print('''Question 2. A wheel is at rest. Its angular velocity increases uniformly and becomes 80 rad/s after 5 sec. Total angular displacement is:
                A)800 rad
                B)400 rad
                C)200 rad
                D)100 rad''')
          ans6 = input("Enter your answer:")
          if ans6 == 'C':
            print("Good job! That's the correct answer!")
          else:
            print("Incorrect")
          
        else:
          print('''Question 1. A particle moves along a circle of radius 20/pi m with constant tangential acceleration. If the speed of particle is 80 m/s at the end of the second revolution after the motion has begun, find tangential acceleration:
                A)160pi m/s^2
                B)40pi m/s^2
                C)40 m/s^2
                D)640pi m/s^2''')
          ans7 = input("Enter your answer:")
          if ans7 == "C":
            print("Good job! That's the correct answer!")
          else:
            print("Incorrect")
          print('''Question 2. A bucket's whirled in a vertical circle with a string. The water in bucket doesn't fall even when bucket's inverted at top of its path. In this position:
                A)mg = mv^2/r
                B)mg is greater than mv^2/r
                C)mg is not greater than mv^2/r
                D)mg is not less than mv^2/r''')
          ans8 = input("Enter your answer:")
          if ans8 == "C":
            print("Good job! That's the correct answer!")
          else:
            print("Incorrect")

      

    else:
      print("Enter valid subject")

  else:
    print("Happy learning!")

input()