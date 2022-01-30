classdef CamInfo

properties (GetAccess=public, SetAccess=protected)
   receiverId
   senderId
   data
end

methods (Access=public)
   function obj = CamInfo(receiverId,senderId,filePath)
       obj.receiverId = receiverId;
       obj.senderId = senderId;
       obj.data = containers.Map('KeyType','double','ValueType','any');
       f = readmatrix(filePath);
       for i=1:size(f,1)
           id1 = num2str(f(i,2));
           id2 = num2str(f(i,3));
           if strcmp(id1,obj.receiverId) && strcmp(id2,obj.senderId)
               simTime = f(i,1); % sec
               longitude = f(i,4)*10^-7; % degree
               latitude = f(i,5)*10^-7; % degree
               [easting,northing,~,~] = wgs2utm(latitude,longitude); % meters
               heading = deg2rad(f(i,6)/10); % radian
               speed = f(i,7)/100; % meter/sec
               if f(i,8) == 1, speed = (-1)*speed; end
               acceleration = f(i,9)/1000; % meter/sec^2
               curvature = f(i,10)/10000; % meter^-1
               yawRate = deg2rad(f(i,11)/100); % radian/sec
               kinematicInfo = KinematicInfo(easting,northing, ...
                   heading,speed,acceleration,curvature,yawRate);
               obj.data(simTime) = kinematicInfo;
           end
       end
   end
end

end