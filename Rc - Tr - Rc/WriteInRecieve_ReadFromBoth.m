clear all
close all

count = 0;
d2t = 120;
baudrate = 9600;

Receive = serialport("COM5", baudrate);
Transmit = serialport("COM3", baudrate);
flush(Receive);
flush(Transmit);


write(Receive, d2t, "uint8");
disp("receiver sent:");
disp(d2t);
flush(Receive);

while true
    if Transmit.NumBytesAvailable > 0
        data = read(Transmit, 1, "uint8");
        disp("transmitter got:")
        disp(data);
        %flush(Transmit);
    end

    if Receive.NumBytesAvailable > 0
        data = read(Receive, 1, "uint8");
        disp("receiver got:")
        disp(data);
        %flush(Receive);
        if (data == 224)
            count = count + 1;
        end
    end

end

