clc;
clear all;

rootdir = '..\LIDC image set\Renamed\LIDC';
set = 3; %LIDC set number %Check set 11

currentdir = strcat(rootdir,int2str(set),'\');
% currentdir = '..\Data Set - Others\renamedData110\'; %Non LIDC sets

slices = size(ls(currentdir),1) - 2; %Number of slices in the set
image = image3D(currentdir,slices);

bw = zeros(size(image));

for i=1:slices
    bw(:,:,i) = im2bw(wl(image(:,:,i),564,1500),0.5);
end


invert = not(bw);
comps = bwconncomp(invert);
pixelarea = cellfun(@numel,comps.PixelIdxList);
[largest,pos] = max(pixelarea);
pixelarea(pos) = 0;
[secondlargest,pos2] = max(pixelarea);

segmentedLung = zeros(size(image));
segmentedLung(comps.PixelIdxList{pos2}) = 1;

%imshow3D(blank)
%figure;
%imshow3D(image)

componentsMask = not(segmentedLung);
comps = bwconncomp(componentsMask);

props = regionprops(comps);

for i=1:comps.NumObjects
    if props(i).Area == 1
        componentsMask(comps.PixelIdxList{i}) = 0;
    end
end
