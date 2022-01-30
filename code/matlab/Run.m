clear;
clc;

%% Initialization

% Station IDs
observerVehicleId = '1982038771';
egoVehicleId = '4184398590';
%observerVehicleId = '4184398590';
%egoVehicleId = '2357136044';
%observerVehicleId = '1982038771';
%egoVehicleId = '2357136044';

% Time of the first CAM from ego to observer, multiplied by 100, rounded up
% i.e., ceil(100*tCam)
tStart = 2112; 
%tStart = 2106; 
%tStart = 1125; 

% Time of the last CAM from ego to observer, multiplied by 100, rounded down
% i.e., floor(100*tCam)
tEnd = 15710;
%tEnd = 9571;
%tEnd = 9592;

% Ground-truth data
observerInfo = TrueInfo(observerVehicleId,'/home/kaan/V2X/analysis/data/camdata/world_data.csv');
trueInfo = TrueInfo(egoVehicleId,'/home/kaan/V2X/analysis/data/camdata/world_data.csv');

% CAM based data
camBasedInfo = CamInfo(observerVehicleId,egoVehicleId,'/home/kaan/V2X/analysis/data/camdata/cam_data.csv');

% We count time by tens of milliseconds
tSeconds = (tStart:tEnd)/100;
numPoints = tEnd-tStart+1;

%%

% Kalman tracker
kalman = KalmanTracker;

% Process noise params
kalman.yaw_proc_n = 0.1;
kalman.accel_proc_n = 1;

% Measurement noise params
kalman.easting_meas_n = 5;
kalman.northing_meas_n = 5;

% Kalman1
%kalman.speed_meas_n = 0.017;
%kalman.accel_meas_n = 2.5e-5;
%kalman.heading_meas_n = 7.75e-05;
%kalman.yaw_meas_n = 7.75e-07;

% Kalman2
kalman.speed_meas_n = 1e-8;
kalman.accel_meas_n = 1e-8;
kalman.heading_meas_n = 1e-8;
kalman.yaw_meas_n = 1e-8;

% Initial uncertainities
easting_initial_u = 100;
northing_initial_u = 100;
speed_initial_u = 100;
accel_initial_u = 100;
heading_initial_u = 100;
yaw_initial_u = 100;

%% Observer vehicle true information

% read true information of observer vehicle
for k=keys(observerInfo.data)
    t = k{1};
    tObserver = round(t*100); % 1 time unit: 10 msec
    xObserver(tObserver) = observerInfo.data(t).easting;
    yObserver(tObserver) = observerInfo.data(t).northing;    
    tetaObserver(tObserver) = observerInfo.data(t).heading;
    vObserver(tObserver) = observerInfo.data(t).speed;
    wObserver(tObserver) = observerInfo.data(t).yawRate;
    aObserver(tObserver) = observerInfo.data(t).acceleration;
end
% fill empty middle points with the last available information
lastx = 0;
lasty = 0;
lastteta = 0;
lastv = 0;
lastw = 0;
lasta = 0;
for i=1:size(xObserver,2)
    if xObserver(i) == 0
        xObserver(i) = lastx;
        yObserver(i) = lasty;
        tetaObserver(i) = lastteta;
        vObserver(i) = lastv;
        wObserver(i) = lastw;
        aObserver(i) = lasta;
    else
        lastx = xObserver(i);
        lasty = yObserver(i);
        lastteta = tetaObserver(i);
        lastv = vObserver(i);
        lastw = wObserver(i);
        lasta = aObserver(i);
    end
end
xObserver = xObserver(tStart:tEnd);
yObserver = yObserver(tStart:tEnd);
tetaObserver = tetaObserver(tStart:tEnd);
vObserver = vObserver(tStart:tEnd);
wObserver = wObserver(tStart:tEnd);
aObserver = aObserver(tStart:tEnd);
% Here, xObserver and yObserver vectors have the true position information 
% of observer vehicle with respect to time indexed in tens of milliseconds.
clear tObserver lastx lasty lastteta lastv lastw lasta k i t

%% Ego vehicle true information

% read true information of ego vehicle
for k=keys(trueInfo.data)
    t = k{1};
    tTrue = round(t*100); % 1 time unit: 10 msec
    xTrue(tTrue) = trueInfo.data(t).easting;
    yTrue(tTrue) = trueInfo.data(t).northing;
    tetaTrue(tTrue) = trueInfo.data(t).heading;
    vTrue(tTrue) = trueInfo.data(t).speed;
    wTrue(tTrue) = trueInfo.data(t).yawRate;
    aTrue(tTrue) = trueInfo.data(t).acceleration;
end
% fill empty middle points with the last available information
lastx = 0;
lasty = 0;
lastteta = 0;
lastv = 0;
lastw = 0;
lasta = 0;
for i=1:size(xTrue,2)
    if xTrue(i) == 0
        xTrue(i) = lastx;
        yTrue(i) = lasty;
        tetaTrue(i) = lastteta;
        vTrue(i) = lastv;
        wTrue(i) = lastw;
        aTrue(i) = lasta;
    else
        lastx = xTrue(i);
        lasty = yTrue(i);
        lastteta = tetaTrue(i);
        lastv = vTrue(i);
        lastw = wTrue(i);
        lasta = aTrue(i);
    end
end
xTrue = xTrue(tStart:tEnd);
yTrue = yTrue(tStart:tEnd);
tetaTrue = tetaTrue(tStart:tEnd);
vTrue = vTrue(tStart:tEnd);
wTrue = wTrue(tStart:tEnd);
aTrue = aTrue(tStart:tEnd);
% Here, xTrue and yTrue vectors have the true position information of ego 
% vehicle with respect to time indexed in tens of milliseconds.
clear tTrue lastx lasty lastteta lastv lastw lasta k i t

%% Ego vehicle cam based information

% read cam based information of ego vehicle
for k=keys(camBasedInfo.data)
    t = k{1};
    tCam = round(t*100);
    xCam(tCam) = camBasedInfo.data(t).easting;
    yCam(tCam) = camBasedInfo.data(t).northing;
    tetaCam(tCam) = camBasedInfo.data(t).heading;
    vCam(tCam) = camBasedInfo.data(t).speed;
    wCam(tCam) = camBasedInfo.data(t).yawRate;
    aCam(tCam) = camBasedInfo.data(t).acceleration;
end
% fill empty middle points with the last available information
lastx = 0;
lasty = 0;
lastteta = 0;
lastv = 0;
lastw = 0;
lasta = 0;
for i=1:size(xCam,2)
    if xCam(i) == 0
        xCam(i) = lastx;
        yCam(i) = lasty;
        tetaCam(i) = lastteta;
        vCam(i) = lastv;
        wCam(i) = lastw;
        aCam(i) = lasta;
    else
        lastx = xCam(i);
        lasty = yCam(i);
        lastteta = tetaCam(i);
        lastv = vCam(i);
        lastw = wCam(i);
        lasta = aCam(i);
    end
end
xCam = xCam(tStart:tEnd);
yCam = yCam(tStart:tEnd);
tetaCam = tetaCam(tStart:tEnd);
vCam = vCam(tStart:tEnd);
wCam = wCam(tStart:tEnd);
aCam = aCam(tStart:tEnd);
% Here, xCam and yCam vectors have the cam based position information of 
% ego vehicle with respect to time indexed in tens of milliseconds.
clear tCam lastx lasty lastteta lastv lastw lasta k i t

%% Distance between ego and observer

distanceBetweenTwo = zeros(1,numPoints);
for i=1:numPoints
    distanceBetweenTwo(i) = sqrt((yTrue(i)-yObserver(i))^2 + (xTrue(i)-xObserver(i))^2);
end
clear i;

%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,distanceBetweenTwo);
title('Distance between ego and observer vehicles');
xlabel('Time (seconds)');
ylabel('Distance (meters)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
saveas(f,'figure1_distance_between_vehicles','fig');
saveas(f,'figure1_distance_between_vehicles','png');
close(f);

%% Ego vehicle plots

ego_true_northing = zeros(1,numPoints);
ego_true_easting = zeros(1,numPoints);
ego_true_heading = zeros(1,numPoints);
ego_true_speed = zeros(1,numPoints);
ego_true_yaw = zeros(1,numPoints);
ego_true_accel = zeros(1,numPoints);
ego_true_time = zeros(1,numPoints);

ego_cam_northing = zeros(1,camBasedInfo.data.length);
ego_cam_easting = zeros(1,camBasedInfo.data.length);
ego_cam_heading = zeros(1,camBasedInfo.data.length);
ego_cam_speed = zeros(1,camBasedInfo.data.length);
ego_cam_yaw = zeros(1,camBasedInfo.data.length);
ego_cam_accel = zeros(1,camBasedInfo.data.length);
ego_cam_time = zeros(1,camBasedInfo.data.length);

i = 0;
for k=keys(trueInfo.data)
    t = k{1};
    i = i+1;
    ego_true_northing(i) = trueInfo.data(t).northing;
    ego_true_easting(i) = trueInfo.data(t).easting;
    ego_true_heading(i) = trueInfo.data(t).heading;
    ego_true_speed(i) = trueInfo.data(t).speed;
    ego_true_yaw(i) = trueInfo.data(t).yawRate;
    ego_true_accel(i) = trueInfo.data(t).acceleration;
    ego_true_time(i) = t;
end

i = 0;
for k=keys(camBasedInfo.data)
    t = k{1};
    i = i+1;
    ego_cam_northing(i) = camBasedInfo.data(t).northing;
    ego_cam_easting(i) = camBasedInfo.data(t).easting;
    ego_cam_heading(i) = camBasedInfo.data(t).heading;
    ego_cam_speed(i) = camBasedInfo.data(t).speed;
    ego_cam_yaw(i) = camBasedInfo.data(t).yawRate;
    ego_cam_accel(i) = camBasedInfo.data(t).acceleration;
    ego_cam_time(i) = t;
end

%%

f = figure('Position',[0,0,1200,800]);
scatter(ego_true_easting,ego_true_northing,1,'blue','filled');
hold on
scatter(ego_cam_easting,ego_cam_northing,7,'red','filled');
title('Position of ego vehicle');
xlabel('Easting (meters)');
ylabel('Northing (meters)');
grid on;
legend('True information', 'CAM based data');
hold off
saveas(f,'figure2_ego_vehicle_true_position','fig');
saveas(f,'figure2_ego_vehicle_true_position','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
scatter(ego_true_time,ego_true_heading,3,'blue','filled');
hold on
scatter(ego_cam_time,ego_cam_heading,7,'red','filled');
title('Heading of ego vehicle');
xlabel('Time (seconds)');
ylabel('Heading (rad)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
legend('True information', 'CAM based data');
hold off
saveas(f,'figure3_ego_vehicle_true_heading','fig');
saveas(f,'figure3_ego_vehicle_true_heading','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
scatter(ego_true_time,ego_true_speed,3,'blue','filled');
hold on
scatter(ego_cam_time,ego_cam_speed,7,'red','filled');
title('Speed of ego vehicle');
xlabel('Time (seconds)');
ylabel('Speed (m/s)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
legend('True information', 'CAM based data');
hold off
saveas(f,'figure4_ego_vehicle_true_speed','fig');
saveas(f,'figure4_ego_vehicle_true_speed','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
scatter(ego_true_time,ego_true_yaw,3,'blue','filled');
hold on
scatter(ego_cam_time,ego_cam_yaw,7,'red','filled');
title('Yaw rate of ego vehicle');
xlabel('Time (seconds)');
ylabel('Yaw Rate (rad/s)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
legend('True information', 'CAM based data');
hold off
saveas(f,'figure5_ego_vehicle_true_yaw','fig');
saveas(f,'figure5_ego_vehicle_true_yaw','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
scatter(ego_true_time,ego_true_accel,3,'blue','filled');
hold on
scatter(ego_cam_time,ego_cam_accel,7,'red','filled');
title('Acceleration of ego vehicle');
xlabel('Time (seconds)');
ylabel('Acceleration (m/s^2)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
legend('True information', 'CAM based data');
hold off
saveas(f,'figure6_ego_vehicle_true_acceleration','fig');
saveas(f,'figure6_ego_vehicle_true_acceleration','png');
close(f);

%% Error of ego vehicle, cam based, at each time instant

posErrorCam = zeros(1,numPoints);
headingErrorCam = zeros(1,numPoints);
speedErrorCam = zeros(1,numPoints);
yawErrorCam = zeros(1,numPoints);
accelErrorCam = zeros(1,numPoints);
for i=1:numPoints
    posErrorCam(i) = sqrt((yTrue(i)-yCam(i))^2 + (xTrue(i)-xCam(i))^2);
    headingErrorCam(i) = abs(tetaTrue(i)-tetaCam(i));
    speedErrorCam(i) = abs(vTrue(i)-vCam(i));
    yawErrorCam(i) = abs(wTrue(i)-wCam(i));
    accelErrorCam(i) = abs(aTrue(i)-aCam(i));
end
clear i;

%% Line plots %%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,posErrorCam);
title('CAM based position error of ego vehicle');
xlabel('Time (seconds)');
ylabel('Position Error (meters)');
%%xlim([0,150]);
%%xticks(0:10:150);
grid on;
saveas(f,'figure7_ego_vehicle_cam_based_position_error','fig');
saveas(f,'figure7_ego_vehicle_cam_based_position_error','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,headingErrorCam);
title('CAM based heading error of ego vehicle');
xlabel('Time (seconds)');
ylabel('Heading Error (rad)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
saveas(f,'figure8_ego_vehicle_cam_based_heading_error','fig');
saveas(f,'figure8_ego_vehicle_cam_based_heading_error','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,speedErrorCam);
title('CAM based speed error of ego vehicle');
xlabel('Time (seconds)');
ylabel('Speed Error (meters/sec)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
saveas(f,'figure9_ego_vehicle_cam_based_speed_error','fig');
saveas(f,'figure9_ego_vehicle_cam_based_speed_error','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,yawErrorCam);
title('CAM based yaw rate error of ego vehicle');
xlabel('Time (seconds)');
ylabel('Yaw Rate Error (rad/sec)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
saveas(f,'figure10_ego_vehicle_cam_based_yaw_error','fig');
saveas(f,'figure10_ego_vehicle_cam_based_yaw_error','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,accelErrorCam);
title('CAM based acceleration error of ego vehicle');
xlabel('Time (seconds)');
ylabel('Acceleration Error (meter/sec^2)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
saveas(f,'figure11_ego_vehicle_cam_based_acceleration_error','fig');
saveas(f,'figure11_ego_vehicle_cam_based_acceleration_error','png');
close(f);

%% Ego vehicle kalman tracker

% create a map for kalman based predictions of ego vehicle position
kalmanBasedInfo = containers.Map('KeyType','double','ValueType','any');

% combine time instants of true data and cam data
timesCombined = tSeconds;
for k=keys(camBasedInfo.data)
    timesCombined(end+1) = k{1};    
end
timesCombined = sort(timesCombined);

% initialize kalman filter
tLast = timesCombined(1);
kinematic = camBasedInfo.data(tLast);
Xu = [ kinematic.easting; kinematic.northing; kinematic.heading; ...
    kinematic.speed; kinematic.yawRate; kinematic.acceleration ];
Pu = diag([ easting_initial_u; ...
            northing_initial_u; ...
            heading_initial_u; ...
            speed_initial_u; ...
            yaw_initial_u; ...
            accel_initial_u; ]);
Kk = zeros(6,6);
kalmanBasedInfo(tLast) = kinematic;

% save uncertainity and kalman gains
xxPu(1) = Pu(1,1);
yyPu(1) = Pu(2,2);
ttPu(1) = Pu(3,3);
vvPu(1) = Pu(4,4);
wwPu(1) = Pu(5,5);
aaPu(1) = Pu(6,6);
xxKk(1) = Kk(1,1);
yyKk(1) = Kk(2,2);
ttKk(1) = Kk(3,3);
vvKk(1) = Kk(4,4);
wwKk(1) = Kk(5,5);
aaKk(1) = Kk(6,6);

% run kalman tracker
for i=2:length(timesCombined)
    tCurrent = timesCombined(i);
    fprintf('tCurrent: %f\n',tCurrent);
    dt = tCurrent-tLast;
    
    if isKey(trueInfo.data,tCurrent)
        % run predict equations
        Xp = kalman.predict_state(Xu,dt);
        %Pp = kalman.predict_errorcov(Pu,Xu,dt);
        Zp = eye(6)*Xp;
        kinematic = KinematicInfo(Zp(1),Zp(2),Zp(3),Zp(4),Zp(6),0,Zp(5));
        kalmanBasedInfo(tCurrent) = kinematic;
    end
    
    if isKey(camBasedInfo.data,tCurrent)
        tLast = tCurrent;
        % run predict equations
        Xp = kalman.predict_state(Xu,dt);
        Pp = kalman.predict_errorcov(Pu,Xu,dt);
        % run update equations
        kinematic = camBasedInfo.data(tLast);
        Zu = [ kinematic.easting; kinematic.northing; kinematic.heading; ...
            kinematic.speed; kinematic.yawRate; kinematic.acceleration ];
        Yr = kalman.get_residual(Zu, Xp);
        Kk = kalman.get_kalmangain(Pp);
        Xu = kalman.update_state(Xp, Kk, Yr);
        Pu = kalman.update_errorcov(Pp, Kk);
        Zp = eye(6)* Xu;
        kinematic = KinematicInfo(Zp(1),Zp(2),Zp(3),Zp(4),Zp(6),0,Zp(5));
        kalmanBasedInfo(tCurrent) = kinematic;
    end
    
    % save uncertainity and kalman gains for x and y states
    xxPu(i) = Pu(1,1);
    yyPu(i) = Pu(2,2);
    ttPu(i) = Pu(3,3);
    vvPu(i) = Pu(4,4);
    wwPu(i) = Pu(5,5);
    aaPu(i) = Pu(6,6);
    xxKk(i) = Kk(1,1);
    yyKk(i) = Kk(2,2);
    ttKk(i) = Kk(3,3);
    vvKk(i) = Kk(4,4);
    wwKk(i) = Kk(5,5);
    aaKk(i) = Kk(6,6);
end
clear kinematic tLast tCurrent dt Xp Pp Zp Xu Pu Zu Yr Kk k i 

% read kalman tracker based information of ego vehicle
for k=keys(kalmanBasedInfo)
    t = k{1};
    tKalman = round(t*100); % 1 time unit: 10 msec
    xKalman(tKalman) = kalmanBasedInfo(t).easting;
    yKalman(tKalman) = kalmanBasedInfo(t).northing;
    tetaKalman(tKalman) = kalmanBasedInfo(t).heading;
    vKalman(tKalman) = kalmanBasedInfo(t).speed;
    wKalman(tKalman) = kalmanBasedInfo(t).yawRate;
    aKalman(tKalman) = kalmanBasedInfo(t).acceleration;
end
% fill empty middle points with the last available information
lastx = 0;
lasty = 0;
lastteta = 0;
lastv = 0;
lastw = 0;
lasta = 0;
for i=1:size(xObserver,2)
    if xObserver(i) == 0
        xKalman(i) = lastx;
        yKalman(i) = lasty;
        tetaKalman(i) = lastteta;
        vKalman(i) = lastv;
        wKalman(i) = lastw;
        aKalman(i) = lasta;
    else
        lastx = xKalman(i);
        lasty = yKalman(i);
        lastteta = tetaKalman(i);
        lastv = vKalman(i);
        lastw = wKalman(i);
        lasta = aKalman(i);
    end
end
xKalman = xKalman(tStart:tEnd);
yKalman = yKalman(tStart:tEnd);
tetaKalman = tetaKalman(tStart:tEnd);
vKalman = vKalman(tStart:tEnd);
wKalman = wKalman(tStart:tEnd);
aKalman = aKalman(tStart:tEnd);
clear tKalman lastx lasty lastteta lastv lastw lasta k i t

%% Error of ego vehicle, kalman based, at each time instant

posErrorKalman = zeros(1,numPoints);
headingErrorKalman = zeros(1,numPoints);
speedErrorKalman = zeros(1,numPoints);
yawErrorKalman = zeros(1,numPoints);
accelErrorKalman = zeros(1,numPoints);
for i=1:numPoints
    posErrorKalman(i) = sqrt((yTrue(i)-yKalman(i))^2 + (xTrue(i)-xKalman(i))^2);
    headingErrorKalman(i) = abs(tetaTrue(i)-tetaKalman(i));
    speedErrorKalman(i) = abs(vTrue(i)-vKalman(i));
    yawErrorKalman(i) = abs(wTrue(i)-wKalman(i));
    accelErrorKalman(i) = abs(aTrue(i)-aKalman(i));
end
clear i;

%% Line plots %%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,posErrorKalman);
title('Kalman based position error of ego vehicle');
xlabel('Time (seconds)');
ylabel('Position Error (meters)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
saveas(f,'figure12_ego_vehicle_kalman_based_position_error','fig');
saveas(f,'figure12_ego_vehicle_kalman_based_position_error','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,headingErrorKalman);
title('Kalman based heading error of ego vehicle');
xlabel('Time (seconds)');
ylabel('Heading Error (rad)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
saveas(f,'figure13_ego_vehicle_kalman_based_heading_error','fig');
saveas(f,'figure13_ego_vehicle_kalman_based_heading_error','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,speedErrorKalman);
title('Kalman based speed error of ego vehicle');
xlabel('Time (seconds)');
ylabel('Speed Error (meters/sec)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
saveas(f,'figure14_ego_vehicle_kalman_based_speed_error','fig');
saveas(f,'figure14_ego_vehicle_kalman_based_speed_error','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,yawErrorKalman);
title('Kalman based yaw rate error of ego vehicle');
xlabel('Time (seconds)');
ylabel('Yaw Rate Error (rad/sec)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
saveas(f,'figure15_ego_vehicle_kalman_based_yaw_error','fig');
saveas(f,'figure15_ego_vehicle_kalman_based_yaw_error','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);
plot(tSeconds,accelErrorKalman);
title('Kalman based acceleration error of ego vehicle');
xlabel('Time (seconds)');
ylabel('Acceleration Error (meter/sec^2)');
%xlim([0,150]);
%xticks(0:10:150);
grid on;
saveas(f,'figure16_ego_vehicle_kalman_based_acceleration_error','fig');
saveas(f,'figure16_ego_vehicle_kalman_based_acceleration_error','png');
close(f);

%% Extra

f = figure('Position',[0,0,1200,800]);
area(tSeconds,posErrorCam, 'FaceColor', '#0072BD', 'EdgeColor', 'black', 'LineStyle', 'none', 'LineWidth', 1);
hold on;
area(tSeconds,posErrorKalman, 'FaceColor', '#EDB120', 'EdgeColor', 'black', 'LineStyle', 'none', 'LineWidth', 1);
title('Position error');
xlabel('Time (seconds)');
ylabel('Error (meters)');
%xlim([20,150]);
%xticks(20:10:150);
grid on;
legend('CAM based', 'Kalman based');
hold off
saveas(f,'figure17_ego_vehicle_kalman_vs_cam_position_error','fig');
saveas(f,'figure17_ego_vehicle_kalman_vs_cam_position_error','png');
close(f);

%%

f = figure('Position',[0,0,1200,800]);

subplot(2,2,1)  
area(timesCombined,xxPu, 'FaceColor', '#EDB120', 'EdgeColor', 'black', 'LineStyle', '-', 'LineWidth', 1);
title('Uncertainity (x)');
xlabel('Time (seconds)');
ylabel('Value');
%xlim([20,150]);
%xticks(20:10:150);
ylim([0,1]);
yticks(0:0.1:1);
grid on;
legend('x');

subplot(2,2,2)
area(timesCombined,yyPu, 'FaceColor', '#EDB120', 'EdgeColor', 'black', 'LineStyle', '-', 'LineWidth', 1);
title('Uncertainity (y)');
xlabel('Time (seconds)');
ylabel('Value');
%xlim([20,150]);
%xticks(20:10:150);
ylim([0,1]);
yticks(0:0.1:1);
grid on;
legend('y');

subplot(2,2,3)  
area(timesCombined,xxKk, 'FaceColor', '#EDB120', 'EdgeColor', 'black', 'LineStyle', '-', 'LineWidth', 1);
title('Kalman Gain (x)');
xlabel('Time (seconds)');
ylabel('Value');
%xlim([20,150]);
%xticks(20:10:150);
ylim([0,1]);
yticks(0:0.1:1);
grid on;
legend('x');

subplot(2,2,4)
area(timesCombined,yyKk, 'FaceColor', '#EDB120', 'EdgeColor', 'black', 'LineStyle', '-', 'LineWidth', 1);
title('Kalman Gain (y)');
xlabel('Time (seconds)');
ylabel('Value');
%xlim([20,150]);
%xticks(20:10:150);
ylim([0,1]);
yticks(0:0.1:1);
grid on;
legend('y');

saveas(f,'figure18_ego_vehicle_kalman_plots','fig');
saveas(f,'figure18_ego_vehicle_kalman_plots','png');
close(f);
