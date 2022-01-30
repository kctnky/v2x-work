ego_kk_northing = zeros(1,kalmanBasedInfo.length);
ego_kk_easting = zeros(1,kalmanBasedInfo.length);
ego_kk_heading = zeros(1,kalmanBasedInfo.length);
ego_kk_speed = zeros(1,kalmanBasedInfo.length);
ego_kk_yaw = zeros(1,kalmanBasedInfo.length);
ego_kk_accel = zeros(1,kalmanBasedInfo.length);
ego_kk_time = zeros(1,kalmanBasedInfo.length);

i = 0;
for k=keys(kalmanBasedInfo)
    t = k{1};
    i = i+1;
    ego_kk_northing(i) = kalmanBasedInfo(t).northing;
    ego_kk_easting(i) = kalmanBasedInfo(t).easting;
    ego_kk_heading(i) = kalmanBasedInfo(t).heading;
    ego_kk_speed(i) = kalmanBasedInfo(t).speed;
    ego_kk_yaw(i) = kalmanBasedInfo(t).yawRate;
    ego_kk_accel(i) = kalmanBasedInfo(t).acceleration;
    ego_kk_time(i) = t;
end

%%

figure('Position',[0,0,1200,800]);
scatter(ego_kk_easting,ego_kk_northing,1,'blue','filled');
title('Position of ego vehicle');
xlabel('Easting (meters)');
ylabel('Northing (meters)');
grid on;