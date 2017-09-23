clear all;

loaddir = '..\LIDC image set\Features\';
%savepath = '..\LIDC image set\featurevar';

set = 60; % sets 35, 43 are anomalies. Do not use them.

load(strcat(loaddir,int2str(set)));
%load(savepath);

imshow3D(image);
figure;
imshow3D(componentsMask);
