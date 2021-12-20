plotfile('4/3new',3);

function plotfile(filename, nFigure)
fileID = fopen(filename);
formatSpec = '%i';
data = fscanf(fileID,formatSpec,[6 Inf]);
x = data(1,:); y = data(2,:); z = data(3,:);
r = data(4,:); g = data(5,:); b = data(6,:);
figure(nFigure);
clf();
scatter3(x,y,z,1,[r',g',b']./255,'.');
end