classdef KinematicInfo

properties (GetAccess=public, SetAccess=protected)
   easting % meters
   northing % meters
   heading % radian
   speed % meter/sec
   acceleration % meter/sec^2
   curvature % meter^-1
   yawRate % radian/sec
end

methods (Access=public)
   function obj = KinematicInfo(easting,northing,heading,speed, ...
           acceleration,curvature,yawRate)
       obj.easting = easting;
       obj.northing = northing;
       obj.heading = heading;
       obj.speed = speed;
       obj.acceleration = acceleration;
       obj.curvature = curvature;
       obj.yawRate = yawRate;
   end
end

end