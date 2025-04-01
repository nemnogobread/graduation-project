clear all
close all

Receive = serialport("COM5",9600);
Transmit = serialport("COM3", 9600);
flush(Receive);
flush(Transmit);
counter = 0;
%{
flush(Receive);
write(Receive, RECEIVER, "uint8");
while Receive.NumBytesAvailable == 0
end
Response = read(Receive, 1,"uint8");
if Response ~= RECEIVER
    error('Device does not response.');
end 
%}
for i = 0:5
    flush(Receive);
    flush(Transmit);
    %myinput = randi([0, 255]);
    myinput = 255;
    write(Transmit, myinput, "uint8");

    while Receive.NumBytesAvailable == 0
    end

    data = read(Receive, 1, "uint8");

    %flush(Transmit);
    
    if myinput ~= data
        counter = counter + 1 ;
    end

    disp(myinput);
    disp(data);
end

disp("Final: ")
disp(counter);
