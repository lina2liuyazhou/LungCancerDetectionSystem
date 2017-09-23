function [ compnumber ] = getcomponent( y,x,z,comps,sz)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

index = sub2ind(sz,x,y,z);

for compnumber = 1:comps.NumObjects
    if ~isempty(find(comps.PixelIdxList{compnumber}==index, 1))
        return;
    end
end

compnumber = -1;

end

