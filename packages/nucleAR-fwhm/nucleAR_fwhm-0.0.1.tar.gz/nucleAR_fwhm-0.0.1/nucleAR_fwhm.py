def fwhm(X1, X2, X3, Y1, Y2, Y3):
    # The highest value of COUNTS: Y2
    # Its respective CHANNEL number: X2

    Y4 = (Y2)/2 # The value of half maximum is at the half of heighest peak
    print("The half of max value: ", Y4) #This is the point to the left side of the peak

    # This is a point on the left side of the peak
    # The COUNT value closest to and lower than half of max, with channel number LESS than highest count channel number: Y1
    # Its respective channel number: X1

    X5 = ((((Y4 - Y1)*(X2 - X1))/(Y2 - Y1))+(X1))
    #The channel number for count value closest and lowest to half of max, with channel number LESS than highest count channel number	
    print("The SMALLER value of CHANNEL number at half of max: ", X5)

    # This is the point to the right side of the peak	
    # The COUNT value closest to and lower than half of max, with channel number GREATER than highest count channel number: Y3
    # Its respective channel number: X3
        
    X4 = ((((Y4 - Y3)*(X2 - X3))/(Y2 - Y3))+(X3))
    #The channel number for count value closest and lowest to half of max, with channel number GREATER than highest count channel number
    print("The LARGER value of CHANNEL number at half of max: ", X4)
        
    X = X4-X5

    print("The full width at half maximum(F.W.H.M.) is nearly: ", X) #This value helps to determine the resolution power of the instrument

# in the required code "from nuc_fwhm import fwhm"
# to use the function "fwhm(-six numbers as arguments)"
# the six numbers are X1, X2, X3, Y1, Y2, Y3