  
rootdir = 'D:\Lung\DataSets\LIDC image set\Renamed\LIDC';
workspacedir = 'D:\Lung\DataSets\LIDC image set\Workspaces\';
set=12
currentdir = strcat(rootdir,int2str(set),'\');
% currentdir = '..\Data Set - Others\renamedData110\'; %Non LIDC sets

slices = size(ls(currentdir),1) - 2; %Number of slices in the set
image = image3D(currentdir,slices);


bw = zeros(size(image));

for i=1:slices
    bw(:,:,i) = im2bw(wl(image(:,:,i),564,1500),0.5); %Getting BW image of lungs : Lungs - white
end

invert = not(bw); %Invert to get Lungs - black, remaining white

comps = bwconncomp(invert);
pixelarea = cellfun(@numel,comps.PixelIdxList);
[largest,pos] = max(pixelarea);
pixelarea(pos) = 0;
[secondlargest,pos2] = max(pixelarea);

segmentedLung = zeros(size(image));
segmentedLung(comps.PixelIdxList{pos2}) = 1;

%imshow3D(blank)
%figure;
imshow3D(image)

componentsMask = not(segmentedLung);
comps = bwconncomp(componentsMask);

props = regionprops(comps);


for i=1:comps.NumObjects
    if or(props(i).BoundingBox(6) > 10, or(props(i).Area == 1, or(props(i).BoundingBox(5) > 40, or(props(i).BoundingBox(4) > 40 , or(abs( props(i).BoundingBox(5) - props(i).BoundingBox(4)) > 10,props(i).Area < 20))))) % Bounding box > 20
        componentsMask(comps.PixelIdxList{i}) = 0;
    end
end

comps2 = bwconncomp(componentsMask);

%imshow3D(componentsMask)
%figure
%imshow3D(image)
%figure
%imshow3D(segmentedLung)
%fileID = fopen('exp.txt','w');
%for i=1:comps2.NumObjects
 %       fprintf(fileID,'%d\n',i);
  %      fprintf(fileID,'%9d\n',comps2.PixelIdxList{i});
%end

%mkdir(strcat('..\seg\',int2str(set)));
%for i=1:slices
 %   dicomwrite(segmentedLung(:,:,i),strcat('..\seg\',int2str(set),'\',int2str(i),'.dcm'));
%end

%mkdir(strcat('..\compmask\',int2str(set)));
%for i=1:slices
 %   dicomwrite(componentsMask(:,:,i),strcat('..\compmask\',int2str(set),'\',int2str(i),'.dcm'));
%end 