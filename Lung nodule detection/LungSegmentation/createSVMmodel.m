clear all;
load('..\LIDC image set\NonNodules');
load('..\LIDC image set\Nodulefeatures');

for i =40:100
    if i~=151&i~=153&i~=144&i~=202&i~=167&i~=185
        feats = [feats;addfeatures(FEATURES,PROPERTIES,PROPERTIES_3D,0,i,0)];
    end
end

y = [ones(52,1);zeros(size(feats,1),1)];
 trainingset = [featurevar;feats];
 temp = trainingset;
 trainingset = trainingset(:,4:13);
 trainingset = [trainingset,temp(:,27),temp(:,40:42),temp(:,46)];
%trainingset = [([featurevar;feats])(:,4:13);([featurevar;feats])(:,:13)];
model = fitcsvm(trainingset,y);

% res =[];
% for i=1:size(trainingset,1)
%     res=[res;predict(model,trainingset(i,:))];
% end

load('..\LIDC image set\Features\42');
compfeats = [];
for i =1:comps.NumObjects
    compfeats = [compfeats;addfeatures(FEATURES,PROPERTIES,PROPERTIES_3D,0,i,0)];
end
temp = compfeats;
 compfeats = compfeats(:,4:13);
 compfeats = [compfeats,temp(:,27),temp(:,40:42),temp(:,46)];

res =[];
for i=1:size(FEATURES,1)
    res=[res;predict(model,compfeats(i,:))];
end
