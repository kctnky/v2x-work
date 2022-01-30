classdef TrueInfo

properties (GetAccess=public, SetAccess=protected)
   stationId
   data
end

methods (Access=public)
   function obj = TrueInfo(stationId,filePath)
       obj.stationId = stationId;
       obj.data = containers.Map('KeyType','double','ValueType','any');
       f = readmatrix(filePath);
       for i=1:size(f,1)
           id = num2str(f(i,2));
           if strcmp(id,obj.stationId) == 1
               simTime = f(i,1); % sec
               longitude = f(i,3)*10^-7; % degree
               latitude = f(i,4)*10^-7; % degree
               [easting,northing,~,~] = wgs2utm(latitude,longitude); % meters
               heading = deg2rad(f(i,5)/10); % radian
               speed = f(i,6)/100; % meter/sec
               if f(i,7) == 1, speed = (-1)*speed; end
               acceleration = f(i,8); % meter/sec^2
               curvature = f(i,9)/10000; % meter^-1
               yawRate = deg2rad(f(i,10)/100); % radian/sec
               kinematicInfo = KinematicInfo(easting,northing, ...
                   heading,speed,acceleration,curvature,yawRate);
               obj.data(simTime) = kinematicInfo;
           end
       end
   end
end

end