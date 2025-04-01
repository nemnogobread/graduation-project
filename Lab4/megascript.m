clear all
close all

vc = 5.04; % питание
% разница моментов включения времени +- 40 пс
name = 'g_osc_1_4';
y=view_on_oscilloscope_cmp1234('g_osc_1_4', vc);


load g_osc_1_4_5.04
z=y(:,1);
pl = fix(40/0.4);
period = fix(240/0.4);
th = -0.25;
shift = fix(40/0.4);
vizstep = period - shift; %4fix(75/0.4);


[tt, p1, ttt1, p1t] = identical_pulses_single(z, pl, period, th, 'threshold', vizstep, shift);

% %save g_osc_1_4_pulses