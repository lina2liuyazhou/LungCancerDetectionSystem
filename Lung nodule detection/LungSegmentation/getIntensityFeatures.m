function [ intensityFeatures ] = getIntensityFeatures( Dicom,NoduleMask )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes 

grayImg = roi(Dicom,NoduleMask);
comps = bwconncomp(NoduleMask);
props = regionprops(comps);

intensityFeatures = zeros(comps.NumObjects,4);

for i=1:comps.NumObjects
    img = zeros(size(NoduleMask));
    img(comps.PixelIdxList{i}) = grayImg(comps.PixelIdxList{i});
    l = props(i).BoundingBox(3) + 0.5;
    h = l + props(i).BoundingBox(6) - 1;
    numberOfSlices = props(i).BoundingBox(6);
    
    moment = 0;
    minVal = inf;
    maxVal = 0;
    sumVal = 0;
    
    for j=l:h
        for a=1:size(NoduleMask,1)
            for b=1:size(NoduleMask,2)
                if img(a,b,j) ~= 0
                    moment = moment + (power(img(a,b,j),2)/(1+abs(a-b)));
                    sumVal = sumVal + img(a,b,j);
                    if img(a,b,j) > maxVal
                        maxVal = img(a,b,j);
                    end
                    if img(a,b,j) < minVal
                        minVal = img(a,b,j);
                    end
                end
            end
        end
    end
    
    intensityFeatures(i,1) = moment/numberOfSlices;
    intensityFeatures(i,2) = minVal;
    intensityFeatures(i,3) = maxVal;
    intensityFeatures(i,4) = sumVal/size(comps.PixelIdxList{i},1);

end

