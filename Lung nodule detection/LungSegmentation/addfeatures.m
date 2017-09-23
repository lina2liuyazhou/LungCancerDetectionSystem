function [ features ] = addfeatures( feats,props,props3,set,compnum,malignancy)
%UNTITLED Summaryt of this function goes here
%   Detailed explanation goes here

features = zeros(size(1,47));

props3 = transpose(props3);

features(1) = set;
features(2) = compnum;
features(3) = malignancy;
features(4:13) = feats(compnum,:);
features(14:23) = struct2array(props(compnum)); %area 1,centroid 3,bounding box 6
features(24:47) = struct2array(props3(compnum)); %refer regionprops3

end

