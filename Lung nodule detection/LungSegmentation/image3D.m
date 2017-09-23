%function to construct the 3d image. It takes a string str which holds the
%path to the first image. From there a sequencial access is made by
%incrementing the number from 1 through n.
%returns Dicom, 3D image

function [Dicom ] = image3D( str,n )
    Dicom = dicomread(strcat(str,int2str(1),'.dcm')); 
	Dicom = wiener2(Dicom);
    i=2;
    while i <= n
        try
        strtemp = strcat(str,int2str(i),'.dcm');                            %i th image path
        im = dicomread(strtemp);                                            %i th image
        im = wiener2(im);                                                   %applying the wiener filter
        Dicom = cat(3,Dicom,im);                                            %stacking the ith image
        catch
            n = n+1;
        end
        i = i + 1;
    end
end