      subroutine wave(eta,t,x,H0,d0)      
      
      real (kind=8) t,x,H0,d0
      real (kind=8) eta
      real (kind=8) k,c
!       k=sqrt(3.d0*H0/(4*d0**3))
!       c=1.d0+H0/(2.d0*d0)
!       
!       eta=d0+H0*(cosh(5.d0-k*c*t))**(-2.d0)

     
      eta=.01d0*sin(2.d0*3.14d0/2.d0*t)
      return
      end