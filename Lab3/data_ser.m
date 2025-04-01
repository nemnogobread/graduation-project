clear all;
close all;

Receive = serialport("COM5",9600);
Transmit = serialport("COM3", 9600);
counter = 0;

for i = 0:100

    flush(Receive);
    flush(Transmit);
    myinput = randi([0, 255]);
    write(Transmit, myinput, "uint8");

    while Receive.NumBytesAvailable == 0
    end

    data = read(Receive, 1, "uint8");
    
    if myinput ~= data
        counter = counter + 1 ;
    end

    disp(myinput);
    disp(data);
end

disp("Final: ")
disp(counter);

close all;
clear all;