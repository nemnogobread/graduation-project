clear all
close all

Receive = serialport("COM3",9600);
Transmit = serialport("COM5", 9600);
flush(Receive);
flush(Transmit);

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

while true
    flush(Receive);
    flush(Transmit);
    d2t = 3
    write(Transmit, d2t, "uint8");

    while Receive.NumBytesAvailable == 0
    end

    if Receive.NumBytesAvailable > 0
        disp("here1");
        data = read(Receive, 1, "uint8")
        flush(Receive);
        disp(data)
    end

end
