function [ output ] = wl( imHU,lev,win )
%dicom images have the density values in HU(hounsfield). Selecting a
%perticular range of values is what this function does. win is the window
%size and lev is level. For lung window we use w/l as 1500/564. 
[r,c] = size(imHU);
lLim = lev - 0.5 * win;
uLim = lev + 0.5 * win;
s = win/255;
output = uint8(zeros([r c]));
for i=1:r
    for j=1:c
        inPixel = imHU(i,j);
        if inPixel <= lLim
            outPixel = 0;
        elseif inPixel < uLim 
             outPixel = double(inPixel - lLim)/s; 
        else  
            outPixel = 255;
        end
        output(i,j) = outPixel;
    end
end


end

