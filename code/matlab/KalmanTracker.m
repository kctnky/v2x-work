classdef KalmanTracker

properties (GetAccess=public, SetAccess=public)    
    % process noise, Q matrix
    yaw_proc_n % radian/sec
    accel_proc_n % meter/sec^2
    
    % measurement noise, R matrix
    easting_meas_n % meters
    northing_meas_n % meters
    heading_meas_n % radian
    speed_meas_n % meter/sec
    yaw_meas_n % radian/sec
    accel_meas_n % meter/sec^2
end

methods (Access=public)
    
    function obj = KalmanTracker()        
        % default values for process noise
        obj.yaw_proc_n = 1;
        obj.accel_proc_n = 1;
        
        % default values for measurement noise 
        obj.easting_meas_n = 1e-6;
        obj.northing_meas_n = 1e-6;
        obj.heading_meas_n = 1e-6;
        obj.speed_meas_n = 1e-6;
        obj.yaw_meas_n = 1e-6;
        obj.accel_meas_n = 1e-6;
    end

    function predicted_state = predict_state(~, last_updated_state, dt)
        % state vector should have 6 elements
        x = last_updated_state(1);
        y = last_updated_state(2);
        teta = last_updated_state(3);
        v = last_updated_state(4);
        w = last_updated_state(5);
        a = last_updated_state(6);
        
        % Here, two independent processes are modeled in motion dynamics
        % The first, constant-acceleration model, [ x y v a ]
        % The second, constant-yaw-model, [ teta, w ]
        
        % new state estimation
        predicted_state = zeros(6, 1);
        predicted_state(1) = x + v*sin(teta)*dt + 0.5*a*sin(teta)*dt*dt;
        predicted_state(2) = y + v*cos(teta)*dt + 0.5*a*cos(teta)*dt*dt;
        predicted_state(3) = mod(teta + w*dt + pi, 2*pi) - pi;
        predicted_state(4) = v + a*dt;
        predicted_state(5) = w;
        predicted_state(6) = a;
        
        % --- old model ---
        %if (abs(w) < 1e-6)
        %    w = sign(w)*1e-6;
        %end
        %
        %dx = (1/w^2)*((v*w+a*w*dt)*sin(teta+w*dt)+a*cos(teta+w*dt)- ...
        %    v*w*sin(teta)-a*cos(teta));
        %dy = (1/w^2)*((-v*w-a*w*dt)*cos(teta+w*dt)+a*sin(teta+w*dt)+ ...
        %    v*w*cos(teta)-a*sin(teta));
        %
        %predicted_state = zeros(6, 1);
        %predicted_state(1) = x + dx;
        %predicted_state(2) = y + dy;
        %predicted_state(3) = mod(teta + w*dt + pi, 2*pi) - pi;
        %predicted_state(4) = v + a*dt;
        %predicted_state(5) = w;
        %predicted_state(6) = a;
        % --- end of old model ---
    end

    function predicted_errorcov = predict_errorcov(obj, last_updated_errorcov, ...
            last_updated_state, dt)
        % define symbols
        syms x y teta v w a T;

        % define state function
        f = [ x + v*sin(teta)*T + 0.5*a*sin(teta)*T*T ; ...
              y + v*cos(teta)*T + 0.5*a*cos(teta)*T*T ; ...
              teta + w*T ; ...
              v + a*T ; ...
              w ; ...
              a ];
          
        % define state vector
        statevec = [ x ; y ; teta ; v ; w ; a ];

        % obtain jacobian of state function with respect to state vector
        J = jacobian(f, statevec);

        % state vector should have 6 elements
        x = last_updated_state(1);
        y = last_updated_state(2);
        teta = last_updated_state(3);
        v = last_updated_state(4);
        w = last_updated_state(5);
        a = last_updated_state(6);
        T = dt;
        
        % evaluate jacobian matrix
        F = eval(subs(J));
        FT = transpose(F);
        
        % process noise
        a_n = obj.accel_proc_n;
        w_n = obj.yaw_proc_n;
        s = sin(teta);
        c = cos(teta);
        ss = sin(teta)*sin(teta);
        sc = sin(teta)*cos(teta);
        cc = cos(teta)*cos(teta);
        Q = [ 0.25*(dt^4)*ss*a_n	0.25*(dt^4)*sc*a_n      0               0.5*(dt^3)*s*a_n	0       0.5*(dt^2)*s*a_n ; ...
              0.25*(dt^4)*sc*a_n	0.25*(dt^4)*cc*a_n      0               0.5*(dt^3)*c*a_n	0       0.5*(dt^2)*c*a_n ; ...
              0                     0                       0.5*(dt^2)*w_n	0                   dt*w_n	0 ; ...
              0.5*(dt^3)*s*a_n      0.5*(dt^3)*c*a_n        0               dt^2*a_n            0       dt*a_n ; ...
              0                     0                       dt*w_n          0                   1*w_n	0 ; ...
              0.5*(dt^2)*s*a_n      0.5*(dt^2)*c*a_n        0               dt*a_n              0       1*a_n ];
        
        % new error covariance estimation
        predicted_errorcov = F * last_updated_errorcov * FT + Q;
        
        % --- old model --- 
        %f = [ x + ((1/w^2)*((v*w+a*w*T)*sin(teta+w*T)+a*cos(teta+w*T)- ...
        %          v*w*sin(teta)-a*cos(teta))) ; ...
        %      y + ((1/w^2)*((-v*w-a*w*T)*cos(teta+w*T)+a*sin(teta+w*T)+ ...
        %          v*w*cos(teta)-a*sin(teta))) ; ...
        %      teta + w*T ; v + a*T ; w ; a ];
        %
        %if (abs(w) < 1e-6)
        %    w = sign(w)*1e-6;
        %end
        %
        % An approach to find Q matrix
        %G = [ F(1,6) F(1,5) ; F(2,6) F(2,5) ; F(3,6) F(3,5) ; ...
        %    F(4,6) F(4,5) ; F(5,6) F(5,5) ; F(6,6) F(6,5) ];
        %GT = transpose(G);        
        %Q = G * [ obj.accel_proc_n^2 0 ; 0 obj.yaw_proc_n^2 ] * GT;
        % --- end of old model ---
        
    end

    function updated_state = update_state(~, predicted_state, kalman_gain, ...
            measurement_residual)
        % compute the updated state estimation
        updated_state = predicted_state + kalman_gain * measurement_residual;
    end

    function updated_errorcov = update_errorcov(~, predicted_errorcov, ...
            kalman_gain)
        % compute the updated error estimation
        I = eye(6);
        H = eye(6);
        updated_errorcov = (I - kalman_gain * H) * predicted_errorcov;
    end

    function residual = get_residual(~, measurement_vector, predicted_state)
        % residual is the difference between measurement and last prediction
        residual = measurement_vector - eye(6) * predicted_state;
    end

    function K = get_kalmangain(obj, predicted_errorcov)
        % output vector is same with the state vector
        H = eye(6);
        HT = transpose(H);

        % measurement noise
        R = diag([obj.easting_meas_n; obj.northing_meas_n; ...
            obj.heading_meas_n; obj.speed_meas_n; ...
            obj.yaw_meas_n; obj.accel_meas_n]);

        % compute Kalman gain
        S = inv(R + H * predicted_errorcov * HT);
        K = predicted_errorcov * HT * S;
    end
    
end % methods (Access=public)

end % classdef KalmanTracker