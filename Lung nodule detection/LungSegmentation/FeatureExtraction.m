loaddir = '..\LIDC image set\Workspaces\';
savedir = '..\LIDC image set\Features\';

% sets 35, 43 are anomalies

for set = 1:60
    
    if or(set==35,set==43)
        continue;
    end
    
    load(strcat(loaddir,int2str(set)),'slices','componentsMask','image');
    
    comps = bwconncomp(componentsMask);
    PROPERTIES = regionprops(comps);
    PROPERTIES_3D = regionprops3(comps);
    
    %Extract volume of each connected component
    FEATURES = zeros(size(comps.NumObjects,7));
    
    % Geometric features :
    % Field 1 : Volume
    % Field 2 : Surface Area
    % Field 3 : Sphericity
    % Field 4 : Centroid Offset
    % Field 5 : Circularity
    % Field 6 : Elongation
    
    % Intensity features :
    % Field 7 : Moment
    % Field 8 : Minimum Intensity
    % Field 9 : Maximum Intensity
    % Field 10 : Average Intensity
    
    for i=1:comps.NumObjects
        FEATURES(i,1) = PROPERTIES(i).Area;
        volume = PROPERTIES(i).Area;
        %Extract other 3-D features here.
        
        surfaceArea = 0;
        centroidOffset = 0;
        circularity = 0;
        elongation = 0;
        moment = 0;
        
        cx = PROPERTIES(i).Centroid(1);
        cy = PROPERTIES(i).Centroid(2);
        
        img = zeros(size(componentsMask));
        img(comps.PixelIdxList{i}) = 1;
        l = PROPERTIES(i).BoundingBox(3) + 0.5;
        h = l + PROPERTIES(i).BoundingBox(6) - 1;
        numberOfSlices = PROPERTIES(i).BoundingBox(6);
        
        for j=l:h
            %Apply bwperim, etc on img(:,:,j).. Get results, take average for 2D
            %features. Store in X(i,n)
            
            comps2 = bwconncomp(img(:,:,j));
            props2 = regionprops(comps2);
            
            perim = bwperim(img(:,:,j));
            comps2d = bwconncomp(perim);
            props2d = regionprops(comps2d);
            
            rmin = inf;
            rmax = 0;
            
            for a=1:size(perim,1)
                for b=1:size(perim,2)
                    if perim(a,b)==1
                        dist = sqrt(power(a-props2(1).Centroid(2),2)+power(b-props2(1).Centroid(2),2));
                        
                        if dist > rmax
                            rmax = dist;
                        end
                        
                        if dist < rmin
                            rmin = dist;
                        end
                    end
                end
            end
            
            if rmin == rmax
                e = 1;
            else
                e = rmin/rmax;
            end
            
            elongation = elongation + e;
            
            if or(j==l,j==h)
                surfaceArea = surfaceArea + props2(1).Area;
            else
                surfaceArea = surfaceArea + props2d(1).Area;
            end
            
            cx2 = props2(1).Centroid(1);
            cy2 = props2(1).Centroid(2);
            
            centroidOffset = centroidOffset + abs(cx-cx2) + abs(cy-cy2);
            
            circularity = circularity + (4*pi*props2(1).Area/power(props2d(1).Area,2));
            
        end
        
        FEATURES(i,2) = surfaceArea;
        sphericity = power(pi,1/3)*power(6*volume,2/3)/surfaceArea;
        FEATURES(i,3) = sphericity;
        FEATURES(i,4) = centroidOffset;
        FEATURES(i,5) = circularity/numberOfSlices;
        FEATURES(i,6) = elongation/numberOfSlices;
    end
    
    FEATURES = [FEATURES getIntensityFeatures(image,componentsMask)];
    
    save(strcat(savedir,int2str(set)),'image','componentsMask','FEATURES','PROPERTIES','PROPERTIES_3D','comps');
    
    clearvars -except set loaddir savedir;
    
    set
end