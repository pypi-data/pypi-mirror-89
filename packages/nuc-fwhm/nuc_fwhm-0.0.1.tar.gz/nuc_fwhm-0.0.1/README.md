# nuclear_fwhm
Full Width at Half Maximum(FWHM) value for required equipment.

The highest value of COUNTS: Y2
Its respective CHANNEL number: X2

The value of half maximum is at the half of heighest peak
The first value is the point to the left side of the peak

This is a point on the left side of the peak
The COUNT value closest to and lower than half of max, with channel number LESS than highest count channel number: Y1
Its respective channel number: X1

The channel number for count value closest and lowest to half of max, with channel number LESS than highest count channel number	

This is the point to the right side of the peak	
The COUNT value closest to and lower than half of max, with channel number GREATER than highest count channel number: Y3
Its respective channel number: X3
        
The channel number for count value closest and lowest to half of max, with channel number GREATER than highest count channel number

USING INSTRUCTIONS:      
1. in the required code "from nuc_fwhm import fwhm"
2. to use the function "fwhm(-six numbers as arguments)"
3. the six numbers are X1, X2, X3, Y1, Y2, Y3 i.e. fwhm(X1, X2, X3, Y1, Y2, Y3)
